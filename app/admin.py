from django.contrib import admin
from app.models import Usuario

# Register your models here.

# class UsuarioAdmin(admin.ModelAdmin):
#     list_display = ('nome', 'email', 'senha')


admin.site.register(Usuario)

