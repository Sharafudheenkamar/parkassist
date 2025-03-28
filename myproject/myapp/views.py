from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class Indexview(View):
    def get(self,request):
        return render(request,'index.html')
    
class Loginview(View):
    def get(self,request):
        return render(request,'login.html')
class Admindashboard(View):
    def get(self,request):
        return render(request,'admininstrator/admindashboard.html')
class Parkdashboard(View):
    def get(self,request):
        return render(request,'parkassistant/parkdashboard.html')
    
class Addparkingslot(View):
    def get(self,request):
        return render(request,'admininstrator/addparkingslot.html')
class Viewparkingslot(View):
    def get(self,request):
        return render(request,'admininstrator/viewparkingslot.html')
class Deleteparkingslot(View):
    def get(self,request):
        return render(request,'admininstrator/viewparkingslot.html')   
class Editparkingslot(View):
    def get(self,request):
        return render(request,'admininstrator/editparkingslot.html')
class Viewpayments(View):
    def get(self,request):
        return render(request,'admininstrator/viewpayments.html')
class Viewcustomers(View):
    def get(self,request):
        return render(request,'admininstrator/viewcustomers.html')
class ParkViewcustomers(View):
    def get(self,request):
        return render(request,'parkassistant/viewcustomers.html')
    
class ParkViewparkingslot(View):
    def get(self,request):
        return render(request,'parkassistant/viewparkingslot.html')
class ParkViewpayments(View):
    def get(self,request):
        return render(request,'parkassistant/viewpayments.html')

class UserRegistration(APIView):
    def post(self, request, *args, **kwargs):
        loginserializer=LoginTableSerializer(data=request.data)
        userserializer = UserTableSerializer(data=request.data)
        
        if loginserializer.is_valid() and userserializer.is_valid():
            # Save the new user
            c=loginserializer.save()
            userserializer.save(LOGINID=c)
            return Response(
                {"message": "User registered successfully", "data": userserializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Error in registration", "errors": userserializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
class Loginapi(APIView):
    def post(self, request):
        response_dict = {}

        # Get data from the request
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate input
        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the user from LoginTable
        t_user = LoginTable.objects.filter(username=username).first()

        if not t_user:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_401_UNAUTHORIZED)

        # # Check password using check_password
        # if not check_password(password, t_user.password):
        #     response_dict["message"] = "failed"
        #     return Response(response_dict, status=HTTP_401_UNAUTHORIZED)

        # Successful login response
        response_dict["message"] = "success"
        response_dict["login_id"] = t_user.id

        return Response(response_dict, status=status.HTTP_200_OK)
    


