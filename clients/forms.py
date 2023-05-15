from django import forms
from django.forms import ModelForm
from .models import Client, Car, Services
from multiselectfield import MultiSelectFormField


# form Client
class ClientForm(ModelForm):
    
    firstName = forms.CharField(max_length=100, required=True)
    lastName = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=False)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    zipcode = forms.CharField(max_length=10, required=False)    
    
    brand = forms.CharField(max_length=50, required=True)
    model = forms.CharField(max_length=50, required=True)
    year = forms.IntegerField(required=True)
    
    class Meta:
        model = Client
        fields = '__all__'
        

# form Client
class UpdateClientForm(forms.ModelForm):    
    class Meta:
        model = Client
        fields = ['firstName', 'lastName', 'email', 'phone', 'address', 'city', 'state', 'zipcode']

        
# form Car        
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['license', 'brand', 'model', 'year', 'color', 'version', 'serieNumber', 'vin', 'engine', 'oil', 'traction', 'comments', 'image']
        widgets = {
            'id_client': forms.TextInput(attrs={'readonly': True}),
        }





# search client and cars
class SearchCarForm(forms.Form):
    car_id = forms.IntegerField(label='Car ID', widget=forms.TextInput(attrs={'class': 'form-control'}))
    

# new service
class NewServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['services', 'cost', 'description', 'status', 'mechanic', 'comments']
        widgets = {
            'services': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),            
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'mechanic': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# Search Client
class SearchClientForm(forms.ModelForm):
    firstName = forms.CharField(max_length=100, required=False)
    lastName = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(max_length=100, required=False)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = Client
        fields = ['firstName', 'lastName', 'email', 'phone']
        
        

