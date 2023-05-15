from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from django.core.files.storage import default_storage

from .forms import *
from .models import Client, Car, Services
from django.conf import settings
from decimal import Decimal


#pdf generator
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def index(request):
    return render(request, 'clients/index.html')


def home(request):
    return render(request, 'clients/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Reemplaza 'home' con la URL a la que quieres redirigir después del inicio de sesión exitoso.
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'clients/index.html')  # Reemplaza 'login.html' con la plantilla de inicio de sesión que quieras utilizar.


def logout_view(request):
    logout(request)
    return redirect('index')


def client_list(request):
    clients = Client.objects.all()
    cars = Car.objects.all()
    form = SearchClientForm()
    return render(request, 'clients/client_list.html', {'clients': clients, 'cars': cars, 'form': form})


def client_detail(request, id_client):
    client = get_object_or_404(Client, pk=id_client)
    cars = Car.objects.filter(id_client=client)
    services = Services.objects.filter(id_client=client)
    return render(request, 'clients/client_detail.html', {'client': client, 'cars': cars, 'services': services})



# Create client
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            # Extract client data from form
            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            
            # Search for client with matching email and phone number
            query = Q(email__exact=email.strip()) | Q(phone__exact=phone.strip())
            existing_client = Client.objects.filter(query).first()
            
            if existing_client:
                # Client already exists, show error message
                form.add_error('email', 'Client with this email/phone already exists.')
            else:
                # Client doesn't exist, save client and car data to the database
                client = form.save()
                car = Car(
                    id_client=client,
                    brand=form.cleaned_data['brand'],
                    model=form.cleaned_data['model'],
                    year=form.cleaned_data['year']
                )
                car.save()
                
                # Redirect to home page
                return render(request, 'clients/home.html', {'form': form})
    else:
        form = ClientForm()
    
    # Render registration page with form
    return render(request, 'clients/register.html', {'form': form})



# Search client
def search_client(request):
    if request.method == 'POST':
        form = SearchClientForm(request.POST)
        if form.is_valid():
            # Extract search parameters from form
            first_name = form.cleaned_data.get('firstName')
            last_name = form.cleaned_data.get('lastName')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            # Create query using Q objects for each parameter
            query = Q()
            if first_name:
                query |= Q(firstName__icontains=first_name.strip())
            if last_name:
                query |= Q(lastName__icontains=last_name.strip())
            if email:
                query |= Q(email__exact=email.strip())
            if phone:
                query |= Q(phone__exact=phone.strip())

            # Search for clients matching the query
            clients = Client.objects.filter(query)

            # Create a list to store clients and their associated cars
            clients_with_cars = []
            client_car_ids = []

            # Loop through all clients and get the associated car
            for client in clients:
                try:
                    car = Car.objects.get(id_client=client)
                    clients_with_cars.append((client, car))
                    client_car_ids.append((client.id_client, car.id_car))  # Add client and car IDs to the list
                except Car.DoesNotExist:
                    pass

            return render(request, 'clients/client_list.html', {'form': form, 'clients_with_cars': clients_with_cars, 'client_car_ids': client_car_ids})

    else:
        form = SearchClientForm()
        # If no search parameters are provided, show all clients
        clients = Client.objects.all()
        clients_with_cars = []
        client_car_ids = []

    # Loop through all clients and get the associated car
    for client in clients:
        try:
            car = Car.objects.get(id_client=client)
            clients_with_cars.append((client, car))
            client_car_ids.append((client.id_client, car.id_car))  # Add client and car IDs to the list
        except Car.DoesNotExist:
            pass

    return render(request, 'clients/client_list.html', {'form': form, 'clients_with_cars': clients_with_cars, 'client_car_ids': client_car_ids})





def update_client(request, id_client):
    # Obtener el cliente correspondiente
    try:
        client = Client.objects.get(id_client=id_client)              
    
    except Client.DoesNotExist:
        return HttpResponseNotFound('Client not found')
    
    formClient = UpdateClientForm(instance=client)
      
    context = {
        'formClient': formClient,
        'client': client,      
    }
    
    if request.method == 'POST':
       
        formClient = UpdateClientForm(request.POST, instance=client)              
                
        if formClient.is_valid():
            
            formClient.save()
                        
            # Redirigir al usuario a la página de detalles del cliente actualizado
            return redirect('client_detail', id_client=id_client)
    
    return render(request, 'clients/update_client.html', context)




def update_car(request, id_client):
    # Obtener el cliente correspondiente
    try:
        client = Client.objects.get(id_client=id_client)
    except Client.DoesNotExist:
        return HttpResponseNotFound('Client not found')
    
    car = Car.objects.get(id_client=client)
    formCar = CarForm(instance=car)
    context = {
        'formCar': formCar,
        'client': client,
        'car': car,
    }
    
    if request.method == 'POST':
        formCar = CarForm(request.POST, request.FILES, instance=car)
        if formCar.is_valid():
            car = formCar.save(commit=False)
            if 'image' in request.FILES:
                image = request.FILES['image']
                try:
                    width, height = get_image_dimensions(image)
                except AttributeError:
                    raise ValidationError("Invalid image format")
                
                if width > 2000 or height > 2000:
                    return HttpResponseBadRequest('Image dimensions too large')
                
                if image.size > 5 * 1024 * 1024:
                    return HttpResponseBadRequest('Image size too large')
                
                car.image = image
                # Guardar la imagen en el sistema de archivos
                file_path = f'image/{car.id_car}/{image.name}'
                default_storage.save(file_path, image)
            
            car.save()
            # Redirigir al usuario a la página de detalles del cliente actualizado
            return redirect('client_detail', id_client=id_client)
    
    return render(request, 'clients/update_car.html', context)



