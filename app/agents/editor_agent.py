"""
Editor Agent

Suggests improvements or alternate versions for a user's story using Azure AI Inference SDK.
"""
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def suggest_edits(story: str) -> list:
    """Suggest story improvements using Azure AI."""
    try:
        endpoint = os.getenv("AZURE_AI_ENDPOINT", "")
        api_key = os.getenv("AZURE_AI_API_KEY", "")
        
        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
        
        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful story editor. Provide 3 specific, actionable suggestions to improve the story."),
                UserMessage(content=f"Please suggest improvements for this story:\n\n{story}")
            ],
            max_tokens=300,
            temperature=0.7,
            model="storyforge-text"
        )
        
        # Parse suggestions from response
        suggestions_text = response.choices[0].message.content.strip()
        suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip() and not s.strip().startswith('#')]
        return suggestions[:3] if suggestions else [suggestions_text]
        
    except Exception as e:
        # Fallback to generic suggestions if AI call fails
        return [
            "Consider adding more dialogue for your main character.",
            "Describe the setting in greater detail.",
            f"[AI Error: {str(e)}]"
        ]