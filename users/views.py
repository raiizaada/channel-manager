from email.policy import Policy
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rentals.forms import CreateUserForm, InvoiceForm, InvoiceItemFormset, RentalsGalleryForm
from rentals.models import  Activity, Amenities, AmenitiesType, Attributes, BasicRates, Bed, Bookings, Channel, ChannelManagement, CompanyProfile, Country, CustomServices, Discount, Currency, DiscountType, EarlyBirdDiscount, ExtraServices, HouseRules, Invoice, InvoiceItem, LongStayDiscount, OtherRooms, PropertyRole, Rate, Ratetype, Rental, RentalAmenities, RentalBasic, RentalCleaning, RentalDeposit, RentalInstruction, RentalLocation, RentalOtherRooms, RentalPolicy, RentalTax, RentalsGallery, Rentaltype,Policy, Room, Roomtype, SeasonalRates, Subscription, SubscriptionPlan, Tax, Taxtype, UserProfile
from django.contrib.auth.models import User
from django.views import View 
from django.contrib.auth import get_user_model
from rentals.forms import CreateUserForm
from rest_framework import viewsets
from users.serializers import BookingsSerializer, RentalSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rentals.models import  Event
from rentals.utils import Calendar
from rentals.forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

# Dashboard Code start
@login_required(login_url='/users/')
def index(request):
    rentalCount=Rental.objects.filter(user_id=request.user.id).count()
    bookingCount=Bookings.objects.filter(user_id=request.user.id).count()
    bookings=Bookings.objects.filter(user_id=request.user.id)
    context={
        "rentalCount":rentalCount,
        "bookingCount":bookingCount,
        "bookings":bookings
    }
    return render(request,'users/dashboard/dashboard.html',context)

# Dashboard Code end    
   
def customers(request):
    return render(request,'users/customer/customers.html')    

# Authentication Code start

