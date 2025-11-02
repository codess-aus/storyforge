"""
Illustrator Agent

Generates a vibrant, anime-style illustration for a story using Azure OpenAI DALL-E.
"""
import os
import requests

def generate_illustration(story: str) -> str:
    """Generate an anime-style illustration using Azure OpenAI."""
    try:
        # Use separate image endpoint if configured
        endpoint = os.getenv("AZURE_IMAGE_ENDPOINT") or os.getenv("AZURE_AI_ENDPOINT")
        api_key = os.getenv("AZURE_IMAGE_API_KEY") or os.getenv("AZURE_AI_API_KEY")
        
        if not endpoint or not api_key:
            return "https://dummyimage.com/600x400/ff69b4/ffffff&text=Config+Missing"
        
        # Create anime-style prompt from story
        prompt = f"Vibrant anime-style illustration: {story[:200]}. Bright colors, expressive characters, dynamic composition."
        
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        
        payload = {
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1,
            "quality": "medium"
        }
        
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        
        # Log response for debugging
        if response.status_code != 200:
            print(f"Image API error {response.status_code}: {response.text}")
        
        response.raise_for_status()
        result = response.json()
        
        if "data" in result and len(result["data"]) > 0:
            # Azure returns either 'url' or 'b64_json'
            image_data = result["data"][0]
            print(f"Image data keys: {image_data.keys()}")
            
            if "url" in image_data:
                return image_data["url"]
            elif "b64_json" in image_data:
                # Return full base64 data URL for inline display
                return f"data:image/png;base64,{image_data['b64_json']}"
            else:
                return "https://dummyimage.com/600x400/ff69b4/ffffff&text=No+URL+or+B64"
        else:
            return "https://dummyimage.com/600x400/ff69b4/ffffff&text=No+Image+Data"
            
    except Exception as e:
        # Fallback to placeholder if image generation fails
        print(f"Image generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"https://dummyimage.com/600x400/ff69b4/ffffff&text=Error"