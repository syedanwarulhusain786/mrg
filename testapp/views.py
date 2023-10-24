from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect 
# Create your tests here.
from django.core.paginator import Paginator

from django.contrib import messages
from django.shortcuts import render, redirect 

from django.db.models import Q

from django.utils.translation import gettext as _
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import xml.etree.ElementTree as ET


# from accounts.serializers import *
import time
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render
from .models import Video
from django.http import JsonResponse
import datetime
from django.db.models import Q
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

#stripe listen --forward-to localhost:8000/webhook/stripe
def index(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with your home page URL.
        else:
            message="Invalid login credentials"
            return render(request, 'login.html', {'message': message})

    return render(request, 'login.html')
def signup(request):
    
    return render(request, 'signup.html')


def logoutUser(request):
    logout(request)
    return redirect('login')




def get_date(forward, backward):
    # Implement your CSV merging logic here
    # You can use the csv module to read and merge the data from the two files
    # Example logic (for a text file):
    with forward.open() as file_content:
            forwardcontent = file_content.read().decode('utf-8')
    with backward.open() as file_content:
            backwardcontent = file_content.read().decode('utf-8')
    soup1 = BeautifulSoup(forwardcontent, 'xml')
    soup2 = BeautifulSoup(backwardcontent, 'xml')
    forward_title=soup1.find('Title').text.split('M1')[-1].strip()
    forward_date=forward_title.split('-')
    forward_date_start=forward_date[0]
    forward_date_end=forward_date[1]
    backward_title=soup2.find('Title').text.split('M1')[-1].strip()
    # backward_date=backward_title.split('-')
    # backward_date_start=backward_date[0]
    # backward_date_end=backward_date[0]
    if forward_title==backward_title:
        date_str = re.search(r'\d{4}.\d{2}.\d{2}', forward_date_start)
        date_str1 = re.search(r'\d{4}.\d{2}.\d{2}', forward_date_end)
        
        if date_str and date_str1:
            start =forward_date_start.replace(".","-")#datetime.strptime(date_str.group(), '%Y.%m.%d')
            end =forward_date_end.replace(".","-")#datetime.strptime(date_str1.group(), '%Y.%m.%d')
            
        dt={
            'start':start,
            'end':end,
            
        }
        return dt
    else:
        return  dt
def get_rows_back(soup):
    data={}
    back_head=soup['heading'][0:32]
    
    back_pass=back_head[0]
    back_result=back_head[2].replace(' ','_')
    back_profit=back_head[3].replace(' ','_')
    back_r_f=back_head[6].replace(' ','_')
    back_e_dd_per=back_head[9].replace(' ','_').replace('%','')
    back_trades=back_head[10].replace(' ','_')
    for dt in soup['data']:
        data[dt['Pass']]={
            f"back_pass":dt['Pass'],
            f"back_{back_result}":dt['Back Result'],
            f"back_{back_profit}":dt['Profit'],
            f"back_{back_r_f}":dt['Recovery Factor'],
            f"back_{back_e_dd_per}d":dt['Equity DD %'],
            f"back_{back_trades}":dt['Trades'],
        }
    return data

def get_rows_forwad(soup,res,diff,file_name,balance,drawdown):
    deposit=balance
    
    # ok_dd=1000
    # print(ok_dd)
    data=[]
    # print(soup['data'][0])
    forward_head=soup['heading'][0:32]
    forward_pass=forward_head[0]
    forward_result=forward_head[1].replace(' ','_')
    forward_profit=forward_head[2].replace(' ','_')
    forward_r_f=forward_head[5].replace(' ','_')
    forward_e_dd_per=forward_head[8].replace(' ','_').replace('%','')
    forward_trades=forward_head[9].replace(' ','_')
    for dt in soup['data']:
        Mypass=dt['Pass'].strip()

        
        
        if dt['Pass'].strip() in res :#and dt[0].text.strip() =='7703':
            res[Mypass][f"filename"]=file_name
            res[Mypass][f"forward_{forward_result}"]=dt['Result']
            res[Mypass][f"forward_{forward_profit}"]=dt['Profit']
            res[Mypass][f"forward_{forward_r_f}"]=dt['Recovery Factor']
            res[Mypass][f"forward_{forward_e_dd_per}d"]=dt['Equity DD %']
            res[Mypass][f"forward_{forward_trades}"]=dt['Trades']
            try:
                # print(float(dt[3].text),float(res[dt[0].text]['back_Profit']),diff)
                res[Mypass][f"profit_match"]=round((float(dt['Profit'])/(float(res[Mypass]['back_Profit'])/diff))*100,2)
            except:
                res[Mypass][f"profit_match"]=0
            try:
                res[Mypass][f"total_profit"]=round(float(dt['Profit'])+float(res[Mypass]['back_Profit']),2)
            except:
                res[Mypass][f"total_profit"]=0
            try:
                
                res[Mypass][f"max_original_dd"]=round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2)
                
            except:
                res[Mypass][f"max_original_dd"]=0
                
                
            try:
                res[Mypass][f"Lot_Multiple"]=round(drawdown/round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2),2)
                
            except:
                res[Mypass][f"Lot_Multiple"]=0
            try:
                res[Mypass][f"Estimated_Total_DD"]=round((round(drawdown/round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2),2)*round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2)),2)
                
            except:
                res[Mypass][f"Estimated_Total_DD"]=0
                
            try:
                res[Mypass][f"Estimated_Profit"]=round((float(dt['Profit'])+float(res[Mypass]['back_Profit']))*round(drawdown/round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2),2),2)
                
            except:
                res[Mypass][f"Estimated_Profit"]=0
            try:
                res[Mypass][f"Max_DD"]=round((max(float(res[Mypass]['back_Equity_DD_d']), float(dt['Equity DD %']))*balance)/(100*round(drawdown/round((float(res[Mypass]['back_Equity_DD_d']))*(deposit/100),2),2)),2)
                    
            except:
                res[Mypass][f"Max_DD"]=0

            data.append(res[Mypass])   
        
    return data

