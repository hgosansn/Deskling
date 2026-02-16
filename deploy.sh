#!/bin/bash


version=$(jq -r ".version" package.json)

# Tag the release only if it doesn't exist
if git rev-parse "refs/tags/release-v$version" >/dev/null 2>&1; then
    echo "Tag release-v$version already exists. Skipping tag creation."
else
    git tag -a "release-v$version" -m "Release v$version"
    git push -u origin main --tags
fi

echo "Building the project..."
npm run build --prod
echo "Deploying the project..."

aws_profile="${AWS_PERSONAL_PROFILE:-''}"

# Directory containing files to upload
DIRECTORY="./dist"

# Name of your S3 bucket
BUCKET_NAME="hson.fr"

# Upload files to S3 recursively
echo "Uploading files from $DIRECTORY to $BUCKET_NAME..."



aws s3 rm s3://$BUCKET_NAME --recursive ${aws_profile:+--profile "$aws_profile"}

echo "Bucket $BUCKET_NAME cleaned."

aws s3 cp "$DIRECTORY" "s3://$BUCKET_NAME/" --recursive ${aws_profile:+--profile "$aws_profile"}
echo "Upload complete."



# If no param skip invalidation
if [ -z "$1" ]; then
    echo "Skipping invalidation."
    exit 0
fi

echo "Invalidating CloudFront cache..."
DISTRIBUTION_ID=$(aws cloudfront list-distributions --query "DistributionList.Items[?contains(Aliases.Items, '$BUCKET_NAME')].Id" --output text ${aws_profile:+--profile "$aws_profile"})
echo "CloudFront Distribution ID: $DISTRIBUTION_ID"

echo "Creating an invalidation..."
# Create an invalidation
INVALIDATION_ID=$(aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/index.html" ${aws_profile:+--profile "$aws_profile"} --query 'Invalidation.Id' --output text)

# Wait for the invalidation to complete
STATUS="InProgress"
while [ "$STATUS" != "Completed" ]; do
    STATUS=$(aws cloudfront get-invalidation --distribution-id $DISTRIBUTION_ID --id $INVALIDATION_ID ${aws_profile:+--profile "$aws_profile"} --query 'Invalidation.Status' --output text)
    echo "Invalidation status: $STATUS"
    if [ "$STATUS" != "Completed" ]; then
        sleep 10  # Wait for 10 seconds before checking again
    fi
done
echo "Done."
