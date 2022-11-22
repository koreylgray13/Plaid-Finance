import plaid
from plaid.api import plaid_api
from vars import client_id, secret

configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': client_id,
        'secret': secret,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)