
from django.urls import path
from .views import *


urlpatterns = [

    path('Indexview',Indexview.as_view(),name='Indexview'),
    path('Loginview',Loginview.as_view(),name='Loginview'),
    path('Admindashboard',Admindashboard.as_view(),name='Admindashboard'),
    path('Addparkingslot',Addparkingslot.as_view(),name='Addparkingslot'),
    path('Viewparkingslot',Viewparkingslot.as_view(),name='Viewparkingslot'),
    path('Deleteparkingslot',Deleteparkingslot.as_view(),name='Deleteparkingslot'),
    path('Editparkingslot',Editparkingslot.as_view(),name='Editparkingslot'),
    path('Viewpayments',Viewpayments.as_view(),name='Viewpayments'),


    #####parkassistant
    path('Parkdashboard',Parkdashboard.as_view(),name='Parkdashboard'),
    path('ParkViewcustomers',ParkViewcustomers.as_view(),name='ParkViewcustomers'),
    path('ParkViewparkingslot',ParkViewparkingslot.as_view(),name='ParkViewparkingslot'),
    path('ParkViewpayments',ParkViewpayments.as_view(),name='ParkViewpayments'),

    
    ######api view ################
    # path('register/', UserRegistration.as_view(), name='user_registration'),
    # path('loginapi/',Loginapi.as_view(),name='Loginapi'),

]
