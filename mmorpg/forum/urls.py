from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('edit/<int:pk>/', PostEdit.as_view(), name = 'post_edit'),
    path('response/<int:pk>/', make_response, name = 'make_response'),
    path('responses/', ResponseList.as_view(), name='response_list'),
    path('responses/remove/<int:pk>/', remove_response, name='remove_response'),
    path('responses/change/<int:pk>/', change_response, name='change_response'),
]