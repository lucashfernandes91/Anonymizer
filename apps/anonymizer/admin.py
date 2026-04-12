from django.contrib import admin
from .models import EstatisticaGlobal, AcessoUnico


@admin.register(EstatisticaGlobal)
class EstatisticaGlobalAdmin(admin.ModelAdmin):
	list_display = ['imagens_processadas', 'atualizado_em']
	readonly_fields = ['imagens_processadas', 'atualizado_em']

	def has_add_permission(self, request):
		return not EstatisticaGlobal.objects.exists()

	def has_delete_permission(self, request, obj=None):
		return False


@admin.register(AcessoUnico)
class AcessoUnicoAdmin(admin.ModelAdmin):
	list_display = ['session_key', 'ip', 'criado_em']
	readonly_fields = ['session_key', 'ip', 'user_agent', 'criado_em']
	list_filter = ['criado_em']
	search_fields = ['ip', 'session_key']
	ordering = ['-criado_em']

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False
