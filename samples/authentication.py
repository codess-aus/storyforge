from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# For Serverless API or Managed Compute endpoints
client = ChatCompletionsClient(
    endpoint="https://storyforge-resource.cognitiveservices.azure.com/openai/deployments/storyforge-text",
    credential=AzureKeyCredential("<API_KEY>"),
    
)