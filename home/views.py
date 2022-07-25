from ast import Or
from unicodedata import category
from django.shortcuts import render, redirect
from django.shortcuts import render
import pyrebase
from regex import E
from django.contrib import auth, messages
import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from account.views import authe,db
from django.views.decorators.cache import cache_control

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from datetime import timedelta, date


# Create your views here.
def index(request):
    list=[]
    liste=[]
    ads=db.collection('advertiser').get()
    for dat in ads:
        ads=dat.to_dict()
        ads['adverid']=dat.id
        list.append(ads)
        detail=db.collection('advertiser').document(dat.id).collection('advertises').get()
        for datas in detail:
            adatas=datas.to_dict()
            adatas['adveid']=datas.id
            liste.append(adatas)
        print(liste)
    return render(request,'index.html',{'li':liste})

def categories(request):
    return render(request,"categories.html")
def about(request):
    return render(request,"about.html")
def faq(request):
    return render(request,"faq.html")
def contact(request):
    return render(request,"contact.html")
def all_product(request):
    return render(request,"all_product.html")
def popular_products(request):
    return render(request,"all_product.html")
def featured_products(request):
    return render(request,"all_product.html")
def guest_query(request):
    name=request.POST.get('name')
    print(name)
    email=request.POST.get('email')
    subjecte = request.POST.get('subject')
    subject = f'{subjecte}'
    message = request.POST.get('message')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
    return redirect(index)
def advertise(request):
    return render(request,'advertise.html')

