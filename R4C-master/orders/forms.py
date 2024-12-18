from django import forms


class OrderForm(forms.Form):
    """Форма для создания заказа"""
    email = forms.EmailField()
    robot_serial = forms.CharField(max_length=5)
