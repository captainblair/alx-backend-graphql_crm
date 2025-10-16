import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Customer, Product, Order


# GraphQL Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email', 'phone', 'created_at', 'orders')


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock', 'created_at', 'orders')


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ('id', 'customer', 'products', 'total_amount', 'order_date')


# Input Types
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int(required=False, default_value=0)


class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime(required=False)


# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, input):
        try:
            # Check if email already exists
            if Customer.objects.filter(email=input.email).exists():
                return CreateCustomer(
                    customer=None,
                    message="Email already exists",
                    success=False
                )

            # Create customer
            customer = Customer(
                name=input.name,
                email=input.email,
                phone=input.phone if input.phone else None
            )
            
            # Validate and save
            customer.full_clean()
            customer.save()

            return CreateCustomer(
                customer=customer,
                message="Customer created successfully",
                success=True
            )
        except ValidationError as e:
            error_messages = []
            for field, errors in e.message_dict.items():
                error_messages.extend(errors)
            return CreateCustomer(
                customer=None,
                message="; ".join(error_messages),
                success=False
            )
        except Exception as e:
            return CreateCustomer(
                customer=None,
                message=str(e),
                success=False
            )


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    def mutate(self, info, input):
        created_customers = []
        errors = []

        with transaction.atomic():
            for idx, customer_data in enumerate(input):
                try:
                    # Check if email already exists
                    if Customer.objects.filter(email=customer_data.email).exists():
                        errors.append(f"Row {idx + 1}: Email '{customer_data.email}' already exists")
                        continue

                    # Create customer
                    customer = Customer(
                        name=customer_data.name,
                        email=customer_data.email,
                        phone=customer_data.phone if customer_data.phone else None
                    )
                    
                    # Validate and save
                    customer.full_clean()
                    customer.save()
                    created_customers.append(customer)

                except ValidationError as e:
                    error_messages = []
                    for field, field_errors in e.message_dict.items():
                        error_messages.extend(field_errors)
                    errors.append(f"Row {idx + 1}: {'; '.join(error_messages)}")
                except Exception as e:
                    errors.append(f"Row {idx + 1}: {str(e)}")

        return BulkCreateCustomers(
            customers=created_customers,
            errors=errors if errors else None,
            success=len(created_customers) > 0
        )


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)
    message = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, input):
        try:
            # Validate price is positive
            if input.price <= 0:
                return CreateProduct(
                    product=None,
                    message="Price must be positive",
                    success=False
                )

            # Validate stock is not negative
            stock = input.stock if input.stock is not None else 0
            if stock < 0:
                return CreateProduct(
                    product=None,
                    message="Stock cannot be negative",
                    success=False
                )

            # Create product
            product = Product(
                name=input.name,
                price=input.price,
                stock=stock
            )
            
            # Validate and save
            product.full_clean()
            product.save()

            return CreateProduct(
                product=product,
                message="Product created successfully",
                success=True
            )
        except ValidationError as e:
            error_messages = []
            for field, errors in e.message_dict.items():
                error_messages.extend(errors)
            return CreateProduct(
                product=None,
                message="; ".join(error_messages),
                success=False
            )
        except Exception as e:
            return CreateProduct(
                product=None,
                message=str(e),
                success=False
            )


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)
    message = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, input):
        try:
            # Validate customer exists
            try:
                customer = Customer.objects.get(pk=input.customer_id)
            except Customer.DoesNotExist:
                return CreateOrder(
                    order=None,
                    message=f"Customer with ID {input.customer_id} does not exist",
                    success=False
                )

            # Validate at least one product
            if not input.product_ids or len(input.product_ids) == 0:
                return CreateOrder(
                    order=None,
                    message="At least one product must be selected",
                    success=False
                )

            # Validate all products exist
            products = []
            for product_id in input.product_ids:
                try:
                    product = Product.objects.get(pk=product_id)
                    products.append(product)
                except Product.DoesNotExist:
                    return CreateOrder(
                        order=None,
                        message=f"Invalid product ID: {product_id}",
                        success=False
                    )

            # Calculate total amount
            total_amount = sum(product.price for product in products)

            # Create order
            with transaction.atomic():
                order = Order(
                    customer=customer,
                    total_amount=total_amount
                )
                order.save()
                
                # Add products to order
                order.products.set(products)

            return CreateOrder(
                order=order,
                message="Order created successfully",
                success=True
            )
        except Exception as e:
            return CreateOrder(
                order=None,
                message=str(e),
                success=False
            )


# Query
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)
    customer = graphene.Field(CustomerType, id=graphene.ID(required=True))
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    order = graphene.Field(OrderType, id=graphene.ID(required=True))

    def resolve_all_customers(self, info):
        return Customer.objects.all()

    def resolve_all_products(self, info):
        return Product.objects.all()

    def resolve_all_orders(self, info):
        return Order.objects.all()

    def resolve_customer(self, info, id):
        try:
            return Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return None

    def resolve_product(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

    def resolve_order(self, info, id):
        try:
            return Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return None


# Mutation
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
