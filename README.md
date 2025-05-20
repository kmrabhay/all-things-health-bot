# Healthy Nation - Health & Fitness AI Assistant

This project deploys a health and fitness AI assistant using AWS services including Lambda, API Gateway, S3, CloudFront, and Amazon Bedrock.

## Features

- Personalized health and fitness advice based on user profile
- Integration with Amazon Bedrock for AI responses
- User profile data storage in browser localStorage
- Mobile-responsive design
- Form data used as context for personalized responses

## Architecture

The application consists of:

1. **Frontend**: Static website hosted on S3 and served via CloudFront
2. **Backend**: AWS Lambda function that processes requests and calls Amazon Bedrock
3. **API**: API Gateway that exposes the Lambda function
4. **AI**: Amazon Bedrock for generating responses

## Prerequisites

- AWS Account
- AWS CLI configured
- Node.js and npm installed
- AWS CDK installed

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd all-things-health-bot
```

2. Install dependencies:
```
npm install
```

3. Deploy the application:
```
npm run cdk deploy
```

4. After deployment, note the outputs:
   - `WebsiteURL`: The CloudFront URL for your website
   - `S3WebsiteURL`: Direct S3 website URL (backup)
   - `ApiURL`: The API Gateway endpoint

5. Update the API endpoint in the HTML file:
```
node update-api-endpoint.js YOUR_API_ENDPOINT
```

## Custom Domain Setup

To use your custom domain (e.g., healthynation.in):

1. See the detailed instructions in [domain-setup.md](domain-setup.md)
2. You'll need to:
   - Add DNS records at your domain registrar
   - Create an SSL certificate in AWS Certificate Manager
   - Update your CloudFront distribution settings

## AI Model

The application uses Amazon Bedrock's Claude model. To use a custom fine-tuned model:

1. Update the `CUSTOM_MODEL_ID` in `lambda/hello-world/index.py`

## User Profile Data

The application collects the following optional user profile data to provide personalized responses:

- Age
- Gender
- Height
- Weight
- Activity level
- Health goals
- Health conditions

This data is stored in the browser's localStorage and sent with each request to the AI. The Lambda function uses this data to create personalized context for more relevant responses.

## Development

### Local Development

1. Build the project:
```
npm run build
```

2. Watch for changes:
```
npm run watch
```

3. Run tests:
```
npm test
```

### Modifying the Frontend

The frontend code is located in the `public` directory. After making changes, deploy them with:

```
npm run cdk deploy
```

### Modifying the Backend

The Lambda function code is in the `lambda/hello-world` directory. After making changes, deploy them with:

```
npm run cdk deploy
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.