def merge_xml(file1, file2,diff,file_name,balance,drawdown):
            # Implement your CSV merging logic here
        # You can use the csv module to read and merge the data from the two files
        # soup1 = BeautifulSoup(file1, 'xml')
        # soup2 = BeautifulSoup(file2, 'xml')

        # Implement your merging logic here
        
        
        # For demonstration purposes, we'll just concatenate the XML strings
        merged_xml_data = get_rows_back(file2)
        merged_xml_data = get_rows_forwad(file1,merged_xml_data,diff,file_name,balance,drawdown)
        # time.sleep(10)
        
        # Example:
        # Read file1 and file2 and merge the data into merged_data

        return merged_xml_data
q_objects=''    
    
def calculation(date2_str,date1_str):
    # Convert the date strings to datetime objects
    date1 = datetime.strptime(date1_str, '%Y-%m-%d')
    date2 = datetime.strptime(date2_str, '%Y-%m-%d')

    # Calculate the difference in days between the two dates
    date_difference = (date2 - date1).days

    # Calculate the number of weeks
    weeks = date_difference / 7
    return weeks
@login_required(login_url='login')
def download(request):
    files = DownloadItem.objects.all()  # Retrieve all videos from your database
    
    context = {'files': files,"user":request.user}
    return render(request, 'download.html',context)
@login_required(login_url='login')
def video(request):
    videos = Video_Ea.objects.all()  # Retrieve all videos from your database
    
    context = {'videos': videos,"user":request.user}
    return render(request, 'video.html',context)

import json

def upload_file(request):
    merged_data = [] 
    file_name=''
    global extracted_date
    if request.method == 'POST':

        json_data = json.loads(request.body)
        forward_date=json_data[2]['forward']
        start_date=json_data[2]['start_date']
        end_date=json_data[2]['end_date']
        balance=float(json_data[2]['balance'])
        
        drawdown=float(json_data[2]['drawdown'])
        
        g15 = calculation(forward_date, start_date)
        g16 = calculation(end_date, forward_date)
        g17 = g15 / g16
        file_name = json_data[2]['filename'].split('.')[0]
        forward=json_data[1]
        back=json_data[0]
    
        
        
        merged_data = merge_xml(back,forward, g17,file_name,balance,drawdown)
        
        # For demonstration purposes, we'll return the extracted date as an HTTP response.
        return JsonResponse({"page":merged_data})


@login_required(login_url='login')
def video_cards(request):
    videos = Video.objects.all()  # Retrieve all videos from your database
    
    context = {'videos': videos,"user":request.user}
    return render(request, 'library.html', context)