def car_detail(request, id_client):
    # Obtener el cliente correspondiente
    try:
        client = Client.objects.get(id_client=id_client)              
    
    except Client.DoesNotExist:
        return HttpResponseNotFound('Client not found')
    
    car = Car.objects.get(id_client=client)
    
      
    context = {        
        'client': client, 
        'car': car          
    }
    return render(request, 'clients/car_detail.html', context)


def search_car(request):
    if request.method == 'POST':
        form = SearchCarForm(request.POST)
        if form.is_valid():
            car_id = form.cleaned_data['car_id']
            try:
                car = Car.objects.get(id_car=car_id)
                request.session['car_id'] = car.id_car
                request.session['client_id'] = car.id_client.id_client
                return redirect('new_service')
            except Car.DoesNotExist:
                form.add_error('car_id', 'Car not found')
    else:
        form = SearchCarForm()
    return render(request, 'clients/search_car.html', {'form': form})




# Ok
def create_service(request, id_client):
    
    client = get_object_or_404(Client, pk=id_client)
    car = Car.objects.get(id_client=client)
    
    if request.method == 'POST':
        
        form = NewServiceForm(request.POST)
        
        if form.is_valid():
            # Crear un nuevo objeto Services utilizando los datos del formulario y el ID del cliente
            service = form.save(commit=False)
            service.id_car = car
            service.id_client = client
            service.save()
            
            # Mostrar un mensaje de confirmación al usuario
            messages.success(request, 'Service created successfully.')
            
            return redirect('client_detail', id_client=id_client)

           
    else:
        form = NewServiceForm()
    
    return render(request, 'clients/create_service.html', {'form': form, 'client': client, 'car': car})



#view services



def services_view(request):
    services = Services.objects.all().select_related('id_client')
    context = {'services': services}
    return render(request, 'clients/services_view.html', context)




#view client services

def view_client_service(request, id_service):
    service = get_object_or_404(Services, id_service=id_service)
    car_instance = service.id_car
    client_instance = service.id_client
    services_list = ', '.join(service.services)
    form = NewServiceForm(request.POST or None, instance=service)
    
    GST_cost = service.GST_cost()
    QST_cost = service.QST_cost()
    
    total_cost = service.total_cost()
    
    context = {
        'form': form,
        'service': service,
        
        'services': services_list,
        
        'car_instance': car_instance,
        'client_instance': client_instance,        
        'TAX_GST': GST_cost,
        'TAX_QST': QST_cost ,
        'total_cost': total_cost,
        
        # constants taxes settings
        'tax_gst': (Decimal(settings.TAX_GST) * 100).quantize(Decimal('0.01')),
        'tax_qst': (Decimal(settings.TAX_QST) * 100).quantize(Decimal('0.01'))
    }
    return render(request, 'clients/view_client_service.html', context)






def update_service(request, id_service):
    service = get_object_or_404(Services, id_service=id_service)
    form = NewServiceForm(request.POST or None, instance=service)
    car_instance = service.id_car
    client_instance = service.id_client
    if form.is_valid():
        form.save()
        messages.success(request, f'Service {service.id_service} updated successfully')
        return redirect('client_list')
    context = {'form': form, 'service': service, 'id_service': id_service, 'car_instance': car_instance, 'client_instance': client_instance}
    return render(request, 'clients/update_service.html', context)




from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from xhtml2pdf import pisa
from io import BytesIO


def generate_pdf(request, id_service):
    service = get_object_or_404(Services, id_service=id_service)
    car_instance = service.id_car
    client_instance = service.id_client
    services_list = ', '.join(service.services)
    
    GST_cost = service.GST_cost()
    QST_cost = service.QST_cost()
    
    total_cost = service.total_cost()
    
    context = {
        'service': service,
        'services': services_list,
        'car_instance': car_instance,
        'client_instance': client_instance,
        'TAX_GST': GST_cost,
        'TAX_QST': QST_cost,
        'total_cost': total_cost,
    }
    
    template = get_template('clients/view_client_service.html')
    html = template.render(context)
    
    # Create a byte buffer to receive PDF data.
    buffer = BytesIO()
    
    # Create the PDF object, using the buffer as its "file."
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), buffer)
    
    # Use the content-disposition attachment to specify the filename.
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="service_{}.pdf"'.format(id_service)
    
    return response



def generate_pdf1(request, id_service):
    service = get_object_or_404(Services, id_service=id_service)
    car_instance = service.id_car
    client_instance = service.id_client
    services_list = ', '.join(service.services)
    
    GST_cost = service.GST_cost()
    QST_cost = service.QST_cost()
    
    total_cost = service.total_cost()
    
    context = {
        'service': service,
        'services': services_list,
        'car_instance': car_instance,
        'client_instance': client_instance,        
        'TAX_GST': GST_cost,
        'TAX_QST': QST_cost ,
        'total_cost': total_cost,
    }
    
    # Renderizamos la plantilla del PDF con los datos del contexto
    template = get_template('clients/view_client_service.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="service_{}.pdf"'.format(service.id_service)
    # Generamos el PDF a partir del HTML renderizado
    pisa_status = pisa.CreatePDF(html, dest=response)
    # Si el PDF se generó correctamente, lo devolvemos
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: {}'.format(pisa_status.err))
    return response
