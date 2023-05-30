aws iam create-policy --profile default --policy-name netrics-config-policy1 --policy-document file://s3-bucket-policy.json
aws s3api put-public-access-block \
    --bucket netrics-config1 \
    --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
