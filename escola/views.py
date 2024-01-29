from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .serializer import AlunoSerializer, CursoSerializer, MatriculaSerializer, ListaMatriculasAlunoSerializer, ListaAlunosMatriculadosEmUmCursoSerializer, AlunoSerializerV2
from .models import Aluno, Curso, Matricula


# class UserRateThrottleCustom(UserRateThrottle):
#     rate = '1/minute'  # Defina a taxa desejada


class AlunosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os alunos e alunas"""

    queryset = Aluno.objects.all()
    authentication_classes = [BasicAuthentication]
    # throttle_classes = [UserRateThrottleCustom]
    
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.version == 'v2':
            return AlunoSerializerV2
        else:
            return AlunoSerializer


    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated, DjangoModelPermissions]) # False: sem o pk, True: com pk
    def matriculas(self, request, pk):

        alunos = Matricula.objects.filter(aluno__id=pk)
        serializer = ListaMatriculasAlunoSerializer(alunos, many=True, context={'request': request})
        return Response(serializer.data)


class CursosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os cursos"""

    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
   

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            id = str(serializer.data['id'])
            response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            response['Location'] = self.request.build_absolute_uri() + id

            return response



class MatriculasViewSet(viewsets.ModelViewSet):
    """Exibindo todas as matriculas"""


    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    authentication_classes = [BasicAuthentication]


    @method_decorator(cache_page(20))
    def dispatch(self, *args, **kwargs):
        return super(MatriculasViewSet, self).dispatch(*args, **kwargs)
    

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
    http_method_names = ['get', 'post', 'patch', 'put']


    def get_queryset(self):
        queryset = Matricula.objects.filter(curso__id=self.kwargs.get('pk'))
        return queryset
