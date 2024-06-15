#!/bin/bash

FUNCTION_NAME="ebs-autoscale-function"
RUNTIME="python3.11"
HANDLER="lambda_function.lambda_handler"
IAM_ROLE="arn:aws:iam::047738378124:role/ebs-autoscale"
ZIP_FILE="code.zip"

cd ./src && zip -r $ZIP_FILE .

aws lambda create-function \
    --function-name $FUNCTION_NAME \
    --role $IAM_ROLE \
    --timeout 60 \
    --environment "Variables={SNS_ALERT=arn:aws:sns:us-west-2:047738378124:ebs-autoscale-alert}" \
    --layers arn:aws:lambda:us-west-2:047738378124:layer:ebs-autoscale-layer:2 \
    --runtime $RUNTIME \
    --handler $HANDLER \
    --zip-file fileb://$ZIP_FILE