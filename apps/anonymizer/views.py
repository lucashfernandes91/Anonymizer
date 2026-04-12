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
from rest_framework.decorators import api_view
from rest_framework.response import Response


MAX_SIZE = 10 * 1024 * 1024  # 10MB

Image.MAX_IMAGE_PIXELS = 20_000_000

MESES = [
	'janeiro','fevereiro','março','abril','maio','junho',
	'julho','agosto','setembro','outubro','novembro','dezembro'
]


def formatar_datetime_exif(valor):
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


def _processar_imagem(image_file):
	"""Lógica central de anonimização — reutilizada pela view web e pela API."""
	image_file.seek(0)
	img = Image.open(image_file)

	if img.width * img.height > 20_000_000:
		return None, 'Imagem muito grande'

	if img.format not in ["JPG", "JPEG", "PNG", "WEBP"]:
		return None, 'Formato não suportado. Use JPG,JPEG, PNG ou WEBP'

	exif_raw, gps_detectado, lat, lon = extrair_gps(img)
	exif = sanitizar_exif(exif_raw)

	for campo in ('DateTimeOriginal', 'DateTimeDigitized', 'DateTime'):
		if exif.get(campo):
			exif[campo] = formatar_datetime_exif(exif[campo])

	img = img.convert("RGB")
	buffer = io.BytesIO()
	img.save(buffer, format="JPEG", quality=85, optimize=True)
	buffer.seek(0)

	EstatisticaGlobal.incrementar()

	image_file.seek(0)
	metadados = extrair_classificar_metadados(image_file)

	lat = float(lat) if lat is not None else None
	lon = float(lon) if lon is not None else None

	endereco = None
	if lat is not None and lon is not None:
		endereco = obter_endereco(lat, lon)
		if isinstance(endereco, str):
			endereco = {"display": endereco}

	return {
		'img': img,
		'buffer': buffer,
		'exif': exif,
		'gps_detectado': gps_detectado,
		'lat': lat,
		'lon': lon,
		'endereco': endereco,
		'metadados': metadados,
	}, None


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
			context["erro"] = "Arquivo muito grande (máx 10MB)"
			return render(request, "home.html", context)

		try:
			img = Image.open(image)
			img.verify()
		except UnidentifiedImageError:
			context["erro"] = "Arquivo inválido (não é imagem)"
			return render(request, "home.html", context)

		image.seek(0)

		result, erro = _processar_imagem(image)

		if erro:
			context["erro"] = erro
			return render(request, "home.html", context)

		image.seek(0)
		original_b64 = base64.b64encode(image.read()).decode()
		anon_b64 = base64.b64encode(result['buffer'].getvalue()).decode()

		context = {
			"original": original_b64,
			"anon": anon_b64,
			"exif": result['exif'],
			"gps": result['gps_detectado'],
			"lat": result['lat'],
			"lon": result['lon'],
			"endereco": result['endereco'],
			"metadados": result['metadados'],
			"total_imagens": EstatisticaGlobal.total(),
			"total_acessos": AcessoUnico.total(),
		}

	return render(request, "home.html", context)


@api_view(['POST'])
def anonymize_api(request):
	if rate_limit(request):
		return Response({'error': 'Muitas requisições. Tente novamente em breve.'}, status=429)

	image_file = request.FILES.get('image')
	if not image_file:
		return Response({'error': 'Nenhuma imagem enviada'}, status=400)

	if image_file.size > MAX_SIZE:
		return Response({'error': 'Arquivo muito grande (máx 10MB)'}, status=400)

	try:
		img = Image.open(image_file)
		img.verify()
	except UnidentifiedImageError:
		return Response({'error': 'Arquivo inválido (não é imagem)'}, status=400)

	image_file.seek(0)
	result, erro = _processar_imagem(image_file)
	if erro:
		return Response({'error': erro}, status=400)

	nome_original = image_file.name or 'imagem'
	nome_base = nome_original.rsplit('.', 1)[0]
	nome_saida = f"{nome_base}_anonimizado.jpg"

	response = HttpResponse(result['buffer'].getvalue(), content_type='image/jpeg')
	response['Content-Disposition'] = f'attachment; filename="{nome_saida}"'
	response['X-Campos-Removidos'] = str(len(result['metadados']))
	response['X-Tem-GPS'] = str(result['gps_detectado']).lower()
	response['X-Lat'] = str(result['lat']) if result['lat'] is not None else ''
	response['X-Lon'] = str(result['lon']) if result['lon'] is not None else ''
	response['X-Dispositivo'] = (result['exif'].get('Make', '') + ' ' + result['exif'].get('Model', '')).strip()
	response['X-Data-Foto'] = result['exif'].get('DateTimeOriginal') or ''
	return response
