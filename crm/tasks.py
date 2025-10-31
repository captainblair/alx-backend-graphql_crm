from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    """Generate weekly CRM report using GraphQL queries"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Query for CRM statistics
        query = gql("""
        query {
            allCustomers {
                edges {
                    node {
                        id
                    }
                }
            }
            allOrders {
                edges {
                    node {
                        id
                        totalAmount
                    }
                }
            }
        }
        """)
        
        result = client.execute(query)
        
        # Calculate statistics
        total_customers = len(result['allCustomers']['edges'])
        total_orders = len(result['allOrders']['edges'])
        total_revenue = sum(float(order['node']['totalAmount']) for order in result['allOrders']['edges'])
        
        # Log the report
        report = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue:.2f} revenue"
        
        with open('/tmp/crm_report_log.txt', 'a') as log_file:
            log_file.write(report + '\n')
            
        return report
        
    except Exception as e:
        error_msg = f"{timestamp} - Error generating report: {str(e)}"
        with open('/tmp/crm_report_log.txt', 'a') as log_file:
            log_file.write(error_msg + '\n')
        return error_msg