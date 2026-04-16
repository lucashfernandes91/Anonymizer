from django.db import models

# Create your models here.
class EstatisticaGlobal(models.Model):
	"""
	Contador global único — só existe 1 registro nessa tabela (singleton).
	Armazena o total de imagens processadas.
	"""
	imagens_processadas = models.PositiveIntegerField(default=0)
	atualizado_em = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Estatística Global"

	def __str__(self):
		return f"{self.imagens_processadas} imagens processadas"

	@classmethod
	def incrementar(cls):
		"""Incrementa o contador de forma atômica (thread-safe)."""
		from django.db.models import F
		obj, _ = cls.objects.get_or_create(pk=1)
		cls.objects.filter(pk=1).update(imagens_processadas=F('imagens_processadas') + 1)

	@classmethod
	def total(cls):
		obj, _ = cls.objects.get_or_create(pk=1)
		return obj.imagens_processadas


class ImagemProcessada(models.Model):
	"""
	Registra cada imagem processada vinculada à sessão do usuário.
	"""
	ORIGEM_CHOICES = [
		('web', 'Interface Web'),
		('api', 'API'),
	]

	acesso = models.ForeignKey(
		'AcessoUnico',
		on_delete=models.CASCADE,
		related_name='imagens',
	)
	nome_original = models.CharField(max_length=255, blank=True)
	tamanho_bytes = models.PositiveIntegerField(default=0)
	tinha_gps = models.BooleanField(default=False)
	lat = models.FloatField(null=True, blank=True)
	lon = models.FloatField(null=True, blank=True)
	dispositivo = models.CharField(max_length=255, blank=True)
	data_foto = models.CharField(max_length=100, blank=True)
	campos_removidos = models.PositiveIntegerField(default=0)
	origem = models.CharField(max_length=10, choices=ORIGEM_CHOICES, default='web')
	processada_em = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Imagem Processada"
		verbose_name_plural = "Imagens Processadas"
		ordering = ['-processada_em']

	def __str__(self):
		return f"{self.nome_original} — {self.processada_em.strftime('%d/%m/%Y %H:%M')}"


class AcessoUnico(models.Model):
	"""
	Registra acessos únicos por session_key.
	Cada sessão Django é contada uma única vez.
	"""
	session_key = models.CharField(max_length=64, unique=True)
	ip = models.GenericIPAddressField(null=True, blank=True)
	user_agent = models.TextField(blank=True)
	criado_em = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Acesso Único"
		verbose_name_plural = "Acessos Únicos"

	def __str__(self):
		return f"{self.session_key} — {self.criado_em.strftime('%d/%m/%Y %H:%M')}"

	@classmethod
	def total(cls):
		return cls.objects.count()
