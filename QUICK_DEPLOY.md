# Quick API Deployment to Azure

## Deploy FastAPI to Azure Container Apps

```bash
# 1. Build and push Docker image
az acr build --registry storyforgeacr \
  --image storyforge-api:latest \
  --file Dockerfile .

# 2. Deploy to Container Apps
az containerapp create \
  --name storyforge-api \
  --resource-group rg-storyforge \
  --environment storyforge-env \
  --image storyforgeacr.azurecr.io/storyforge-api:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server storyforgeacr.azurecr.io \
  --env-vars \
    AZURE_AI_ENDPOINT=secretref:ai-endpoint \
    AZURE_AI_API_KEY=secretref:ai-key \
    AZURE_IMAGE_ENDPOINT=secretref:image-endpoint \
    AZURE_IMAGE_API_KEY=secretref:image-key

# 3. Get the API URL
az containerapp show \
  --name storyforge-api \
  --resource-group rg-storyforge \
  --query properties.configuration.ingress.fqdn
```

## Update write.md with the deployed API URL

Once deployed, edit `docs/write.md` and change:
```javascript
const API_BASE = 'http://localhost:8001';
```

To:
```javascript
const API_BASE = 'https://your-api-url.azurecontainerapps.io';
```

Then commit and push to GitHub.
