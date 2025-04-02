from pyexpat.errors import messages
from django.shortcuts import redirect, render,HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .serializers import *

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
                return HttpResponse('''<script>alert("Welcome to Park Assistant page");window.location="/Parkdashboard"</script>''')

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
        user=Parkassist.objects.get(LOGINID__id=request.session['userid'])
        form=Slotform(request.POST)
        if form.is_valid():
            re=form.save(commit=True)
            re.parkid=user
            re.save()
            return HttpResponse('''<script>alert("Parking slot added successfully");window.location="/ParkViewparkingslot"</script>''')



class Viewparkingslot(View):
    def get(self,request):
        sl=Slot.objects.all()
        return render(request,'administrator/viewparkingslot.html',{'slots':sl})
class Deleteparkingslot(View):
    def get(self,request,id):
        sl=Slot.objects.get(id=id)
        sl.delete()
        return redirect('ParkViewparkingslot')
class Editparkingslot(View):
    def get(self,request,id):
        sl=Slot.objects.get(id=id)
        return render(request,'parkassistant/editparkingslot.html',{'sl':sl})

    def post(self,request,id):
        sl=Slot.objects.get(id=id)
        form=Slotform(request.POST,instance=sl)
        if form.is_valid():
            re=form.save()
            re.save()
            return HttpResponse('''<script>alert("Parking slot edited successfully");window.location="/ParkViewparkingslot"</script>''')


        
        
class Viewpayments(View):
    def get(self,request):
        tr=Transaction.objects.all()
        return render(request,'administrator/viewpayments.html',{'tr':tr})
class Viewcustomers(View):
    def get(self,request):
        cust=Booking.objects.all()
        return render(request,'administrator/viewcustomers.html',{'customers':cust})
class ParkViewcustomers(View):
    def get(self,request):
        cust=Booking.objects.filter(slotid__parkid__LOGINID__id=request.session['userid']).all()
        return render(request,'parkassistant/viewcustomers.html',{'customers':cust})
    
class ParkViewparkingslot(View):
    def get(self,request):
        sl=Slot.objects.filter(parkid__LOGINID__id=request.session['userid']).all()
        return render(request,'parkassistant/viewparkingslot.html',{'slots':sl})
