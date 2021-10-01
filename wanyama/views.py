from django.shortcuts import (
    render, redirect, HttpResponse, get_list_or_404, 
    HttpResponseRedirect
)
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import *
from farmer.models import Farmer
from django.contrib import messages
from .forms import AnimalRegistrationForm, ExpenseIncomeForm


class HomeView(generic.TemplateView):
    template_name = 'wanyama_templates/home.html'


class AboutView(generic.TemplateView):
    template_name = 'wanyama_templates/about.html'


# Create your views here.
class IndexView(generic.ListView):
    template_name                   = 'wanyama_templates/index.html'
    model = Livestock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['cattles']      = Livestock.objects.filter(owner = self.request.user.farmer)
            context['animal_total'] = context['cattles'].count()
        except:
            messages.error(self.request,
            'you must register as a farmer')
        context['with_no_tag']      = Livestock.objects.filter(tag = None)
        return context


class CategoryWiseView(IndexView):
    template_name                   = 'wanyama_templates/index.html'
    model = Livestock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cat_id = Category.objects.get(title = self.kwargs['cat'])
            context['cattles']      = Livestock.objects.filter(owner = self.request.user.farmer, cartegory=cat_id)
            context['animal_total'] = context['cattles'].count()
        except:
            messages.error(self.request,
            'you must register as a farmer')
        context['with_no_tag']      = Livestock.objects.filter(tag = None)
        return context

class StatusWiseView(IndexView):
    model = Livestock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['cattles']      = Livestock.objects.filter(owner = self.request.user.farmer, status__icontains=self.kwargs['status'])
            context['animal_total'] = context['cattles'].count()
        except:
            messages.error(self.request,
            'you must register as a farmer')
        context['with_no_tag']      = Livestock.objects.filter(tag = None)
        return context


class GenderWiseView(IndexView):
    model = Livestock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['cattles']      = Livestock.objects.filter(owner = self.request.user.farmer, gender__icontains=self.kwargs['gender'])
            context['animal_total'] = context['cattles'].count()
        except:
            messages.error(self.request,
            'you must register as a farmer')
        context['with_no_tag']      = Livestock.objects.filter(tag = None)
        return context



class ExpensesView(generic.TemplateView):
    template_name                   = 'wanyama_templates/expenses.html'
    model = ExpenseIncome

    def get_context_data(self, **kwargs):
        context                     = super().get_context_data(**kwargs)
        context['ie_object']        = ExpenseIncome.objects.filter(farmer = self.request.user.farmer)
        context['with_no_tag']      = Livestock.objects.filter(tag = None)

        purchases = ExpenseIncome.objects.filter(ei_type = 'PURCHASES', farmer = self.request.user.farmer)
        sales = ExpenseIncome.objects.filter(ei_type = 'SALES', farmer = self.request.user.farmer)
        others = ExpenseIncome.objects.filter(ei_type = 'OTHERS', farmer = self.request.user.farmer)
 
        
        context['total_purchases'] = sum(purchases.values_list('amount', flat=True))
        context['total_sales'] = sum(sales.values_list('amount', flat=True))
        context['total_others'] = sum(others.values_list('amount', flat=True))
        return context


class AddExpensesView(generic.CreateView):
    template_name                   = 'wanyama_templates/add-expense.html'
    model                           = ExpenseIncome
    form_class                      = ExpenseIncomeForm
    success_url                     = reverse_lazy('wanyama:expenses')

    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class) 
        if form.is_valid():
            form.instance.farmer = request.user.farmer
            return self.form_valid(form)
        
        else:
            return self.form_invalid(form)



def deleteExpenses(request, pk):
    ExpenseIncome.objects.get(pk=pk).delete()
    return redirect('wanyama:expenses')


class EditExpenses(generic.UpdateView):
    template_name                   = 'wanyama_templates/edit-expense.html'
    model                           = ExpenseIncome
    form_class                      = ExpenseIncomeForm
    success_url                     = reverse_lazy('wanyama:expenses')


class EI_only(ExpensesView):
    template_name                   = 'wanyama_templates/expenses.html'
    model = ExpenseIncome

    def get_context_data(self, **kwargs):
        context                     = super().get_context_data(**kwargs)
        only_expense_income = self.kwargs['ei']
        context['ie_object']        = ExpenseIncome.objects.filter(farmer = self.request.user.farmer, ei_type = only_expense_income.upper())
        return context



class DetailedView(generic.DetailView):
    template_name                   = 'wanyama_templates/animal.html'
    model                           = Livestock
 
    def get_context_data(self, **kwargs):
        context                     = super().get_context_data(**kwargs)
        context['with_no_tag']      = Livestock.objects.filter(tag = None, owner=self.request.user.farmer)

        return context


class AddCattleView(generic.CreateView):
    template_name                   = 'wanyama_templates/add-animal.html'
    model                           = Livestock
    form_class                      = AnimalRegistrationForm
    success_url                     = reverse_lazy('wanyama:index')
    

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        farmer = Farmer.objects.get(user = request.user)
        if form.is_valid():
            form.instance.owner = farmer
            return self.form_valid(form)
        
        else:
            print('form is invalid')
            return self.form_invalid(form)


class UpdateAnimalDetailsView(generic.UpdateView):
    template_name                   = 'wanyama_templates/edit-animal.html'
    model                           = Livestock
    form_class                      = AnimalRegistrationForm


def deleteAnimalView(request, pk):
    livestock=Livestock.objects.get(pk=pk, owner=request.user.farmer)
    messages.info(request, 'livestock {livestock.livestock_name} deleted successfully')    
    livestock.delete()
    return redirect('wanyama:index')


def generateTagView(request, pk):
    livestock                       = Livestock.objects.get(pk=pk)
    Tag.objects.create(livestock=livestock)
    messages.info(request, 'generated tag for {livestock.livestock_name}')
    return redirect('wanyama:detailed', pk=pk)


def generateForAll(request):
    untaged = Livestock.objects.filter(tag = None, owner = request.user.farmer)
    for unt in untaged:
        livestock = Livestock.objects.get(pk=unt.pk)
        Tag.objects.create(livestock=livestock)
        
    messages.info(request, 'Tags generated for all with no tags')
    return redirect('wanyama:index')

