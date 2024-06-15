#!/bin/bash

ACCOUNT="$1"
REGION="$2"
FUNCTION_NAME="ebs-autoscale-function"
RUNTIME="python3.11"
HANDLER="lambda_function.lambda_handler"
IAM_ROLE="arn:aws:iam::$1:role/ebs-autoscale"
ZIP_FILE="code.zip"

cd ./src && zip -r $ZIP_FILE .

aws lambda create-function \
    --function-name $FUNCTION_NAME \
    --role $IAM_ROLE \
    --timeout 60 \
    --environment "Variables={SNS_ALERT=arn:aws:sns:$2:$1:ebs-autoscale-alert}" \
    --layers arn:aws:lambda:$2:$1:layer:ebs-autoscale-layer:2 \
    --runtime $RUNTIME \
    --handler $HANDLER \
    --zip-file fileb://$ZIP_FILE
