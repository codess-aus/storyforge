curl -X POST "https://ai-agentworkshophub566567976778.cognitiveservices.azure.com/openai/deployments/storyforge-image/images/generations?api-version=2025-04-01-preview" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_IMAGE_API_KEY" \
  -d '{
     "prompt" : "A photograph of a red fox in an autumn forest",
     "size" : "1024x1024",
     "quality" : "medium",
     "output_compression" : 100,
     "output_format" : "png",
     "n" : 1
    }' | jq -r '.data[0].b64_json' | base64 --decode > generated_image.png