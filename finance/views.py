from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Account, Expense, Income
from .serializers import  RegisterSerializer, LoginSerializer,AccountSerializer, ExpenseSerializer, IncomeSerializer


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "detail": "Muvaffaqiyatli ro'yxatdan o'tildi!",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

class AccountViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        accounts = Account.objects.filter(user=request.user)
        return Response(AccountSerializer(accounts, many=True).data)
        
    def create(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

class ExpenseViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        expenses = Expense.objects.filter(user=request.user)
        return Response(ExpenseSerializer(expenses, many=True).data)
        
    def create(self, request):
        serializer = ExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

class IncomeViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        incomes = Income.objects.filter(user=request.user)
        return Response(IncomeSerializer(incomes, many=True).data)
        
    def create(self, request):
        serializer = IncomeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

class ReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        incomes = Income.objects.filter(user=request.user)
        expenses = Expense.objects.filter(user=request.user)
        
        total_inc = sum([i.amount for i in incomes])
        total_exp = sum([e.amount for e in expenses])

        return Response({
            "total_income": total_inc,
            "total_expense": total_exp,
            "net_balance": total_inc - total_exp
        })


class ExpenseDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    
    def put(self, request, pk):
        
        expense = get_object_or_404(Expense, pk=pk, account__user=request.user)
        
        
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Muvaffaqiyatli o'zgartirildi!",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk, account__user=request.user)
        expense.delete()
        
        return Response({
            "message": "Muvaffaqiyatli o'chirildi!"
        }, status=status.HTTP_204_NO_CONTENT)


class IncomeDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    
    def put(self, request, pk):
        income = get_object_or_404(Income, pk=pk, account__user=request.user)
        serializer = IncomeSerializer(income, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Kirim muvaffaqiyatli o'zgartirildi!",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
    def delete(self, request, pk):
        income = get_object_or_404(Income, pk=pk, account__user=request.user)
        income.delete()
        
        return Response({
            "message": "Kirim muvaffaqiyatli o'chirildi!"
        }, status=status.HTTP_204_NO_CONTENT)