## Hourly Price Data Fetcher
This folder contains the source code for the hourly stock price data fetcher service. The service uses `serverless` framework to deploy.

### Setup
1. Follow the `fetcher` folder's setup instructions to set up the RDS, change `serverless.yml` to use the correct database credentials.
2. Uncomment the `resources` section in the `serverless.yml` file.
3. Run the following command:
```bash
serverless plugin install -n serverless-python-requirements
serverless deploy
```
