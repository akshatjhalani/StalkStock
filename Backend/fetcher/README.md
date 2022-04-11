## Daily Price Data Fetcher
This folder contains the source code for the daily stock price data fetcher service. The service uses `serverless` framework to deploy.

### Setup
1. Create a postgresql instance with RDS, save the credentials in Secrets Manager. Change the `serverless.yml` file to update the database credentials accordingly.
2. Run the following command:
```bash
serverless plugin install -n serverless-python-requirements
serverless deploy
```
