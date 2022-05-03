# Deploy Snowflake Reader

## Setup

Create the following environment variables on your host
```
export SNOWSQL_ACCOUNT=provider_account
export SNOWSQL_USER=provider_user
export SNOWSQL_PWD=provider_pass
export CONSUMER_USER=consumer_user
export CONSUMER_PWD=consumer_pwd
```

Build the image from the Dockerfile 

```
docker build --tag snowflake/deploy-reader:snowsql --no-cache .
```

## Deployment

Run the following `.sql` scripts in the order in which they are shown
```
docker run --rm -e SNOWSQL_ACCOUNT=$SNOWSQL_ACCOUNT -e SNOWSQL_USER=$SNOWSQL_USER -e SNOWSQL_PWD=$SNOWSQL_PWD snowflake/deploy-reader:snowsql -f create_reader_account.sql --variable consumer_user=$CONSUMER_USER --variable consumer_pass=$CONSUMER_PWD
```
```
docker run --rm -e SNOWSQL_ACCOUNT=$SNOWSQL_ACCOUNT -e SNOWSQL_USER=$SNOWSQL_USER -e SNOWSQL_PWD=$SNOWSQL_PWD snowflake/deploy-reader:snowsql -f create_share.sql
```
```
docker run --rm -e SNOWSQL_ACCOUNT=$SNOWSQL_ACCOUNT -e SNOWSQL_USER=$SNOWSQL_USER -e SNOWSQL_PWD=$SNOWSQL_PWD snowflake/deploy-reader:snowsql -f alter_share.sql
```

In the output of the `alter_share.sql` you'll get the "locator" for the new reader account. Note this value as you need it in the next step as the `SNOWSQL_ACCOUNT` environment variable.

Add the environment variable below using the "locator" from the `alter_share.sql` output.
```
export CONSUMER_ACCOUNT=consumer_account_locator
```

Note that reader account creation can take several minutes. If your connection to the new reader account returns a `403` status simply retry. 

You can now run the final `.sql` script to setup the reader account objects from the provider share.
```
docker run --rm -e SNOWSQL_ACCOUNT=$CONSUMER_ACCOUNT -e SNOWSQL_USER=$CONSUMER_USER -e SNOWSQL_PWD=$CONSUMER_PWD snowflake/deploy-reader:snowsql -f create_reader_account_objects.sql
```