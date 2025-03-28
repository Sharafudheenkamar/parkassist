from pyexpat.errors import messages
from django.shortcuts import redirect, render,HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import Parkassistform, Slotform
from .models import *

# Create your views here.
class Indexview(View):
    def get(self,request):
        return render(request,'index.html')
    
class Loginview(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self, request):
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        print(username,password)


        try:
            login_obj = LoginTable.objects.get(Username=username, Password=password)
            request.session['userid'] = login_obj.id

            if login_obj.Type == "admin":
                return HttpResponse('''<script>alert("Welcome to Admin page");window.location="/Admindashboard"</script>''')
            elif login_obj.Type == "parkassistant":
                return HttpResponse('''<script>alert("Welcome to Park Assistant page");window.location="/Parkdashboard.html"</script>''')

        except LoginTable.DoesNotExist:
            return HttpResponse('''<script>alert("Invalid password");window.location="/"</script>''')    


class LogoutView(View):
    def get(self, request):
        if 'userid' in request.session:
            del request.session['userid']
        return HttpResponse('''<script>alert("You have been logged out successfully");window.location="/"</script>''')

    def post(self, request):
        if 'userid' in request.session:
            del request.session['userid']
        return HttpResponse('''<script>alert("You have been logged out successfully");window.location="/"</script>''')
class Admindashboard(View):
    def get(self,request):
        return render(request,'administrator/admindashboard.html')
class Parkdashboard(View):
    def get(self,request):
        return render(request,'parkassistant/parkdashboard.html')
    
class Addparkingslot(View):
    def get(self,request):
        return render(request,'parkassistant/addparkingslot.html')
    def post(self,request):
        user=UserTable.objects.get(LOGINID__id=request.sesssion['userid']).id
        form=Slotform(request.POST)
        if form.is_valid():
            re=form.save(commit=True)
            re.User=user
            re.save()
            return HttpResponse('''<script>alert("Parking slot added successfully");window.location="/Parkdashboard.html"</script>''')



class Viewparkingslot(View):
    def get(self,request):
        return render(request,'administrator/viewparkingslot.html')
class Deleteparkingslot(View):
    def get(self,request):
        return render(request,'administrator/viewparkingslot.html')   
class Editparkingslot(View):
    def get(self,request):
        return render(request,'parkassistant/editparkingslot.html')
class Viewpayments(View):
    def get(self,request):
        return render(request,'administrator/viewpayments.html')
class Viewcustomers(View):
    def get(self,request):
        return render(request,'administrator/viewcustomers.html')
class ParkViewcustomers(View):
    def get(self,request):
        return render(request,'parkassistant/viewcustomers.html')
    
class ParkViewparkingslot(View):
    def get(self,request):
        return render(request,'parkassistant/viewparkingslot.html')
class ParkViewpayments(View):
    def get(self,request):
      return render(request,'parkassistant/viewpayments.html')
class Registration(View):
    def get(self,request):
        return render(request,'parkassistant/registration.html')
    def post(self,request):
                # Check if username exists

        park_form = Parkassistform(request.POST)
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        if LoginTable.objects.filter(Username=username).exists():
            return HttpResponse('''<script>alert("Username already exist");window.location="/"</script>''')

        if park_form.is_valid():
            # Create login entry
            login_entry = LoginTable.objects.create(
                Username=username,
                Password=password,
                Type="parkassistant"
            )
            
            # Save Parkassist entry with reference to login entry
            park_assist = park_form.save(commit=False)
            park_assist.LOGINID = login_entry
            park_assist.save()

            # (request, "Parking Assistant registered successfully!")
            return redirect("Loginview")  # Change to your success URL
        else:
            messages.error(request, "Error in form submission. Please check the details.")
            return render(request, "registration.html")
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
    


