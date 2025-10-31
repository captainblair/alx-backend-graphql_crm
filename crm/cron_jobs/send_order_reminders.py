#!/usr/bin/env python3

import os
import sys
import django
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

# GraphQL client setup
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

# Query for orders from last 7 days
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
query = gql(f"""
query {{
  allOrders(orderDateGte: "{seven_days_ago}") {{
    edges {{
      node {{
        id
        customer {{
          email
        }}
        orderDate
      }}
    }}
  }}
}}
""")

result = client.execute(query)

# Log reminders
with open('/tmp/order_reminders_log.txt', 'a') as log_file:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for edge in result['allOrders']['edges']:
        order = edge['node']
        log_file.write(f"{timestamp}: Order ID {order['id']}, Customer: {order['customer']['email']}\n")

print("Order reminders processed!")