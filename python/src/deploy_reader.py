import snowflake.connector
import json
import os

def get_config(config_file):
    with open(config_file, 'r') as json_file:
        config = json.load(json_file)
    return config

def create_connection(account, user, password):
    tries = 0
    retries = 5
    while tries < retries:
        try:
            connection = snowflake.connector.connect(
                user = user
                ,password = password
                ,account = account
            )
            return connection
        except Exception as e:
            print(e)
            print("Retrying connection...")
            tries += 1
            continue

def create_cursor(connection):
    cursor = connection.cursor()
    return cursor

def create_reader(config, provider_user, provider_pwd, consumer_user, consumer_pwd):
    provider_account = config['accounts']['provider']['name']
    role = config['roles']['account']
    consumer_account = config['accounts']['consumer']['name']
    consumer_account_type = "reader"

    cnxn = create_connection(provider_account, provider_user, provider_pwd)
    cur = create_cursor(cnxn)

    try:
        cur.execute("use role {role}".format(role=role))
        cur.execute('''
        create managed account {account}
        admin_name='{user}'
        ,admin_password='{password}'
        ,type={type}
        '''.format(
            account=consumer_account
            ,user=consumer_user
            ,password=consumer_pwd
            ,type=consumer_account_type
            )
        )
    finally:
        cur.close()
        cnxn.close()

def create_share(config, provider_user, provider_pwd):
    provider_account = config['accounts']['provider']['name']
    role = config['roles']['account']
    share = config['accounts']['provider']['share']
    database = config['accounts']['provider']['database']
    schema = config['accounts']['provider']['schema']

    cnxn = create_connection(provider_account, provider_user, provider_pwd)
    cur = create_cursor(cnxn)
    
    try:
        cur.execute("use role {role}".format(role=role))
        cur.execute("create or replace share {share}".format(share=share))
        cur.execute("grant usage on database {database} to share {share}".format(database=database, share=share))
        cur.execute("grant usage on schema {database}.{schema} to share {share}".format(database=database, schema=schema, share=share))
        cur.execute("grant select on all tables in schema {database}.{schema} to share {share}".format(database=database, schema=schema, share=share))
    finally:
        cur.close()
        cnxn.close()

def alter_share(config, provider_user, provider_pwd):
    provider_account = config['accounts']['provider']['name']
    role = config['roles']['account']
    provider_share = config['accounts']['provider']['share']
    consumer_account = config['accounts']['consumer']['name']

    cnxn = create_connection(provider_account, provider_user, provider_pwd)
    cur = create_cursor(cnxn)

    try:
        cur.execute("use role {role}".format(role=role))
        cur.execute("""show managed accounts like '%{consumer_account}%'""".format(consumer_account=consumer_account))
        locator = cur.fetchone()[3]
        cur.execute("alter share {share} add accounts = {locator}".format(share=provider_share,locator=locator))
        return locator.lower()
    finally:
        cur.close()
        cnxn.close()

def configure_reader(config, locator,  consumer_user, consumer_pwd):
    account_role = config['roles']['account']
    admin_role = config['roles']['sys']
    query_role = config['roles']['public']
    database = config['accounts']['consumer']['database']
    warehouse_name = "query_wh"
    warehouse_size = "xsmall"
    warehouse_type = "standard"
    auto_suspend = "60"
    auto_resume = "true"
    initially_suspended = "true"

    share = config['accounts']['provider']['share']
    provider_account = config['accounts']['provider']['name']
    
    cnxn = create_connection(locator, consumer_user, consumer_pwd)
    cur = create_cursor(cnxn)

    try:
        cur.execute("use role {role}".format(role=account_role))
        cur.execute("create or replace database {database} from share {account}.{share}".format(database=database, account=provider_account, share=share))
        cur.execute("grant imported privileges on database {database} to role {query_role}".format(database=database, query_role=query_role))
        cur.execute("use role {role}".format(role=admin_role))
        cur.execute("""create or replace warehouse {warehouse_name}
        warehouse_size = {warehouse_size}
        warehouse_type = {warehouse_type}
        auto_suspend = {auto_suspend}
        auto_resume = {auto_resume}
        initially_suspended = {initially_suspended}
        """.format(
            warehouse_name=warehouse_name
            ,warehouse_size=warehouse_size
            ,warehouse_type=warehouse_type
            ,auto_suspend=auto_suspend
            ,auto_resume=auto_resume
            ,initially_suspended=initially_suspended
        ))
        cur.execute("grant usage on warehouse {warehouse_name} to role {query_role}".format(warehouse_name=warehouse_name, query_role=query_role))
    finally:
        cur.close()
        cnxn.close()

def main():
    config = get_config('config.json')

    provider_user = os.environ['PROVIDER_USER']
    provider_pwd = os.environ['PROVIDER_PWD']

    consumer_user = os.environ['CONSUMER_USER']
    consumer_pwd = os.environ['CONSUMER_PWD']

    print("Creating reader account...")
    create_reader(config, provider_user, provider_pwd, consumer_user, consumer_pwd)
    print("Creating share...")
    create_share(config, provider_user, provider_pwd)
    print("Altering share...")
    locator = alter_share(config, provider_user, provider_pwd)
    print("Configuring reader account...")
    configure_reader(config, locator,  consumer_user, consumer_pwd)
    print("All done.")

if __name__ == '__main__':
	main()