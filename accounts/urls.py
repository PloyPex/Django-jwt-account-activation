from django.urls import path

from .views import AccountActivate

app_name = 'accounts'

urlpatterns = [
	path('activate/<key>', AccountActivate.as_view(), name='activate'),
]
