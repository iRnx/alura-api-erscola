from rest_framework import serializers
from escola.models import Aluno, Curso, Matricula


class AlunoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aluno
        fields = ('id', 'nome', 'rg', 'cpf', 'data_nascimento', 'foto', 'arquivo_pdf')


class CursoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Curso
        fields = '__all__'


class MatriculaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Matricula
        exclude = []


class ListaMatriculasAlunoSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Matricula
        fields = ('curso', 'periodo')

    curso = serializers.ReadOnlyField(source='curso.descricao')
    periodo = serializers.SerializerMethodField()

    def get_periodo(self, obj):
        return obj.get_periodo_display()
   

class ListaAlunosMatriculadosEmUmCursoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Matricula
        fields = ('aluno_nome',)

    aluno_nome = serializers.ReadOnlyField(source='aluno.nome')


# API V2
class AlunoSerializerV2(serializers.ModelSerializer):

    class Meta:
        model = Aluno
        fields = ('id', 'nome', 'rg', 'cpf', 'data_nascimento', 'celular', 'foto', 'arquivo_pdf')