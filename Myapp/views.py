import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render,HttpResponse
from Myapp.models import *

# Create your views here.

def Login(request):
    return render(request, 'login_index.html')

def login_post(request):
    uname=request.POST['Username']
    password=request.POST['Password']
    log=login.objects.filter(Username=uname,Password=password)
    if log.exists():
        logid=log[0].id
        request.session['lid']=logid
        if log[0].Usertype == 'admin':
            return HttpResponse("<script>alert('Login Success');window.location='/homepage'</script>")
        if log[0].Usertype == 'seller':
            return HttpResponse("<script>alert('Login Success');window.location='/Home_Page'</script>")
        if log[0].Usertype == 'customer':
            return HttpResponse("<script>alert('Login Success');window.location='/customer_home'</script>")
        else:
            return HttpResponse("<script>alert('Invalid Authentication');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('Check your Username and Password');window.location='/'</script>")

def forgot_password(request):
    return render(request,"forgot_password.html")

def forgot_password_post(request):
    email = request.POST['email']
    data = login.objects.filter(Username=email)
    if data.exists():
        pwd = data[0].Password
        import smtplib

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("demo@gmail.com", "tcap lzzh lmrz afio")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "demo@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for E-commerce Project"
        body = "Your Password is:- - " + str(pwd)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return HttpResponse("<script>alert('password sended');window.location='/'</script>")
    return HttpResponse("mail incorrect")


