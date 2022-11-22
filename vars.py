import json

class Account:

    def __init__(self, name, atoken, ptoken):
        self.name = name
        self.atoken = atoken
        self.ptoken = ptoken
        self.id = id

class Transactions:
    def __init__(tranObj, pending_transaction_id, category_id, category, location, payment_meta, account_owner, name, account_id, amount, iso_currency_code, unofficial_currency_code, date, pending, transaction_id, payment_channel, authorized_date, authorized_datetime, datetime, transaction_code, check_number, merchant_name, personal_finance_category, transaction_type):
        tranObj.pending_transaction_id = pending_transaction_id
        tranObj.category_id = category_id
        tranObj.category = category
        tranObj.location = location
        tranObj.payment_meta = payment_meta
        tranObj.account_owner = account_owner
        tranObj.name = name
        tranObj.account_id = account_id
        tranObj.amount = amount
        tranObj.iso_currency_code = iso_currency_code
        tranObj.unofficial_currency_code = unofficial_currency_code
        tranObj.date = date
        tranObj.pending = pending
        tranObj.transaction_id = transaction_id
        tranObj.payment_channel = payment_channel
        tranObj.authorized_date = authorized_date
        tranObj.authorized_datetime = authorized_datetime
        tranObj.datetime = datetime
        tranObj.transaction_code = transaction_code
        tranObj.check_number = check_number
        tranObj.merchant_name = merchant_name
        tranObj.personal_finance_category = personal_finance_category
        tranObj.transaction_type = transaction_type




client_id = 'CLIENT-ID'
secret = 'SECRET'
start_date = '2021-08-01'
end_date = '2022-12-10'

with open("items.json", "rb") as f:
    # Load JSON File
    items_json = json.load(f)

    # Tokens
    chase_id = items_json['Accounts'][0]['item_id']
    chase_access = items_json['Accounts'][0]['access_token']

    chime_id = items_json['Accounts'][1]['item_id']
    chime_access = items_json['Accounts'][1]['access_token']

    huntington_id = items_json['Accounts'][2]['item_id']
    huntington_access = items_json['Accounts'][2]['access_token']

    discover_id = items_json['Accounts'][3]['item_id']
    discover_access = items_json['Accounts'][3]['access_token']


huntington = Account("Huntington", huntington_access, huntington_id)
chime = Account("Chime", chime_access, chime_id)
chase = Account("Chase", chase_access, chase_id)
discover = Account("Discover", discover_access, discover_id)







