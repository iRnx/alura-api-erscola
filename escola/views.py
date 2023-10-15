from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializer import AlunoSerializer, CursoSerializer, MatriculaSerializer, ListaMatriculasAlunoSerializer, ListaAlunosMatriculadosEmUmCursoSerializer
from .models import Aluno, Curso, Matricula



class AlunosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os alunos e alunas"""

    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


    @action(detail=True, methods=['GET']) # False: sem o pk, True: com pk
    def matriculas(self, request, pk):

        alunos = Matricula.objects.filter(aluno__id=pk)
        serializer = ListaMatriculasAlunoSerializer(alunos, many=True, context={'request': request})
        return Response(serializer.data)


class CursosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os cursos"""

    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class MatriculasViewSet(viewsets.ModelViewSet):
    """Exibindo todas as matriculas"""

    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer


# class ListaMatriculasAluno(generics.ListAPIView):
#     """Listando as matriculas de um aluno """

#     serializer_class = ListaMatriculasAlunoSerializer

#     def get_queryset(self):
#         queryset = Matricula.objects.filter(aluno__id=self.kwargs.get('pk'))
#         return queryset
    

# Endpoint cursos
class ListaAlunosMatriculados(generics.ListAPIView):
    """Listando alunos e alunas matriculados em um curso"""

    serializer_class = ListaAlunosMatriculadosEmUmCursoSerializer

    def get_queryset(self):
        queryset = Matricula.objects.filter(curso__id=self.kwargs.get('pk'))
        return queryset