@login_required(login_url='login')
def faq(request):
    Faqs = Faq.objects.all()  # Retrieve all videos from your database
    print()
    context = {'Faqs': Faqs,"user":request.user}
    return render(request, 'faq.html',context)


stripe.api_key=settings.STRIPE_SECRET_KEY
endpoint_secret=settings.STRIPE_WEBHOOK_SECRET
def CreateCheckoutSessionView(request):
    if request.method == 'POST':
        host=request.get_host()
        
        username=request.POST['username']
        bemail=request.POST['bemail']
        password=request.POST['password']
        bfirstname=request.POST['bfirstname']
        blastname=request.POST['blastname']
        fullname=request.POST['fullname']
        baddress1=request.POST['baddress1']
        baddress2=request.POST['baddress2']
        bstate=request.POST['bstate']
        
        bcity=request.POST['bcity']
        bzipcode=request.POST['bzipcode']
        bcountry=request.POST['bcountry']
        bphone=request.POST['bphone']
        
        user = User(username=username, email=bemail, first_name=bfirstname, last_name=blastname)

        # Set the user's password (you should hash the password)
        user.set_password(password)

        # Set is_active to False
        user.is_active = False

        # Save the User object to the database
        user.save()
        ids=user.id

        
        checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price_data': {
                    'currency':'inr',
                    'unit_amount':599000,
                    'product_data':{
                        'name':'codepiep order'
                    },
                },
                'quantity': 1,
                },

        ],
        metadata={
                'ids':ids,
                "fullname":fullname,
                "baddress1":baddress1,
                "baddress2":baddress2,
                "bstate":bstate,
                "bcity":bcity,
                "bzipcode":bzipcode,
                "bcountry":bcountry,
                "bphone":bphone,
            },
        mode='payment',
        success_url="http://{}{}".format(host,reverse('success')),
        cancel_url="http://{}{}".format(host,reverse('cancel')),
        )
    return redirect(checkout_session.url, code=303)
def success(request):
    context={
       'payment_status' :'success'
    }
    return render(request,'success.html',context)
def cancel(request):
    context={
       'payment_status' :'cancel'
    }
    return render(request,'cancel.html',context)

@csrf_exempt

def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event["type"]== 'checkout.session.completed':
        session = event['data']['object']
        if session.payment_status=="paid":
            register_user(session)
        
    # Passed signature verification
    return HttpResponse(status=200)


def register_user(session):
    user_obj=User.objects.get(id=int(session['metadata']['ids']))
    user_obj.is_active = True
    user_obj.save()
    # line_item=session.list_line_items(session.id,limit=1).data[0]
    # intent=line_item['description']
    pay=Payment(
        user = user_obj,
        transaction_id = session.payment_intent,#intent['payment_intent'],
        amount =session.amount_total,#intent["amount_total"],
        
        # Address Fields
        address1 = session['metadata']['baddress1'],
        address2 = session['metadata']['baddress2'],
        city = session['metadata']['bcity'],
        state = session['metadata']['bstate'],
        zipcode = session['metadata']['bzipcode'],
        country = session['metadata']['bcountry'],
    )
    pay.save()
@login_required(login_url='login')    
def setfinder(request):
    
    return render(request, 'setfinder.html')
@login_required(login_url='login')
def home(request):
    
    return render(request, 'home.html')





