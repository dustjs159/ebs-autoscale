#!/bin/bash
FUNCTION_NAME="ebs-autoscale-function"
ZIP_FILE="code.zip"

zip -jr $ZIP_FILE ./src/*

aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://$ZIP_FILE \
    --no-cli-pager

rm -rf *.zip