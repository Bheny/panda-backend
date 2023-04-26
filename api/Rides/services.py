import random
import string
import requests
import datetime 
# from .models import Ride

def send_sms(otp, number):
    if number and len(number) == 10:
        response = requests.get("https://sms.arkesel.com/sms/api?action=send-sms&api_key=OlZNNGJVWldVVE5UdEl2eEs=&to="+ number +"&from=MIJO&sms="+"DO NOT SHARE!!, \nYour OTP is "+ otp +"\nPlease Enter it in 15 minutes. No Staff of Mijo will ask for this Code!\nremember not to share with anyone !!!")
        return response.json
       
    

def generateOTP(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    


def random_string_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_request_id_generator(instance):
    id = random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(request_id=id).exists()

    if qs_exists:
        return unique_request_id_generator(instance)
    
    return id


def unique_otp_generator(instance):
    otp = generateOTP()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(otp=otp).exists()

    if qs_exists:
        return unique_otp_generator(instance)
    
    return otp

def random_int_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def search_rides(request):
    # Get user input from form
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    
    # Convert input strings to datetime objects
    start_datetime = datetime.datetime.strptime(start_date + start_time, '%Y-%m-%d%H:%M')
    end_datetime = datetime.datetime.strptime(end_date + end_time, '%Y-%m-%d%H:%M')
    
    # Search for rides that fall within the specified time frame
    matched_rides = Ride.objects.filter(date__range=(start_datetime.date(), end_datetime.date()), time__range=(start_datetime.time(), end_datetime.time()))
    
    return matched_rides
