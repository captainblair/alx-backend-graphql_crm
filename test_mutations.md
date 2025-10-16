# GraphQL Mutation Tests

Visit: http://localhost:8000/graphql

## Test 1: Create a Single Customer

```graphql
mutation {
  createCustomer(input: {
    name: "Alice"
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

**Expected Response:**
```json
{
  "data": {
    "createCustomer": {
      "customer": {
        "id": "1",
        "name": "Alice",
        "email": "alice@example.com",
        "phone": "+1234567890"
      },
      "message": "Customer created successfully",
      "success": true
    }
  }
}
```

## Test 2: Bulk Create Customers

```graphql
mutation {
  bulkCreateCustomers(input: [
    { name: "Bob", email: "bob@example.com", phone: "123-456-7890" }
    { name: "Carol", email: "carol@example.com" }
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

**Expected Response:**
```json
{
  "data": {
    "bulkCreateCustomers": {
      "customers": [
        {
          "id": "2",
          "name": "Bob",
          "email": "bob@example.com"
        },
        {
          "id": "3",
          "name": "Carol",
          "email": "carol@example.com"
        }
      ],
      "errors": null,
      "success": true
    }
  }
}
```

## Test 3: Create a Product

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

**Expected Response:**
```json
{
  "data": {
    "createProduct": {
      "product": {
        "id": "1",
        "name": "Laptop",
        "price": "999.99",
        "stock": 10
      },
      "message": "Product created successfully",
      "success": true
    }
  }
}
```

## Test 4: Create Another Product

```graphql
mutation {
  createProduct(input: {
    name: "Mouse"
    price: "29.99"
    stock: 50
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

## Test 5: Create an Order with Products

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

**Expected Response:**
```json
{
  "data": {
    "createOrder": {
      "order": {
        "id": "1",
        "customer": {
          "name": "Alice"
        },
        "products": [
          {
            "name": "Laptop",
            "price": "999.99"
          },
          {
            "name": "Mouse",
            "price": "29.99"
          }
        ],
        "totalAmount": "1029.98",
        "orderDate": "2025-10-16T19:45:00"
      },
      "message": "Order created successfully",
      "success": true
    }
  }
}
```

## Error Handling Tests

### Test 6: Duplicate Email

```graphql
mutation {
  createCustomer(input: {
    name: "Alice Duplicate"
    email: "alice@example.com"
    phone: "+9999999999"
  }) {
    customer {
      id
      name
    }
    message
    success
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "createCustomer": {
      "customer": null,
      "message": "Email already exists",
      "success": false
    }
  }
}
```

### Test 7: Invalid Phone Format

```graphql
mutation {
  createCustomer(input: {
    name: "Invalid Phone"
    email: "invalid@example.com"
    phone: "abc-def-ghij"
  }) {
    customer {
      id
      name
    }
    message
    success
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "createCustomer": {
      "customer": null,
      "message": "Phone number must be in format: '+1234567890' or '123-456-7890'",
      "success": false
    }
  }
}
```

### Test 8: Negative Price

```graphql
mutation {
  createProduct(input: {
    name: "Invalid Product"
    price: "-10.00"
    stock: 5
  }) {
    product {
      id
      name
    }
    message
    success
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "createProduct": {
      "product": null,
      "message": "Price must be positive",
      "success": false
    }
  }
}
```

### Test 9: Invalid Customer ID

```graphql
mutation {
  createOrder(input: {
    customerId: "999"
    productIds: ["1"]
  }) {
    order {
      id
    }
    message
    success
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "createOrder": {
      "order": null,
      "message": "Customer with ID 999 does not exist",
      "success": false
    }
  }
}
```

### Test 10: Invalid Product ID

```graphql
mutation {
  createOrder(input: {
    customerId: "1"
    productIds: ["999"]
  }) {
    order {
      id
    }
    message
    success
  }
}
```

**Expected Response:**
```json
{
  "data": {
    "createOrder": {
      "order": null,
      "message": "Invalid product ID: 999",
      "success": false
    }
  }
}
```

## Query Tests

### Test 11: Get All Customers

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

### Test 12: Get All Products

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

### Test 13: Get All Orders

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