def add_category(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        return render(request,'admin/add_Category.html')

def add_category_post(request):
    name=request.POST['name']
    cat=category()
    cat.Name=name
    cat.save()
    return HttpResponse("<script>alert('added');window.location='/add_category'</script>")

def view_category(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        res=category.objects.all()
        return render(request,'admin/view Category.html',{'data':res})

def delete_category(request,id):
    category.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted');window.location='/add_category'</script>")


def view_feedback(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        aaa=feedback.objects.all()
        return render(request,'admin/Feedback.html',{'data':aaa})

def view_Customer(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        bbb=customer.objects.all()
        return render(request,'admin/Customer.html',{'data':bbb})

def view_Seller(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    ccc=seller.objects.filter(LOGIN__Usertype='pending')
    return render(request,'admin/Seller.html',{'data':ccc})

def approve_seller(request,id):
    login.objects.filter(id=id).update(Usertype='seller')
    return HttpResponse("<script>alert('Approved');window.location='/view_Seller'</script>")

def reject_seller(request,id):
    login.objects.filter(id=id).update(Usertype='reject')
    return HttpResponse("<script>alert('Rejected');window.location='/view_Seller'</script>")

def verified_sellers(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        ddd=seller.objects.filter(LOGIN__Usertype='seller')
        return render(request,'admin/Verified_sellers.html',{'data':ddd})

def homepage(request):
    return render(request,'admin/index.html')


def logout(request):
    request.session['lid']=''
    return HttpResponse("<script>alert('logout successfully');window.location='/'</script>")

# ===================================== Seller ==================================

def Product_Add(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        data = category.objects.all()
        return render(request,'Seller/Product_Add.html',{'data':data})

def Product_Add_post(request):
    name = request.POST['Product_Name']
    price = request.POST['Price']
    image = request.FILES['fileField']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime("Y%m%d-%H%M%S")
    fs.save(r"C:\Users\DELL\Downloads\Ecommerce\Ecommerce\Myapp\static\images\\" + dt + '.jpg',image)
    path = '/static/images/' + dt +'.jpg'
    category = request.POST['select']
    description = request.POST['Description']
    data = product.objects.filter(Name=name,Image=image)
    if data.exists():
        return HttpResponse("<script>alert('Product already exists');window.location='/Product_Add'</script>")
    else:

        cat = product()
        cat.Name=name
        cat.Price=price
        cat.Image=path
        cat.Category_id=category
        cat.Description=description
        cat.Seller = seller.objects.get(LOGIN=request.session['lid'])
        cat.save()
        return HttpResponse("<script>alert('added');window.location='/Product_Add'</script>")

def Update_Product(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        data = product.objects.get(id=id)
        data1 = category.objects.all()
    return render(request,'seller/Update_Product.html',{"data":data,"id":id,"data1":data1})

def Update_Product_post(request,id):
   try:
       name = request.POST['Product_Name']
       price = request.POST['Price']
       image = request.FILES['fileField']
       fs = FileSystemStorage()
       dt = datetime.datetime.now().strftime("Y%m%d-%H%M%S")
       fs.save(r"C:\Users\DELL\Downloads\Ecommerce\Ecommerce\Myapp\static\images\\" + dt + '.jpg', image)
       path = '/static/images/' + dt + '.jpg'
       category = request.POST['select']
       description = request.POST['Description']
       product.objects.filter(id=id).update(Name=name, Price=price, Image=path, Category=category,
                                            Description=description)
       return HttpResponse("<script>alert('Updated');window.location='/View_Product'</script>")
   except Exception as e:
       name = request.POST['Product_Name']
       price = request.POST['Price']

       category = request.POST['select']
       description = request.POST['Description']
       product.objects.filter(id=id).update(Name=name, Price=price, Category=category,
                                            Description=description)
       return HttpResponse("<script>alert('Updated');window.location='/View_Product'</script>")

def Delete_Product(request,id):
    product.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Deleted');window.location='/View_Product'</script>")

def View_Product(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        v=product.objects.filter(SELLER__LOGIN=request.session['lid'])
        return render(request, 'Seller/View_Product.html',{'data':v})

def view_ratingss(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        res = Rating.objects.filter(PRODUCT_id = id)
        fs = "/static/star/full.jpg"
        hs = "/static/star/half.jpg"
        es = "/static/star/empty.jpg"
        data = []

        for rt in res:
            a = float(rt.Rating)

            if a >= 0.0 and a < 0.4:
                ar = [es, es, es, es, es]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )

            elif a >= 0.4 and a < 0.8:
                ar = [hs, es, es, es, es]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )

            elif a >= 0.8 and a < 1.4:
                ar = [fs, es, es, es, es]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )

            elif a >= 1.4 and a < 1.8:
                ar = [fs, hs, es, es, es]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )

            elif a >= 1.8 and a < 2.4:
                ar = [fs, fs, es, es, es]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )

            elif a >= 2.4 and a < 2.8:
                ar = [fs, fs, hs, es, es]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )
            elif a >= 2.8 and a < 3.4:
                ar = [fs, fs, fs, es, es]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )

            elif a >= 3.4 and a < 3.8:
                ar = [fs, fs, fs, hs, es]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )

            elif a >= 3.8 and a < 4.4:
                ar = [fs, fs, fs, fs, es]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )
            elif a >= 4.4 and a < 4.8:
                ar = [fs, fs, fs, fs, hs]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )

            elif a >= 4.8 and a <= 5.0:
                ar = [fs, fs, fs, fs, fs]
                data.append(
                    {
                        "Rating": ar,
                        "CUSTOMER": rt.CUSTOMER,
                        "PRODUCT": rt.PRODUCT,
                        "date": rt.date

                    }
                )

        return render(request,'Seller/Rating.html',{'data':data})

