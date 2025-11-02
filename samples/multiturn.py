import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
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
        AssistantMessage(content="Paris, the capital of France, is known for its stunning architecture, art museums, historical landmarks, and romantic atmosphere. Here are some of the top attractions to see in Paris:\n\n1. The Eiffel Tower: The iconic Eiffel Tower is one of the most recognizable landmarks in the world and offers breathtaking views of the city.\n2. The Louvre Museum: The Louvre is one of the worlds largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.\n3. Notre-Dame Cathedral: This beautiful cathedral is one of the most famous landmarks in Paris and is known for its Gothic architecture and stunning stained glass windows.\n\nThese are just a few of the many attractions that Paris has to offer. With so much to see and do, its no wonder that Paris is one of the most popular tourist destinations in the world."),
        UserMessage(content="What is so great about #1?")
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=model_name
)

print(response.choices[0].message.content)