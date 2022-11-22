import pandas as pd
import sqlite3 as db
from sqlalchemy import create_engine, ForeignKey
import cryptocompare
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.transactions_get_request import TransactionsGetRequest
import os, requests, json
from plaid.exceptions import ApiException, ServiceException
from endpoint import client
from vars import *
from datetime import datetime
import json
from plaid.models import *
from plaid.models import LinkTokenCreateRequest
from plaid.models import LinkTokenCreateRequestUser
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import date
from plaid_python_adapter.exceptions import (
    PlaidAdapterError,
    PlaidCreateLinkTokenError,
    PlaidExchangePublicTokenError,
    PlaidAuthError,
    PlaidIdentityError,
    PlaidApiInternalServerError,
    PlaidBankTransferSyncEventError,
    PlaidAdapterConfigurationError,
)


class PlaidAdapter:

    def __init__(self):
        retry_strategy = Retry(
            total=5,
            backoff_factor=10,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE"]
        )
        self.adapter = HTTPAdapter(max_retries=retry_strategy)
        self.http = requests.Session()
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}
        # http.mount("https://", adapter)

        self.initialize_plaid()

    def initialize_plaid(self, client_name='None', country_codes=['US'], language='en', products=['auth'],
                         account_subtypes=["checking", "savings"]):
        self.client_name = client_name
        self.country_codes = country_codes
        self.language = language
        self.products = products
        self.account_subtypes = account_subtypes
        self.plaid_client_id = client_id
        self.plaid_public_key = ''
        self.plaid_secret = secret
        self.plaid_environment = 'development'
        self.plaid_base_url = 'http:///link/token/create'
        if not [x for x in (
        self.plaid_client_id, self.plaid_public_key, self.plaid_secret, self.plaid_environment, self.plaid_base_url) if
                x is None]:
            pass
        else:
            raise PlaidAdapterConfigurationError('Missing Plaid Configuration!')

    def create_link_token(self, client_user_id=None, access_token=None):
        request = {}
        request['client_id'] = self.plaid_client_id
        request['secret'] = self.plaid_secret
        request['client_name'] = self.client_name
        request['country_codes'] = self.country_codes
        request['language'] = self.language
        user = {}
        user['client_user_id'] = client_user_id
        request['user'] = user
        # This is required if the user already linked his account with Plaid and needs to verify the authentication.
        if access_token:
            request['access_token'] = access_token
        else:
            request['products'] = self.products
            account_filters = {}
            depository = {}
            depository['account_subtypes'] = self.account_subtypes
            account_filters['depository'] = depository
            request['account_filters'] = account_filters
        link_url = self.plaid_base_url + '/link/token/create'
        create_link_token_response = requests.post(link_url, data=json.dumps(request), headers=self.headers)
        res_http_code = create_link_token_response.status_code
        response_text = create_link_token_response.text
        if res_http_code != 200:
            if res_http_code == 500:
                raise PlaidApiInternalServerError(response_text)
            else:
                raise PlaidCreateLinkTokenError(response_text)

        return json.loads(response_text)

    def exchange_public_token(self, public_token=None):
        request = {}
        request['client_id'] = self.plaid_client_id
        request['secret'] = self.plaid_secret
        if public_token is None:
            raise PlaidExchangePublicTokenError('Missing mandatory public token!')
        request['public_token'] = public_token
        exchange_public_token_url = self.plaid_base_url + '/item/public_token/exchange'
        exchange_public_token_response = requests.post(exchange_public_token_url, data=json.dumps(request),
                                                       headers=self.headers)
        res_http_code = exchange_public_token_response.status_code
        response_text = exchange_public_token_response.text
        if res_http_code != 200:
            if res_http_code == 500:
                raise PlaidApiInternalServerError(response_text)
            else:
                raise PlaidExchangePublicTokenError(response_text)
        return json.loads(response_text)

    def auth_request(self, access_token=None, account_ids=None):
        request = {}
        request['client_id'] = self.plaid_client_id
        request['secret'] = self.plaid_secret
        request['access_token'] = access_token
        if account_ids:
            options = {}
            options['account_ids'] = account_ids
            request['options'] = options
        auth_request_url = self.plaid_base_url + '/auth/get'
        auth_response = requests.post(auth_request_url, data=json.dumps(request), headers=self.headers)
        res_http_code = auth_response.status_code
        response_text = auth_response.text
        if res_http_code != 200:
            if res_http_code == 500:
                raise PlaidApiInternalServerError(response_text)
            else:
                raise PlaidAuthError(response_text)

        return json.loads(response_text)

    def identity_request(self, access_token=None, account_ids=None):
        request = {}
        request['client_id'] = self.plaid_client_id
        request['secret'] = self.plaid_secret
        request['access_token'] = access_token
        if account_ids:
            options = {}
            options['account_ids'] = account_ids
            request['options'] = options
        identity_request_url = self.plaid_base_url + '/identity/get'
        identity_response = requests.post(identity_request_url, data=json.dumps(request), headers=self.headers)
        res_http_code = identity_response.status_code
        response_text = identity_response.text
        if res_http_code != 200:
            if res_http_code == 500:
                raise PlaidApiInternalServerError(response_text)
            else:
                raise PlaidIdentityError(response_text)

        return json.loads(response_text)

    def sync_bank_transfer_event(self, after_id=None, count=None):
        request = {}
        request['client_id'] = self.plaid_client_id
        request['secret'] = self.plaid_secret
        if after_id is not None:
            request['after_id'] = after_id
        if count is not None:
            request['count'] = count
        sync_bank_transfer_url = self.plaid_base_url + '/bank_transfer/event/sync'
        bank_transfer_sync_response = requests.post(sync_bank_transfer_url, data=json.dumps(request),
                                                    headers=self.headers)
        res_http_code = bank_transfer_sync_response.status_code
        response_text = bank_transfer_sync_response.text
        if res_http_code != 200:
            if res_http_code == 500:
                raise PlaidApiInternalServerError(response_text)
            else:
                raise PlaidBankTransferSyncEventError(response_text)
        return json.loads(response_text)