def Sales_Report(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        q =ordersub.objects.all()
        return render(request,'Seller/Sales_Report.html',{'data':q})

def View_Order(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        u=ordersub.objects.all()
        return render(request, 'Seller/View_Order.html',{'data':u})

def  update_order_status(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    return render(request,'Seller/Delivery_status.html',{'id':id})

def update_order_status_post(request,id):
    dst=request.POST['select']
    orderr.objects.filter(id=id).update(Status=dst)
    return HttpResponse("<script>alert('status updated');window.location='/View_Order'</script>")

def view_profile(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    else:
        y=seller.objects.get(LOGIN=request.session['lid'])
        return render(request,'Seller/view_profile.html',{'data':y})

def Home_Page(request):
    return render(request,'Seller/index.html')


def Seller1(request):
    return render(request, 'seller_register.html')

def Seller1_post(request):
    name=request.POST['Name']
    password = request.POST['Password']
    email = request.POST['Email']
    phone = request.POST['Phone']
    place = request.POST['Place']
    post  = request.POST['POST']
    pin   = request.POST['PIN']
    log=login.objects.filter(Username=email)
    if log.exists():
        return HttpResponse("<script>alert('the user already exists');window.location='/'</script>")
    else:
        obj = login()
        obj.Username=name
        obj.Password=password
        obj.Usertype = 'pending'
        obj.save()

        cat=seller()
        cat.Name=name
        cat.LOGIN=obj
        cat.Email=email
        cat.Phone=phone
        cat.Place=place
        cat.Post=post
        cat.PIN=pin
        cat.save()
        return HttpResponse("<script>alert('Registration Success');window.location='/'</script>")

# ================================ Customer =========================================================

def customer_home(request):
    return render(request,"Customer/index.html")

def customer_reg(request):
    return render(request, 'customer_registration.html')

def customer_reg_post(request):
    name=request.POST['Name']
    password = request.POST['Password']
    email = request.POST['Email']
    phone = request.POST['Phone']
    place = request.POST['Place']
    post  = request.POST['POST']
    pin   = request.POST['PIN']
    log=login.objects.filter(Username=email)
    if log.exists():
        return HttpResponse("<script>alert('The Customer  is already exists');window.location='/'</script>")
    else:
        obj = login()
        obj.Username=name
        obj.Password=password
        obj.Usertype = 'customer'
        obj.save()

        cat=customer()
        cat.Name=name
        cat.LOGIN=obj
        cat.Email=email
        cat.Phone=phone
        cat.Place=place
        cat.Post=post
        cat.PIN=pin
        cat.save()
        return HttpResponse("<script>alert('Registration Success');window.location='/'</script>")

def customer_view_profile(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    data = customer.objects.get(LOGIN=request.session['lid'])
    return render(request,"Customer/view_profile.html",{"data":data})

def customer_view_category(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    data = category.objects.all()
    return render(request,"Customer/view_category.html",{"data":data})

def customer_view_product(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    data = product.objects.filter(CATEGORY_id = id)
    return render(request,"Customer/view_product.html",{"data":data})

# ============================= CART ===========================================

def add_to_cart(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    return render(request,"Customer/add_to_cart.html",{"id":id})

def add_to_cart_post(request,id):
    quantity = request.POST['textfield']
    data = cart.objects.filter(CUSTOMER__LOGIN=request.session['lid'],PRODUCT=id)
    if data.exists():
        return HttpResponse("<script>alert('Product Already in Cart!!');window.location='/user_view_category'</script>")
    else:
        obj = cart()
        obj.CUSTOMER = customer.objects.get(LOGIN=request.session['lid'])
        obj.PRODUCT_id = id
        obj.Quantity = quantity
        obj.save()
        return HttpResponse("<script>alert('Add to cart');window.location='/customer_view_category'</script>")

def view_cart(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    data = cart.objects.filter(CUSTOMER__LOGIN=request.session['lid'])
    return render(request,"Customer/view_cart.html",{"data":data})

def place_order(request,id):
    data = cart.objects.filter(CUSTOMER__LOGIN=request.session['lid'])
    amount = 0
    for i in data:
        product_amount = i.PRODUCT.Price
        quantity = i.Quantity
        amount = int(quantity) * int(product_amount)

    if data.exists():

        obj = orderr()
        obj.Date = datetime.datetime.now().date()
        obj.Status = 'pending'
        obj.Payment_Status = 'pending'
        obj.Payment_Date = 'pending'
        obj.CUSTOMER = customer.objects.get(LOGIN=request.session['lid'])
        obj.Amount = amount
        obj.save()

        for i in data:
            obj1 = ordersub()
            obj1.order_date = datetime.datetime.now().date()
            obj1.Quantity = i.Quantity
            obj1.ORDERR = obj
            obj1.save()
            cart.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Order Placed');window.location='/view_cart'</script>")


def view_order(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session expired!Login again');window.location='/'</script>")
    data = orderr.objects.filter(CUSTOMER__LOGIN=request.session['lid'],Payment_Status='pending',Payment_Date='pending')
    return render(request,"Customer/view_order.html",{"data":data})

def cancel_order(request,id):
    orderr.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Order Cancelled');window.location='/view_cart'</script>")

#===================== PAYMENT =====================================

def payment_mode(request,rid):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session expired!Login again');window.location='/'</script>")
    data = orderr.objects.get(id=rid)
    request.session['orginalamount'] = data.Amount
    request.session['requestid'] = rid
    return render(request,"Customer/payment_mode.html",{"rid":rid})

def payment_mode_post(request,rid):
    mode = request.POST['RadioGroup1']
    data1 = orderr.objects.filter(id=rid)
    if mode == 'offline':
        data1.update(Payment_Status=mode,Payment_Date = datetime.datetime.now().date())
        return HttpResponse("<script>alert('Offline Payment');window.location='/view_order'</script>")
    else:
        import razorpay

        razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
        razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

        razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

        amount = float(data1[0].Amount) * 100
        # amount = float(amount)

        # Create a Razorpay order (you need to implement this based on your logic)
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt': 'order_rcptid_11',
            'payment_capture': '1',  # Auto-capture payment
        }

        # Create an order
        order = razorpay_client.order.create(data=order_data)


        return render(request, 'Customer/UserPayProceed.html', {'razorpay_api_key': razorpay_api_key,
                                                            'amount': order_data['amount'],
                                                            'currency': order_data['currency'],
                                                            'order_id': order['id'],
                                                            'rid': rid
        })


def on_payment_success(request,id):
    dt = datetime.datetime.now().date()
    orderr.objects.filter(id=id).update(Payment_Status='online',Payment_Date=dt)
    return HttpResponse("<script>alert('Success!');window.location='/view_order'</script>")



def view_previous_order(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session expired!Login again');window.location='/'</script>")
    data = ordersub.objects.filter(Q(ORDERR__Payment_Status='online')|Q(ORDERR__Payment_Status='offline'),ORDERR__CUSTOMER__LOGIN=request.session['lid'])
    return render(request,"Customer/view_previous_order.html",{"data":data})


def customer_send_feedback(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    return render(request,"Customer/send_feedback.html")

def customer_send_feedback_post(request):
    feedbacks = request.POST['textarea']
    obj = feedback()
    obj.Date = datetime.datetime.now().date()
    obj.Feedback = feedbacks
    obj.CUSTOMER = customer.objects.get(LOGIN=request.session['lid'])
    obj.save()
    return HttpResponse("<script>alert('Success!');window.location='/customer_send_feedback'</script>")

def view_rating(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again!');window.location='/'</script>")
    res = Rating.objects.filter(CUSTOMER__LOGIN=request.session['lid'],PRODUCT_id = id)
    fs = "/static/star/full.jpg"
    hs = "/static/star/half.jpg"
    es = "/static/star/empty.jpg"
    data = []

    for rt in res:
        a = float(rt.Rating)

        if a >= 0.0 and a < 0.4:
            ar = [es, es, es, es, es]
            data.append(
                {
                    "Rating":ar,
                    "CUSTOMER":rt.CUSTOMER,
                    "PRODUCT":rt.PRODUCT,
                    "date":rt.date

                }
            )

        elif a >= 0.4 and a < 0.8:
            ar = [hs, es, es, es, es]
            data.append(
                {
                    "Rating": ar,
                    "CUSTOMER": rt.CUSTOMER,
                    "PRODUCT": rt.PRODUCT,
                    "date": rt.date

                }
            )

        elif a >= 0.8 and a < 1.4:
            ar = [fs, es, es, es, es]
            data.append(
                {
                    "Rating": ar,
                    "CUSTOMER": rt.CUSTOMER,
                    "PRODUCT": rt.PRODUCT,
                    "date": rt.date

                }
            )

        elif a >= 1.4 and a < 1.8:
            ar = [fs, hs, es, es, es]
            data.append(
                {
                    "Rating": ar,
                    "CUSTOMER": rt.CUSTOMER,
                    "PRODUCT": rt.PRODUCT,
                    "date": rt.date

                }
            )

        elif a >= 1.8 and a < 2.4:
            ar = [fs, fs, es, es, es]
            data.append(
                {
                    "Rating": ar,
                    "CUSTOMER": rt.CUSTOMER,
                    "PRODUCT": rt.PRODUCT,
                    "date": rt.date

                }
            )

        elif a >= 2.4 and a < 2.8:
            ar = [fs, fs, hs, es, es]
            data.append(
                {
                    "Rating": ar,
                    "CUSTOMER": rt.CUSTOMER,
                    "PRODUCT": rt.PRODUCT,
                    "date": rt.date

                }
            )
        elif a >= 2.8 and a < 3.4:
            ar = [fs, fs, fs, es, es]
            data.append(
                {
                    "Rating": ar,
                    "CUSTOMER": rt.CUSTOMER,
                    "PRODUCT": rt.PRODUCT,
                    "date": rt.date

                }
            )

        elif a >= 3.4 and a < 3.8:
            ar = [fs, fs, fs, hs, es]
            data.append(
                {
                    "Rating": ar,
                    "CUSTOMER": rt.CUSTOMER,
                    "PRODUCT": rt.PRODUCT,
                    "date": rt.date

                }
            )

        elif a >= 3.8 and a < 4.4:
            ar = [fs, fs, fs, fs, es]
            data.append(
                {
                    "Rating": ar,
                    "CUSTOMER": rt.CUSTOMER,
                    "PRODUCT": rt.PRODUCT,
                    "date": rt.date

                }
            )
        elif a >= 4.4 and a < 4.8:
            ar = [fs, fs, fs, fs, hs]
            data.append(
                {
                    "Rating": ar,
                    "CUSTOMER": rt.CUSTOMER,
                    "PRODUCT": rt.PRODUCT,
                    "date": rt.date

                }
            )

        elif a >= 4.8 and a <= 5.0:
            ar = [fs, fs, fs, fs, fs]
            data.append(
                {
                    "Rating": ar,
                    "CUSTOMER": rt.CUSTOMER,
                    "PRODUCT": rt.PRODUCT,
                    "date": rt.date

                }
            )
    return render(request,"Customer/view_rating.html",{"data":data})




def send_rating(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired,Login again !');window.location='/'</script>")
    return render(request,'Customer/send_rating.html',{"id":id})

def send_rating_post(request,id):
    rt = request.POST['star']
    ob = Rating()
    details = Rating.objects.filter(CUSTOMER__LOGIN=request.session['lid'])
    if details.exists():
        Rating.objects.filter(CUSTOMER__LOGIN=request.session['lid']).update(Rating=rt,date=datetime.datetime.now().date())
        return HttpResponse("<script>alert('Sended');window.location='/customer_view_product'</script>")
    else:
        ob.Rating = rt
        ob.CUSTOMER = customer.objects.get(LOGIN=request.session['lid'])
        ob.PRODUCT_id = id
        ob.date = datetime.datetime.now().date()
        ob.save()
        return HttpResponse("<script>alert('Sended');window.location='/customer_home'</script>")

