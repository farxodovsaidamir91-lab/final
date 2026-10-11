from django.urls import path
from .views import RegisterView, LoginView,AccountViewSet, ExpenseViewSet, IncomeViewSet, ReportView, ExpenseDetailAPIView, IncomeDetailAPIView


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),

    path('accounts/', AccountViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('expenses/', ExpenseViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('incomes/', IncomeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reports/', ReportView.as_view()),
    path('expenses/<int:pk>/', ExpenseDetailAPIView.as_view(), name='expense-detail'),
    path('incomes/<int:pk>/', IncomeDetailAPIView.as_view(), name='income-detail'),
]