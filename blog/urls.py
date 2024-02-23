from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path(
        route='tag/<slug:tag_slug>/',
        view=views.post_list,
        name='post_list_by_tag'
    ),
    path(
        route='<int:year>/<int:month>/<int:day>/<slug:post>/',
        view=views.post_detail,
        name='post_detail'
    ),
]
