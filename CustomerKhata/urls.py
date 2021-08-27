from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('validate_otp/', views.validateOTP, name="validate_otp"),
    path('', views.home, name="home"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('add_transaction/<str:pk>/', views.add_transaction, name="add_transaction"),
    path('add_customer/', views.Add_Customer, name="add_customer"),
    path('add_Customer_form_submission/', views.Add_Customer_form_submission, name="Add_Customer_form_submission"),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    path('transaction_pdf_view/<str:pk>/', views.ViewtransactionPDF.as_view(), name="transaction_pdf_view"),
    path('transaction_pdf_download/<str:pk>/', views.DownloadtransactionPDF.as_view(), name="transaction_pdf_download"),

]
