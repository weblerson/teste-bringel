from rest_framework import viewsets
from rest_framework import permissions

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample

from ..models import Customer
from ..serializers import CustomerSerializer


@extend_schema_view(
    list=extend_schema(
        examples=[
            OpenApiExample(
                'List example',
                description='Example of returning a page with a customer with id 1, username John and email '
                            'john@dev.dev',
                value={
                    'id': 1,
                    'username': 'John',
                    'email': 'john@dev.dev'
                }
            )
        ],
        description='Return a paginated list of customers.',
        auth=None,
        responses={status.HTTP_200_OK: CustomerSerializer(many=True)}
    ),
    retrieve=extend_schema(
        examples=[
            OpenApiExample(
                'Retrieve example',
                description='Example of returns a single customer with id 1, username John and email john@dev.dev',
                value={
                    'id': 1,
                    'username': 'John',
                    'email': 'john@dev.dev'
                }
            )
        ],
        description='Return a single customer.',
        auth=None,
        responses={status.HTTP_200_OK: CustomerSerializer}
    ),
    create=extend_schema(
        examples=[
            OpenApiExample(
                'Create request example (common customer)',
                description='Example of creating a common customer with username John and email john@dev.dev',
                value={
                    'username': 'John',
                    'email': 'john@dev.dev',
                    'is_staff': False
                }
            ),
            OpenApiExample(
                'Create request example (staff customer)',
                description='Example of creating a staff customer with username John and email john@dev.dev',
                value={
                    'username': 'John',
                    'email': 'john@dev.dev',
                    'is_staff': True
                }
            )
        ],
        description='Create a single customer',
        auth=None,
        request=CustomerSerializer,
        responses={
            status.HTTP_201_CREATED: CustomerSerializer,
            status.HTTP_400_BAD_REQUEST: None,
        }
    ),
    update=extend_schema(
        examples=[
            OpenApiExample(
                'Update request example',
                description='Update the customer\'s all data to Nina',
                value={
                    'username': 'Nina',
                    'email': 'nina@nina.dev',
                    'password': 'nina',
                    'is_staff': False
                }
            )
        ],
        description='Update a customer data',
        auth=None,
        request=CustomerSerializer,
        responses={
            status.HTTP_200_OK: CustomerSerializer,
            status.HTTP_400_BAD_REQUEST: None
        }
    ),
    partial_update=extend_schema(
        examples=[
            OpenApiExample(
                'Partial update request example',
                description='Update the customer\'s username from John to Nina',
                value={
                    'username': 'Nina'
                }
            )
        ],
        description='Update a customer data',
        auth=None,
        request=CustomerSerializer,
        responses={
            status.HTTP_200_OK: CustomerSerializer,
            status.HTTP_400_BAD_REQUEST: None
        }
    )
)
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(30))
    @method_decorator(vary_on_headers('Authorization'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description='Delete a customer',
        auth=None,
        responses={
            status.HTTP_204_NO_CONTENT: None
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        A customer cannot remove an account that is not theirs
        """
        customer: Customer = self.get_object()
        if request.user != customer:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        match self.action:
            case 'list' | 'retrieve' | 'create':
                permission_classes = [permissions.AllowAny]

            case _:
                permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]
