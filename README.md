# ALX Backend GraphQL CRM

A Django-based CRM system with GraphQL API supporting customers, products, and orders management.

## Features

- **Customer Management**: Create and manage customer records with validation
- **Product Management**: Create products with price and stock tracking
- **Order Management**: Create orders with multiple products and automatic total calculation
- **Bulk Operations**: Support for bulk customer creation with partial success handling
- **Validation**: Robust validation for emails, phone numbers, prices, and stock
- **Error Handling**: User-friendly error messages for all operations

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Seed the database (optional):**
   ```bash
   python seed_db.py
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Models

### Customer
- `name`: String (required)
- `email`: Email (required, unique)
- `phone`: String (optional, validated format)
- `created_at`: DateTime (auto)

### Product
- `name`: String (required)
- `price`: Decimal (required, positive)
- `stock`: Integer (default: 0, non-negative)
- `created_at`: DateTime (auto)

### Order
- `customer`: ForeignKey to Customer
- `products`: ManyToMany to Product
- `total_amount`: Decimal (auto-calculated)
- `order_date`: DateTime (auto)

## GraphQL API

Visit: http://localhost:8000/graphql

### Queries

#### Get all customers
```graphql
{
  allCustomers {
    id
    name
    email
    phone
    orders {
      id
      totalAmount
    }
  }
}
```

#### Get all products
```graphql
{
  allProducts {
    id
    name
    price
    stock
  }
}
```

#### Get all orders
```graphql
{
  allOrders {
    id
    customer {
      name
      email
    }
    products {
      name
      price
    }
    totalAmount
    orderDate
  }
}
```

### Mutations

#### Create a single customer
```graphql
mutation {
  createCustomer(input: {
    name: "Alice Johnson"
    email: "alice@example.com"
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
      phone
    }
    message
    success
  }
}
```

#### Bulk create customers
```graphql
mutation {
  bulkCreateCustomers(input: [
    { name: "Bob Smith", email: "bob@example.com", phone: "123-456-7890" }
    { name: "Carol Williams", email: "carol@example.com" }
  ]) {
    customers {
      id
      name
      email
    }
    errors
    success
  }
}
```

#### Create a product
```graphql
mutation {
  createProduct(input: {
    name: "Laptop"
    price: "999.99"
    stock: 10
  }) {
    product {
      id
      name
      price
      stock
    }
    message
    success
  }
}
```

#### Create an order
```graphql
mutation {
  createOrder(input: {
    customerId: "1"
    productIds: ["1", "2"]
  }) {
    order {
      id
      customer {
        name
        email
      }
      products {
        name
        price
      }
      totalAmount
      orderDate
    }
    message
    success
  }
}
```

## Validation Rules

### Customer
- Email must be unique
- Phone format: `+1234567890` or `123-456-7890`

### Product
- Price must be positive
- Stock cannot be negative

### Order
- Customer ID must exist
- All product IDs must exist
- At least one product required
- Total amount auto-calculated from product prices

## Error Handling

All mutations return:
- `success`: Boolean indicating operation success
- `message`: User-friendly error or success message
- `errors`: List of errors (for bulk operations)

Example error responses:
- "Email already exists"
- "Invalid product ID: 999"
- "Price must be positive"
- "Phone number must be in format: '+1234567890' or '123-456-7890'"

## Project Structure

- `alx_backend_graphql/` - Main project directory
  - `settings.py` - Django settings with GraphQL configuration
  - `urls.py` - URL routing including GraphQL endpoint
  - `schema.py` - Main GraphQL schema
- `crm/` - CRM application
  - `models.py` - Database models
  - `schema.py` - CRM GraphQL types and mutations
- `seed_db.py` - Database seeding script
- `manage.py` - Django management script

## Testing

1. Start the server: `python manage.py runserver`
2. Visit: http://localhost:8000/graphql
3. Use the GraphiQL interface to test queries and mutations
4. Check the examples above for sample queries

## License

MIT
