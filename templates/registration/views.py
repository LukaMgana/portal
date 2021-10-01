from django.http.response import HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views import generic
from .forms import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


# accessible as landing page, first time
class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.is_staff: 
                dish_obj = Dish.objects.get(user=self.request.user)        
                context['total_dishes'] = DishFood.objects.filter(dish=dish_obj).count()
        return context

# access home page with all data form database
class Home(generic.TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.is_staff: 
                dish_obj = Dish.objects.get(user=self.request.user)        
                context['total_dishes'] = DishFood.objects.filter(dish=dish_obj).count()
        if self.request.user.is_staff:
            context['allfoods'] = get_list_or_404(Food, canteen=self.request.user)
        else:
            context['allfoods'] = get_list_or_404(Food)
    
        context['allcategory'] = get_list_or_404(Menu)
        return context
    
    
    
class CategoryView(generic.TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        context['allcategory'] = get_list_or_404(Menu)
        try:
            menu = get_object_or_404(Menu, name=self.kwargs['menu'])
            context['allfoods'] = get_list_or_404(Food, menu=menu)
        except:
            messages.error(self.request, 'This Menu has no food yet')
        return context
     

@method_decorator(login_required, name='dispatch')
class ToDish(Home):    
    def post(self, request, **kwargs):
        if request.method=='POST':
            food_pk = self.kwargs['food']
        
            user = User.objects.get(id=request.user.pk)
            # print(user)
            # print(Dish.objects.filter(user=user).first())
            food = Food.objects.get(id=food_pk)
            # print(food)

            try:
                dish_obj = Dish.objects.get(user=user)
            except:
                dish_obj = Dish.objects.create(user=user)
            
            try:
                dishfood_obj = DishFood.objects.get(food=food, dish = dish_obj)
                messages.info(self.request, 'food already in dish')
            except:
                dishfood_obj = DishFood.objects.create(food=food, dish = dish_obj)
                messages.success(self.request, 'food added in dish')

        return  HttpResponseRedirect(reverse('home'))
    
    
@method_decorator(login_required, name='dispatch')
class PostFood(generic.CreateView): 
    template_name = 'sampuli.html'
    form_class = FoodPostForm  
    success_url = reverse_lazy('home')


    def post(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        canteen = User.objects.get(id=request.user.pk)
        if form.is_valid():
            print('daaah')
            form.instance.canteen = canteen
            messages.info(request, 'add fresh')
            return  self.form_valid(form)
            

        else:
            # print('Please enter valid food informations')
            return  HttpResponseRedirect(reverse('postfood'))
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FoodPostForm
        return context




class MyDish(generic.TemplateView):
    template_name = 'dishes.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        try:
            user = self.request.user
            dish_obj = Dish.objects.get(user=user)
            context['dishes'] = a = get_list_or_404(DishFood, dish=dish_obj)            
            context['total_dishes'] = DishFood.objects.filter(dish=dish_obj).count()
            # calculate total dish cost
            b = DishFood.objects.filter(dish=dish_obj)
            cost_list = []
            for cost in b:
                cost_list.append(cost.food.price)
            context['total_cost'] = sum(cost_list)
            context['dish_pk'] = dish_obj.pk
        except:
            messages.info(self.request, 'you have no dishes yet')
        return context
    
    
def deletefood(request, pk):
    Food.objects.get(pk=pk, canteen = request.user).delete()
    messages.info(request, 'food delete successfully')
    return HttpResponseRedirect(reverse('home'))


def removefood(request, pk):
    DishFood.objects.get(pk=pk).delete()
    messages.info(request, 'food removed successfully')
    return HttpResponseRedirect(reverse('dishes'))


class Checkout(generic.TemplateView):
    template_name = 'home.html'


class Register(generic.CreateView):
    form_class = CanteenRegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')
    
    def post(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.info(request, 'registered')
            return  self.form_valid(form)
            

        else:
            # print('Please enter valid food informations')
            return  HttpResponseRedirect(reverse('register'))
    
    
@method_decorator(login_required, name='dispatch')
class Myorder(generic.TemplateView):
    template_name = 'my-order.html'



@method_decorator(login_required, name='dispatch')
class OrderPlaced(generic.TemplateView):
    template_name = 'order-placed.html'

@method_decorator(staff_member_required, name='dispatch')
class StaffDashboard(generic.TemplateView):
    template_name='staff-dashboard.html'

    