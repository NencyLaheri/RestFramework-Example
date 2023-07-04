from django.contrib.auth.models import User,Group
from rest_framework import viewsets
from rest_framework import permissions
from quickstart.serializers import UserSerializer,groupSerializer,StudentSerialzer,SongSerializer,SingerSerializer
from django.shortcuts import get_object_or_404
from .models import StudentModel,Singer,Song
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import io
from rest_framework.decorators import api_view,throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,IsAuthenticatedOrReadOnly,DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly,DjangoObjectPermissions
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication 
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.reverse import reverse
from rest_framework import renderers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page,never_cache
from rest_framework.throttling import UserRateThrottle
from rest_framework.filters import SearchFilter,OrderingFilter,BaseFilterBackend
from django_filters.rest_framework import DjangoFilterBackend  
from rest_framework.pagination import PageNumberPagination  
from .paginationc import custompagination

class UserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated]


class GroupViewset(viewsets.ModelViewSet):
    queryset=Group.objects.all()
    serializer_class=groupSerializer
    permission_classes=[permissions.IsAuthenticated]



def StudentView(request):
    stu=StudentModel.objects.get(id=1)
    serializer=StudentSerialzer(stu)
    json_data=JSONRenderer().render(serializer.data)
    # return HttpResponse(json_data,content_type='application/json')
    # return JsonResponse(serializer.data)

    stream = io.BytesIO(json_data)
    data = JSONParser().parse(stream)
    deserializer = StudentSerialzer(data=data)
    deserializer.is_valid()
    print(deserializer.validated_data)
    return HttpResponse(deserializer.validated_data)



