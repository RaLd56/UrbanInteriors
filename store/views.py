from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, CustomUserCreationForm, EmployeeLogin, AddGoodForm, DeleteGoodForm, SearchQuery
from django.contrib import messages
from store.models import Key, Good, Order, OrderItem
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse


def in_employee_group(user):
    return user.groups.filter(name='employee_group').exists()

def store(request):

    just_in_items = Good.objects.all().reverse()[:9]

    login_form = LoginForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('store')  # Перенаправление после успешного входа
                else:
                    messages.error(request, 'There is no such user') 
    else:
        login_form = LoginForm()

    return render(request, 'store/store.html', {
        'login_form': login_form, 'just_in_items': just_in_items
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')  # Перенаправление на страницу входа после успешной регистрации
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'store/register.html', {'form': form})


@login_required
def profile(request):
    is_in_group = request.user.groups.filter(name='employee_group').exists()
    cart_items = OrderItem.objects.filter(order__user=request.user, order__status='PENDING')
    order, created = Order.objects.get_or_create(user=request.user, status='PENDING')
    order.update_total_price()
    total_price = order.total_price
    return render(request, 'store/profile.html', {'is_in_group': is_in_group, 'cart_items': cart_items, 'total_price': total_price})

@login_required
def employee(request):
    if request.method == 'POST':
        form = EmployeeLogin(request.POST)
        if form.is_valid():
            key = form.cleaned_data['employee_key']
            if key == str(Key.objects.get(id=1)):
                employee_group, created = Group.objects.get_or_create(name='employee_group')
                request.user.groups.add(employee_group)
            return redirect('employee_panel') 
    else:
        form = EmployeeLogin()
    return render(request, 'store/employee.html', {'form': form})

@user_passes_test(in_employee_group)
def employee_panel(request):
    return render(request, 'store/employee_panel.html')

@user_passes_test(in_employee_group)
def add_good(request):
    if request.method == 'POST':
        form = AddGoodForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()  
            messages.success(request, 'A good was succesfully added')
            return redirect('employee_panel')  
    else:
        form = AddGoodForm()

    return render(request, 'store/add_good.html', {'form': form})

@user_passes_test(in_employee_group)
def delete_good(request):
    goods = [str(good) for good in Good.objects.all()]

    if request.method == 'POST':
        form = DeleteGoodForm(request.POST)
        if form.is_valid():
            name_to_delete = form.cleaned_data['name']
            try:
                good = Good.objects.get(name=name_to_delete)
                good.delete()  
                messages.success(request, 'A good was successfully deleted')
                return redirect('employee_panel')
            except Good.DoesNotExist:
                messages.error(request, 'There is no such item')
    else:
        form = DeleteGoodForm()

    return render(request, 'store/delete_good.html', {'form': form, 'goods': goods})




@user_passes_test(in_employee_group)
def report(request):
    return render(request, 'store/report.html')

def product_detail(request, id):
    product = get_object_or_404(Good, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

def category(request, category_name):
    category_items = Good.objects.all().filter(category=category_name, stock__gt=0)
    return render(request, 'store/category.html', { 'category_name': category_name, 'category_items': category_items })

@login_required
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            product = Good.objects.get(id=product_id)
        except Good.DoesNotExist:
            return JsonResponse({'status': 'failed', 'message': 'Product not found'}, status=404)
        
        order, created = Order.objects.get_or_create(user=request.user, status='PENDING')
        
        try:
            order_item = OrderItem.objects.get(order=order, product=product)
            order_item.quantity += quantity
        except OrderItem.DoesNotExist:
            order_item = OrderItem(order=order, product=product, quantity=quantity, price=product.price)
        
        # Сохраняем OrderItem
        order_item.save()

        # Обновляем общую стоимость заказа
        order.update_total_price()

        return JsonResponse({'status': 'success', 'order_total': order.total_price, 'item_count': order.items.count()})
    
    return JsonResponse({'status': 'failed'}, status=400)

@login_required
def update_cart_item(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        order = Order.objects.get(user=request.user, status='PENDING')
        
        item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__status='PENDING')
        
        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease':
            if item.quantity > 1:
                item.quantity -= 1
        
        item.save()
        order.update_total_price()
        
        response_data = {
            'status': 'success',
            'new_quantity': item.quantity,
            'total_price': order.total_price
        }
        
        return JsonResponse(response_data)
    return JsonResponse({'status': 'failed'}, status=400)

@login_required
def delete_cart_item(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        item_id = request.POST.get('item_id')
        order = Order.objects.get(user=request.user, status='PENDING')
        
        item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__status='PENDING')
        item.delete()
        order.update_total_price()
        
        response_data = {
            'status': 'success',
            'total_price': order.total_price
        }
        
        return JsonResponse(response_data)
    return JsonResponse({'status': 'failed'}, status=400)


def search(request):
    form = SearchQuery(request.GET or None)
    results =[]

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Good.objects.filter(name__icontains=query)  # Поиск по полю name

    return render(request, 'search_results.html', {'form': form, 'results': results})