def get_rows_forward(xmlDataForward, back, diff, file_name, deposit, drawdown):
    data = []

    data = []
    for row in xmlDataForward.find_all('Row'):
        rowData = []
        for cell in row.find_all('Cell'):
            cellData = cell.find('Data')
            rowData.append(cellData.text if cellData is not None else '')

        data.append(rowData)
        

    forward_head = data[0]
    forward_pass = forward_head[0]
    forward_result = forward_head[1].replace(' ', '_')
    forward_profit = forward_head[3].replace(' ', '_')
    forward_r_f = forward_head[6].replace(' ', '_')
    forward_e_dd_per = forward_head[9].replace(' ', '_').replace('%', '')
    forward_trades = forward_head[10].replace(' ', '_')
    data.pop(0)

    data_dict = {}

    for dt in data:

        forward_pass = dt[0]
        print(dt)
        print(back[forward_pass]['back_Profit'])
        print(diff)
        profit_match = 0  # Default value

        if back[forward_pass]['back_Profit'] != 0:
            profit_match = round((float(dt[2]) / (float(back[forward_pass]['back_Profit']) / diff) * 100), 2)

        total_profit = round(float(dt[2]) + float(back[forward_pass]['back_Profit']), 2)
        max_original_dd = round(float(back[forward_pass]['back_Equity_DD_d']) * (float(float(deposit)) / 100), 2)
        lot_multiple = 0

        if back[forward_pass]['back_Equity_DD_d'] != 0:
            lot_multiple = round(drawdown / (round(float(back[forward_pass]['back_Equity_DD_d'])* (float(deposit) / 100), 2)), 2)

        estimated_total_dd = 0
        estimated_profit = 0

        if back[forward_pass]['back_Equity_DD_d'] != 0:
            estimated_total_dd = round(round(drawdown / (round(float(back[forward_pass]['back_Equity_DD_d']) * (float(deposit) / 100), 2)) * round(float(back[forward_pass]['back_Equity_DD_d']) * (float(deposit) / 100), 2)), 2)
            estimated_profit = round((dt[2] + float(back[forward_pass]['back_Profit'])) * (round(drawdown / (round(float(back[forward_pass]['back_Equity_DD_d']) * (float(deposit) / 100), 2)), 2)), 2)

        max_dd = round(max(float(back[forward_pass]['back_Equity_DD_d']), dt[10]) * (float(deposit) / 100), 2)

        data_dict[forward_pass] = {
            "file_name": file_name,
            "pass": dt[0],
            "forward_result": dt[1],
            "forward_profit": dt[2],
            "forward_r_f": dt[6],
            "forward_e_dd_per": dt[9],
            "forward_trades": dt[10],
            "back_Result": back[forward_pass]['back_Result'],
            "back_Profit": back[forward_pass]['back_Profit'],
            "back_Recovery_Factor": back[forward_pass]['back_Recovery_Factor'],
            "back_Equity_DD_d": back[forward_pass]['back_Equity_DD_d'],
            "back_Trades": back[forward_pass]['back_Trades'],
            "profit_match": profit_match,
            "total_profit": total_profit,
            "max_original_dd": max_original_dd,
            'lot_Multiple': lot_multiple,
            "Estimated_Total_DD": estimated_total_dd,
            "Estimated_Profit": estimated_profit,
            "Max_DD": max_dd,
        }

    return data_dict

def calculation(date2_str, date1_str):
    # Convert the date strings to datetime objects
    date1 = datetime.strptime(date1_str, '%Y-%m-%d')
    date2 = datetime.strptime(date2_str, '%Y-%m-%d')

    # Calculate the difference in days between the two dates
    date_difference = (date2 - date1).days

    # Calculate the number of weeks
    weeks = date_difference / 7
    return weeks










@login_required(login_url='login')
@csrf_exempt
def handle_custom_download_submit(request):
    # Verify nonce if needed
        # Handle form data and files here
    row_id = request.POST.get('row_id')
    
    if 'fileforward' in request.FILES and 'fileset' in request.FILES:
        fileforward = request.FILES['fileforward']
        filenameset = request.FILES['fileset']
        
        # Handle file uploads here

        # Check if both files were uploaded successfully
        if fileforward and filenameset:
            xmlContentForward = fileforward.read()
            Contentfilenameset = filenameset.read()
            
            # Parse XML data from the 'Forward' file
            # Your XML parsing code goes here

            data = {}  # Your data processing logic goes here
            headers = []
            is_first_row = True

            soup = BeautifulSoup(xmlContentForward, 'lxml-xml')  # Use 'lxml-xml' parser for XML content

            for row in soup.find_all('Row'):
                rowData = []
                passValue = None

                for cell in row.find_all('Cell'):
                    cellData = cell.find('Data')
                    cellValue = cellData.text if cellData else ''

                    if is_first_row:
                        headers.append(cellValue.replace(' ', '').replace('_', '').lower())
                    else:
                        rowData.append(cellValue)

                if not is_first_row:
                    passValue = rowData[0]
                    if passValue == row_id:
                        data[passValue] = dict(zip(headers, rowData))

                is_first_row = False
                    # Prepare response data
            response = data[row_id]

            # Send response as JSON
            return JsonResponse(response)

        else:
            return JsonResponse({'message': 'Error uploading .set file files.'})

    else:
        return JsonResponse({'message': 'File fields not found.'})




