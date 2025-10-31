from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """Log heartbeat message to confirm CRM application health"""
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("{ hello }")
        client.execute(query)
    except:
        pass
    
    message = f"{timestamp} CRM is alive\n"
    
    with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
        log_file.write(message)

def update_low_stock():
    """Update low stock products via GraphQL mutation"""
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        mutation = gql("""
        mutation {
            updateLowStockProducts {
                products {
                    name
                    stock
                }
                message
                success
            }
        }
        """)
        
        result = client.execute(mutation)
        
        with open('/tmp/low_stock_updates_log.txt', 'a') as log_file:
            if result['updateLowStockProducts']['success']:
                for product in result['updateLowStockProducts']['products']:
                    log_file.write(f"{timestamp}: Updated {product['name']} - New stock: {product['stock']}\n")
            else:
                log_file.write(f"{timestamp}: Failed to update low stock products\n")
    except Exception as e:
        with open('/tmp/low_stock_updates_log.txt', 'a') as log_file:
            log_file.write(f"{timestamp}: Error updating low stock products: {str(e)}\n")