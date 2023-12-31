from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# path('api-auth/', include('rest_framework.urls')),

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('stocks/', views.StockList.as_view(), name='stock-list'),
    path('stocks/<int:pk>/', views.StockDetail.as_view(), name='stock-detail'),
    path('options/', views.OptionList.as_view(), name='option-list'),
    path('options/<int:pk>/', views.OptionDetail.as_view(), name='option-detail'),
    path('financial-calculators/', views.FinancialCalculatorList.as_view(), name='financialcalculator-list'),
    path('financial-calculators/<int:pk>/', views.FinancialCalculatorDetail.as_view(), name='financialcalculator-detail'),
    path('strategies/', views.StrategyList.as_view(), name='strategy-list'),
    path('strategies/<int:pk>/', views.StrategyDetail.as_view(), name='strategy-detail'),
    path('probability-of-profits/', views.ProbabilityOfProfitList.as_view(), name='probabilityofprofit-list'),
    path('probability-of-profits/<int:pk>/', views.ProbabilityOfProfitDetail.as_view(), name='probabilityofprofit-detail'),
    path('user-strategies/', views.UserStrategiesListView.as_view(), name='user-strategies-list'),
    path('', views.api_root, name='api-root'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