class ParkViewpayments(View):
    def get(self,request):
      tr=Transaction.objects.filter(station__LOGINID__id=request.session['userid']).all()
      return render(request,'parkassistant/viewpayments.html',{'tr':tr})
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
        print(request.data)
        data={}
        data=request.data
        data['Username']=request.data.get('Email')
        print(data)
        loginserializer=LoginTableSerializer(data=data)
        userserializer = UserTableSerializer(data=data)
        
        if loginserializer.is_valid() and userserializer.is_valid():
            # Save the new user
            c=loginserializer.save(Type='user')
            d=userserializer.save(LOGINID=c)
            Wallet.objects.create(user=d,amount=10000)
            return Response(
                {"message": "User registered successfully", "data": userserializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Error in registration", "errors": userserializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import UserTable
from .serializers import UserTableSerializer

class UserProfileView(APIView):
    def get(self, request, login_id=None):
        """Retrieve a user's profile."""
        if login_id:
            user = get_object_or_404(UserTable, LOGINID__id=login_id)
            serializer = UserTableSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        users = UserTable.objects.all()
        serializer = UserTableSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, login_id):
        """Update a user's profile."""
        user = get_object_or_404(UserTable, LOGINID__id=login_id)
        serializer = UserTableSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Loginapi(APIView):
    def post(self, request):
        print(request.data)
        response_dict = {}

        # Get data from the request
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate input
        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the user from LoginTable
        t_user = LoginTable.objects.filter(Username=username,Password=password).first()

        if not t_user:
            response_dict["message"] = "no user found"
            return Response(response_dict, status=status.HTTP_200_OK)

        # # Check password using check_password
        # if not check_password(password, t_user.password):
        #     response_dict["message"] = "failed"
        #     return Response(response_dict, status=HTTP_401_UNAUTHORIZED)

        # Successful login response
        response_dict["message"] = "success"
        response_dict["login_id"] = t_user.id
        response_dict["usertype"] = t_user.Type
        print(response_dict)

        return Response(response_dict, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from .models import Parkassist, Slot, Booking
from .serializers import SlotSerializer

class AvailableSlotsView(APIView):
    """
    API to get available slots for a given park ID.
    """
    def get(self, request, parkid):
        try:
            slots = Slot.objects.filter(parkid=parkid)
            serializer = SlotSerializer(slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Parkassist.DoesNotExist:
            return Response({"error": "Park not found"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from .models import Slot, Booking

class AvailableTimeView(APIView):
    """
    API to get available time slots for a specific slot and date, with price calculation.
    """

    def get(self, request, slotid, date, duration):
        try:
            slot = Slot.objects.get(id=slotid)
            park = slot.parkid
            duration = int(duration)  # Convert duration to an integer (in minutes)

            # Get bookings for the selected slot and date
            existing_bookings = Booking.objects.filter(slotid=slot, bookingdate=date).order_by("bookingstarttime")

            # Get opening and closing times
            opening_time = park.openingtime
            closing_time = park.closingtime

            if not opening_time or not closing_time:
                return Response({"error": "Opening and closing times not set for this park"},
                                status=status.HTTP_400_BAD_REQUEST)

            available_intervals = []

            # Convert time fields to datetime objects
            current_time = datetime.combine(datetime.today(), opening_time)
            closing_datetime = datetime.combine(datetime.today(), closing_time)

            for booking in existing_bookings:
                booked_start = datetime.combine(datetime.today(), booking.bookingstarttime)
                booked_end = datetime.combine(datetime.today(), booking.bookingendtime)

                # If there's a gap before the booked slot, add it
                if current_time < booked_start:
                    available_intervals.append((current_time.time(), booked_start.time()))

                # Move the current_time pointer
                current_time = booked_end

            # Check for available time at the end
            if current_time < closing_datetime:
                available_intervals.append((current_time.time(), closing_datetime.time()))

            # Filter available slots based on selected duration
            valid_slots = []
            price_per_minute = slot.slotprice / 60  # Convert price per hour to per minute

            for start, end in available_intervals:
                start_dt = datetime.combine(datetime.today(), start)
                end_dt = datetime.combine(datetime.today(), end)

                while start_dt + timedelta(minutes=duration) <= end_dt:
                    slot_price = round(price_per_minute * duration, 2)  # Calculate price for selected duration
                    valid_slots.append({
                        "start_time": start_dt.time(),
                        "end_time": (start_dt + timedelta(minutes=duration)).time(),
                        "price": f"₹{slot_price}"  # Include price for the duration
                    })
                    start_dt += timedelta(minutes=duration)  # Move to next slot

            return Response({
                "available_time_slots": valid_slots,
                "slot": slot.id,
                "slot_price_per_hour": f"₹{slot.slotprice}",  # Added slot price per hour
                "date": date
            }, status=status.HTTP_200_OK)

        except Slot.DoesNotExist:
            return Response({"error": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)

class BookSlotView(APIView):
    """
    API to book an available slot.
    """
    def post(self, request):
        print(request.data)
        user_id = request.data.get("user")
        print(user_id)
        user_id = UserTable.objects.get(LOGINID__id=user_id).id
        slotid = request.data.get("slotid")
        date = request.data.get("bookingdate")
        start_time = request.data.get("bookingstarttime")
        end_time = request.data.get("bookingendtime")
        amount=request.data.get("amount")
        station=Slot.objects.get(id=slotid).parkid
        transactiontype=request.data.get("transactiontype")

        try:
            slot = Slot.objects.get(id=slotid)

            # Ensure the selected time is available
            existing_bookings = Booking.objects.filter(slotid=slot, bookingdate=date,
                                                       bookingstarttime__lt=end_time,
                                                       bookingendtime__gt=start_time)

            if existing_bookings.exists():
                return Response({"error": "Selected time is already booked"}, status=status.HTTP_400_BAD_REQUEST)

            # Save booking
            booking = Booking.objects.create(
                slotid=slot,
                user_id=user_id,
                bookingdate=date,
                bookingstarttime=start_time,
                bookingendtime=end_time
            )
            booking.save()
            tr=Transaction.objects.create(user=user_id,station=station,amount=amount,transactiontype=transactiontype)
            tr.save()

            return Response({"message": "Booking successful"}, status=status.HTTP_201_CREATED)

        except Slot.DoesNotExist:
            return Response({"error": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)

class Viewwallet(APIView):
    def get(self,request,id):
        user=UserTable.objects.get(LOGINID__id=id).id
        ser=Wallet.objects.filter(user__id=user).first()
        ser=Walletserializer(ser)
        return Response(ser.data)
    def post(self, request, id):
        """Create a new wallet entry for a user"""
        user = get_object_or_404(UserTable, LOGINID__id=id)
        data = request.data.copy()
        data["user"] = user.id  # Assigning the user to the wallet

        serializer = Walletserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """Update wallet details for a user"""
        try:
            print(request.data)
            user = get_object_or_404(UserTable, LOGINID__id=id)
            print(user)
            wallet = Wallet.objects.filter(user=user).first()
            print(wallet)
            added_balance = float(request.data.get("amount", 0))

            if added_balance < 0:
                return Response({"message": "Balance must be a positive value"}, status=status.HTTP_400_BAD_REQUEST)

            wallet.amount += added_balance  # Update balance
            wallet.save()

            
            if not wallet:
                return Response({"message": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response(status=status.HTTP_200_OK)
            
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        