def xrpBalance(tokens):
    x = cryptocompare.get_price('XRP', currency='USD')
    xrpPrice = x['XRP']['USD']
    balance = xrpPrice * tokens
    balance = round(balance)
    balanceStr = f"You have {tokens} XRP tokens worth a total of ${balance}"
    return balanceStr


def updateLink(access_token):
    # Create a one-time use link_token for the Item.
    # This link_token can be used to initialize Link
    # in update mode for the user.
    # Create a link_token for the given user
    request = LinkTokenCreateRequest(
            client_name="My App",
            country_codes=[CountryCode('US')],
            language='en',
            access_token = access_token,
            webhook='https://webhook.sample.com',
            user=LinkTokenCreateRequestUser(
                client_user_id='klg'
            )
        )
    response = client.link_token_create(request)
    return response


def createLink():
    request = LinkTokenCreateRequest(
        products=[Products('auth'), Products('transactions')],
        client_name="Plaid Test App",
        country_codes=[CountryCode('US')],
        redirect_uri='https://domainname.com/oauth-page.html',
        language='en',
        webhook='https://sample-webhook-uri.com',
        link_customization_name='default',
        account_filters=LinkTokenAccountFilters(
            depository=DepositoryFilter(
                account_subtypes=DepositoryAccountSubtypes(
                    [DepositoryAccountSubtype('checking'), DepositoryAccountSubtype('savings')]
                )
            )
        ),
        user=LinkTokenCreateRequestUser(
            client_user_id='123-test-user-id'
        ),
    )
    # create link token
    response = client.link_token_create(request)
    link_token = response['link_token']


def modifyHTML(link):
    pass


def launchLink():
    pass


def exchangeToken(public_token):
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = client.item_public_token_exchange(request)
    access_token = response['access_token']
    item_id = response['item_id']
    return access_token, item_id


def pullItems(access_token):
    request = AccountsBalanceGetRequest(access_token=access_token)
    response = client.accounts_balance_get(request)
    json_string = json.dumps(response.to_dict())
    return json_string


def pullTransactions(access_token, start, end):
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=datetime.strptime(start, '%Y-%m-%d').date(),
        end_date=datetime.strptime(end, '%Y-%m-%d').date(),
        options=TransactionsGetRequestOptions()
    )
    response = client.transactions_get(request)
    transactions = response['transactions']

    while len(transactions) < response['total_transactions']:
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=datetime.strptime(start, '%Y-%m-%d').date(),
            end_date=datetime.strptime(end, '%Y-%m-%d').date(),
            options=TransactionsGetRequestOptions(
                offset=len(transactions)
            )
        )
        response = client.transactions_get(request)
        transactions.extend(response['transactions'])
        return transactions


