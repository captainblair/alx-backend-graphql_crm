# GraphQL Filtering and Ordering Tests

Visit: http://localhost:8000/graphql

## Customer Filtering Tests

### Test 1: Filter customers by name (case-insensitive)

```graphql
query {
  allCustomers(nameIcontains: "Ali") {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
```

### Test 2: Filter customers by name and creation date

```graphql
query {
  allCustomers(nameIcontains: "Ali", createdAtGte: "2025-01-01") {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
```

### Test 3: Filter customers by email

```graphql
query {
  allCustomers(emailIcontains: "example.com") {
    edges {
      node {
        id
        name
        email
        phone
      }
    }
  }
}
```

### Test 4: Filter customers by phone pattern (starts with +1)

```graphql
query {
  allCustomers(phonePattern: "+1") {
    edges {
      node {
        id
        name
        email
        phone
      }
    }
  }
}
```

### Test 5: Filter customers with date range

```graphql
query {
  allCustomers(
    createdAtGte: "2025-01-01"
    createdAtLte: "2025-12-31"
  ) {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
```

## Product Filtering Tests

### Test 6: Filter products by price range

```graphql
query {
  allProducts(priceGte: "100", priceLte: "1000") {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

### Test 7: Filter products by price range and sort by stock (descending)

```graphql
query {
  allProducts(
    priceGte: "100"
    priceLte: "1000"
    orderBy: "-stock"
  ) {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

### Test 8: Filter products by name

```graphql
query {
  allProducts(nameIcontains: "Laptop") {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

### Test 9: Filter products with low stock

```graphql
query {
  allProducts(lowStock: true) {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

### Test 10: Filter products by stock range

```graphql
query {
  allProducts(stockGte: 10, stockLte: 50) {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

## Order Filtering Tests

### Test 11: Filter orders by customer name

```graphql
query {
  allOrders(customerName: "Alice") {
    edges {
      node {
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
  }
}
```

### Test 12: Filter orders by product name

```graphql
query {
  allOrders(productName: "Laptop") {
    edges {
      node {
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
    }
  }
}
```

### Test 13: Filter orders by customer name, product name, and total amount

```graphql
query {
  allOrders(
    customerName: "Alice"
    productName: "Laptop"
    totalAmountGte: "500"
  ) {
    edges {
      node {
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
    }
  }
}
```

### Test 14: Filter orders by total amount range

```graphql
query {
  allOrders(totalAmountGte: "100", totalAmountLte: "1000") {
    edges {
      node {
        id
        customer {
          name
        }
        totalAmount
        orderDate
      }
    }
  }
}
```

### Test 15: Filter orders by date range

```graphql
query {
  allOrders(
    orderDateGte: "2025-01-01"
    orderDateLte: "2025-12-31"
  ) {
    edges {
      node {
        id
        customer {
          name
        }
        totalAmount
        orderDate
      }
    }
  }
}
```

### Test 16: Filter orders by specific product ID

```graphql
query {
  allOrders(productId: 1) {
    edges {
      node {
        id
        customer {
          name
        }
        products {
          id
          name
          price
        }
        totalAmount
      }
    }
  }
}
```

### Test 17: Filter orders by customer ID

```graphql
query {
  allOrders(customerId: 1) {
    edges {
      node {
        id
        customer {
          id
          name
          email
        }
        products {
          name
        }
        totalAmount
        orderDate
      }
    }
  }
}
```

## Ordering Tests

### Test 18: Sort customers by name (ascending)

```graphql
query {
  allCustomers(orderBy: "name") {
    edges {
      node {
        id
        name
        email
      }
    }
  }
}
```

### Test 19: Sort customers by creation date (descending)

```graphql
query {
  allCustomers(orderBy: "-created_at") {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
```

### Test 20: Sort products by price (ascending)

```graphql
query {
  allProducts(orderBy: "price") {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

### Test 21: Sort products by stock (descending)

```graphql
query {
  allProducts(orderBy: "-stock") {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

### Test 22: Sort orders by total amount (descending)

```graphql
query {
  allOrders(orderBy: "-total_amount") {
    edges {
      node {
        id
        customer {
          name
        }
        totalAmount
        orderDate
      }
    }
  }
}
```

### Test 23: Sort orders by order date (ascending)

```graphql
query {
  allOrders(orderBy: "order_date") {
    edges {
      node {
        id
        customer {
          name
        }
        totalAmount
        orderDate
      }
    }
  }
}
```

## Combined Filter and Sort Tests

### Test 24: Filter and sort customers

```graphql
query {
  allCustomers(
    nameIcontains: "a"
    orderBy: "name"
  ) {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
```

### Test 25: Filter and sort products

```graphql
query {
  allProducts(
    priceGte: "50"
    priceLte: "500"
    orderBy: "-price"
  ) {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

### Test 26: Filter and sort orders

```graphql
query {
  allOrders(
    customerName: "Alice"
    totalAmountGte: "100"
    orderBy: "-order_date"
  ) {
    edges {
      node {
        id
        customer {
          name
        }
        products {
          name
        }
        totalAmount
        orderDate
      }
    }
  }
}
```

## Pagination Tests

### Test 27: Get first 5 customers

```graphql
query {
  allCustomers(first: 5) {
    edges {
      node {
        id
        name
        email
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
}
```

### Test 28: Get customers with pagination and filtering

```graphql
query {
  allCustomers(
    first: 5
    nameIcontains: "a"
    orderBy: "name"
  ) {
    edges {
      node {
        id
        name
        email
      }
      cursor
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
}
```
