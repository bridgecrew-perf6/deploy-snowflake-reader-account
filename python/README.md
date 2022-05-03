# Deploy Snowflake Reader Python

## Setup

Prior to building the Docker image modify the contents of the `config.json` file.

Build the image from the Dockerfile .

```
docker build --tag snowflake/deploy-reader:python --no-cache .
```

Create enviornment variables on your host. These will be passed to the container at run time.

```
export PROVIDER_USER
export PROVIDER_PWD
export CONSUMER_USER
export CONSUMER_PWD
```

`$PROVIDER_{}` variables should be the credentials for the data provider account. `$CONSUMER_{}` variables should be the administrative credentials for a user on the consumer/reader account.

## Deployment

Run the following to deploy the reader account.

```
docker run --rm -it -e PROVIDER_USER=$PROVIDER_USER -e PROVIDER_PWD=$PROVIDER_PWD -e CONSUMER_USER=$CONSUMER_USER -e CONSUMER_PWD=$CONSUMER_PWD snowflake/deploy-reader:python deploy_reader.py
```

## Notes

Use the following to get shell access in a new container.

```
docker run --rm -it --entrypoint bash snowflake/deploy-reader:python
```