def cleanAccounts(access_token):
    now = datetime.now()
    ts = now.strftime("%m/%d/%Y %H:%M:%S")
    req = pullItems(access_token=access_token)
    account_json = json.loads(req)
    accounts = account_json['accounts']
    all_accounts = []
    for x in accounts:
        account_details = {
            'account_id': x['account_id'],
            'current': x['balances']['current'],
            'available': x['balances']['available'],
            'name': x['name'],
            'mask': x['mask'],
            'type': x['type'],
            'subtype': x['subtype'],
            'timestamp': ts
        }
        all_accounts.append(account_details)
    df = pd.DataFrame(all_accounts)
    return df


def cleanTrans(access_token, start, end):
    transactions = pullTransactions(access_token=access_token, start=start, end=end)
    trans = []
    for x in transactions:
        tran = {
            'pending_transaction_id': x["pending_transaction_id"],
            'category_id': x["category_id"],
            'category': x["category"],
            'location': x["location"],
            'payment_meta': x["payment_meta"],
            'account_owner': x['account_owner'],
            'name': x["name"],
            'account_id': x["account_id"],
            'amount': x["amount"],
            'iso_currency_code': x["iso_currency_code"],
            'unofficial_currency_code': x['unofficial_currency_code'],
            'date': x['date'],
            'pending': x['pending'],
            'transaction_id': x['transaction_id'],
            'payment_channel': x['payment_channel'],
            'authorized_date': x['authorized_date'],
            'authorized_datetime': x['authorized_datetime'],
            'datetime': x['datetime'],
            'transaction_code': x['transaction_code'],
            'check_number': x['check_number'],
            'merchant_name': x['merchant_name'],
            'personal_finance_category': x['personal_finance_category'],
            'transaction_type': x['transaction_type']
        }
        trans.append(tran)
    df = pd.DataFrame(trans)
    df['category'] = df['category'].str.get(0)
    df['location'] = df['location'].str.get(0)
    df['payment_meta'] = df['payment_meta'].str.get(0)
    return df


def trans2SQL(df):
    path = "C:\\Users\\korey\\Projects\\projectBolt\\finance.db"
    engine = create_engine(f'sqlite:///finance.db')

    data = df
    data.to_sql('transactions', engine, if_exists='append', index=False)


def account2SQL(df):
    path = "C:\\Users\\korey\\Projects\\projectBolt\\finance.db"
    engine = create_engine(f'sqlite:///finance.db')

    data = df
    data.to_sql('accounts', engine, if_exists='append', index=False)


def updateAccounts():
    accounts = []
    newDf = pd.DataFrame()
    skip = []
    items_json = r"C:\Users\kgray\Projects\projectBolt\Items.json"
    with open(items_json, 'r') as f:
        acc = f.read()
        acc_json = json.loads(acc)
        acc_json = acc_json['Accounts']

    for account in acc_json:
        try:
            name = account['Name']
            token = account['access_token']
            x = cleanAccounts(token)
            accountDf = pd.DataFrame(x)
            account2SQL(accountDf)

        except (ApiException, ServiceException):
            skip.append(name)
            continue

    skipped_message = ("Skipped Items: " + str(skip))
    return skipped_message


def queryTables():
    conn = db.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(c.fetchall())
    conn.close


def queryTrans():
    dbPath = r"C:\Users\kgray\Projects\projectBolt\finance.db"
    engine = create_engine(f'sqlite:///{dbPath}')
    sqlTransQuery = """
    SELECT * FROM transactions
    """

    transactionDf = pd.read_sql(sqlTransQuery, engine)
    return transactionDf


def queryAccounts():
    dbPath = r"C:\Users\kgray\Projects\projectBolt\finance.db"
    engine = create_engine(f'sqlite:///{dbPath}')
    sqlAccQuery = """
    SELECT * 
    FROM accounts a1
    WHERE timestamp = (SELECT MAX(timestamp) FROM accounts a2 
    WHERE a1.mask = a2.mask)
    ORDER BY account_id, timestamp
    """

    accDf = pd.read_sql(sqlAccQuery, engine)
    return accDf


def updateLoanBalance():
    conn = db.connect('finance.db')
    c = conn.cursor()

    Name = input("Which Record Are You Updating? ")
    Value = input("What Is The New Value? ")

    sqlUpdate = f"""
    UPDATE loans
    SET Balance = {Value}
    WHERE Name = "{Name}"
    """

    c.execute(sqlUpdate)
    conn.commit()
    conn.close()

    print("Loan Balance Successfully Updated")
