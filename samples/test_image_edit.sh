curl -X POST "https://ai-agentworkshophub566567976778.cognitiveservices.azure.com/openai/deployments/storyforge-image/images/edits?api-version=2025-04-01-preview" \
  -H "Authorization: Bearer $AZURE_API_KEY" \
  -F "image=@image_to_edit.png" \
  -F "mask=@mask.png" \
  -F "prompt=Make this black and white"  | jq -r '.data[0].b64_json' | base64 --decode > edited_image.png