from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import auth
import datetime
from django.http import HttpResponse
from django.http import JsonResponse
import json
# Create your views here.
# def index(request):
#     if request.user.is_authenticated:
#         customer = request.user.customer 
#         order,created=Order.objects.get_or_create(customer=customer,complete=False)
#         cart=order.orderitem_set.all()
#         cartItems = order.get_cart_items if 'order' in locals() else 0

#     else:
#         items=[]
#         order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
#         cartItems=order['get_cart_items']
#     items = Item.objects.all()
#     Staff = staff.objects.all() 
#     return render(request, 'index.html',  {'items': items, 'staff': Staff,'cartItems':cartItems})

def index(request):
    cartItems = 0  # Default value
    
    if request.user.is_authenticated:
        try:
            customer = request.user.customer  # Ensure user has a customer profile
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cartItems = order.get_cart_items
        except Exception as e:
            print("Error fetching cart items:", e)
            cartItems = 0  # Prevent infinite recursion

    items = Item.objects.all()
    staff_members = staff.objects.all()  # Avoid conflicts with class name

    return render(request, 'index.html', {'items': items, 'staff': staff_members, 'cartItems': cartItems})

def menu(request):
    items = Item.objects.all()
    return render(request, 'menu.html', {'items': items})
def cart(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer  # Ensure the customer exists
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cart = order.orderitem_set.all()
        except Customer.DoesNotExist:
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cart = []
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart = []
    
    return render(request, 'cart.html', {'cart': cart, 'order': order})

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        cart=order.orderitem_set.all()
    else:

        cart=[]
        order={'get_cart_total':0,'get_cart_items':0}
    #context={'cart'=items}
    return render(request, 'checkout.html',{'cart':cart,'order':order,'shipping':False})
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem, Item  # Import your models

def updateItem(request):
    try:
        data = json.loads(request.body)  # Load JSON data from request body
        productId = data.get('productId')
        action = data.get('action')

        print('Action:', action)
        print('Product ID:', productId)

        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not logged in'}, status=401)

        # Get customer profile
        customer = getattr(request.user, 'customer', None)
        if customer is None:
            return JsonResponse({'error': 'Customer profile missing'}, status=400)

        # Get product
        product = get_object_or_404(Item, id=productId)

        # Get or create order
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # Get the existing order item (Fixed: Avoid multiple objects error)
        orderItem = OrderItem.objects.filter(order=order, product=product).first()

        if orderItem:
            # Update quantity
            if action == 'add':
                orderItem.quantity += 1
            elif action == 'remove':
                orderItem.quantity -= 1
            orderItem.save()

            # Remove item if quantity is 0
            if orderItem.quantity <= 0:
                orderItem.delete()
        else:
            # Create a new order item if it doesn't exist and action is 'add'
            if action == 'add':
                orderItem = OrderItem.objects.create(order=order, product=product, quantity=1)

        return JsonResponse({'message': 'Item updated successfully'}, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def processOrder(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received Data:", data)  # Debugging line

            transaction_id = datetime.datetime.now().timestamp()
            if request.user.is_authenticated:
                customer = request.user.customer
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
                total = float(data['form']['total'])

                if total == float(order.get_cart_total):
                    order.complete = True
                    order.transaction_id = transaction_id
                    order.save()

                return JsonResponse({'message': 'Payment completed'}, status=200)
            
            return JsonResponse({'error': 'User not logged in'}, status=403)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
def contact(request):
    return render(request, 'contact.html')
def service(request):
    return render(request, 'service.html')
def testimonial(request):
    return render(request, 'testimonial.html')
def about(request):
    return render(request, 'about.html')
def team(request):
    return render(request, 'team.html')
@login_required
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Link booking to logged-in user
            booking.email = request.user.email  # Auto-fill email
            booking.save()
            return redirect('success')  # Ensure 'success' URL is defined
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})
def success(request):
    return render(request, 'success.html')
@login_required
def my_table(request):
    tables = Booking.objects.filter(user=request.user)
    return render(request, 'my_table.html', {'tables': tables})
def logout(request):
    auth.logout(request)
    return redirect('index')  # Redirect to the homepage or any desired page after logout