from django.shortcuts import render

from rest_framework.mixins import (
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin
)

from rest_framework.decorators import action

from rest_framework.response import Response

from rest_framework.viewsets import (
    ModelViewSet,
    GenericViewSet
)

from rest_framework.permissions import IsAuthenticated

from .serializers import (
    PortfolioSerializer,
    CreatePortfolioSerializer,
    InvestmentSerializer,
    CompanySerializer,
    CustomerSerializer
)

from .models import (
    Portfolio,
    Investment,
    Company,
    Customer
)

from .tasks import portfolio_analysis


class InvestmentViewSet(ModelViewSet):
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Investment.objects.filter(portfolio_id=self.kwargs['portfolio_pk'])

    def get_serializer_context(self):
        return {'portfolio_id': self.kwargs['portfolio_pk']}


class PortfolioViewSet(CreateModelMixin,
                       RetrieveModelMixin,
                       ListModelMixin,
                       DestroyModelMixin,
                       GenericViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        customer_id = Customer.objects.get(user_id=user_id)
        return Portfolio.objects.filter(customer_id=customer_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePortfolioSerializer
        return PortfolioSerializer

    @action(detail=True)
    def analyse(self, request, pk):
        portfolio = Portfolio.objects.get(id=pk)
        serializer = PortfolioSerializer(portfolio)
        portfolio_analysis.delay(serializer.data)
        print("Found")
        return Response(serializer.data)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


class CustomerViewSet(CreateModelMixin,
                      RetrieveModelMixin,
                      DestroyModelMixin,
                      GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        customer = Customer.objects.get(user=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
