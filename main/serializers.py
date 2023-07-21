from rest_framework import serializers

from .models import Portfolio, Investment, Company, Customer


class InvestmentSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField('get_company_name')

    class Meta:
        model = Investment
        fields = ['company', 'company_name', 'shares']

    def get_company_name(self, investment):
        return investment.company.name

    def create(self, validated_data):
        portoflio_id = self.context['portfolio_id']
        return Investment.objects.create(portfolio_id=portoflio_id, **validated_data)


class InvestmentInPorfolioSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField('get_company_name')
    company_symbol = serializers.SerializerMethodField('get_company_symbol')

    class Meta:
        model = Investment
        fields = ['company', 'company_name', 'company_symbol', 'shares']

    def get_company_name(self, investment):
        return investment.company.name

    def get_company_symbol(self, investment):
        return investment.company.symbol


class CreatePortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = ["customer"]


class PortfolioSerializer(serializers.ModelSerializer):
    investments = InvestmentInPorfolioSerializer(many=True)

    class Meta:
        model = Portfolio
        fields = ['customer', 'investments']


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)
    symbol = serializers.CharField(max_length=30)

    class Meta:
        model = Company
        fields = ["name", "symbol"]


class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField('get_first_name')
    last_name = serializers.SerializerMethodField('get_last_name')

    class Meta:
        model = Customer
        fields = ['user', 'first_name', 'last_name', 'birth_date']

    def get_first_name(self, customer):
        return customer.user.first_name

    def get_last_name(self, customer):
        return customer.user.last_name
