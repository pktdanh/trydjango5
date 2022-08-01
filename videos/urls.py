from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name= 'videos'
# router = DefaultRouter()

# router.register(r'video', views.VideoListView, basename='get_list_videos')
# router.register(r'inverted-index', views.TitleInvertedIndexView, basename='title_reverted_index')

urlpatterns = [
    path('',views.index,name='index'),
    path('video/', views.VideoListView.as_view(), name='get_list_videos'),
    path('video2/<pk>/', views.VideoDetailView.as_view(), name='get_detail_videos'),
    path('category/', views.CategoryListView.as_view(), name='get_all_categories'),
    path('search/', views.TextSearchView.as_view(), name='text_search_video'),
    path('reverted-index/', views.InvertedIndexView.as_view(), name='reverted_index'),
    path('inverted-index/', views.TitleInvertedIndexView.as_view(), name='title_reverted_index'),
    # path('', include(router.urls))

]
