from django import forms
from order.models import BillingAddress, Payment_details

country_choice = [
        ('ban', 'Bangladesh'),
        ('usa', 'United States'),
        ('uk', 'United Kingdom'),        
        ('ger', 'Germany'),
        ('fra', 'France'),
        ('ind', 'India'),
        ('aus', 'Australia'),
        ('bra', 'Brazil'),
        ('can', 'Canada'),
    ]


class BillingForm(forms.ModelForm):    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = BillingAddress
        fields = ['first_name', 'last_name', 'company_name', 'country', 'address', 'postcode', 'city', 'province', 'phone_no', 'email']
        widgets= {'country': forms.Select(choices=country_choice)}

    # country = forms.ChoiceField(choices=[
    #     ('usa', 'United States'),
    #     ('uk', 'United Kingdom'),
    #     ('ger', 'Germany'),
    #     ('fra', 'France'),
    #     ('ind', 'India'),
    #     ('aus', 'Australia'),
    #     ('bra', 'Brazil'),
    #     ('can', 'Canada'),
    # ], widget=forms.Select(attrs={'class': 'form-control'}))



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment_details
        fields = '__all__'

  