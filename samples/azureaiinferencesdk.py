import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://storyforge-resource.cognitiveservices.azure.com/openai/deployments/storyforge-text"
model_name = "storyforge-text"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential("<API_KEY>"),
    
)

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="I am going to Paris, what should I see?"),
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=model_name
)

print(response.choices[0].message.content)