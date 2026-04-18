from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Order, OrderItem, Product


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['article', 'name', 'unit', 'price', 'manufacturer', 'supplier', 'cake_type', 'category', 'discount', 'stock', 'description', 'image']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}


class OrderForm(forms.ModelForm):
    items_text = forms.CharField(
        label='Состав заказа',
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Пример: T001C1,2\nT002F4,1'})
    )

    class Meta:
        model = Order
        fields = ['customer', 'status', 'pickup_point', 'order_date', 'delivery_date', 'pickup_code']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save_items(self, order: Order) -> None:
        order.items.all().delete()
        raw = self.cleaned_data.get('items_text', '').strip()
        if not raw:
            return
        for line in raw.splitlines():
            if not line.strip():
                continue
            article, quantity = [part.strip() for part in line.split(',')[:2]]
            OrderItem.objects.create(order=order, product=Product.objects.get(article=article), quantity=int(quantity))
