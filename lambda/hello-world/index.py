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
    
    # Extract the prompt and profile data from the API Gateway event
    prompt = ""
    profile_data = {}
    
    if event.get('queryStringParameters') and event.get('queryStringParameters').get('prompt'):
        prompt = event['queryStringParameters']['prompt']
    elif event.get('body'):
        try:
            body = json.loads(event['body'])
            prompt = body.get('prompt', '')
            profile_data = body.get('profileData', {})
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
    
    # Create personalized context from profile data if available
    personalized_context = ""
    if any(profile_data.values()):
        personalized_context = "User Profile Information:\n"
        
        if profile_data.get('age'):
            personalized_context += f"- Age: {profile_data['age']} years\n"
        
        if profile_data.get('gender'):
            personalized_context += f"- Gender: {profile_data['gender']}\n"
        
        if profile_data.get('height') and profile_data.get('weight'):
            height_cm = float(profile_data['height'])
            weight_kg = float(profile_data['weight'])
            
            # Calculate BMI if both height and weight are provided
            if height_cm > 0 and weight_kg > 0:
                height_m = height_cm / 100
                bmi = weight_kg / (height_m * height_m)
                bmi_category = get_bmi_category(bmi)
                personalized_context += f"- Height: {height_cm} cm\n"
                personalized_context += f"- Weight: {weight_kg} kg\n"
                personalized_context += f"- BMI: {bmi:.1f} ({bmi_category})\n"
        elif profile_data.get('height'):
            personalized_context += f"- Height: {profile_data['height']} cm\n"
        elif profile_data.get('weight'):
            personalized_context += f"- Weight: {profile_data['weight']} kg\n"
        
        if profile_data.get('activityLevel'):
            personalized_context += f"- Activity Level: {profile_data['activityLevel']}\n"
        
        if profile_data.get('goals'):
            personalized_context += f"- Health Goals: {profile_data['goals']}\n"
        
        if profile_data.get('healthConditions'):
            personalized_context += f"- Health Conditions: {profile_data['healthConditions']}\n"
        
        personalized_context += "\nTailor your response to this user's specific profile. Consider their age, gender, BMI, activity level, goals, and health conditions when providing advice. Make your response personalized and relevant to their situation.\n"
    
    # Combine all context with the user's prompt
    enhanced_prompt = f"{health_context}\n\n{personalized_context}\nUser query: {prompt}"
    
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

def get_bmi_category(bmi):
    """Return BMI category based on BMI value"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"

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