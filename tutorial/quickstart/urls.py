from django.urls import path,include,re_path
from quickstart import views
from rest_framework import routers

from rest_framework.authtoken.views import obtain_auth_token

router=routers.DefaultRouter()
router.register(r'studentview',views.StudenetViewset,basename='student')
router.register(r'users',views.UserViewset)
router.register(r'song',views.SongViewset,basename='song')
router.register(r'singer',views.SingerViewset,basename='singer')

urlpatterns = [
    path('',include(router.urls)),
    path('slist',views.StudenetViewset.as_view({'get':'list'})),
    path('sret/<int:pk>',views.StudenetViewset.as_view({'get':'retrieve'})),
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),
    # path('student/', views.StudentView),
    # path('student/<int:pk>/', views.student_detail),
    # path('students/', views.student_list),
    # path('stdlist/', views.Student_list.as_view()),
    path('stddetail/<int:id>', views.stddetail),
    path('stdcreate/', views.stdcreate),
    path('stdupdate/<int:id>', views.stdupdate),
    path('stddelete/<int:id>', views.stddelete),
    path('stdlist/', views.stdlist),
    path('studentlist/', views.StudentList.as_view(),name='slist'),
    path('studentdetail/<int:id>', views.StudentDetail.as_view(),name='sdetail'),
    path('smlist/', views.StudentListmixin.as_view(),name='smlist'),
    path('sglist/', views.StudentListGeneric.as_view()),
    path('sgcreate/', views.StudentCreateGeneric.as_view()),
    path('sgdetail/<int:id>', views.StudentGenericDetail.as_view()),
    path('smdetail/<int:id>', views.StudentDetailMixin.as_view()),
    path('hello/', views.HelloView.as_view(),name='hello'),
    path('gettoken/',obtain_auth_token),
    # path('',views.api_root),
    path('sc/', views.empty_view),


    path('slistdetail/', views.Studentlistspiview.as_view()),
    # re_path('^slistdetail/(?P<name>.+)/$',views.Studentlistspiview.as_view()),


]

# urlpatterns=format_suffix_patterns(urlpatterns)

