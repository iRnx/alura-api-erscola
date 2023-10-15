from django.contrib import admin
from escola.models import Aluno, Curso, Matricula


@admin.register(Aluno)
class AlunosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'rg', 'cpf', 'data_nascimento')
    list_display_links = ('id', 'nome')
    search_fields = ('nome', 'cpf')
    list_per_page = 20


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_curso', 'descricao')
    list_display_links = ('id', 'codigo_curso')
    search_fields = ('codigo_curso',)


@admin.register(Matricula)
class MatriculasAdmin(admin.ModelAdmin):
    list_display = ('id', 'aluno', 'curso', 'periodo')
    list_display_links = ('id',)
