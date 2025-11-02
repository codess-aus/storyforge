"""
Prompt Agent

Generates creative prompts for the user using Azure AI Inference SDK.
"""
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def generate_prompt(user_id: str) -> str:
    """Generate a creative writing prompt using Azure AI."""
    try:
        endpoint = os.getenv("AZURE_AI_ENDPOINT", "")
        api_key = os.getenv("AZURE_AI_API_KEY", "")
        
        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
        
        response = client.complete(
            messages=[
                SystemMessage(content="You are a creative writing prompt generator. Generate unique, inspiring story prompts in 1-2 sentences."),
                UserMessage(content=f"Generate a creative writing prompt for user {user_id}")
            ],
            max_tokens=100,
            temperature=0.9,
            model="storyforge-text"
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Fallback to placeholder if AI call fails
        return f"Write a story about a robot who learns to dream. (User: {user_id}) [AI Error: {str(e)}]"