@csrf_exempt
def student_detail(request, pk):
  
    try:
        stu = StudentModel.objects.get(pk=pk)
    except StudentModel.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StudentSerialzer(stu)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StudentSerialzer(stu, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        stu.delete()
        return HttpResponse(status=204)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000
    

class StudenetViewset(viewsets.ModelViewSet):
    pagination_class=custompagination
    queryset=StudentModel.objects.all()
    serializer_class=StudentSerialzer
    # authentication_classes=[SessionAuthentication]
    # permission_classes = [DjangoObjectPermissions]


    # def list(self,request):
    #     queryset=StudentModel.objects.all()
    #     serializer=StudentSerialzer(queryset,many=True)
    #     return Response(serializer.data)

    # def retrieve(self,request,pk):
    #     queryset=StudentModel.objects.all()
    #     s=get_object_or_404(queryset,pk=pk)
    #     serializer=StudentSerialzer(s)
    #     return Response(serializer.data)
    
# @api_view(['GET','POST'])
# def student_list(request):
# class Student_list(APIView):
#     # if request.method=='GET':
#         def get(self,request):

#             s=StudentModel.objects.all()
#             serializers=StudentSerialzer(s,many=True)
#             return Response(serializers.data)
 
#     # elif request.method=='POST':
#         def post(self,request):
#             serializers=StudentSerialzer(data=request.data)
#             if serializers.is_valid():
#                 serializers.save()
#                 return Response(serializers.data,status=status.HTTP_201_CREATED)
#             return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)



class CustomUserRateThrottle(UserRateThrottle):
    rate= '5/day'

@api_view(['GET'])
# @throttle_classes([CustomUserRateThrottle])
def stdlist(request, format=None):
    # throttle_scope='burst'
    s=StudentModel.objects.all()
    serializer=StudentSerialzer(s,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def stddetail(request,id, format=None):
    s=StudentModel.objects.get(id=id)
    serializer=StudentSerialzer(s)
    return Response(serializer.data)

@api_view(['POST'])
def stdcreate(request, format=None):
    serializer=StudentSerialzer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def stdupdate(request,id, format=None):
    s=StudentModel.objects.get(id=id)
    serializer=StudentSerialzer(instance=s,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



@api_view(['DELETE'])
def stddelete(request,id, format=None):
    s=StudentModel.objects.get(id=id)
    s.delete()
    return Response('deleted')


class StudentList(APIView):
    
    def get(self,request, format=None):
        s=StudentModel.objects.all()
        serializer=StudentSerialzer(s,many=True)
        return Response(serializer.data)

    def post(self,request, format=None):
        serializer=StudentSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class StudentDetail(APIView):
    # permission_classes = [IsAuthenticated]
    # @method_decorator(never_cache)
    def get_object(self,id):
        try:
            s=StudentModel.objects.get(id=id)
            return s
        except StudentModel.DoesNotExist:
            raise Http404

    # @method_decorator(never_cache)
    def get(self,request,id,format=None):
        s=self.get_object(id)
        serializer=StudentSerialzer(s)
        return Response(serializer.data)


   
    # @method_decorator(never_cache)
    def put(self,request,id,format=None):
        s=self.get_object(id)
        serializer=StudentSerialzer(s,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # @method_decorator(never_cache)
    def delete(self,requst,id,format=None):
        s=self.get_object(id)
        s.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
class StudentListmixin(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=StudentModel.objects.all()
    serializer_class=StudentSerialzer
    authentication_classes=[SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # throttle_classes=[UserRateThrottle]
    throttle_scope='burst'

    @method_decorator(cache_page(30))
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    @method_decorator(cache_page(30))
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class StudentDetailMixin(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=StudentModel.objects.all()
    serializer_class=StudentSerialzer
    lookup_url_kwarg='id'


    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

 


class StudentListGeneric(generics.ListCreateAPIView):
    queryset=StudentModel.objects.all()
    serializer_class=StudentSerialzer


class StudentCreateGeneric(generics.CreateAPIView):
    queryset=StudentModel.objects.all()
    serializer_class=StudentSerialzer


class StudentGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentModel.objects.all()
    serializer_class = StudentSerialzer
    lookup_url_kwarg='id'



class HelloView(APIView):
    authentication_classes=[SessionAuthentication]
    permission_classes = [IsAuthenticated]             
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)



class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

@api_view(['GET'])
def api_root(request,foramt=None):
    return Response({'studentlist': reverse('smlist', request=request),'Message': reverse('hello', request=request)})



class StudentHighlight(generics.GenericAPIView):
    
    queryset = StudentModel.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        s = self.get_object()
        return Response(s.highlighted)


class SongViewset(viewsets.ModelViewSet):

    queryset=Song.objects.all()
    serializer_class=SongSerializer
    


class SingerViewset(viewsets.ModelViewSet):
    
    queryset=Singer.objects.all()
    serializer_class=SingerSerializer
    lookup_field='id'



class IsSingerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(name=request.user)
#-------------filtering------------------
class Studentlistspiview(generics.ListAPIView):
  
    #generic filtering--------
    # model=Singer
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['name']
    # #searchfields---------
    # filter_backends=[SearchFilter]
    # search_fields=['^name']
    # #orderingfilter--------
    # filter_backends=[OrderingFilter]
    # ordering_fields='__all__'
   


    # def get_queryset(self):
    #     name = self.request.user
    #     return Singer.objects.filter(name=name)

    # def get_queryset(self):
    #     #Filtering against the current user-----
    #     user = self.request.user
    #     return Singer.objects.filter(name=user)

    #     #Filtering against the url-----
    #     # name = self.kwargs['name']
    #     # return Singer.objects.filter(name=name)

    #     #Filtering against query parameters-----
    #     # queryset = Singer.objects.all()
    #     # name = self.request.query_params.get('name')
    #     # print(name)
    #     # if name is not None:
    #     #     queryset = queryset.filter(name=name)
    #     # return queryset

    
#---------status code-----------
@api_view(['GET'])
def empty_view(request):
    content = {'please move along': 'nothing to see here'}
    return Response(content, status=status.HTTP_404_NOT_FOUND)
 