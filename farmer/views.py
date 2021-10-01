from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from wanyama.models import *
from .models import *
from django.contrib.auth.models import User

from .forms import FarmerRegisterForm

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'wanyama_templates/home.html'
    

class RegisterView(generic.CreateView):
    template_name = 'registration/registration.html'
    form_class = FarmerRegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        farmer = Farmer.objects.create(user=user)
        farmer.email = user.email
        return super().form_valid(form)


class FarmerRegisterView(generic.CreateView):
    form_class = FarmerRegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')
    
    def post(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        if form.is_valid():
            form.instance.first_name = first_name
            form.instance.last_name = last_name
            form.instance.email = email
            messages.info(self.request, "{first_name}'s proflie created successfully")
            return  self.form_valid(form)
            

        else:
            # print('Please enter valid food informations')
            return  HttpResponseRedirect(reverse('farmer:register'))
    



class FarmerProfileView(generic.TemplateView):
    template_name = 'farmer_templates/farmer_profile.html'


class EditProfileView(generic.UpdateView):
    template_name = 'farmer_templates/edit-profile.html'
    model = User

    def get_object(self, *args, **kwargs):
        id = User.objects.get(username = self.kwargs['user'])
        return User.objects.get(pk=id.pk)
