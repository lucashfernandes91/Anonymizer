import io
import time
import base64
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from PIL import Image, UnidentifiedImageError, ExifTags

from .services import obter_endereco, extrair_classificar_metadados
from .models import EstatisticaGlobal, AcessoUnico


MAX_SIZE = 10 * 1024 * 1024  # 10MB

# proteção contra image bomb (global)
Image.MAX_IMAGE_PIXELS = 20_000_000

MESES = [
	'janeiro','fevereiro','março','abril','maio','junho',
	'julho','agosto','setembro','outubro','novembro','dezembro'
]


def formatar_datetime_exif(valor):
	"""Converte '2022:05:02 12:32:28' → '02 de maio de 2022 às 12:32'"""
	try:
		dt = datetime.strptime(valor, '%Y:%m:%d %H:%M:%S')
		return f"{dt.day:02d} de {MESES[dt.month-1]} de {dt.year} às {dt.hour:02d}:{dt.minute:02d}"
	except Exception:
		return valor


def sanitizar_exif(exif_dict):
	resultado = {}
	for key, value in exif_dict.items():
		val_str = str(value)
		if val_str.count('\\x') > 5:
			continue
		if len(val_str) > 200:
			val_str = val_str[:200] + '...'
		resultado[key] = val_str
	return resultado


def registrar_acesso(request):
	if not request.session.session_key:
		request.session.create()
	session_key = request.session.session_key
	AcessoUnico.objects.get_or_create(
		session_key=session_key,
		defaults={
			'ip': _get_ip(request),
			'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500],
		}
	)


def _get_ip(request):
	x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded:
		return x_forwarded.split(',')[0].strip()
	return request.META.get('REMOTE_ADDR')


def rate_limit(request, limit=10, window=60):
	ip = _get_ip(request)
	key = f"rate:{ip}"
	data = cache.get(key)
	now = time.time()
	if not data:
		cache.set(key, {"count": 1, "start": now}, timeout=window)
		return False
	if now - data["start"] > window:
		cache.set(key, {"count": 1, "start": now}, timeout=window)
		return False
	if data["count"] >= limit:
		return True
	data["count"] += 1
	cache.set(key, data, timeout=window)
	return False


def extrair_gps(img):
	"""Extrai lat/lon e EXIF da imagem antes de anonimizar."""
	exif_data = {}
	gps_detectado = False
	lat = None
	lon = None

	try:
		raw_exif = img._getexif()
		if not raw_exif:
			return exif_data, gps_detectado, lat, lon

		for tag_id, value in raw_exif.items():
			tag_name = ExifTags.TAGS.get(tag_id, tag_id)

			if tag_name == "GPSInfo":
				gps_detectado = True
				gps_data = {}
				for t in value:
					sub_tag = ExifTags.GPSTAGS.get(t, t)
					gps_data[sub_tag] = value[t]

				if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
					lat = _dms_to_decimal(
						gps_data.get("GPSLatitude"),
						gps_data.get("GPSLatitudeRef")
					)
					lon = _dms_to_decimal(
						gps_data.get("GPSLongitude"),
						gps_data.get("GPSLongitudeRef")
					)

			if isinstance(value, bytes):
				continue

			exif_data[tag_name] = str(value)

	except Exception as e:
		print("ERRO ao extrair EXIF:", e)

	return exif_data, gps_detectado, lat, lon


def _dms_to_decimal(dms, ref):
	"""Converte coordenadas DMS para decimal."""
	try:
		def to_float(x):
			if isinstance(x, tuple):
				return float(x[0]) / float(x[1])
			return float(x)

		graus    = to_float(dms[0])
		minutos  = to_float(dms[1])
		segundos = to_float(dms[2])
		decimal  = graus + (minutos / 60.0) + (segundos / 3600.0)

		if ref in ["S", "W"]:
			decimal = -decimal

		return decimal

	except Exception as e:
		print("Erro ao converter GPS:", e)
		return None


def home(request):
	registrar_acesso(request)

	context = {
		'total_imagens': EstatisticaGlobal.total(),
		'total_acessos': AcessoUnico.total(),
	}

	if request.method == "POST":

		if rate_limit(request):
			return render(request, "429.html", status=429)

		image = request.FILES.get("image")

		if not image:
			context["erro"] = "Nenhuma imagem enviada"
			return render(request, "home.html", context)

		if image.size > MAX_SIZE:
			context["erro"] = "Arquivo muito grande (máx 5MB)"
			return render(request, "home.html", context)

		try:
			img = Image.open(image)
			img.verify()
		except UnidentifiedImageError:
			context["erro"] = "Arquivo inválido (não é imagem)"
			return render(request, "home.html", context)

		# reabrir após verify() — consome o file pointer
		image.seek(0)
		img = Image.open(image)

		if img.width * img.height > 20_000_000:
			context["erro"] = "Imagem muito grande"
			return render(request, "home.html", context)

		if img.format not in ["JPEG", "PNG", "WEBP"]:
			context["erro"] = "Formato não suportado"
			return render(request, "home.html", context)

		# extrai EXIF e GPS ANTES de converter/limpar
		exif_raw, gps_detectado, lat, lon = extrair_gps(img)
		exif = sanitizar_exif(exif_raw)

		# formata datas para exibição legível
		for campo in ('DateTimeOriginal', 'DateTimeDigitized', 'DateTime'):
			if exif.get(campo):
				exif[campo] = formatar_datetime_exif(exif[campo])

		# limpeza total — converte para RGB, descarta todos os metadados
		img = img.convert("RGB")
		buffer = io.BytesIO()
		img.save(buffer, format="JPEG", quality=85, optimize=True)
		buffer.seek(0)

		EstatisticaGlobal.incrementar()

		image.seek(0)
		original_b64 = base64.b64encode(image.read()).decode()
		anon_b64 = base64.b64encode(buffer.getvalue()).decode()

		image.seek(0)
		metadados = extrair_classificar_metadados(image)

		# reverse geocoding — só executa se tiver GPS
		lat = float(lat) if lat is not None else None
		lon = float(lon) if lon is not None else None

		endereco = None
		if lat is not None and lon is not None:
			endereco = obter_endereco(lat, lon)
			if isinstance(endereco, str):
				endereco = {"display": endereco}

		context = {
			"original": original_b64,
			"anon": anon_b64,
			"exif": exif,
			"gps": gps_detectado,
			"lat": lat,
			"lon": lon,
			"endereco": endereco,
			"metadados": metadados,
			"total_imagens": EstatisticaGlobal.total(),
			"total_acessos": AcessoUnico.total(),
		}

	return render(request, "home.html", context)
