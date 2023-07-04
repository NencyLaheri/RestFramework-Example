from rest_framework import validators
from .models import StudentModel,Song,Singer
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields=['url','username','email','groups']


class groupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Group
        fields=['url','name']


def namev(value):
    if len(value)<=2:
        raise serializers.ValidationError('name shold be more than 2 char')
class StudentSerialzer(serializers.ModelSerializer):
    # name=serializers.CharField(max_length=100)
    # roll=serializers.IntegerField()
    # city=serializers.CharField(max_length=100)


    # def create(self,validated_data):
    #     return StudentModel.objects.create(**validated_data)
    name=serializers.CharField(validators=[namev])
    class Meta:
        model=StudentModel
        fields='__all__'
        # validators=[validators.UniqueTogetherValidator(queryset=StudentModel.objects.all(),fields=['name','roll'])]


class songrelatedfield(serializers.RelatedField):
    def to_representation(self, value):
        return value.title

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model=Song
        fields=['id','title','singer','duration']

    # def validate(self,data):
    #     t=data.get('title')
    #     d=data.get('duration')
    #     if len(t)<2 or len(t)>100:
    #         raise serializers.ValidationError('title must be more than 2 char and less than 100')
    #     if d<1:
    #         raise serializers.ValidationError('duration must be more than 1')

    #     return data
   

class SingerSerializer(serializers.ModelSerializer):
    song=songrelatedfield(many=True,read_only=True)
    name=serializers.CharField(validators=[UniqueValidator(queryset=Singer.objects.all(),message=("Name already exists"))])
    class Meta:
        model=Singer
        fields=['id','name','gender','song']
        # extra_kwargs = {
        #     'name': {'validators': [UniqueValidator(queryset=Singer.objects.all())]}
        # }

    # def validate_name(self,value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError('name must be more than 2 char.')


    


# class customhyperlinkrelatedfield(serializers.HyperlinkedRelatedField):
#     view_name='song-detail'
#     queryset=Song.objects.all()
#     titile=serializers.Ser

#     def get_url(self, obj, view_name, request, format):
#         url_kwargs={}

