## Sagemaker
This folder contains the source codes for building a sagemaker pipeline to predict the stock price.

### Dockerfile
The dockerfile is used to build the docker image for the pipeline to execute. The generated docker image needs to be uploaded to the ECR repository.
The `image_uri` in the pipeline needs to be the ECR repository URI.

### Pipelined.ipynb
This file can be executed n the sagemaker studio to generate a pipeline. The pipeline includes the following steps:
1. Processing Data: Download the raw stock data from the S3 bucket and calculate the macd histgram. The processed data is uploaded to the S3 bucket.
2. Model Training: Training the DeepAR model with pre-tuned hyperparameters and processed macd histgram data. The trained model is uploaded to the S3 bucket.
3. Oneshot Evaluation: The trained model is deployed to the sagemaker API endpoint and the model is evaluated on the latest prices to predict the future stock price. After evaluation, the API endpoint is removed to reduce cost. The predicted stock price is uploaded to the S3 bucket.

### Setup
1. Build docker image:
    ```bash
    docker build -t stalk-stock-processor .
    ```
2. Upload image to ECR (remember to create the ECR repository, and replace the following repo url):
    ```bash
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 555178539686.dkr.ecr.us-east-1.amazonaws.com
    docker tag stalk-stock-processor:latest 555178539686.dkr.ecr.us-east-1.amazonaws.com/stalk-stock-processor:latest
    docker push 555178539686.dkr.ecr.us-east-1.amazonaws.com/stalk-stock-processor:latest
    ```
3. Edit the `pipelined.ipynb` file to update the ECR repository URI to the `image_uri` variable.
4. Create a sagemaker studio, upload the `pipelined.ipynb` file to the studio and run.
