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
        """
        Create and return a new `Strategy` instance, given the validated data.
        """
        return Strategy.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Strategy` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.action_type = validated_data.get('action_type', instance.action_type)
        instance.strike = validated_data.get('strike', instance.strike)
        instance.premium = validated_data.get('premium', instance.premium)
        instance.n = validated_data.get('n', instance.n)
        instance.action = validated_data.get('action', instance.action)
        instance.save()
        return instance

# NOTE Not Hyperlinked: class UserSerializer(serializers.ModelSerializer):
class UserSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # NOTE Not Hyperlinked: strategies = serializers.PrimaryKeyRelatedField(many=True, queryset=Strategy.objects.all())
    strategies = serializers.HyperlinkedIdentityField(many=True, view_name='strategy-detail')

    class Meta:
        model = Strategy
        fields = ['id', 'username', 'password', 'strategies']

# class StrategySerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(blank=False, max_length=25)
#     action_type = serializers.CharField(required=True, max_length=25)
#     strike = serializers.FloatField(required=True)
#     premium = serializers.FloatField(required=False)
#     n = serializers.IntegerField(required=False)
#     action = serializers.CharField(required=True, max_length=25)