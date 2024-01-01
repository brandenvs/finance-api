from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('stocks/', views.StockList.as_view(), name='stock-list'),
    path('stocks/<int:pk>/', views.StockDetail.as_view(), name='stock-detail'),
    path('strategies/', views.StrategyList.as_view(), name='strategy-list'),
    path('strategies/<int:pk>/', views.StrategyDetail.as_view(), name='strategy-detail'),
    path('strategy-analysis-results/', views.StrategyAnalysisResultList.as_view(), name='strategy-analysis-list'),
    path('strategy-analysis-results/<int:pk>/', views.StrategyAnalysisResultDetail.as_view(), name='strategy-analysis-detail'),
    path('', views.api_root, name='api-root'),
]

# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls')),
# ]

urlpatterns = format_suffix_patterns(urlpatterns)
