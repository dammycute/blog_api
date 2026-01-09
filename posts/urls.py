from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import PostViewset, 
from .views import PostView, PostUpdateDeleteView, TagView

# router = DefaultRouter()
# router.register(r'posts', PostViewset)


urlpatterns = [
    # path('', include(router.urls)),
    path('post', PostView.as_view(), name='posts'),
    path('post/<uuid:pk>', PostUpdateDeleteView.as_view(), name='post_update_delete'),
    path('tag', TagView.as_view(), name='tags'),
]
