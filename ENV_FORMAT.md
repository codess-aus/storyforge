# Environment Variable Configuration Guide

## Correct Format for .env

Your `.env` file should use these formats:

### Text/Chat Model Endpoint
```properties
# Include everything UP TO the deployment name (no /chat/completions or query params)
AZURE_AI_ENDPOINT=https://storyforge-resource.cognitiveservices.azure.com/openai/deployments/storyforge-text
AZURE_AI_API_KEY=your-key-here
```

### Image Model Endpoint
```properties
# For image generation, include the full path with API version
AZURE_IMAGE_ENDPOINT=https://ai-agentworkshophub566567976778.cognitiveservices.azure.com/openai/deployments/storyforge-image/images/generations?api-version=2025-04-01-preview
AZURE_IMAGE_API_KEY=your-key-here
```

## What Azure AI Foundry Gives You

When you copy from Azure AI Foundry portal, you might get:
```
https://myresource.cognitiveservices.azure.com/openai/deployments/my-model/chat/completions?api-version=2025-01-01-preview
```

**For this app, remove the `/chat/completions?api-version=...` part:**
```
https://myresource.cognitiveservices.azure.com/openai/deployments/my-model
```

The azure-ai-inference SDK adds the rest automatically.
