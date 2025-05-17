import json
import boto3
import os

# Custom model ID - replace with your actual fine-tuned model ID
CUSTOM_MODEL_ID = "custom.model-id" # Replace with your actual fine-tuned model ID

def handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    
    # Handle OPTIONS request for CORS
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key'
            },
            'body': ''
        }
    
    # Extract the prompt from the API Gateway event
    prompt = ""
    if event.get('queryStringParameters') and event.get('queryStringParameters').get('prompt'):
        prompt = event['queryStringParameters']['prompt']
    elif event.get('body'):
        try:
            body = json.loads(event['body'])
            prompt = body.get('prompt', '')
        except:
            return cors_response(400, {'error': 'Invalid request body'})
    
    if not prompt:
        return cors_response(400, {'error': 'No prompt provided'})
    
    # Add health and fitness context to the prompt
    health_context = """You are a specialized AI assistant focused on health, nutrition, and fitness. 
    Provide evidence-based information about:
    - Health conditions and preventive measures
    - Nutrition advice and balanced diet plans
    - Workout routines for different fitness levels
    - Training plans for running, swimming, cycling, or triathlons
    - Recovery strategies and injury prevention
    - Mental health and wellness practices
    - Sleep optimization techniques
    - Supplement information and recommendations
    
    Always include a disclaimer that you're not providing medical advice when discussing health conditions.
    For fitness plans, emphasize the importance of starting gradually and listening to one's body.
    For nutrition advice, focus on balanced approaches rather than extreme diets."""
    
    enhanced_prompt = f"{health_context}\n\nUser query: {prompt}"
    
    # Initialize Bedrock client
    bedrock_runtime = boto3.client(service_name='bedrock-runtime')
    
    try:
        # Call the custom fine-tuned model
        response = bedrock_runtime.invoke_model(
            modelId=CUSTOM_MODEL_ID,  # Use the custom model ID
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": enhanced_prompt
                    }
                ]
            })
        )
        
        # Parse the response
        response_body = json.loads(response['body'].read())
        model_response = response_body['content'][0]['text']
        
        return cors_response(200, {'response': model_response})
        
    except Exception as e:
        print(f"Error calling Bedrock: {str(e)}")
        
        # Fall back to standard Claude v2 if custom model fails
        try:
            fallback_response = bedrock_runtime.invoke_model(
                modelId='anthropic.claude-v2',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user",
                            "content": enhanced_prompt
                        }
                    ]
                })
            )
            
            fallback_body = json.loads(fallback_response['body'].read())
            fallback_text = fallback_body['content'][0]['text']
            
            return cors_response(200, {
                'response': fallback_text,
                'note': 'Response from fallback model (Claude v2)'
            })
            
        except Exception as fallback_error:
            return cors_response(500, {'error': f'Error processing request: {str(e)}'})

def cors_response(status_code, body_dict):
    """Helper function to create responses with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key'
        },
        'body': json.dumps(body_dict)
    }