## User Login and Registration Service
This folder contains the source code for the user login and registration service.

### Setup
1. Zip this folder
2. Create multiple funcions on AWS console with the following name:
    - lambda_handler_login
    - lambda_handler_register
    - lambda_handler_get_stock_details
3. For each of the funcitons, set the handler to:
    - main.lambda_handler_login
    - main.lambda_handler_register
    - main.lambda_handler_get_stock_details