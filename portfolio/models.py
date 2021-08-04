from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

import requests

class CustomUser(AbstractUser):
    email = models.CharField(blank=False, max_length=200)
    customusername = models.CharField(blank=False, max_length=200)
    password = models.TextField(blank=False, max_length=200)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=50)
    def __str__(self):
        return self.username
    def _create_customuser(self, username, email, password,
                    phone, address, city, country):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        customuser = self.model(username=username, email=email, phone=phone,address=address,city=city, country=country)
        customuser.set_password(password)
        customuser.save(using=self._db)
        return customuser
    def create_customuser(self, username, email, password, phone, address, city, country):
        return self._create_user(self, username, email, password,
                    phone, address, city, country)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    cust_number = models.IntegerField(blank=False, null=False)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    cell_phone = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cust_number)


class Investment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='investments')
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    acquired_value = models.DecimalField(max_digits=10, decimal_places=2)
    acquired_date = models.DateField(default=timezone.now)
    recent_value = models.DecimalField(max_digits=10, decimal_places=2)
    recent_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def updated(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def results_by_investment(self):
        return self.recent_value - self.acquired_value

    def cust_number(self):
        return self.customer.cust_number


class Stock(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='stocks')
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    shares = models.DecimalField (max_digits=10, decimal_places=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def initial_stock_value(self):
        return self.shares * self.purchase_price

    def cust_number(self):
        return self.customer.cust_number

    # def current_stock_price(self):
    #     symbol_f = str(self.symbol)
    #     main_api = 'http://api.marketstack.com/v1/eod?'
    #     api_key = 'access_key=6843585e726a5236a46d7722a5844f9f&limit=1&symbols='
    #     url = main_api + api_key + symbol_f
    #     json_data = requests.get(url).json()
    #     open_price = float(json_data["data"][0]["open"])
    #     share_value = open_price
    #     return share_value
    #
    # def current_stock_value(self):
    #     return float(self.current_stock_price()) * float(self.shares)

class Fund(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='funds')
    fund_name = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    weeks_high_amt = models.DecimalField(max_digits=10, decimal_places=2)
    weeks_low_amt = models.DecimalField(max_digits=10, decimal_places=2)
    ex_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def initial_profit_value(self):
        return self.weeks_high_amt - self.weeks_low_amt



