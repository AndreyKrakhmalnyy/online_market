from django import forms

class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = ()
    delivery_address = forms.BooleanField(required=False)
    payment_on_get = forms.CharField()
    
    