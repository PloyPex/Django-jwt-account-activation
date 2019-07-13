from django.urls import path

from .views import AccountActivateView

app_name = 'accounts'

urlpatterns = [
	path('activate/<slug:key>/', AccountActivateView.as_view(), name='activate'),
]