def register(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account successfully created for ' + user)
                LastInsertId = (User.objects.last()).id
                LastRow = User.objects.get(id=LastInsertId)
       
                if LastRow.is_staff==0 and LastRow.is_superuser== 0:
                
                    UserProfiles = UserProfile() 
                    UserProfiles.first_name = 'NA'
                    UserProfiles.last_name = 'NA'
                    UserProfiles.phone = 'NA'
                    UserProfiles.address = 'NA'
                    UserProfiles.city= 'NA'
                    UserProfiles.state='NA'
                    UserProfiles.coutry = 'NA'
                    UserProfiles.postal_code = '201308'
                    UserProfiles.property_phone_number = 'NA'
                    UserProfiles.tollfree = 'NA'
                    UserProfiles.website = 'NA'
                    UserProfiles.property_logo = 'NA'
                    UserProfiles.status = '1'
                    UserProfiles.user_id =  LastRow.id           
                    UserProfiles.save()
                

                return redirect('/')
            else:
                messages.success(request, 'Invalid credentials.')    
            

        context = {'form':form}
    return render(request,'users/authentication/register.html',context)  

def auth_view(request):
    username = password = ""
    username = request.POST.get('username')
    password =request.POST.get('password')
    if username == 'demon':
        users=authenticate(username=username, password=password)   
        if users is not None:
                login(request, users)
                return HttpResponseRedirect('/dashboard')
        else:
                messages.info(request, 'Your account is deactivated,please contact support team.')
                    
    else:
        try:
            users=authenticate(username=User.objects.get(email=username),password=password)
        except:   
            users=authenticate(username=username, password=password) 
        if users is not None:
                login(request, users)
                return HttpResponseRedirect('/dashboard')
        else:
                messages.info(request, 'Your account is deactivated,please contact support team.')
    context = {}
    return render(request,'users/authentication/signin.html',context)                 
                  
def logoutuser(request):
    logout(request)
    return redirect('/signin')    

def resetpassword(request):
    return render (request,'users/authentication/reset-password.html')

def error_404_view(request,exception):
    return render(request,'404.html')

def error_back(request):
    return redirect(request.META.get('HTTP_REFERER'))
    
# Authentication Code end

# Rental-Type Code Start

@login_required(login_url='/users/')
def rental_type_insert(request):
    if request.method == "POST": 
        rentaltype=Rentaltype()
        rentaltype.room_type_name=request.POST.get('room_type_name')
        rentaltype.noof_beds=request.POST.get('noof_beds')
        rentaltype.max_occupancy=request.POST.get('max_occupancy')
        rentaltype.noof_rooms=request.POST.get('noof_rooms')
        rentaltype.picture=request.FILES.get('picture')
        rentaltype.rental_description=request.POST.get('rental_description')
        rentaltype.status=request.POST.get('status')
       
        rentaltype.save()
        messages.success(request, ' Row added Successfully.')
    return redirect ('/users/rental-type')

    

@login_required(login_url='/users/')     
def rental_type_add(request):
    return render(request,"users/rentals/rental-type-add.html")  

# @login_required(login_url='/users/')
def rental_type(request):  
    rentaltype = Rentaltype.objects.all()
    return render(request,"users/rentals/rental-type.html",{'rentaltype':rentaltype})  

@login_required(login_url='/users/')
def rental_type_edit(request, id):  
    rentaltype= Rentaltype.objects.get(id=id)  
    return render(request,'users/rentals/rental-type-edit.html', {'rentaltype':rentaltype})  

@login_required(login_url='/users/')
def rental_type_update(request, id):    
    if request.method == "POST": 
        rentaltype= Rentaltype.objects.get(id=id)
        rentaltype.room_type_name=request.POST.get('room_type_name')
        rentaltype.noof_beds=request.POST.get('noof_beds')
        rentaltype.max_occupancy=request.POST.get('max_occupancy')
        rentaltype.noof_rooms=request.POST.get('noof_rooms')
        if 'picture' in request.FILES:
             rentaltype.picture=request.FILES.get('picture')
        rentaltype.rental_description=request.POST.get('rental_description')
        rentaltype.status=request.POST.get('status')
        rentaltype.save()
        messages.success(request, ' Row updated Successfully.')
        return redirect('/users/rental-type')
   
    return render(request, 'users/rentals/rental-type-edit.html', {'rentaltype': rentaltype})  

@login_required(login_url='/users/')
def rental_type_destroy(request, id):  
    rentaltype = Rentaltype.objects.get(id=id)  
    rentaltype.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect("/users/rental-type") 

# Rental-Type Code end    

# Rentals Code start


@login_required(login_url='/users/')
def rental_insert(request):
    if request.method == "POST": 
        rental=Rental()
        rental.rental_name=request.POST.get('rental_name')
        rental.rental_short_description=request.POST.get('rental_short_description')
        rental.rental_description=request.POST.get('rental_description')
        rental.cover_image=request.FILES.get('cover_image')
        rental.user_id=request.user.id
        rental.save()
        LastInsertId = (Rental.objects.last()).id
        LastRow = Rental.objects.get(id=LastInsertId)

        rentalbasic=RentalBasic()
        rentalbasic.rental_type=""
        rentalbasic.rental_basis=""
        rentalbasic.floorspace=""
        rentalbasic.floorspace_units=""
        rentalbasic.grounds=""
        rentalbasic.grounds_units=""
        rentalbasic.floors_building=""
        rentalbasic.entrance=""
        rentalbasic.rental_licence=""
        rentalbasic.user_id=request.user.id
        rentalbasic.rental_id=LastRow.id
        rentalbasic.save()

        location=RentalLocation()
        location.country=""
        location.address=""
        location.apartment=""
        location.city=""
        location.state=""
        location.postal=""
        location.user_id=request.user.id
        location.rental_id=LastRow.id
        location.save()

        rentalamenities=RentalAmenities()
        rentalamenities.amenities=""
        rentalamenities.user_id=request.user.id
        rentalamenities.rental_id=LastRow.id
        rentalamenities.save()

        longstaydiscount=LongStayDiscount()
        longstaydiscount.seven_nights=""
        longstaydiscount.fourteen_nights=""
        longstaydiscount.twenty_one_nights=""
        longstaydiscount.twenty_eight_nights=""
        longstaydiscount.user_id=request.user.id
        longstaydiscount.rental_id=LastRow.id
        longstaydiscount.save()

        earlybirddiscount=EarlyBirdDiscount()
        earlybirddiscount.booking_less=""
        earlybirddiscount.booking_less_discount=""
        earlybirddiscount.booking_more=""
        earlybirddiscount.booking_more_discount=""
        earlybirddiscount.user_id=request.user.id
        earlybirddiscount.rental_id=LastRow.id
        earlybirddiscount.save()

        houserules=HouseRules()
        houserules.for_kid=""
        houserules.wheelchair_access=""
        houserules.parties_allowed=""
        houserules.smoking_allowed=""
        houserules.pets=""
        houserules.house_rules=""
        houserules.user_id=request.user.id
        houserules.rental_id=LastRow.id
        houserules.save()

        rentalpolicy=RentalPolicy()
        rentalpolicy.name=""
        rentalpolicy.description=""
        rentalpolicy.user_id=request.user.id
        rentalpolicy.rental_id=LastRow.id
        rentalpolicy.save()

        rentalinstruction=RentalInstruction()
        rentalinstruction.checkin_instruction=""
        rentalinstruction.checkout_instruction=""
        rentalinstruction.checkin_contact=""
        rentalinstruction.key_collection=""
        rentalinstruction.telephone_country=""
        rentalinstruction.telephone_number=""
        rentalinstruction.instructions=""
        rentalinstruction.attach_instruction=""
        rentalinstruction.checkin_from=""
        rentalinstruction.checkout_until=""
        rentalinstruction.airport_instruction=""
        rentalinstruction.property_directions=""
        rentalinstruction.user_id=request.user.id
        rentalinstruction.rental_id=LastRow.id
        rentalinstruction.save()

        basicrates=BasicRates()
        basicrates.currency=""
        basicrates.basic_night=""
        basicrates.weekend_night=""
        basicrates.guest_number=""
        basicrates.minimum_stay=""
        basicrates.maximum_stay=""
        basicrates.user_id=request.user.id
        basicrates.rental_id=LastRow.id
        basicrates.save()

        rentalcleaning=RentalCleaning()
        rentalcleaning.cleaning_available=""
        rentalcleaning.cleaning_basis=""
        rentalcleaning.price=""
        rentalcleaning.user_id=request.user.id
        rentalcleaning.rental_id=LastRow.id
        rentalcleaning.save()

        rentaldeposit=RentalDeposit()
        rentaldeposit.security_deposit=""
        rentaldeposit.amount=""
        rentaldeposit.user_id=request.user.id
        rentaldeposit.rental_id=LastRow.id
        rentaldeposit.save()

        path1 ="/rentals/overview/"
        path2=str(LastInsertId)
        path = path1+path2
    messages.success(request, 'Row updated Successfully.')
    return HttpResponseRedirect(path)
        
       
@login_required(login_url='/users/')
def rental_add(request): 
    return render(request,"users/rentals/rental-add.html") 


@login_required(login_url='/users/')
def rentals(request):  
    rental= Rental.objects.filter(user_id=request.user.id)
    # if request.method == "POST": 
    #     rental_id=request.POST.get('rental_id')
    #     rentalsearch=Rental.objects.filter(id=rental_id).values()
    context={
        'rental':rental,
       
    }
    return render(request,"users/rentals/rentals.html",context) 

def rental_preview(request,id):
    rental=Rental.objects.get(id=id)
    rentalbasic=RentalBasic.objects.get(rental_id=rental.id)
    rentallocation=RentalLocation.objects.get(rental_id=rental.id)
    basicrates=BasicRates.objects.get(rental_id=rental.id)
    rentaldiscounts=LongStayDiscount.objects.get(rental_id=rental.id)
    houserules=HouseRules.objects.get(rental_id=rental.id)
    gallery=RentalsGallery.objects.filter(rental_id=rental.id)
    instruction=RentalInstruction.objects.get(rental_id=rental.id)
    policy=RentalPolicy.objects.get(rental_id=rental.id)

    context={
        'rental':rental,       
        'rentalbasic':rentalbasic,
        'rentallocation':rentallocation,
        'basicrates':basicrates,
        'rentaldiscounts':rentaldiscounts,
        'houserules':houserules,
        'gallery':gallery,
        'instruction':instruction,
        'policy':policy
    }

    return render(request,'users/rentals/rental-preview.html',context)



@login_required(login_url='/users/')
def rental_edit(request, id):  
    rental = Rental.objects.get(id=id)
   
    context={
       
        'rental':rental,
        'rental_id':id
    }  
    return render(request,'users/rentals/rental-edit.html',context)  

@login_required(login_url='/')
def rental_update(request, id): 
    
    if request.method == "POST": 
        rental= Rental.objects.get(id=id)
        rental.rental_name=request.POST.get('rental_name')
        if 'rental_logo' in request.FILES:
           rental.rental_logo = request.FILES['rental_logo']
        rental.rental_url=request.POST.get('rental_url')
        rental.rental_type_id=request.POST.get('rental_type')
        rental.amenities_id=request.POST.getlist('amenities_id[]')
        rental.activities_id=request.POST.getlist('activities_id[]')
        rental.policy_id=request.POST.getlist('policy_id[]')
        rental.rental_description=request.POST.get('rental_description')
       
        rental.save()
        #return redirect("/rentals/basic/") 
        path1 ="/rentals/basic/"
        path2=str(id)
        path = path1+path2
        messages.success(request, 'Row updated Successfully.')
        return HttpResponseRedirect(path)
   
    #return render(request, 'users/rentals/rental-edit.html', {'rental': rental})  

@login_required(login_url='/users/')
def rental_destroy(request, id):  
    rental= Rental.objects.get(id=id) 
    if rental.rental_logo:
        rental.rental_logo.delete() 
    rental.delete()  
    return redirect("/users/rentals")  


def rental_basic(request,id):
    rental=Rental.objects.get(id=id)
    rentalbasic=RentalBasic.objects.get(rental_id=rental.id)
    rentaltype=Rentaltype.objects.all()
    context={
        'rentalbasic':rentalbasic,
        'rentaltype':rentaltype,
        'rental_id':id

    }
    return render(request,'users/rentals/rental-basic.html',context)

def rental_basic_update(request,id):
    if request.method == "POST": 
        rentalbasic=RentalBasic.objects.get(id=id)
        rentalbasic.rental_type=request.POST.get('rental_type')
        rentalbasic.rental_basis=request.POST.get('rental_basis')
        rentalbasic.floorspace=request.POST.get('floorspace')
        rentalbasic.floorspace_units=request.POST.get('floorspace_units')
        rentalbasic.grounds=request.POST.get('grounds')
        rentalbasic.grounds_units=request.POST.get('grounds_units')
        rentalbasic.floors_building=request.POST.get('floors_building')
        rentalbasic.entrance=request.POST.get('entrance')
        rentalbasic.rental_licence=request.POST.get('rental_licence')
        rentalbasic.save()
    #return redirect('/rentals/photo')  
        #path1 ="/rentals/photo/"
        #path2=str(id)
        #path = path1+path2
    #return HttpResponseRedirect(path)    
    messages.success(request, 'Data Updated Successfully.')    
    return redirect(request.META.get('HTTP_REFERER'))    

def rental_location(request,id):
    rental=Rental.objects.get(id=id)
    rentallocation=RentalLocation.objects.get(rental_id=rental.id)
    country=Country.objects.all()
    context={
        'rentallocation':rentallocation,
        'country':country,
        'rental_id':id
    }
    return render(request,'users/rentals/rental-location.html',context)

def rental_location_update(request,id):
    if request.method == "POST": 
        rentallocation=RentalLocation.objects.get(id=id)
        rentallocation.country=request.POST.get("country")
        rentallocation.address=request.POST.get("address")
        rentallocation.apartment=request.POST.get("apartment")
        rentallocation.city=request.POST.get("city")
        rentallocation.state=request.POST.get("state")
        rentallocation.postal=request.POST.get("postal")
        rentallocation.save()
    messages.success(request, 'Data Updated Successfully.')    
    return redirect(request.META.get('HTTP_REFERER'))    

def rental_rooms(request,id):
    rental=Rental.objects.get(id=id)
    rooms=Room.objects.all()
    roomtype=Roomtype.objects.all()
    bed=Bed.objects.all()
    otherrooms=OtherRooms.objects.all()
    context={
        'rooms':rooms,
        'roomtype':roomtype,
        'bed':bed,
        'rental_id':id,
        'otherrooms':otherrooms,
        'rental':rental
    }
    return render(request,'users/rentals/rental-rooms.html',context)    

def rental_other_rooms_insert(request,id):
    rental=Rental.objects.get(id=id)
    
    if request.method == "POST": 
        rentalotherrooms=RentalOtherRooms()
        rentalotherrooms.other_rooms=request.POST.getlist('other_rooms[]') 
        rentalotherrooms.user_id=request.user.id
        rentalotherrooms.rental_id=id       
        rentalotherrooms.save()
    messages.success(request, 'Data Updated Successfully.') 
    return redirect(request.META.get('HTTP_REFERER'))   

def rental_amenities(request,id):
    rental=Rental.objects.get(id=id)
    rentalamenities=RentalAmenities.objects.get(rental_id=rental.id)
    amenities=Amenities.objects.all()
    amenitiestype=AmenitiesType.objects.all()
    
    
    context={
        'amenities':amenities,
        'amenitiestype':amenitiestype,
        'rentalamenities':rentalamenities,
        'rental_id':id,
        'amentitle':rentalamenities.amenities

    }
  
   
    
    return render(request,'users/rentals/rental-amenities.html',context) 



def rental_amenities_update(request,id):
    if request.method == "POST": 
        rentalamenities=RentalAmenities.objects.get(id=id)
        rentalamenities.amenities=request.POST.getlist('amenities[]') 
        rentalamenities.save()
    messages.success(request, 'Data Updated Successfully.') 
    return redirect(request.META.get('HTTP_REFERER'))    


def rental_basic_rates(request,id):
    rental=Rental.objects.get(id=id)
    basicrates=BasicRates.objects.get(rental_id=rental.id)
    currency=Currency.objects.all()
    context={
        'basicrates':basicrates,
        'currency':currency,
        'rental_id':id
    }
    return render(request,'users/rentals/rental-basic-rates.html',context)

def rental_basic_rates_update(request,id):  
    if request.method == "POST": 
        basicrates=BasicRates.objects.get(id=id)
        basicrates.currency=request.POST.get('currency')
        basicrates.basic_night=request.POST.get('basic_night')
        basicrates.weekend_night=request.POST.get('weekend_night')
        basicrates.guest_number=request.POST.get('guest_number')
        basicrates.minimum_stay=request.POST.get('minimum_stay')
        basicrates.maximum_stay=request.POST.get('maximum_stay')
        basicrates.checkin_days=request.POST.getlist('checkin_days[]')
        basicrates.checkout_days=request.POST.getlist('checkout_days[]')
        next = request.POST.get('next', '/')
        basicrates.save()
    #return HttpResponseRedirect(next)    
    # return redirect('/rentals/seasonal-rates')  
    messages.success(request, 'Data Updated Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))    


def rental_seasonal_rates(request,id):
    rental=Rental.objects.get(id=id)
    seasonalrates=SeasonalRates.objects.filter(rental_id=rental.id)
    context={        
        'rental_id':id,
        'seasonalrates':seasonalrates,
        'rental':rental
    }
    # seasonalrates=SeasonalRates.objects.get(rental_id=rental.id)
    return render(request,'users/rentals/rental-seasonal-rates.html',context)

def rental_seasonal_rates_insert(request,id):
    rental=Rental.objects.get(id=id)
    if request.method == "POST":
        seasonalrates=SeasonalRates()
        seasonalrates.season_name=request.POST.get('season_name')
        seasonalrates.start_date=request.POST.get('start_date')
        seasonalrates.end_date=request.POST.get('end_date')
        seasonalrates.basic_night=request.POST.get('basic_night')
        seasonalrates.weekend_night=request.POST.get('weekend_night')
        seasonalrates.minimum_stay=request.POST.get('minimum_stay')
        seasonalrates.maximum_stay=request.POST.get('maximum_stay')
        seasonalrates.checkin_days=request.POST.getlist('checkin_days[]')
        seasonalrates.checkout_days=request.POST.getlist('checkout_days[]')
        seasonalrates.user_id=request.user.id
        seasonalrates.rental_id=id
        seasonalrates.save()
        messages.success(request, 'Data Added Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))
    #return render(request,'users/rentals/rental-seasonal-rates.html',{'rental':rental})        


def rental_seasonal_rates_edit(request,id):
    rental=Rental.objects.get(id=id)
    seasonalrates=SeasonalRates.objects.get(rental_id=rental.id)
    return render(request,'users/rentals/rental-seasonal-rates.html',{'seasonalrates':seasonalrates})


def rental_seasonal_rates_update(request,id):  
    if request.method == "POST": 
        seasonalrates=SeasonalRates.objects.get(id=id)
        seasonalrates.season_name=request.POST.get('season_name')
        seasonalrates.start_date=request.POST.get('start_date')
        seasonalrates.end_date=request.POST.get('end_date')
        seasonalrates.basic_night=request.POST.get('basic_night')
        seasonalrates.weekend_night=request.POST.get('weekend_night')
        seasonalrates.minimum_stay=request.POST.get('minimum_stay')
        seasonalrates.maximum_stay=request.POST.get('maximum_stay')
        seasonalrates.save()
    messages.success(request, 'Data Updated Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))    

def rental_seasonal_destroy(request, id):  
    rentalSeasonal = SeasonalRates.objects.get(id=id)  
    rentalSeasonal.delete()
    messages.success(request, 'Row deleted Successfully.')  
    return redirect(request.META.get('HTTP_REFERER'))

def rental_discount(request,id):
    rental=Rental.objects.get(id=id)
    longstaydiscount=LongStayDiscount.objects.get(rental_id=rental.id)
    earlybirddiscount=EarlyBirdDiscount.objects.get(rental_id=rental.id)
    context={
        'longstaydiscount':longstaydiscount,
        'earlybirddiscount':earlybirddiscount,
        'rental_id':id
    }
    return render(request,'users/rentals/rental-discount.html',context)

def long_stay_discount_update(request,id):
    if request.method == "POST": 
        longstaydiscount=LongStayDiscount.objects.get(id=id)
        longstaydiscount.seven_nights=request.POST.get('seven_nights')
        longstaydiscount.fourteen_nights=request.POST.get('fourteen_nights') 
        longstaydiscount.twenty_one_nights=request.POST.get('twenty_one_nights') 
        longstaydiscount.twenty_eight_nights=request.POST.get('twenty_eight_nights') 
        longstaydiscount.save()
    messages.success(request, 'Data Updated Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))  

def early_bird_discount_update(request,id):
    if request.method == "POST": 
        earlybirddiscount=EarlyBirdDiscount.objects.get(id=id)
        earlybirddiscount.booking_less=request.POST.get('booking_less')
        earlybirddiscount.booking_less_discount=request.POST.get('booking_less_discount') 
        earlybirddiscount.booking_more=request.POST.get('booking_more') 
        earlybirddiscount.booking_more_discount=request.POST.get('booking_more_discount') 
        earlybirddiscount.save()
    messages.success(request, 'Data Updated Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))      




def rental_additional_info(request,id):
    rental=Rental.objects.get(id=id)
    rentalcleaning=RentalCleaning.objects.get(rental_id=rental.id)
    rentaldeposit=RentalDeposit.objects.get(rental_id=rental.id)
    rentaltax=RentalTax.objects.filter(rental_id=rental.id)
    extraservices=ExtraServices.objects.filter(rental_id=rental.id)
    customservices=CustomServices.objects.filter(rental_id=rental.id)
    
    context={
        'rentalcleaning':rentalcleaning,
        'rentaldeposit':rentaldeposit,
        'rental':rental,
        'rental_id':id,
        'rentaltax':rentaltax,
        'extraservices':extraservices,
        'customservices':customservices
    }
    return render(request,'users/rentals/rental-additional-info.html',context)

def rental_cleaning_update(request,id):
    if request.method == "POST": 
        rentalcleaning=RentalCleaning.objects.get(id=id)
        rentalcleaning.cleaning_available=request.POST.get('cleaning_available')
        rentalcleaning.cleaning_basis=request.POST.get('cleaning_basis') 
        rentalcleaning.price=request.POST.get('price') 
        rentalcleaning.save()
    messages.success(request, 'Data Updated Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))   

def rental_deposit_update(request,id):
    if request.method == "POST": 
        rentaldeposit=RentalDeposit.objects.get(id=id)
        rentaldeposit.security_deposit=request.POST.get('security_deposit')
        rentaldeposit.amount=request.POST.get('amount') 
        rentaldeposit.save()
    messages.success(request, 'Data Updated Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))   

def rental_tax_insert(request,id):
    rental=Rental.objects.get(id=id)
    if request.method == "POST": 
        rentaltax=RentalTax()
        rentaltax.tax_type=request.POST.get('tax_type')
        rentaltax.fee_basis=request.POST.get('fee_basis') 
        rentaltax.percentage=request.POST.get('percentage')
        rentaltax.amountin=request.POST.get('amountin')
        rentaltax.user_id=request.user.id
        rentaltax.rental_id=id
        rentaltax.save()
        messages.success(request, 'Data Updated Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))  
    #return render(request,'/users/rentals/rental-additional-info.html',{'rental':rental}) 

def rental_tax_update(request,id):
    rentaltax=RentalTax.objects.get(id=id)
    if request.method == "POST": 
        rentaltax.tax_type=request.POST.get('tax_type')
        rentaltax.fee_basis=request.POST.get('fee_basis') 
        rentaltax.percentage=request.POST.get('percentage')
        rentaltax.amountin=request.POST.get('amountin')
        rentaltax.user_id=request.user.id
        rentaltax.rental_id=id
        rentaltax.save()
        messages.success(request, 'Data Updated Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))


def rental_tax_destroy(request, id):  
    rentaltax = RentalTax.objects.get(id=id)  
    rentaltax.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect(request.META.get('HTTP_REFERER'))

def rental_extra_services_insert(request,id):
    rental=Rental.objects.get(id=id)
    if request.method == "POST": 
        extraservices=ExtraServices()
        extraservices.service_name=request.POST.get('service_name')
        extraservices.service_provided=request.POST.get('service_provided') 
        extraservices.fee_basis=request.POST.get('fee_basis')
        extraservices.service_price=request.POST.get('service_price')
        extraservices.earliest_guest_order=request.POST.get('earliest_guest_order')
        extraservices.service_provided=request.POST.get('service_provided') 
        extraservices.latest_guest_order=request.POST.get('latest_guest_order')
        extraservices.guest_cancel_order=request.POST.get('guest_cancel_order')
        extraservices.extra_message=request.POST.get('extra_message')
        extraservices.user_id=request.user.id
        extraservices.rental_id=id
        extraservices.save()
        messages.success(request, 'Data Updated Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))  
    #return render(request,'/users/rentals/rental-additional-info.html',{'rental':rental})    

def rental_custom_services_insert(request,id):
    rental=Rental.objects.get(id=id)
    if request.method == "POST": 
        customservices=CustomServices()
        customservices.custom_service_name=request.POST.get('custom_service_name')
        customservices.custom_service_provided=request.POST.get('custom_service_provided') 
        customservices.custom_fee_basis=request.POST.get('custom_fee_basis')
        customservices.custom_service_price=request.POST.get('custom_service_price')
        customservices.custom_earliest_guest_order=request.POST.get('custom_earliest_guest_order')
        customservices.custom_service_provided=request.POST.get('custom_service_provided') 
        customservices.custom_latest_guest_order=request.POST.get('custom_latest_guest_order')
        customservices.custom_guest_cancel_order=request.POST.get('custom_guest_cancel_order')
        customservices.custom_extra_message=request.POST.get('custom_extra_message')
        customservices.user_id=request.user.id
        customservices.rental_id=id
        customservices.save()
        messages.success(request, 'Data Updated Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))  
    #return render(request,'/users/rentals/rental-additional-info.html',{'rental':rental})         



def rental_house_rules(request,id):
    rental=Rental.objects.get(id=id)
    houserules=HouseRules.objects.get(rental_id=rental.id)
    context={
        'houserules':houserules,
        'rental_id':id
    }
    return render(request,'users/rentals/rental-house-rules.html',context) 

def rental_house_rules_update(request,id):
    if request.method == "POST": 
        houserules=HouseRules.objects.get(id=id)
        houserules.for_kid=request.POST.get('for_kid')
        houserules.wheelchair_access=request.POST.get('wheelchair_access')
        houserules.parties_allowed=request.POST.get('parties_allowed')
        houserules.smoking_allowed=request.POST.get('smoking_allowed')
        houserules.pets=request.POST.get('pets')
        houserules.house_rules=request.POST.get('house_rules')
        houserules.save()
        messages.success(request, 'Data Updated Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))         

def rental_policy(request,id):
    rental=Rental.objects.get(id=id)
    rentalpolicy=RentalPolicy.objects.get(rental_id=rental.id)
    context={
        'rentalpolicy':rentalpolicy,
        'rental_id':id
    }
    return render(request,'users/rentals/rental-policy.html',context) 

def rental_policy_update(request,id):
    if request.method == "POST": 
        rentalpolicy=RentalPolicy.objects.get(id=id)
        rentalpolicy.name=request.POST.get('name')
        rentalpolicy.description=request.POST.get('description')
        rentalpolicy.save()
    messages.success(request, 'Data Updated Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))     



def rental_instruction(request,id):
    rental=Rental.objects.get(id=id)
    rentalinstruction=RentalInstruction.objects.get(rental_id=rental.id)
    country=Country.objects.all()
    context={
        'rentalinstruction':rentalinstruction,
        'country':country,
        'rental_id':id
    }
    return render(request,'users/rentals/rental-instructions.html',context)                           

def rental_instruction_update(request,id):
    if request.method == "POST": 
        rentalinstruction=RentalInstruction.objects.get(id=id)
        rentalinstruction.checkin_instruction=request.POST.get('checkin_instruction')
        rentalinstruction.checkout_instruction=request.POST.get('checkout_instruction')
        rentalinstruction.checkin_contact=request.POST.get('checkin_contact')
        rentalinstruction.key_collection=request.POST.get('key_collection')
        rentalinstruction.telephone_country=request.POST.get('telephone_country')
        rentalinstruction.telephone_number=request.POST.get('telephone_number')
        rentalinstruction.instructions=request.POST.get('instructions')
        rentalinstruction.attach_instruction=request.FILES.get('attach_instruction')
        rentalinstruction.checkin_from=request.POST.get('checkin_from')
        rentalinstruction.checkout_until=request.POST.get('checkout_until')
        rentalinstruction.airport_instruction=request.POST.get('airport_instruction')
        rentalinstruction.property_directions=request.POST.get('property_directions')
        rentalinstruction.save()
    messages.success(request, 'Data Updated Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))  

def rental_select_channels(request,id):
    channels=Channel.objects.all()
    context={
        'channels':channels,
        'rental_id':id
    }
    return render (request,'users/rentals/rental-channels.html',context)    
        


# Rental Code end    

# Channels Code Start

@login_required(login_url='/')
def channel_insert(request,id):
    if request.method == "POST": 
        channel=ChannelManagement()
        channel.channel_id=Channel.objects.get(id=id)
        channel.user_id=request.user.id
        channel.rental_id=85
        channel.save()
        messages.success(request, 'Row added Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))  
 

@login_required(login_url='/users/')
def channels(request):  
    channels = Channel.objects.all()
    rentals=Rental.objects.all()
    context={
        'channels':channels,
        'rentals':rentals
    }   
    
    return render(request,"users/channels/channels.html",context)  

@login_required(login_url='/users/')
def channel_edit(request, id):  
    channel= Channel.objects.get(id=id)  
    return render(request,'users/channels/channel-edit.html', {'channel':channel})  

@login_required(login_url='/users/')
def channel_update(request, id):    
    if request.method == "POST": 
        channel= Channel.objects.get(id=id)
        channel.channel_title=request.POST.get('channel_title')
        if 'channel_image' in request.FILES:
           channel.channel_image = request.FILES['channel_image']
        channel.channel_description=request.POST.get('channel_description')
        channel.status=request.POST.get('status')
        channel.save()
        messages.success(request, ' Row updated Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))  
   
    return render(request, 'users/channels/channel-edit.html', {'channel': channel})  

@login_required(login_url='/users/')
def channel_destroy(request, id):  
    channel = ChannelManagement.objects.get(id=id)  
    channel.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect(request.META.get('HTTP_REFERER'))  

# Channel Code End    

# Policy Code Start

@login_required(login_url='/users/')
def policy(request):
    policy=Policy.objects.filter(user_id=request.user.id) 
    return render(request, 'users/policy/policy.html',{'policy':policy})

@login_required(login_url='/users/')
def policy_add(request):
    return render(request, 'users/policy/policy-add.html') 

@login_required(login_url='/users/')
def policy_insert(request):
    if request.method == "POST":
        policy=Policy()
        policy.policy_number=request.POST.get('policy_number')
        policy.policy_name=request.POST.get('policy_name')
        policy.policy_type=request.POST.get('policy_type')
        policy.description=request.POST.get('description')
        policy.status=request.POST.get('status')
        policy.user_id=request.user.id
        policy.save()
        messages.success(request, ' Row added Successfully.')
        return redirect('/users/policy')
       
@login_required(login_url='/users/')
def policy_edit(request,id):
    try:
        policy=Policy.objects.get(id=id,user_id=request.user.id)
    except ObjectDoesNotExist:
         return redirect('/404.html')
    return render(request, 'users/policy/policy-edit.html',{'policy':policy})       

@login_required(login_url='/users/')
def policy_update(request,id):
    policy=Policy.objects.get(id=id)
    if request.method == "POST":  
        policy.policy_number=request.POST.get('policy_number')
        policy.policy_name=request.POST.get('policy_name')
        policy.policy_type=request.POST.get('policy_type')
        policy.description=request.POST.get('description')
        policy.status=request.POST.get('status')
        activity.user_id=request.user.id
        policy.save()
        messages.success(request, ' Row updated Successfully.')
        return redirect('/users/policy')
    return render(request, 'users/policy/policy-edit.html',{'policy':policy})

@login_required(login_url='/users/')
def policy_destroy(request,id): 
    policy = Policy.objects.get(id=id)  
    policy.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect("/users/policy")  

# Policy Code end

# Booking Code start

@login_required(login_url='/users/')  
def booking(request):
    bookings=Bookings.objects.filter(user_id=request.user.id) 
    return render (request,'users/bookings/bookings.html', {'bookings': bookings})

@login_required(login_url='/users/')  
def booking_edit(request, id):
    bookings=Bookings.objects.get(id=id) 
    channels=Channel.objects.all()
    context={
        'bookings':bookings,
        'channels':channels
    }
    return render (request,'users/bookings/booking-edit.html',context)    

@login_required(login_url='/users/')  
def booking_update(request ,id):
    bookings=Bookings.objects.get(id=id) 
    channels=Channel.objects.all()
    if request.method == "POST":
        bookings.rental=request.POST.get('rental')
        bookings.channel_id=request.POST.get('channel')
        bookings.booking_type=request.POST.get('booking_type')
        bookings.first_name =  request.POST.get('first_name')
        bookings.last_name =  request.POST.get('last_name')
        bookings.phone =  request.POST.get('phone')
        bookings.address =  request.POST.get('address')
        bookings.city=  request.POST.get('city')
        bookings.state= request.POST.get('state')
        bookings.country =  request.POST.get('country')
        bookings.postal_code =  request.POST.get('postal_code')
        bookings.check_in=request.POST.get('check_in')
        bookings.check_out=request.POST.get('check_out')
        bookings.status=request.POST.get('status')
        
        bookings.save()
        messages.success(request, ' Row updated Successfully.')
        return redirect('/users/bookings') 
        
    context={
        'bookings':bookings,
        'channels':channels
    }    
    return render(request, 'users/bookings/booking-edit.html',context)     

@login_required(login_url='/users/')  
def booking_view(request,id):
    bookings=Bookings.objects.get(id=id)
    return render (request,'users/bookings/bookings_view.html', {'bookings': bookings})

@login_required(login_url='/users/')  
def booking_list(request, id):
    bookings=Bookings.objects.get(id=id) 
    channels=Channel.objects.all()
    context={
        'bookings':bookings,
        'channels':channels
    }
    return render (request,'users/bookings/booking-list.html',context) 

# Rate Type code start

@login_required(login_url='/users/')
def rate_type(request):
    ratetype=Ratetype.objects.filter(user_id=request.user.id) 
    return render(request, 'users/rates/rate-type.html', {'ratetype': ratetype})

@login_required(login_url='/users/')
def rate_type_insert(request):
    if request.method == "POST":
        ratetype=Ratetype()
        ratetype.ratetype_name=request.POST.get('ratetype_name')
        ratetype.status=request.POST.get('status')
        ratetype.user_id=request.user.id
        ratetype.save()
        messages.success(request, ' Row added Successfully.')
        return redirect('/users/rate-type')    

@login_required(login_url='/users/')
def rate_type_add(request):
    return render(request, 'users/rates/rate-type-add.html')

@login_required(login_url='/users/')
def rate_type_edit(request,id):
    ratetype=Ratetype.objects.get(id=id) 
    return render(request, 'users/rates/rate-type-edit.html', {'ratetype': ratetype})

@login_required(login_url='/users/')
def rate_type_update(request,id):
    ratetype=Ratetype.objects.get(id=id)
    if request.method == "POST":
        ratetype.ratetype_name=request.POST.get('ratetype_name')
        ratetype.status=request.POST.get('status')
        ratetype.save()
        messages.success(request, ' Row updated Successfully.')
        return redirect('/users/rate-type') 
    return render(request,' users/rates/rate-type-edit.html', {'ratetype': ratetype})

@login_required(login_url='/users/')
def rate_type_destroy(request, id):  
    ratetype = Ratetype.objects.get(id=id)  
    ratetype.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect("/users/rate-type")   

#Rate Type code end

#Rate code start

@login_required(login_url='/users/')
def rate(request):
    rate=Rate.objects.filter(user_id=request.user.id) 
    return render(request, 'users/rates/rate.html' ,{'rate': rate})

@login_required(login_url='/users/')
def rate_add(request):
    ratetype=Ratetype.objects.filter(user_id=request.user.id) 
    return render(request, 'users/rates/rate-add.html',{'ratetype': ratetype})

@login_required(login_url='/users/')
def rate_insert(request):
    if request.method == "POST":
        rate=Rate()
        rate.rate_type_id=request.POST.get('rate_type')
        rate.rate_name=request.POST.get('rate_name')
        rate.included_occupants=request.POST.get('included_occupants')
        rate.extra_adult_charge=request.POST.get('extra_adult_charge')
        rate.extra_children_charge=request.POST.get('extra_children_charge')
        rate.weekend_surcharge=request.POST.get('weekend_surcharge')
        rate.day_surcharge=request.POST.getlist('day_surcharge[]')
        rate.disable_rates=request.POST.get('disable_rates')
        rate.description=request.POST.get('description')
        rate.status=request.POST.get('status')
        rate.user_id=request.user.id
        rate.save()
        messages.success(request, ' Row added Successfully.')
        return redirect('/users/rate')


@login_required(login_url='/users/')
def rate_edit(request,id):
    rate=Rate() 
    ratetype=Ratetype.objects.all() 
    rental=Rental.objects.get(id=id)

    
    context = {
        'rate':rate,
        'ratetype':ratetype,
        'rental':rental
    }
    
    return render(request, 'users/rates/rate-edit.html',context)

@login_required(login_url='/users/')
def rate_update(request,id):
    rate=Rate.objects.get(id=id,rental_id=rental.id)
    rental=Rental()
    if request.method == "POST":
       rate.rate_type_id=request.POST.get('rate_type')
       rate.rate_name=request.POST.get('rate_name')
       rate.included_occupants=request.POST.get('included_occupants')
       rate.extra_adult_charge=request.POST.get('extra_adult_charge')
       rate.extra_children_charge=request.POST.get('extra_children_charge')
       rate.weekend_surcharge=request.POST.get('weekend_surcharge')
       rate.day_surcharge=request.POST.getlist('day_surcharge[]')
       rate.disable_rates=request.POST.get('disable_rates')
       rate.description=request.POST.get('description')
       rate.status=request.POST.get('status')
       rate.rental_id=rental.id
       rate.user_id=request.user.id
       
       rate.save()
       messages.success(request, ' Row edited Successfully.')
       return redirect('/users/rate')
        
    return render(request,' users/rates/rate-edit.html', {'rental': rental})

@login_required(login_url='/users/')
def rate_destroy(request, id):  
    rate = Rate.objects.get(id=id)  
    rate.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect("/users/rate")       

#Rate code end

# Discount Type Code start
@login_required(login_url='/users/')
def discount_type(request):
    discounttype=DiscountType.objects.filter(user_id=request.user.id) 
    return render(request, 'users/discounts/discount-type.html', {'discounttype': discounttype})

@login_required(login_url='/users/')
def discount_type_insert(request):
    if request.method == "POST":
        discounttype=DiscountType()
        discounttype.discounttype_name=request.POST.get('discounttype_name')
        discounttype.status=request.POST.get('status')
        discounttype.user_id=request.user.id
        discounttype.save()
        messages.success(request, ' Row added Successfully.')
        return redirect('/users/discount-type')    

@login_required(login_url='/users/')
def discount_type_add(request):
    return render(request, 'users/discounts/discount-type-add.html')

@login_required(login_url='/users/')
def discount_type_edit(request,id):
    discounttype=DiscountType.objects.get(id=id) 
    return render(request, 'users/discounts/discount-type-edit.html', {'discounttype': discounttype})

@login_required(login_url='/users/')
def discount_type_update(request,id):
    discounttype=DiscountType.objects.get(id=id)
    if request.method == "POST":
        discounttype.discounttype_name=request.POST.get('discounttype_name')
        discounttype.status=request.POST.get('status')
        discounttype.save()
        messages.success(request, ' Row updated Successfully.')
        return redirect('/users/discount-type') 
    return render(request,' users/discounts/discount-type-edit.html', {'discounttype': discounttype})

@login_required(login_url='/users/')
def discount_type_destroy(request, id):  
    discounttype = DiscountType.objects.get(id=id)  
    discounttype.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect("/users/discount-type")   

#Discount Type Code end

#Discount Code start

@login_required(login_url='/users/')
def discount(request):
    discount=Discount.objects.filter(user_id=request.user.id) 
    return render(request, 'users/discounts/discounts.html' ,{'discount': discount})

@login_required(login_url='/users/')
def discount_add(request):
    discounttype=DiscountType.objects.filter(user_id=request.user.id) 
    return render(request, 'users/discounts/discount-add.html',{'discounttype': discounttype})

@login_required(login_url='/users/')
def discount_insert(request):
    if request.method == "POST":
        discount=Discount()
        discount.discounts_name=request.POST.get('discounts_name')
        discount.discount_type_id=request.POST.get('discount_type')
        discount.discounts_amount=request.POST.get('discounts_amount')
        discount.status=request.POST.get('status')
        discount.user_id=request.user.id

        discount.save()
        messages.success(request, ' Row added Successfully.')
        return redirect('/users/discounts')

@login_required(login_url='/users/')
def discount_edit(request,id):
    discount=Discount.objects.get(id=id) 
    discounttype=DiscountType.objects.all() 
    context = {
        'discount':discount,
        'discounttype':discounttype
    }
    return render(request, 'users/discounts/discount-edit.html',context)

@login_required(login_url='/users/')
def discount_update(request,id):
    discount=Discount.objects.get(id=id)
    if request.method == "POST":
        discount.discounts_name=request.POST.get('discounts_name')
        discount.discount_type_id=request.POST.get('discount_type')
        discount.discounts_amount=request.POST.get('discounts_amount')
        discount.status=request.POST.get('status')
        
        discount.save()
        messages.success(request, ' Row edited Successfully.')
        return redirect('/users/discounts')
        
    return render(request,' users/discounts/discount-edit.html', {'discount': discount})

@login_required(login_url='/users/')
def discount_destroy(request, id):  
    discount = Discount.objects.get(id=id)  
    discount.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect("/users/discounts")  


#Currency Code start

@login_required(login_url='/users/')
def currency(request):
    currency=Currency.objects.all()
    return render(request, 'users/discounts/currency.html' ,{'currency': currency})

@login_required(login_url='/users/')
def currency_add(request):
    return render(request, 'users/discounts/currency-add.html')

@login_required(login_url='/users/')
def currency_insert(request):
    if request.method == "POST":
        currency=Currency()
        currency.title=request.POST.get('title')
        currency.code=request.POST.get('code')
        currency.symbol=request.POST.get('symbol')
        currency.decimal_place=request.POST.get('decimal_place')
        currency.currency_value=request.POST.get('currency_value')
        currency.status=request.POST.get('status')
      

        currency.save()
        messages.success(request, ' Row added Successfully.')
        return redirect('/users/currency')

@login_required(login_url='/users/')
def currency_edit(request,id):
    currency=Currency.objects.get(id=id) 
    context = {
        'currency':currency
    }
    return render(request, 'users/discounts/currency-edit.html',context)

@login_required(login_url='/users/')
def currency_update(request,id):
    currency=Currency.objects.get(id=id)
    if request.method == "POST":
        currency.title=request.POST.get('title')
        currency.code=request.POST.get('code')
        currency.symbol=request.POST.get('symbol')
        currency.decimal_place=request.POST.get('decimal_place')
        currency.currency_value=request.POST.get('currency_value')
        currency.status=request.POST.get('status')
        
        currency.save()
        messages.success(request, ' Row edited Successfully.')
        return redirect('/users/currency')
        
    return render(request,' users/discounts/currency-edit.html', {'currency': currency})

@login_required(login_url='/users/')
def currency_destroy(request, id):  
    currency = Currency.objects.get(id=id)  
    currency.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect("/users/currency")  


# Invoice code start


class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices":invoices,
        }

        return render(self.request, 'users/invoice/invoice-list.html', context)
    
    def post(self, request):        
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))
        try:

            update_status_for_invoices = int(request.POST['status'])
        except KeyError:
            update_status_for_invoices = "Guest"

        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('/users/invoice/')

def createInvoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices, 
    this will be protected view, only admin has the authority to read and make
    changes here.
    """

    # heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = InvoiceItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = InvoiceItemFormset(request.POST)
        form = InvoiceForm(request.POST)
        
        if form.is_valid():
            invoice = Invoice.objects.create(customer=form.data["customer"],
                    customer_email=form.data["customer_email"],
                    billing_address= form.data["billing_address"],
                   
                    message=form.data["message"],
                    )
            # invoice.save()
            
        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if service and description and quantity and rate:
                    amount = float(rate)*float(quantity)
                    total += amount
                    InvoiceItem(customer=invoice,
                            service=service,
                            description=description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
            invoice.total_amount = total
            invoice.save()
            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/users/invoice')
    context = {
        "title" : "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'users/invoice/invoice-create.html', context)


def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    invoiceitem = invoice.invoiceitem_set.all()
    companyprofile=CompanyProfile.objects.all()

    context = {
        "company": {
            "name": "Apex Websoft",
            "address" :"Noida Up india",
            "phone": "7303699947",
            "email": "amanrajput110298@gmail.com",
        },
        'companyprofile':companyprofile,
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
       
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "invoiceitem": invoiceitem,

    }
    return render(request, 'users/invoice/invoice-details.html', context)

def generate_PDF(request, id):
    # Use False instead of output path to save pdf to a variable
    # pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail', args=[id])), False)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response


def change_status(request):
    return redirect('users:invoice:invoice-list')

def view_404(request,  *args, **kwargs):

    return redirect('users:invoice:invoice-list')  

@login_required(login_url='/users/')
def company_insert(request):  
    if request.method == "POST":
        companyprofile=CompanyProfile()
        companyprofile.company_name=request.POST.get('company_name') 
        companyprofile.company_logo=request.FILES.get('company_logo') 
        companyprofile.company_email=request.POST.get('company_email') 
        companyprofile.company_tel=request.POST.get('company_tel') 
        companyprofile.company_address=request.POST.get('company_address')
        companyprofile.save()

        return redirect('/users/company')

@login_required(login_url='/users/')
def company_add(request):  
    return render(request,'users/invoice/company-add.html')  

@login_required(login_url='/users/')    
def company(request):  
    companies = CompanyProfile.objects.all()   
    return render(request,"users/invoice/company.html",{'companies':companies})  

@login_required(login_url='/users/')
def company_edit(request, id): 
    company= CompanyProfile.objects.get(id=id)  
    return render(request,'users/invoice/company-edit.html', {'company':company})  

@login_required(login_url='/users/')
def company_update(request, id):  
    company= CompanyProfile.objects.get(id=id)
    if request.method == "POST":
        companyprofile=CompanyProfile()
        companyprofile.company_name=request.POST.get('company_name') 
        companyprofile.company_logo=request.FILES.get('company_logo') 
        companyprofile.company_email=request.POST.get('company_email') 
        companyprofile.company_tel=request.POST.get('company_tel') 
        companyprofile.company_address=request.POST.get('company_address') 
        companyprofile.save()

        return redirect('/users/company')
  
   
     
    return render(request, 'users/invoice/company-edit.html', {'company': company})  

@login_required(login_url='/users/')
def company_destroy(request, id):  
    company = CompanyProfile.objects.get(id=id)  
    company.delete()  
    return redirect("/users/company")         

# Tax Type code start
@login_required(login_url='/users/')
def tax_type(request):
    taxtype=Taxtype.objects.filter(user_id=request.user.id) 
    return render(request, 'users/tax/tax-type.html', {'taxtype': taxtype})

@login_required(login_url='/users/')
def tax_type_insert(request):
    if request.method == "POST":
        taxtype=Taxtype()
        taxtype.taxtype_name=request.POST.get('taxtype_name')
        taxtype.status=request.POST.get('status')
        taxtype.user_id=request.user.id
        taxtype.save()
        messages.success(request, ' Row added Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))    

@login_required(login_url='/users/')
def tax_type_add(request):
    return render(request, 'users/tax/tax-type-add.html')

@login_required(login_url='/users/')
def tax_type_edit(request,id):
    taxtype=Taxtype.objects.get(id=id) 
    return render(request, 'users/tax/tax-type-edit.html', {'taxtype': taxtype})

@login_required(login_url='/users/')
def tax_type_update(request,id):
    taxtype=Taxtype.objects.get(id=id)
    if request.method == "POST":
        taxtype.taxtype_name=request.POST.get('taxtype_name')
        taxtype.status=request.POST.get('status')
        taxtype.save()
        messages.success(request, ' Row updated Successfully.')
        return redirect('/users/tax-type') 
    return render(request, 'users/tax/tax-type-edit.html', {'taxtype': taxtype})

@login_required(login_url='/users/')
def tax_type_destroy(request, id):  
    taxtype = Taxtype.objects.get(id=id)  
    taxtype.delete()
    messages.success(request, ' Row deleted Successfully.')    
    return redirect(request.META.get('HTTP_REFERER'))   


#Tax Type code end

# Tax code start
@login_required(login_url='/users/')
def tax_add(request):
    taxtype=Taxtype.objects.filter(user_id=request.user.id) 
    return render(request, 'users/tax/tax-add.html',{'taxtype':taxtype})

@login_required(login_url='/users/')
def tax_insert(request):  
    if request.method == "POST":
        tax=Tax()
        tax.tax_type_id=request.POST.get('tax_type')
        tax.tax_name=request.POST.get('tax_name')
        tax.tax_percentage=request.POST.get('tax_percentage')
        tax.status=request.POST.get('status')
        tax.user_id=request.user.id
        tax.save()
        messages.success(request, ' Row added Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))      

@login_required(login_url='/users/')       
def tax(request):  
    tax=Tax.objects.filter(user_id=request.user.id)  
    return render(request,"users/tax/tax.html",{'tax':tax})  

@login_required(login_url='/users/')
def tax_edit(request, id):  
    tax = Tax.objects.get(id=id) 
    taxtype=Taxtype.objects.all()
    context={
        'tax':tax,
        'taxtype':taxtype
    }
    return render(request,'users/tax/tax-edit.html',context)  

@login_required(login_url='/users/')
def tax_update(request, id):  
    tax = Tax.objects.get(id=id)
    taxtype=Taxtype.objects.all()
    if request.method == "POST":
        tax.tax_type_id=request.POST.get('tax_type')
        tax.tax_name=request.POST.get('tax_name')
        tax.tax_percentage=request.POST.get('tax_percentage')
        tax.status=request.POST.get('status')
        tax.save()
        messages.success(request, ' Row updated Successfully.')
        return redirect('/users/tax') 

    context={
        'tax': tax,
        'taxtype':taxtype


    }
       
    return render(request, 'users/tax/tax-edit.html',context)  

@login_required(login_url='/users/')
def tax_destroy(request, id):  
    tax = Tax.objects.get(id=id)  
    tax.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect(request.META.get('HTTP_REFERER'))     

# Tax code end

# Amenities code start

@login_required(login_url='/users/')
def amenities_insert(request):  
    if request.method == "POST":
        amenities=Amenities()
        amenities.title=request.POST.get('title')  
        amenities.status=request.POST.get('status')
       
        amenities.save()
        messages.success(request, ' Row added Successfully.')

    return redirect(request.META.get('HTTP_REFERER'))   

@login_required(login_url='/users/')
def amenities_add(request):
    return render (request,"users/amenities/amenities-add.html")     
       
@login_required(login_url='/users/')
def amenities(request):  
    amenities = Amenities.objects.all()
    return render(request,"users/amenities/amenities.html",{'amenities':amenities})  

@login_required(login_url='/users/')
def amenities_edit(request, id):  
    amenities = Amenities.objects.get(id=id)  
    return render(request,'users/amenities/amenities-edit.html', {'amenities':amenities})  

@login_required(login_url='/users/')
def amenities_update(request, id):  
    amenities = Amenities.objects.get(id=id) 
    if request.method == "POST":
        amenities.title=request.POST.get('title')  
        amenities.status=request.POST.get('status')
        amenities.save()
        messages.success(request, ' Row updated Successfully.')

    return redirect(request.META.get('HTTP_REFERER'))  
   

@login_required(login_url='/users/')
def amenities_destroy(request, id):  
    amenities = Amenities.objects.get(id=id)  
    amenities.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect(request.META.get('HTTP_REFERER'))  

# Amenities code end      

# Activity code start

@login_required(login_url='/users/')
def activity(request):  
    activity = Activity.objects.all()   
    return render(request,"users/amenities/activity.html",{'activity':activity})  

@login_required(login_url='/users/')
def activity_add(request):
    return render(request, 'users/amenities/activity-add.html')

@login_required(login_url='/users/')
def activity_insert(request):
    if request.method == "POST":
        activity=Activity()
        activity.name=request.POST.get('name')
        activity.distance=request.POST.get('distance')
        activity.description=request.POST.get('description')
        activity.status=request.POST.get('status')
       
        activity.save()
        messages.success(request, ' Row added Successfully.')
    return redirect(request.META.get('HTTP_REFERER'))     

@login_required(login_url='/users/')
def activity_edit(request,id):  
    activity = Activity.objects.get(id=id)  
    return render(request,'users/amenities/activity-edit.html',{'activity':activity})  

@login_required(login_url='/users/')
def activity_update(request,id):
    activity = Activity.objects.get(id=id)
    if request.method == "POST":
        activity.name=request.POST.get('name')
        activity.distance=request.POST.get('distance')
        activity.description=request.POST.get('description')
        activity.status=request.POST.get('status')
        activity.save()
        messages.success(request, ' Row updated Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))  

      
    
    return render(request, 'users/amenities/activity-edit.html',{'activity':activity})  

@login_required(login_url='/users/')
def activity_destroy(request, id):  
    activity = Activity.objects.get(id=id)  
    activity.delete() 
    messages.success(request, ' Row deleted Successfully.')

    return redirect(request.META.get('HTTP_REFERER'))   


# Activity code end

# Calendar Code start

def calendar(request):
    rental=Rental.objects.filter(user_id=request.user.id)    
    return render(request,'users/calendar/calendar.html',{'rental':rental})

# # Rental-Amenities Code start

# def rental_amenities(request,id):
#     amenities=Amenities.objects.filter(user_id=request.user.id)
#     rental=Rental.objects.get(id=id)
#     rental_amenities=RentalAmenities.objects.filter(rental_id=rental.id)
    

#     context={
#         'amenities':amenities,
#         'rental':rental,
#         'rental_amenities':rental_amenities
#     }
#     return render(request,'users/rentals-amenities/rentals-amenities.html',context)    

# def rental_amenities_insert(request,id):
#     if request.method == "POST":
#         rental=Rental()
#         rental_amenities=RentalAmenities()
#         rental_amenities.amenities_id=request.POST.get('amenities')
#         rental_amenities.user_id=request.user.id
#         rental_amenities.rental=Rental.objects.get(id=id)
#         rental_amenities.save()
#         messages.success(request, ' Row added Successfully.')
#         return redirect(request.META.get('HTTP_REFERER'))
#     return render(request,'users/rentals-amenities/rentals-amenities.html',{'rental':rental})    


# def rental_amenities_destroy(request, id):  
#     rental_amenities = RentalAmenities.objects.get(id=id)  
#     rental_amenities.delete() 
#     messages.success(request, ' Row deleted Successfully.')

#     return redirect(request.META.get('HTTP_REFERER'))

# # Rental-Amenities Code end

# # Rental-Activities Code start

# def rental_activities(request,id):
#     activities=Activity.objects.filter(user_id=request.user.id)
#     rental=Rental.objects.get(id=id)
#     rental_activities=RentalActivities.objects.filter(rental_id=rental.id)
    

#     context={
#         'activities':activities,
#         'rental':rental,
#         'rental_activities':rental_activities
#     }
#     return render(request,'users/rentals-activities/rentals-activities.html',context)    

# def rental_activities_insert(request,id):
#     if request.method == "POST":
#         rental=Rental()
#         rental_activities=RentalActivities()
#         rental_activities.activities_id=request.POST.get('activities')
#         rental_activities.user_id=request.user.id
#         rental_activities.rental=Rental.objects.get(id=id)
#         rental_activities.save()
#         messages.success(request, ' Row added Successfully.')
#         return redirect(request.META.get('HTTP_REFERER'))
#     return render(request,'users/rentals-activities/rentals-activities.html',{'rental':rental})   


# def rental_activity_destroy(request, id):  
#     rental_activity = RentalActivities.objects.get(id=id)  
#     rental_activity.delete() 
#     messages.success(request, ' Row deleted Successfully.')

#     return redirect(request.META.get('HTTP_REFERER'))      


# # Rental-Activities Code end


# # Rental-Policy Code start
# def rental_policy(request,id):
#     policy=Policy.objects.filter(user_id=request.user.id)
#     rental=Rental.objects.get(id=id)
#     rental_policy=RentalPolicy.objects.filter(rental_id=rental.id)
    

#     context={
#         'policy':policy,
#         'rental':rental,
#         'rental_policy':rental_policy
#     }
#     return render(request,'users/rentals-policy/rentals-policy.html',context)    

# def rental_policy_insert(request,id):
#     if request.method == "POST":
#         rental=Rental()
#         rental_policy=RentalPolicy()
#         rental_policy.policy_id=request.POST.get('policy')
#         rental_policy.user_id=request.user.id
#         rental_policy.rental=Rental.objects.get(id=id)
#         rental_policy.save()
#         messages.success(request, ' Row added Successfully.')
#         return redirect(request.META.get('HTTP_REFERER'))
#     return render(request,'users/rentals-policy/rentals-policy.html',{'rental':rental})    

# def rental_policy_destroy(request, id):  
#     rental_policy = RentalPolicy.objects.get(id=id)  
#     rental_policy.delete() 
#     messages.success(request, ' Row deleted Successfully.')

#     return redirect(request.META.get('HTTP_REFERER')) 

# # Rental-Policy Code end


# Rental-Gallery Code start
#def rentals_gallery_insert(request,id):
    #if request.method == "POST":
        #rental=Rental.objects.get(id=id)
        #rentals_gallery=RentalsGallery()
        #rentals_gallery.image=request.FILES.get('image')
        #rentals_gallery.user_id=request.user.id
        #rentals_gallery.rental=id
        #rentals_gallery.save()
        #messages.success(request, ' Row added Successfully.')
        #return redirect(request.META.get('HTTP_REFERER'))
    #return render(request,'users/rentals/rentals-gallery.html',{'rental':rental})   

# def rentals_gallery_insert(request,id):
#     if request.method == "POST":
#         rental=Rental()
#         rentals_gallery=RentalsGallery()
#         rentals_gallery.image=request.FILES.get('image')
#         rentals_gallery.user_id=request.user.id
#         rentals_gallery.rental=Rental.objects.get(id=id)
#         rentals_gallery.save()
#         messages.success(request, ' Row added Successfully.')
#         return redirect(request.META.get('HTTP_REFERER'))
#     return render(request,'users/rentals/rentals-gallery.html',{'rental':rental})   


#def rentals_gallery(request,id):
    
    #rental=Rental.objects.get(id=id)
    #rentals_gallery=RentalsGallery.objects.filter(rental_id=rental.id)
    

    #context={
        
    #    'rental':rental,
     #   'rentals_gallery':rentals_gallery
    #}
    #return render(request,'users/rentals/rentals-gallery.html',context)    





# Rental-Gallery Code end

# Customer Code start

def customers(request):   
    users = UserProfile.objects.all()
    return render (request,'users/customer/customers.html',{'users':users})


# Rentals JSON Rest API

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer


class BookingsViewSet(viewsets.ModelViewSet):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer

def reports(request):
    if request.method=="POST":
        fromdate = request.POST.get('from_date')
        todate = request.POST.get('to_date')
        
        search=Bookings.objects.raw('select id,booking_type,first_name,last_name,created_at from bookings where created_at between"'+fromdate+'" and " '+todate+'"')
        return render(request,'users/reports/reports.html',{'data':search})
    else:
        bookings = Bookings.objects.all()
        return render(request,'users/reports/reports.html',{'data':bookings})
   
# Attributes code start

@login_required(login_url='/users/')
def attributes_insert(request):  
    if request.method == "POST":
        attributes=Attributes()
        attributes.name=request.POST.get('name')  
        attributes.status=request.POST.get('status')
        attributes.user_id= request.user.id
        attributes.save()
        messages.success(request, ' Row added Successfully.')

    return redirect(request.META.get('HTTP_REFERER'))    

@login_required(login_url='/users/')
def attributes_add(request):
    return render (request,"users/attributes/attributes-add.html")     
       
@login_required(login_url='/users/') 
def attributes(request):
    attributes = Attributes.objects.all()  
    return render(request,"users/attributes/attributes.html",{'attributes':attributes})  

@login_required(login_url='/users/')
def attributes_edit(request, id):  
    attributes = Attributes.objects.get(id=id)  
    return render(request,'users/attributes/attributes-edit.html', {'attributes':attributes})  

@login_required(login_url='/users/')
def attributes_update(request, id):  
    attributes = Attributes.objects.get(id=id) 
    if request.method == "POST":
        attributes.name=request.POST.get('name')  
        attributes.status=request.POST.get('status')
        attributes.save()
        messages.success(request, ' Row updated Successfully.')

    return redirect(request.META.get('HTTP_REFERER'))  
   

@login_required(login_url='/users/')
def attributes_destroy(request, id):  
    attributes = Attributes.objects.get(id=id)  
    attributes.delete()
    messages.success(request, ' Row deleted Successfully.')  
    return redirect(request.META.get('HTTP_REFERER'))  

# Attributes code end      
@csrf_exempt
def sort(request):
    books = json.loads(request.POST.get('sort'))
    for b in books:
        book = get_object_or_404(RentalsGallery, pk=int(b['pk']))
        book.position = b['order']
        book.save()
    return JsonResponse(books)

def rentals_gallery(request, id):
    rental=Rental.objects.get(id=id)
    rentals_gallery=RentalsGallery.objects.filter(rental_id=rental.id).order_by('position')
    context={
    'rental':rental,
    'photos':rentals_gallery,
    'rental_id':id
    }
    #messages.success(request, ' Row Updated Successfully.')
    return render(request,'users/rentals/rental-photo.html',context)



def rentals_gallery_insert(request, id):  

    if request.method == "POST":

        rentals_gallery=RentalsGallery()

        rentals_gallery.image=request.FILES.get('image')

        rentals_gallery.user_id=request.user.id

        rentals_gallery.rental_id=id

        rentals_gallery.save()

        rental=rentals_gallery.save()

        data = {'is_valid': True, 'name': rental.image.name, 'url': rental.image.url}

        

    else:

        data = {'is_valid': False}
    messages.success(request, ' Row Updated Successfully.')
    return JsonResponse(data)

def gallery_destroy(request, id):  
    gallery = RentalsGallery.objects.get(id=id)  
    gallery.delete() 
    messages.success(request, ' Row deleted Successfully.')

    return redirect(request.META.get('HTTP_REFERER'))   

class CalendarViewNew(LoginRequiredMixin, generic.View ):
    template_name = "users/calendar/calendar.html"
    form_class = EventForm

    def get(self ,request, id ,*args, **kwargs ):
        
        forms = self.form_class()
        rentals=Rental.objects.all()
        rental=Rental.objects.get(id=id)
        cal=Event.objects.filter(rental_id=rental.id)
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events & cal:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),

                }
            )
        context = {"form": forms, "events": event_list,
                   "events_month": events_month,
                   "rentals":rentals,
                   "rental":rental,
                   "cal":cal}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.rental_id = 53
            form.save() 
            return redirect("/calendar/85")
        context = {"form": forms}
        return render(request, self.template_name, context)

def cal_destroy(request, id):  
    calender = Event.objects.get(id=id)  
    calender.delete()
    return redirect("/users/calendar")

# def profile(request):
#     return render(request,"users/user/profile.html")  

def profile(request):
    users = UserProfile.objects.get(user_id=request.user.id) 
    country=Country.objects.all()
    propertyrole=PropertyRole.objects.all()
    context={
        'users':users,
        'country':country,
        'propertyrole':propertyrole
    }
    return render(request,"users/user/profile.html",context)  

def profile_update(request,id):
    if request.method == "POST":
        users = UserProfile.objects.get(id=id)
        users.first_name =  request.POST.get('first_name')
        users.last_name =  request.POST.get('last_name')
        users.phone =  request.POST.get('phone')
        users.address =  request.POST.get('address')
        users.city=  request.POST.get('city')
        users.state= request.POST.get('state')
        users.country =  request.POST.get('country')
        users.postal_code =  request.POST.get('postal_code')
        users.property_phone_number =  request.POST.get('property_phone_number')
        users.tollfree =  request.POST.get('tollfree')
        users.website =  request.POST.get('website')
        users.property_role =  request.POST.get('property_role')
        users.no_of_properties =  request.POST.get('no_of_properties')
        users.description =  request.POST.get('description')   
        users.save()
        messages.success(request, 'Row updated Successfully.')
        return redirect ('/profile')

def subscription(request):
    subscription=Subscription.objects.all()
    return render (request,"users/subscription/subscription.html",{'subscription':subscription})

def subscription_insert(request,id):
    if request.method == "POST":
        subscrip=Subscription.objects.get(id=id)
        subplan=SubscriptionPlan()
        subplan.user_id=request.user.id
        subplan.subscription_id=subscrip.id
        subplan.subscription_title=subscrip.title
        subplan.price=subscrip.price
        subplan.tenure=subscrip.tenure
        subplan.description=subscrip.description
        subplan.start_date="NA"
        subplan.expiry_date="NA"
        subplan.save()
        
    return HttpResponse('Row added Successfully.')      

    