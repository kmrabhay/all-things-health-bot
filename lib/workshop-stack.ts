import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class WorkshopStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    // Create a helloworld Lambda Function in Python
    const lambda = new cdk.aws_lambda.Function(this, 'HelloWorld', {
      runtime: cdk.aws_lambda.Runtime.PYTHON_3_8,
      code: cdk.aws_lambda.Code.fromAsset('lambda/hello-world'),
      handler: 'index.handler',
      timeout: cdk.Duration.seconds(30),
      memorySize: 256
    });
    
    // Grant the Lambda function permission to invoke Bedrock models
    lambda.addToRolePolicy(new cdk.aws_iam.PolicyStatement({
      actions: ['bedrock:InvokeModel'],
      resources: ['*']  // You can restrict this to specific model ARNs if needed
    }));

    // Create an API Gateway that integrates to the Lambda Function
    // Create an API Gateway that integrates to the Lambda Function
const api = new cdk.aws_apigateway.RestApi(this, 'HelloAPI', {
    restApiName: 'Hello World API',
    deployOptions: {
      stageName: 'prod',
    },
    defaultCorsPreflightOptions: {
      allowOrigins: cdk.aws_apigateway.Cors.ALL_ORIGINS,
      allowMethods: cdk.aws_apigateway.Cors.ALL_METHODS,
      allowHeaders: cdk.aws_apigateway.Cors.DEFAULT_HEADERS,
      allowCredentials: true
    },
    endpointConfiguration: {
      types: [cdk.aws_apigateway.EndpointType.REGIONAL],
    },
});

    // add lambda as integration to API Gateway for both GET and POST methods
    api.root.addMethod('GET', new cdk.aws_apigateway.LambdaIntegration(lambda));
    api.root.addMethod('POST', new cdk.aws_apigateway.LambdaIntegration(lambda));

    // Create an S3 bucket to host the static website
    const websiteBucket = new cdk.aws_s3.Bucket(this, 'WebsiteBucket', {
      websiteIndexDocument: 'index.html',
      publicReadAccess: true,
      blockPublicAccess: new cdk.aws_s3.BlockPublicAccess({
        blockPublicAcls: false,
        blockPublicPolicy: false,
        ignorePublicAcls: false,
        restrictPublicBuckets: false
      }),
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true
    });

    // Deploy the static website files to S3
    new cdk.aws_s3_deployment.BucketDeployment(this, 'DeployWebsite', {
      sources: [cdk.aws_s3_deployment.Source.asset('public')],
      destinationBucket: websiteBucket
    });

    // Output the website URL
    new cdk.CfnOutput(this, 'WebsiteURL', {
      value: websiteBucket.bucketWebsiteUrl
    });
    

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'WorkshopQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
