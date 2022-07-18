from django.urls import path, include
from fix_store import settings
from .views import *


urlpatterns = [
    path('', RadioList.as_view(), name='radio'),
    path('radio_long_download/', radio_run, name='radio_long_download'),
    path('new_radio/', AddStation.as_view(), name='new_radio'),
    path('radio_edit/<int:pk>/', RadioEdit.as_view(), name='radio_edit'),
    path('<int:pk>/delete/', DeleteStation.as_view(), name='delete_st')
]
