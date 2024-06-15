#!/bin/bash

LAYER_NAME="ebs-autoscale-layer"
ZIP_FILE="layer.zip"

cd ./deploy

rm -rf *.zip

pip3 install -t . -r ../requirements.txt

zip -r $ZIP_FILE . -x "*.sh"

find . -type d ! -name "*.sh" -exec rm -rf {} +

aws lambda publish-layer-version \
    --layer-name $LAYER_NAME \
    --compatible-runtimes python3.11 \
    --zip-file fileb://$ZIP_FILE \
    --no-cli-pager