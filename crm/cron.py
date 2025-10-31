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