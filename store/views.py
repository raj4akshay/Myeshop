from django.shortcuts import render, redirect
from .models import Product, Cart, Order, OrderItem, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


# Create your views here.
def get_all_categories(request):
    return {'categories': Category.objects.all()}


def get_cart_items_count(request):
    return {
        'cart_items_count': Cart.objects.filter(user_id=request.user.id).aggregate(Sum('quantity'))['quantity__sum']}


def search_view(request):
    return render(request, 'home.html', {'products': Product.objects.filter(name__icontains=request.GET['name'])})


def home_view(request):
    if 'cid' in request.GET:
        return render(request, 'home.html',
                      {'products': Product.objects.filter(category_id=request.GET['cid'])})
    else:
        return render(request, 'home.html', {'products': Product.objects.all()})


@login_required(login_url='login')
def add_to_cart_view(request):
    product = Product.objects.get(id=request.POST['productid'])
    if not Cart.objects.filter(product_id=request.POST['productid'], user_id=request.user.id).exists():
        cart = Cart()
        cart.product = product
        cart.user = request.user
        cart.quantity = 1
        cart.total = cart.quantity * product.price
        cart.save()
    else:
        cart = Cart.objects.get(product_id=request.POST['productid'], user_id=request.user.id)
        cart.quantity += 1
        cart.total = cart.quantity * product.price
        cart.save()
    return redirect('viewcart')


@login_required(login_url='login')
def cart_view(request):
    return render(request, 'cart.html',
                  {'is_any_cart_item': Cart.objects.filter(user_id=request.user.id).exists(),
                   'cart_items': Cart.objects.filter(user_id=request.user.id),
                   'grand_total': Cart.objects.filter(user_id=request.user.id).aggregate(Sum('total'))['total__sum']})


@login_required(login_url='login')
def remove_from_cart_view(request):
    cart = Cart.objects.get(product_id=request.POST['productid'], user_id=request.user.id)
    cart.delete()
    return redirect('viewcart')


@login_required(login_url='login')
def checkout_view(request):
    return render(request, 'checkout.html', {'amount_to_pay': request.POST['grandtotal']})


@login_required(login_url='login')
def place_order_view(request):
    order = Order()
    order.total = request.POST['grandtotal']
    order.address = request.POST['address']
    order.phone_number = request.POST['phonenumber']
    order.user = request.user
    order.save()

    cart_items = Cart.objects.filter(user_id=request.user.id)
    for cart_item in cart_items:
        order_item = OrderItem()
        product = Product.objects.get(id=cart_item.product_id)
        order_item.quantity = cart_item.quantity
        order_item.price = cart_item.product.price
        order_item.total = cart_item.total
        order_item.order = order
        order_item.product = product
        order_item.user = request.user
        order_item.save()
        cart_item.delete()

    return redirect('vieworders')


def view_orders(request):
    return render(request, 'orders.html', {
        'is_any_order': Order.objects.filter(user_id=request.user.id).exists(),
        'orders': Order.objects.filter(user_id=request.user.id).order_by('-date'),
        'orders_items': OrderItem.objects.filter(user_id=request.user.id)
    })
