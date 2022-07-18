from django.urls import path, include
from fix_store import settings
from repair_shop.views import *
from radio_st.views import RadioList

urlpatterns = [
    path('', index, name='home'),
    path('radio/', RadioList.as_view(), name='radio_play'),
    path('contacts/', about, name='contacts'),
    path('queued/', Queued.as_view(), name='queued'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('cabinet/', AdminWorkCabinet.as_view(), name='cabinet'),
    path('client_card/<slug:client_card_slug>/', ShowCard.as_view(), name='client_card'),
    path('new_order/', AddOrder.as_view(), name='new_order'),
    path('queued/<slug:client_card_slug>/<int:pk>', CardUpdateView.as_view(), name='master-select'),
    path('warranty/<slug:client_card_slug>/<int:pk>', WarrantyUpdateView.as_view(), name='warranty-update')
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns