from rest_framework import serializers
from rest_framework import permissions
from django.contrib.auth.models import User

from .models import (
    Stock,
    Option,
    FinancialCalculator,
    Strategy,
    ProbabilityOfProfit,
)

# Serializers

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
    
    def create(self, validated_data):
        return Stock.objects.create(**validated_data)

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

    def create(self, validated_data):
        return Option.objects.create(**validated_data)

class FinancialCalculatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialCalculator
        fields = '__all__'

    def create(self, validated_data):
        return FinancialCalculator.objects.create(**validated_data)

class StrategySerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Strategy
        fields = '__all__'

    def create(self, validated_data):
        return Strategy.objects.create(**validated_data)
    
class ProbabilityOfProfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbabilityOfProfit
        fields = '__all__'
    
    def create(self, validated_data):
        return ProbabilityOfProfitSerializer.objects.create(**validated_data)

# User Serializer has Hyperlink endpoint
class UserSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    strategies = serializers.HyperlinkedIdentityField(many=True, view_name='strategy-detail')

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'strategies']

"""from rest_framework import serializers
from rest_framework import permissions

from .models import Strategy

# NOTE Not Hyperlinked: class StrategySerializer(serializers.ModelSerializer):
class StrategySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    pinned = serializers.HyperlinkedIdentityField(view_name='strategy-pinned', format='html')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Strategy
        fields = ['url', 'id', 'pinned', 'title', 'action_type', 
                      'strike', 'premium', 'n', 'action', 'owner']

    def create(self, validated_data):
        return Strategy.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.action_type = validated_data.get('action_type', instance.action_type)
        instance.strike = validated_data.get('strike', instance.strike)
        instance.premium = validated_data.get('premium', instance.premium)
        instance.n = validated_data.get('n', instance.n)
        instance.action = validated_data.get('action', instance.action)
        instance.save()
        return instance


class StrategySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(blank=False, max_length=25)
    action_type = serializers.CharField(required=True, max_length=25)
    strike = serializers.FloatField(required=True)
    premium = serializers.FloatField(required=False)
    n = serializers.IntegerField(required=False)
    action = serializers.CharField(required=True, max_length=25)"""