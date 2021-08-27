from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class CustomerTransaction(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    transaction_date = models.DateTimeField(auto_now_add=True, null=True)
    AmountGiven = models.IntegerField(null=True)
    AmountGot = models.IntegerField(null=True)

    def __str__(self):
        return str(self.customer)
