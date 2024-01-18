from django.urls import path
from django.contrib.auth import views

from core.views import frontpage, signup, shop, myaccount, edit_myaccount
from product.views import product


urlpatterns=[
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('account/login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('account/', myaccount, name="account"),
    path('account/edit', edit_myaccount, name="edit_account"),


    path('shop/', shop, name='shop'),
    path('shop/<slug:slug>', product, name='product'),
]