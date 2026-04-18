from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import LoginForm, OrderForm, ProductForm
from .mixins import role_required
from .models import Order, OrderStatus, Product, Supplier


class CakeLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        messages.success(self.request, 'Вход выполнен успешно.')
        return super().form_valid(form)


def _catalog_queryset(request, guest: bool = False):
    products = Product.objects.select_related('category', 'cake_type', 'manufacturer', 'supplier').all()

    query = request.GET.get('q', '').strip()
    supplier = request.GET.get('supplier', '').strip()
    sort = request.GET.get('sort', '').strip()

    if not guest and query:
        products = products.filter(
            Q(article__icontains=query)
            | Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(cake_type__name__icontains=query)
            | Q(manufacturer__name__icontains=query)
            | Q(supplier__name__icontains=query)
        )

    if not guest and supplier:
        products = products.filter(supplier_id=supplier)

    if not guest:
        if sort == 'stock_asc':
            products = products.order_by('stock', 'name')
        elif sort == 'stock_desc':
            products = products.order_by('-stock', 'name')

    return products, query, supplier, sort


def guest_view(request):
    products, query, supplier, sort = _catalog_queryset(request, guest=True)
    return render(request, 'shop/catalog.html', {
        'products': products,
        'is_guest': True,
        'query': query,
        'supplier_value': supplier,
        'sort_value': sort,
        'suppliers': Supplier.objects.all(),
    })


def catalog_view(request):
    guest = not request.user.is_authenticated
    products, query, supplier, sort = _catalog_queryset(request, guest=guest)
    return render(request, 'shop/catalog.html', {
        'products': products,
        'is_guest': guest,
        'query': query,
        'supplier_value': supplier,
        'sort_value': sort,
        'suppliers': Supplier.objects.all(),
    })


@role_required('admin')
def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Товар успешно добавлен.')
        return redirect('catalog')
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Добавление товара'})


@role_required('admin')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    form.fields['article'].disabled = True
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Товар успешно обновлен.')
        return redirect('catalog')
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Редактирование товара', 'product': product})


@role_required('admin')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.order_items.exists() or product.related_products.filter(order_items__isnull=False).exists():
        messages.error(request, 'Товар нельзя удалить: он используется в заказах.')
    else:
        product.related_products.clear()
        product.delete()
        messages.success(request, 'Товар удален.')
    return redirect('catalog')


@login_required
def orders_view(request):
    role = request.user.profile.role
    if role not in {'client', 'manager', 'admin'}:
        messages.error(request, 'Недостаточно прав для просмотра заказов.')
        return redirect('catalog')

    orders = Order.objects.select_related('customer', 'status', 'pickup_point').prefetch_related('items__product')
    if role == 'client':
        orders = orders.filter(customer=request.user.profile)

    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    sort = request.GET.get('sort', '').strip()

    if query:
        orders = orders.filter(
            Q(customer__full_name__icontains=query)
            | Q(pickup_point__address__icontains=query)
            | Q(status__name__icontains=query)
            | Q(pk__icontains=query)
        )

    if status:
        orders = orders.filter(status_id=status)

    if sort == 'pickup_asc':
        orders = orders.order_by('pickup_point__address', 'pk')
    elif sort == 'pickup_desc':
        orders = orders.order_by('-pickup_point__address', 'pk')

    return render(request, 'shop/orders.html', {
        'orders': orders,
        'statuses': OrderStatus.objects.all(),
        'query': query,
        'status_value': status,
        'sort_value': sort,
        'role': role,
    })


@role_required('admin')
def order_create(request):
    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = form.save()
        form.save_items(order)
        messages.success(request, 'Заказ добавлен.')
        return redirect('orders')
    return render(request, 'shop/order_form.html', {'form': form, 'title': 'Добавление заказа'})


@role_required('admin')
def order_update(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items'), pk=pk)
    initial = {'items_text': '\n'.join(f'{item.product.article},{item.quantity}' for item in order.items.all())}
    form = OrderForm(request.POST or None, instance=order, initial=initial)
    if request.method == 'POST' and form.is_valid():
        order = form.save()
        form.save_items(order)
        messages.success(request, 'Заказ обновлен.')
        return redirect('orders')
    return render(request, 'shop/order_form.html', {'form': form, 'title': 'Редактирование заказа', 'order': order})


@role_required('admin')
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    messages.success(request, 'Заказ удален.')
    return redirect('orders')
