from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    def __str__(self):
        return self.username

class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100) 
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} - {self.balance}"

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class IncomeCategory(models.Model):
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.CharField(max_length=100) 
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True, null=True)

class Income(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.CharField(max_length=100) 
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True, null=True)

