from django.urls import path
from .views import *

app_name = 'wanyama'

urlpatterns = [
    path('', IndexView.as_view(), name= 'index'),

    path('detailed-<str:pk>/', DetailedView.as_view(), name='detailed'),
    path('add-cattle/', AddCattleView.as_view(), name='add-cattle'),
    path('generate-tag/<int:pk>/', generateTagView, name='generate-tag'),
    path('generate-tag/', generateForAll, name='all-tag'),

    path('<str:ei>-only/', EI_only.as_view(), name='only'),
    
    path('category-<str:cat>/', CategoryWiseView.as_view(), name='category'),
    path('<str:status>-livestock/', StatusWiseView.as_view(), name='statuswise'),
    
    path('livestock-<str:gender>/', GenderWiseView.as_view(), name='genderwise'),

    path('edit-animal/<int:pk>/', UpdateAnimalDetailsView.as_view(), name='edit'),
    path('delete-animal/<int:pk>/', deleteAnimalView, name='delete'),

    path('expenses/', ExpensesView.as_view(), name='expenses'),
    path('add-expenses/', AddExpensesView.as_view(), name='add-expenses'),
    path('delete-expenses/<int:pk>/', deleteExpenses, name='delete-expenses'),
    path('edit-expenses/<int:pk>/', EditExpenses.as_view(), name='edit-expenses'),

    path('home/', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),

]
