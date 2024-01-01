from rest_framework import serializers
from rest_framework import permissions

from django.contrib.auth.models import User
import json
from .models import (
    Stock,
    Strategy,
    StrategyLeg,
    StrategyAnalysisResult
)

# Serializers

class UserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    strategies = serializers.HyperlinkedIdentityField(many=True, view_name='strategy-list')
    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        model = User
        fields = ['id', 'owner', 'username', 'password', 'strategies']
        
class StockSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Stock
        fields = '__all__'
    
    def create(self, validated_data):
        return Stock.objects.create(**validated_data)

class StrategyLegSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyLeg
        fields = ['id', 'type', 'strike', 'premium', 'n', 'action', 'prevpos', 'expiration']

class StrategySerializer(serializers.ModelSerializer):
    strategy_legs = StrategyLegSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')  # assuming you want to display the username

    class Meta:
        model = Strategy
        fields = ['id', 'owner', 'strategy_name', 'stockprice', 'volatility', 'interestrate', 
                  'minstock', 'maxstock', 'strategy_legs', 'dividendyield', 'profittarg', 
                  'losslimit', 'optcommission', 'stockcommission', 'compute_the_greeks', 
                  'compute_expectation', 'use_dates', 'discard_nonbusinessdays', 'country', 
                  'startdate', 'targetdate', 'days2targetdate', 'distribution', 'nmcprices']

    def create(self, validated_data):
        strategy_legs_data = validated_data.pop('strategy_legs')
        strategy = Strategy.objects.create(**validated_data)
        for leg_data in strategy_legs_data:
            StrategyLeg.objects.create(strategy=strategy, **leg_data)
        return strategy

    def update(self, instance, validated_data):
        strategy_legs_data = validated_data.pop('strategy_legs', None)

        # Update simple fields
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        # Update strategy legs if provided
        if strategy_legs_data is not None:
            # Clear existing legs and add new ones
            instance.strategy_legs.clear()
            for leg_data in strategy_legs_data:
                StrategyLeg.objects.create(strategy=instance, **leg_data)

        return instance

class StrategyAnalysisResultSerializer(serializers.ModelSerializer): 
    class Meta:
        model = StrategyAnalysisResult
        fields = ['id', 'strategy', 'probability_of_profit', 'strategy_cost', 'per_leg_cost', 'profit_ranges', 'minimum_return_in_domain', 'maximum_return_in_domain']

    def validate_per_leg_cost(self, value):
        try:
            json.loads(value)  # check if valid JSON
        except ValueError:
            raise serializers.ValidationError("Invalid format for per_leg_cost. Must be a valid JSON string.")
        return value

    def validate_profit_ranges(self, value):
        try:
            json.loads(value)  # check if valid JSON
        except ValueError:
            raise serializers.ValidationError("Invalid format for profit_ranges. Must be a valid JSON string.")
        return value

    def create(self, validated_data):
        return StrategyAnalysisResult.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.probability_of_profit = validated_data.get('probability_of_profit', instance.probability_of_profit)
        instance.strategy_cost = validated_data.get('strategy_cost', instance.strategy_cost)
        instance.per_leg_cost = validated_data.get('per_leg_cost', instance.per_leg_cost)
        instance.profit_ranges = validated_data.get('profit_ranges', instance.profit_ranges)
        instance.minimum_return_in_domain = validated_data.get('minimum_return_in_domain', instance.minimum_return_in_domain)
        instance.maximum_return_in_domain = validated_data.get('maximum_return_in_domain', instance.maximum_return_in_domain)
        instance.save()
        return instance

"""template[*serializers.py*]
from rest_framework import serializers
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