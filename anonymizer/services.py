import io
import random
from PIL import Image, ExifTags
from django.shortcuts import render
import requests


# Ordenado por criticidade
CRITICIDADE = {
	"GPSInfo": ("CRÍTICO", 1),
	"DateTimeOriginal": ("CRÍTICO", 2),
	"DateTimeDigitized": ("CRÍTICO", 2),
	"DateTime": ("CRÍTICO", 2),
	"Make": ("CRÍTICO", 3),
	"Model": ("CRÍTICO", 3),
	"BodySerialNumber": ("CRÍTICO", 3),

	"Software": ("ALTO", 4),
	"Artist": ("ALTO", 4),
	"Copyright": ("ALTO", 4),

	"ExposureTime": ("MÉDIO", 5),
	"FNumber": ("MÉDIO", 5),
	"ISOSpeedRatings": ("MÉDIO", 5),
	"FocalLength": ("MÉDIO", 5),

	"ImageWidth": ("BAIXO", 6),
	"ImageLength": ("BAIXO", 6),
}


def extrair_exif(img):
	exif_data = {}
	gps_detectado = False
	lat = None
	lon = None

	try:
		exif = img._getexif()

		if exif:
			for tag, value in exif.items():
				tag_name = ExifTags.TAGS.get(tag, tag)

				if tag_name == "GPSInfo":
					gps_detectado = True

					gps_data = {}
					for t in value:
						sub_tag = ExifTags.GPSTAGS.get(t, t)
						gps_data[sub_tag] = value[t]

					if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
						lat = dms_to_decimal(
							gps_data.get("GPSLatitude"),
							gps_data.get("GPSLatitudeRef")
						)

						lon = dms_to_decimal(
							gps_data.get("GPSLongitude"),
							gps_data.get("GPSLongitudeRef")
						)

				# limpa bytes
				if isinstance(value, bytes):
					continue

				exif_data[tag_name] = str(value)

	except Exception as e:
		print("ERRO EXIF:", e)

	return exif_data, gps_detectado, lat, lon


def anonimizar_imagem(image_file):
	img = Image.open(image_file)

	# extrai metadados antes
	exif_original, gps_detectado, lat, lon = extrair_exif(img)

	# remove metadados
	img = img.convert("RGB")
	pixels = img.load()

	for _ in range(100):
		x = random.randint(0, img.width - 1)
		y = random.randint(0, img.height - 1)
		r, g, b = pixels[x, y]
		pixels[x, y] = (
			max(0, min(255, r + random.randint(-3, 3))),
			max(0, min(255, g + random.randint(-3, 3))),
			max(0, min(255, b + random.randint(-3, 3))),
		)

	buffer = io.BytesIO()
	img.save(buffer, format="JPEG", quality=90)
	buffer.seek(0)

	return buffer, exif_original, gps_detectado, lat, lon


def converter_gps(valor):
	try:
		graus = float(valor[0][0]) / float(valor[0][1])
		minutos = float(valor[1][0]) / float(valor[1][1])
		segundos = float(valor[2][0]) / float(valor[2][1])

		return graus + (minutos / 60.0) + (segundos / 3600.0)
	except Exception:
		return None


def obter_endereco(lat, lon):
	"""
	Retorna dicionário com campos separados:
	rua, numero, bairro, cidade, estado, pais, cep, display
	"""
	try:
		url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&addressdetails=1"

		headers = {
			"User-Agent": "anonimizador-app/1.0"
		}

		response = requests.get(url, headers=headers, timeout=5)

		if response.status_code == 200:
			data = response.json()
			addr = data.get("address", {})

			rua = (
				addr.get("road") or
				addr.get("pedestrian") or
				addr.get("footway") or
				addr.get("street") or
				addr.get("path") or
				""
			)

			numero  = addr.get("house_number", "s/n")
			bairro  = addr.get("neighbourhood") or addr.get("suburb") or addr.get("quarter") or ""
			cidade  = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality") or ""
			estado  = addr.get("state", "")
			pais    = addr.get("country", "")
			cep     = addr.get("postcode", "")

			partes = []
			if rua:
				partes.append(f"{rua}, {numero}" if numero != "s/n" else rua)
			if bairro:
				partes.append(bairro)
			if cidade:
				partes.append(cidade)
			if estado:
				partes.append(estado)
			if pais:
				partes.append(pais)

			return {
				"rua":     rua,
				"numero":  numero,
				"bairro":  bairro,
				"cidade":  cidade,
				"estado":  estado,
				"pais":    pais,
				"cep":     cep,
				"display": " — ".join(partes) if partes else data.get("display_name", ""),
			}

	except Exception as e:
		print("Erro ao buscar endereço:", e)

	return None


def parse_gps_info(gps_info):
	gps_parsed = {}

	for key in gps_info:
		nome = ExifTags.GPSTAGS.get(key, key)
		gps_parsed[nome] = gps_info[key]

	return gps_parsed


def extrair_classificar_metadados(image_file):
	image_file.seek(0)
	img = Image.open(image_file)

	exif_data = img._getexif()

	if not exif_data:
		return []

	metadados = []

	for tag_id, valor in exif_data.items():
		tag = ExifTags.TAGS.get(tag_id, tag_id)

		# tratar GPS
		if tag == "GPSInfo":
			valor = parse_gps_info(valor)

		nivel, prioridade = CRITICIDADE.get(tag, ("BAIXO", 999))

		metadados.append({
			"tag": tag,
			"valor": str(valor),
			"criticidade": nivel,
			"prioridade": prioridade
		})

	# ordenação por criticidade
	metadados.sort(key=lambda x: x["prioridade"])

	return metadados


def dms_to_decimal(dms, ref):
	try:
		def to_float(x):
			if isinstance(x, tuple):
				return float(x[0]) / float(x[1])
			return float(x)

		graus    = to_float(dms[0])
		minutos  = to_float(dms[1])
		segundos = to_float(dms[2])

		decimal = graus + (minutos / 60.0) + (segundos / 3600.0)

		if ref in ["S", "W"]:
			decimal = -decimal

		return decimal

	except Exception as e:
		print("Erro ao converter GPS:", e)
		return None
