#!/bin/bash

# Deployment script for Healthy Nation

# Build the project
echo "Building the project..."
npm run build

# Deploy with CDK
echo "Deploying with CDK..."
npm run cdk deploy

# Output success message
echo "Deployment complete!"
echo "Check the outputs above for the WebsiteURL, S3WebsiteURL, and ApiURL."
echo ""
echo "After deployment, update the API endpoint in your HTML file with:"
echo "node update-api-endpoint.js YOUR_API_ENDPOINT"