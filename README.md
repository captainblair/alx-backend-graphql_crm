# ALX Backend GraphQL CRM

A Django-based CRM system with GraphQL API.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Testing the GraphQL Endpoint

1. Visit: http://localhost:8000/graphql

2. Run the following query in the GraphiQL interface:
   ```graphql
   {
     hello
   }
   ```

3. Expected response:
   ```json
   {
     "data": {
       "hello": "Hello, GraphQL!"
     }
   }
   ```

## Project Structure

- `alx_backend_graphql_crm/` - Main project directory
  - `settings.py` - Django settings with GraphQL configuration
  - `urls.py` - URL routing including GraphQL endpoint
  - `schema.py` - GraphQL schema definition
- `crm/` - CRM application
- `manage.py` - Django management script

## GraphQL Configuration

The GraphQL endpoint is configured with:
- **URL:** `/graphql`
- **GraphiQL Interface:** Enabled for development
- **CSRF:** Exempt for GraphQL endpoint