def signup(request):
    return render(request, "ad_signup.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    role = 'advertiser'
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
        data = {"name":name,"email": email, "passw": passw, "role": role}

        db.collection('advertiser').document(uid).set(data)

    except:
        message = "Email already exists. Try with Different Email"
        return render(request, "ad_signup.html", {"messg": message})


    # data={"name":name,"status":"1"}
    # database.child("users").child(uid).child("details").set(data)

    subject = 'TiT-TaT SignUP'
    message = f'Hi User,\n Thank you for SignUp\nYour Login Credentials:\nUsername : {email}\nPassword : {passw}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return render(request, "ad_signin.html")

def signin(request):

    return render(request, 'ad_signin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hello(request):
    if request.session.is_empty():
        return redirect(signin)
    # a=request.session['local']
    # a=authe.get_account_info(idtoken)
    # a=a['users']
    # a=a[0]
    # a=a['localId']
    # data= db.collection('user').document(a).get().to_dict()
    # name=data["name"]
    return redirect(myadver)

#@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "ad_signin.html", {"messg": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    request.session['local'] = a

    datas = db.collection('advertiser').document(a).get().to_dict()
    request.session['name'] = datas["name"]
    request.session['email'] = datas["email"]
    per_data=db.collection('advertiser').document(a).collection('personal').get()
    for per in per_data:
        perd=per.to_dict()
        request.session['url'] = perd["url"]
        request.session['first'] = perd["first"]
        request.session['last'] = perd["last"]
        request.session['house'] = perd["house"]
        request.session['street'] = perd["street"]
        request.session['pincode'] = perd["pincode"]

        request.session['district'] = perd["district"]
        request.session['state'] = perd["state"]
        request.session['phone'] = perd["phone"]


    print(request.session['name'])

    return redirect(adver)

def contact(request):
    return render(request,'ad_contact.html')
def adver(request):
    a=request.session['local']






    return render(request,'adver.html')



def adpos(request,da,am):
    a=request.session['local']
    if da== '1 Day':
        dat=datetime.now()
        datr=datetime.now()+timedelta(1)
    elif da== '3 Day':
        dat=datetime.now()
        datr=datetime.now()+timedelta(3)
    elif da== '5 Day':
        dat=datetime.now()
        datr=datetime.now()+timedelta(5)
    elif da== '7 Day':
        dat=datetime.now()
        datr=datetime.now()+timedelta(7)
    elif da== '14 Day':
        dat=datetime.now()
        datr=datetime.now()+timedelta(14)
    elif da== '30 Day':
        dat=datetime.now()
        datr=datetime.now()+timedelta(30)
    elif da== '60 Day':
        dat=datetime.now()
        datr=datetime.now()+timedelta(60)
    elif da== '100 Day':
        dat=datetime.now()
        datr=datetime.now()+timedelta(100)



    return render(request,'ad_pos.html',{'da':da,'am':am,'dat':dat,'datr':datr})


def myadver(request):
    a=request.session['local']


    return render(request, 'ad_myads.html')
def profile(request):
    a=request.session['local']


    return render(request,'ad_profile.html')
def post_profile(request):

    a=request.session['local']
    first = request.POST.get('first')
    last = request.POST.get('last')
    phone = request.POST.get('phone')
    house = request.POST.get('house')
    street = request.POST.get('street')

    state = request.POST.get('state')
    district = request.POST.get('district')
    pincode = request.POST.get('pincode')
    url = request.POST.get('url')
    today = datetime.now()
    data = {
            "first": first,
            "last": last,
            "phone": phone,
            "house": house,
            "street": street,

            "district": district,
            "pincode": pincode,
            "state": state,
            "url": url,

            "date": today


        }


    dss=db.collection('advertiser').document(a).collection('personal')

    dss.add(data)



    return redirect(signin)
def ad_myads(request):
    #      for pro in data_pro:
	        #     prodict = pro.to_dict()
            # prodict["productid"] = pro.id
            # prodict['userid'] = key
            # list.append(prodict)
    list=[]
    a=request.session['local']
    datas=db.collection('advertiser').document(a).collection('advertises').get()
    for dat in datas:
        ads=dat.to_dict()
        ads['productid']=dat.id
        list.append(ads)
    a=request.session['local']
    print(list)
    return render(request,'ad_myads.html',{'li':list})



def ad_mprofile(request):



    return render(request,'ad_mprofile.html')


def myprofile(request):



    return render(request,'ad_myprofile.html')







from django.conf import settings
client = razorpay.Client(auth = (settings.RAZOR_KEY_ID , settings.RAZOR_KEY_SECRET))
def paying(request):
    amount=request.POST.get('amount')
    amount=int(amount)
    a=request.session['local']
    plan=request.POST.get('plan')
    fromm =request.POST.get('from')
    too= request.POST.get('to')
    com_name = request.POST.get('com_name')
    dats=datetime.now()
    file1=request.POST.get('url')

    data={'amount':amount,'plan':plan,'from':fromm,'to':too,'status':'not paid','com_name':com_name,'dats':dats,'poster':file1,'status':'added'}

    dass=db.collection('advertiser').document(a).collection('advertises')
    dass.add(data)

    amount=amount*100
    currency = 'INR'
     # Rs. 200

    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request,'pay_proceed.html',context=context)
@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            print(result)
            if result is True:
            #      for pro in data_pro:
	        #     prodict = pro.to_dict()
            # prodict["productid"] = pro.id
            # prodict['userid'] = key
            # list.append(prodict)

                a=request.session['local']
                #list=[]
                ads = db.collection('advertiser').document(a).collection('advertises').where('status','==','added').get()
                #amd=amo[0].id
                for ad in ads:
                    am=ad.to_dict()
                    amd=ad.id
                    # adver['adsid']=ad.id
                    # list.append(adver)


                #am=db.collection('advertiser').document(a).collection('advertises').document(amd).get().to_dict()

                amount = am["amount"]
                print(amount) # Rs. 200
                try:
                    print(amount)
                    # capture the payemt
                    amount=amount*100
                    print("hello")
                    client.payment.capture(payment_id, amount)
                    print("hai")
                    print(amount)

                    # render success page on successful caputre of payment
                    db.collection('advertiser').document(a).collection('advertises').document(amd).update({'status':'Paid'})
                    am=db.collection('advertiser').document(a).collection('advertises').document(amd).get().to_dict()


                    person = db.collection('advertiser').document(a).collection('personal').get()
                    personals=person[0].id
                    persons = db.collection('advertiser').document(a).collection('personal').document(personals).get().to_dict()
                    print(persons)
                    print("perid",personals)

                    return render(request, 'payment_sucess.html',{'per':persons,'pid':personals,'ads':am,'adid':amd})
                    #return render(request, 'payment_sucess.html')


                except:

                    # if there is an error while capturing payment.
                    print("failed")
                    db.collection('advertiser').document(a).collection('advertises').document(amd).update({'status':'unpaid'})
                    # print("hek")
                    # datas=db.collection('advertiser').document(a).collection('advertises').document(amd).get().to_dict()
                    # print(datas)
                    # print("adid",amd)
                    person = db.collection('advertiser').document(a).collection('personal').get()
                    personals=person[0].id
                    persons = db.collection('advertiser').document(a).collection('personal').document(personals).get().to_dict()
                    print(persons)
                    print("perid",personals)

                    return render(request, 'payment_fail.html',{'per':persons,'pid':personals,'ads':am,'adid':amd})

                    #return render(request, 'payment_fail.html')
            else:

                # if signature verification fails.
                print("fails")
                return render(request, 'payment_fail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

def proceed(request):

    client = razorpay.Client(auth = (settings.KEY , settings.SECRET))
    payment = client.order.create({"amount": amount*100,"currency":"INR","payment_capture":1})
    print("***********************")
    print(payment)
    print("***********************")
    context={'payment':payment}

    return render(request,'pay_proceed.html',context)




