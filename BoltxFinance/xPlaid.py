import pandas as pd
from sqlalchemy import create_engine
from plaid.exceptions import ApiException, ServiceException
from datetime import datetime
import json
from plaid.models import *
from plaid.models import LinkTokenCreateRequest
from plaid.models import LinkTokenCreateRequestUser
from plaid.model.transactions_sync_request import TransactionsSyncRequest
import plaid
from plaid.api import plaid_api
import webbrowser
import sqlite3


class PlaidManager():

    client_id = ''
    secret = ''
    dbPath = r"C:\Users\kgray\Projects\projectBolt\Data\Finance.db"
    linkPath = r"C:\Users\kgray\Projects\projectBolt\Files\Plaid-Link.html"
    engine = create_engine(f'sqlite:///{dbPath}')

    def __init__(self):
        pass

    # Endpoint
    configuration = plaid.Configuration(
        host=plaid.Environment.Development,
        api_key={
            'clientId': client_id,
            'secret': secret,
        }
    )

    api_client = plaid.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)

    # Plaid Auth
    def updateLinkToken(self, access_token):
        request = LinkTokenCreateRequest(
            client_name="Bolt-Finance",
            country_codes=[CountryCode('US')],
            language='en',
            access_token=access_token,
            webhook='https://webhook.sample.com',
            user=LinkTokenCreateRequestUser(
                client_user_id='klg'
            )
        )
        response = self.client.link_token_create(request)
        return response['link_token']
        print(response['link_token'])

    def exchangePublicToken(self, public_token):
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.client.item_public_token_exchange(request)
        access_token = response['access_token']
        item_id = response['item_id']
        return access_token, item_id

    def createLinkFile(self, linkToken):
        linkText = f"""
    <html>
    <head>
      <link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet'>
      <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap" rel="stylesheet">
      <style>
        .outer {{ justify-self: center; margin: 20% auto 120px auto; width: 60%; ; font-family: 'Roboto', sans-serif;}} a {{ text-decoration: underline; }} li {{ padding-left: 1rem;}}
      </style>
    </head>
    <body style="background-color:#B1EEFC;">
        <div class="outer">
          Continue To Login.
          <button id="link-button" style="background-color: white;border: #0A85EA;color: black;padding: 12px 32px;text-align: center;text-decoration: none;display: inline-block;font-size: 16px;margin: 4px 2px;box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19)">Link Account</button>

        </div>
    <!--=================================================-->
      <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
      <script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"></script>
      <script type="text/javascript">
      (function($) {{
        var handler = Plaid.create({{
          token: "{linkToken}",
          onSuccess: function(public_token, metadata) {{
            console.log('public token is:', public_token);
          }},
          onExit: function(err, metadata) {{
            console.log('onexit invoked');
          }},
          onEvent: function(eventName, metadata) {{
            console.log('event name is:', eventName);
          }}
        }});
        $('#link-button').on('click', function(e) {{ handler.open() }});
      }})(jQuery);
      </script>
    </body>
    </html>
    """

        with open(self.linkPath, "a") as f:
            f.write(linkText)

    def launchLinkUpdate(self, access_token):
        linkToken = self.updateLinkToken(access_token)
        self.createLinkFile(linkToken=linkToken)
        webbrowser.open(self.linkPath)

    # Database Operations
    @staticmethod
    def createDB(table_name, column_names, dbName='finance.db', ):
        conn = sqlite3.connect(f'../{dbName}')
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({column_names})')
        conn.commit()
        conn.close()

    @staticmethod
    def queryTables():
        conn = sqlite3.connect(PlaidManager.dbPath)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(c.fetchall())
        conn.close()

    @staticmethod
    def queryAccounts():
        sqlAccQuery = """
        SELECT * 
        FROM accounts a1
        WHERE timestamp = (SELECT MAX(timestamp) FROM accounts a2 
        WHERE a1.mask = a2.mask)
        ORDER BY account_id, timestamp
        """
        accDf = pd.read_sql(sqlAccQuery, PlaidManager.engine)
        return accDf

    @staticmethod
    def queryTrans():
        sqlAccQuery = "SELECT * FROM transactions"
        accDf = pd.read_sql(sqlAccQuery, PlaidManager.engine)
        return accDf

    @staticmethod
    def queryLoans():
        sqlAccQuery = "SELECT * FROM loans"
        loanDf = pd.read_sql(sqlAccQuery, PlaidManager.engine)
        return loanDf

    @staticmethod
    def exportTrans(path):
        df = PlaidManager.queryTrans()
        df.to_excel(path)

    @staticmethod
    def df2SQL(df, table, mode='append'):
        df.to_sql(table, PlaidManager.engine, if_exists=mode, index=False)

    # Accounts / Transactions
    @staticmethod
    def accounts2DF(access_token):
        now = datetime.now()
        ts = now.strftime("%m/%d/%Y %H:%M:%S")
        request = AccountsBalanceGetRequest(access_token=access_token)
        response = PlaidManager.client.accounts_balance_get(request)
        json_string = json.dumps(response.to_dict())

        account_json = json.loads(json_string)
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

    @staticmethod
    def trans2DF(access_token):
        request = TransactionsSyncRequest(
            access_token=access_token,
        )
        response = PlaidManager.client.transactions_sync(request)
        transactions = response['added']

        # the transactions in the response are paginated, so make multiple calls while incrementing the cursor to
        # retrieve all transactions
        while (response['has_more']):
            request = TransactionsSyncRequest(
                access_token=access_token,
                cursor=response['next_cursor']
            )
            response = PlaidManager.client.transactions_sync(request)
            transactions += response['added']

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
        return df
        df['payment_meta'] = df['payment_meta'].str.get(0)

    @staticmethod
    def updateAccounts():
        skip = []
        items_json = r"C:\Users\kgray\Projects\projectBolt\files\Items.json"

        with open(items_json, 'r') as f:
            acc = f.read()
            acc_json = json.loads(acc)
            acc_json = acc_json['Accounts']

        for account in acc_json:
            try:
                name = account['Name']
                token = account['access_token']
                accountDf = PlaidManager.accounts2DF(token)
                PlaidManager.df2SQL(df=accountDf, table='accounts')


            except (ApiException, ServiceException):
                skip.append(name)
                continue

        skipped_message = ("Skipped Items: " + str(skip))
        return skipped_message

    @staticmethod
    def updateTrans():
        skip = []
        items_json = r"C:\Users\kgray\Projects\projectBolt\files\Items.json"

        with open(items_json, 'r') as f:
            acc = f.read()
            acc_json = json.loads(acc)
            acc_json = acc_json['Accounts']

        for account in acc_json:
            try:
                name = account['Name']
                token = account['access_token']
                transDf = PlaidManager.trans2DF()
                PlaidManager.df2SQL(df=transDf, table='transactions')

            except (ApiException, ServiceException):
                skip.append(name)
                continue

        skipped_message = ("Skipped Items: " + str(skip))
        all_trans = PlaidManager.queryTrans()
        filtered_trans = all_trans.drop_duplicates()
        filtered_trans.to_sql('transactions', PlaidManager.engine, if_exists='replace', index=False)
        return skipped_message