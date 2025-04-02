
from django.urls import path
from .views import *


urlpatterns = [

    path('',Indexview.as_view(),name='Indexview'),
    path('Loginview',Loginview.as_view(),name='Loginview'),
    path('Admindashboard',Admindashboard.as_view(),name='Admindashboard'),
    path('Viewparkingslot',Viewparkingslot.as_view(),name='Viewparkingslot'),
    path('Viewpayments',Viewpayments.as_view(),name='Viewpayments'),
    path('Viewcustomers',Viewcustomers.as_view(),name='Viewcustomers'),
    path('LogoutView',LogoutView.as_view(),name='LogoutView'),
    #####parkassistant
    path('Addparkingslot',Addparkingslot.as_view(),name='Addparkingslot'),
    path('Deleteparkingslot/<int:id>',Deleteparkingslot.as_view(),name='Deleteparkingslot'),
    path('Editparkingslot/<int:id>',Editparkingslot.as_view(),name='Editparkingslot'),
    path('Parkdashboard',Parkdashboard.as_view(),name='Parkdashboard'),
    path('ParkViewcustomers',ParkViewcustomers.as_view(),name='ParkViewcustomers'),
    path('ParkViewparkingslot',ParkViewparkingslot.as_view(),name='ParkViewparkingslot'),
    path('ParkViewpaymentEditparkingslots',ParkViewpayments.as_view(),name='ParkViewpayments'),
    path('Registration',Registration.as_view(),name='Registration'),
    
    ######api view ################
    path('register', UserRegistration.as_view(), name='user_registration'),
    path('login',Loginapi.as_view(),name='Loginapi'),
    path('UserProfileView/<int:login_id>',UserProfileView.as_view(),name='UserProfileView'),
    path('AvailableSlotsView/<int:parkid>',AvailableSlotsView.as_view(),name='AvailableSlotsView'),
    path('AvailableTimeView/<int:slotid>/<str:date>/<str:duration>',AvailableTimeView.as_view(),name='AvailableTimeView'),
    path('BookSlotView',BookSlotView.as_view(),name='BookSlotView')


]
