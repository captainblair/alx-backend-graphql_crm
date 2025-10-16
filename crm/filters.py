import django_filters
from .models import Customer, Product, Order


class CustomerFilter(django_filters.FilterSet):
    """Filter for Customer model with name, email, date range, and phone pattern"""
    
    # Case-insensitive partial match for name
    name = django_filters.CharFilter(lookup_expr='icontains')
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    # Case-insensitive partial match for email
    email = django_filters.CharFilter(lookup_expr='icontains')
    email_icontains = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    
    # Date range filters for created_at
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_at = django_filters.DateTimeFilter(field_name='created_at')
    
    # Custom filter for phone number pattern (e.g., starts with +1)
    phone_pattern = django_filters.CharFilter(field_name='phone', lookup_expr='istartswith')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Customer
        fields = {
            'name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'phone': ['exact', 'icontains', 'istartswith'],
            'created_at': ['exact', 'gte', 'lte'],
        }


class ProductFilter(django_filters.FilterSet):
    """Filter for Product model with name, price range, and stock range"""
    
    # Case-insensitive partial match for name
    name = django_filters.CharFilter(lookup_expr='icontains')
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    # Price range filters
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    price = django_filters.NumberFilter(field_name='price')
    
    # Stock range filters
    stock_gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')
    stock = django_filters.NumberFilter(field_name='stock')
    
    # Low stock filter (stock < 10)
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')
    
    def filter_low_stock(self, queryset, name, value):
        """Filter products with stock less than 10"""
        if value:
            return queryset.filter(stock__lt=10)
        return queryset
    
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains'],
            'price': ['exact', 'gte', 'lte'],
            'stock': ['exact', 'gte', 'lte'],
        }


class OrderFilter(django_filters.FilterSet):
    """Filter for Order model with amount range, date range, and related field lookups"""
    
    # Total amount range filters
    total_amount_gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount_lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    total_amount = django_filters.NumberFilter(field_name='total_amount')
    
    # Order date range filters
    order_date_gte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='gte')
    order_date_lte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='lte')
    order_date = django_filters.DateTimeFilter(field_name='order_date')
    
    # Filter by customer name (related field lookup)
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    customer_name_icontains = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    
    # Filter by product name (related field lookup through ManyToMany)
    product_name = django_filters.CharFilter(field_name='products__name', lookup_expr='icontains')
    product_name_icontains = django_filters.CharFilter(field_name='products__name', lookup_expr='icontains')
    
    # Filter by specific product ID
    product_id = django_filters.NumberFilter(field_name='products__id', lookup_expr='exact')
    
    # Filter by customer ID
    customer_id = django_filters.NumberFilter(field_name='customer__id', lookup_expr='exact')
    
    class Meta:
        model = Order
        fields = {
            'total_amount': ['exact', 'gte', 'lte'],
            'order_date': ['exact', 'gte', 'lte'],
            'customer': ['exact'],
            'products': ['exact'],
        }
