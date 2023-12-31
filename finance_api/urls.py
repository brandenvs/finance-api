from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# path('api-auth/', include('rest_framework.urls')),

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('strategies/', 
            views.StrategyList.as_view(), 
            name='strategy-list'),
    path('strategy/<int:pk>/', 
            views.StrategyDetail.as_view(), 
            name='strategy-detail'),
    path('strategies/<int:pk>/is-pinned/',
            views.StrategyPinned.as_view(),
            name='strategy-pinned'),
    path('users/', 
            views.UserList.as_view(),
            name='user-list'),
    path('users/<int:pk>/',
            views.UserDetail.as_view(),
            name='user-detail'),
])