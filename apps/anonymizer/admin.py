from django.contrib import admin
from .models import EstatisticaGlobal, AcessoUnico, ImagemProcessada


@admin.register(EstatisticaGlobal)
class EstatisticaGlobalAdmin(admin.ModelAdmin):
	list_display = ['imagens_processadas', 'atualizado_em']
	readonly_fields = ['imagens_processadas', 'atualizado_em']

	def has_add_permission(self, request):
		return not EstatisticaGlobal.objects.exists()

	def has_delete_permission(self, request, obj=None):
		return False


class ImagemProcessadaInline(admin.TabularInline):
	model = ImagemProcessada
	extra = 0
	readonly_fields = ['nome_original', 'tamanho_bytes', 'tinha_gps', 'lat', 'lon', 'dispositivo', 'data_foto', 'campos_removidos', 'origem', 'processada_em']
	can_delete = False

	def has_add_permission(self, request, obj=None):
		return False


@admin.register(AcessoUnico)
class AcessoUnicoAdmin(admin.ModelAdmin):
	list_display = ['session_key', 'ip', 'criado_em', 'total_imagens']
	readonly_fields = ['session_key', 'ip', 'user_agent', 'criado_em']
	list_filter = ['criado_em']
	search_fields = ['ip', 'session_key']
	ordering = ['-criado_em']
	inlines = [ImagemProcessadaInline]

	def total_imagens(self, obj):
		return obj.imagens.count()
	total_imagens.short_description = 'Imagens'

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False


@admin.register(ImagemProcessada)
class ImagemProcessadaAdmin(admin.ModelAdmin):
	list_display = ['nome_original', 'acesso', 'tamanho_bytes', 'tinha_gps', 'dispositivo', 'origem', 'processada_em']
	readonly_fields = ['acesso', 'nome_original', 'tamanho_bytes', 'tinha_gps', 'lat', 'lon', 'dispositivo', 'data_foto', 'campos_removidos', 'origem', 'processada_em']
	list_filter = ['tinha_gps', 'origem', 'processada_em']
	search_fields = ['nome_original', 'dispositivo', 'acesso__session_key']
	ordering = ['-processada_em']

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False
