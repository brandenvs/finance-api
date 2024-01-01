from django.urls import include, path

urlpatterns = [
    path('bcode-finance/', include('finance_api.urls')),
    path('bcode-users/', include('user_api.urls')),
]

