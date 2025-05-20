# Deployment Guide for Healthy Nation

This guide provides detailed instructions for deploying the Healthy Nation application to AWS with a custom domain.

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Node.js and npm installed
- AWS CDK installed globally (`npm install -g aws-cdk`)
- Domain name registered in Route 53 (for custom domain deployment)

## Deployment Steps

### 1. Configure AWS CLI

Ensure your AWS CLI is configured with the appropriate credentials:

```bash
aws configure
```

### 2. Bootstrap CDK (First-time only)

If you haven't used CDK in this AWS account and region before:

```bash
cdk bootstrap aws://ACCOUNT-NUMBER/REGION
```

### 3. Update Configuration

#### Custom Domain Setup

1. Ensure your domain is registered in Route 53
2. Update the domain name in `bin/workshop.ts` if needed:

```typescript
const domainName = process.env.DOMAIN_NAME || 'healthynation.in';
```

#### API Endpoint

After deployment, update the API endpoint in `public/index.html`:

```javascript
const response = await fetch('YOUR_API_ENDPOINT', {
    // ...
});
```

### 4. Deploy the Application

#### Option 1: Deploy with Custom Domain (healthynation.in)

```bash
USE_CUSTOM_DOMAIN=true DOMAIN_NAME=healthynation.in npm run cdk deploy
```

#### Option 2: Deploy without Custom Domain

```bash
USE_CUSTOM_DOMAIN=false npm run cdk deploy
```

### 5. Verify Deployment

After deployment completes, CDK will output:
- WebsiteURL: The URL of your deployed website
- ApiURL: The URL of your API Gateway endpoint

Visit the WebsiteURL to verify that the application is working correctly.

### 6. DNS Configuration

If using a custom domain:

1. CDK will automatically create the necessary Route 53 records
2. Wait for the DNS changes to propagate (can take up to 24-48 hours)
3. Verify that the domain resolves to your application

## Updating the Application

### Frontend Updates

1. Modify files in the `public` directory
2. Deploy the changes:

```bash
npm run cdk deploy
```

### Backend Updates

1. Modify the Lambda function in `lambda/hello-world/index.py`
2. Deploy the changes:

```bash
npm run cdk deploy
```

## Troubleshooting

### Certificate Validation Issues

If the ACM certificate validation is taking too long:

1. Check the status in the AWS Console under Certificate Manager
2. Verify that the DNS validation records are correctly set up in Route 53

### CloudFront Distribution Issues

If the CloudFront distribution is not serving the website:

1. Check the distribution status in the AWS Console
2. Verify that the origin settings point to the correct S3 bucket
3. Check that the default root object is set to `index.html`

### API Gateway CORS Issues

If you're experiencing CORS errors:

1. Verify the CORS configuration in the API Gateway
2. Check that the Lambda function is returning the correct CORS headers

## Cleanup

To remove all deployed resources:

```bash
cdk destroy
```

Note: This will delete all resources created by this stack, including the S3 bucket, CloudFront distribution, and Lambda function.