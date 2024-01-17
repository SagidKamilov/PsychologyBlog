from registration.views import registration
from django.urls import path


app_name = 'registration'


urlpatterns = [
    path('create/', registration, name='registration')
]
