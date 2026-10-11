from rest_framework import serializers
from .models import CustomUser, Account, ExpenseCategory, IncomeCategory, Expense, Income


class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        val = attrs.get('email_or_username')
        pwd = attrs.get('password')
        
       
        user = CustomUser.objects.filter(email=val).first() or CustomUser.objects.filter(username=val).first()
        
        if user and user.check_password(pwd):
            if not user.is_active:
                raise serializers.ValidationError("Foydalanuvchi faol emas.")
            return {'user': user}
        raise serializers.ValidationError("Email/Username yoki parol xato.")

    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password', 'confirm_password']  # phone_number olib tashlandi

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Parollar mos kelmadi.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password')
        
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'balance']


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name']


class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ['id', 'name']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'account', 'category', 'amount', 'date', 'note']

    def validate(self, attrs):
        account = attrs.get('account')
        amount = attrs.get('amount')
        
        if account.balance < amount:
            raise serializers.ValidationError("Hisobda yetarli mablag' yo'q!")
        return attrs

    def create(self, validated_data):
        account = validated_data['account']
        amount = validated_data['amount']
        
        account.balance -= amount
        account.save()
        
        return super().create(validated_data)


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'account', 'category', 'amount', 'date', 'note']

    def create(self, validated_data):
        account = validated_data['account']
        amount = validated_data['amount']
        
        account.balance += amount
        account.save()
        
        return super().create(validated_data)