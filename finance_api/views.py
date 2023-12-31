from rest_framework import permissions
from rest_framework import generics

from django.contrib.auth.models import User

from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly

# NOTE The Idiomatic Django Approach - FULL GENERIC

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from .models import Strategy
from .serializers import StrategySerializer

class StrategyList(generics.ListCreateAPIView):
    """
    List all code strategy, or create a new strategy.
    """    
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]    

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StrategyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code strategy.
    """
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

# NOTE The Mixins Approach - PARTIAL GENERIC
    
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
"""

"""
class StrategyList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
"""

"""
class StrategyDetail(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""

# NOTE The Class Approach

"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

"""

"""
class StrategyList(APIView):
    def get(self, request, format=None):
        strategy = Strategy.objects.all()
        serializer = StrategySerializer(strategy, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StrategySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''
"""

"""
class StrategyDetail(APIView):
    def get_strategy(self, request, pk, format=None):
        try:
            strategy = Strategy.objects.get(pk=pk)
        except strategy.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        strategy = self.get_strategy(pk)
        serializer = StrategySerializer(strategy)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        strategy = self.get_strategy(pk)
        serializer = StrategySerializer(strategy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        strategy = self.get_strategy(pk)
        strategy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

# NOTE The Function Approach

"""
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
"""

"""
@api_view(['GET', 'POST'])
def strategy_list(request, format=None):
    if request.method == 'GET':
        strategy = Strategy.objects.all()
        serializer = StrategySerializer(strategy, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = StrategySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

"""
@api_view(['GET', 'PUT', 'DELETE'])
def strategy_detail(request, pk, format=None):
    try:
        strategy = Strategy.objects.get(pk=pk)
    except strategy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StrategySerializer(strategy)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = StrategySerializer(strategy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        strategy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

class StrategyPinned(generics.GenericAPIView):
    queryset = Strategy.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        strategy = self.get_object()
        return Response(strategy.pinned)
    
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'strategies': reverse('strategy-list', request=request, format=format)
    })
