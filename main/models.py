from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class Portfolio(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class Investment(models.Model):
    # If the company deletes, then the investment should be protected
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="investments")
    shares = models.BigIntegerField()
    date_purchased = models.DateTimeField(null=True)
    price_purchased = models.DecimalField(max_digits=6, decimal_places=2)
