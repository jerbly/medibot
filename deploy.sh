#!/usr/bin/env bash
chalice package ./packaged-app/

aws cloudformation package \
     --template-file ./packaged-app/sam.json \
     --s3-bucket jerbly \
     --output-template-file ./packaged-app/packaged.yaml

aws cloudformation deploy \
    --template-file ./packaged-app/packaged.yaml \
    --stack-name medibot-stack \
    --capabilities CAPABILITY_IAM

aws cloudformation describe-stacks --stack-name medibot-stack \
  --query "Stacks[].Outputs[?OutputKey=='EndpointURL'][] | [0].OutputValue"