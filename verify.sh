#!/bin/bash

# Script to verify changes before commit or deploy
echo "🔍 Verifying changes..."

# Run development build
echo "📦 Running development build..."
npm run build:dev
DEV_BUILD_STATUS=$?

if [ $DEV_BUILD_STATUS -ne 0 ]; then
    echo "❌ Development build failed! Please fix the issues before committing."
    exit 1
fi
echo "✅ Development build successful"

# Run production build
echo "🏭 Running production build..."
npm run build
PROD_BUILD_STATUS=$?

if [ $PROD_BUILD_STATUS -ne 0 ]; then
    echo "❌ Production build failed! Please fix the issues before committing."
    exit 1
fi
echo "✅ Production build successful"

echo "🎉 All checks passed! Your changes look good."

# Check if we want to commit after verification
if [ "$1" == "--commit" ] || [ "$1" == "-c" ]; then
    echo "📝 Committing changes..."
    sh commit.sh
fi
