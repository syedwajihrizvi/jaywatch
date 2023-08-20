from typing import Dict
from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

# Register your models here.


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ["customer", "date_created", "investments"]

    def investments(self, portfolio):
        url = reverse('admin:main_investment_changelist') + '?' + urlencode({
            'portfolio__id': str(portfolio.id)
        })
        return format_html('<a href="{}">Investments</a>', url)


@admin.register(models.Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ["company", "shares"]

    def get_model_perms(self, request):
        return {}
