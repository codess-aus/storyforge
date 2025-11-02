# Azure Deployment Guide

## Option 1: Azure Container Apps (Recommended for MVP)

**Why:** Serverless, auto-scaling, cost-effective, easy container deployment.

### Prerequisites
- Azure CLI installed: `az login`
- Docker installed

### Steps

1. **Create a resource group:**
   ```bash
   az group create --name storyforge-rg --location eastus
   ```

2. **Create a container registry:**
   ```bash
   az acr create --resource-group storyforge-rg --name storyforgeacr --sku Basic
   ```

3. **Build and push Docker image:**
   ```bash
   az acr build --registry storyforgeacr --image storyforge-api:latest .
   ```

4. **Create Container Apps environment:**
   ```bash
   az containerapp env create --name storyforge-env --resource-group storyforge-rg --location eastus
   ```

5. **Deploy the API:**
   ```bash
   az containerapp create \
     --name storyforge-api \
     --resource-group storyforge-rg \
     --environment storyforge-env \
     --image storyforgeacr.azurecr.io/storyforge-api:latest \
     --target-port 8000 \
     --ingress external \
     --registry-server storyforgeacr.azurecr.io \
     --env-vars AZURE_AI_ENDPOINT=secretref:ai-endpoint AZURE_AI_API_KEY=secretref:ai-key
   ```

6. **Set secrets:**
   ```bash
   az containerapp secret set --name storyforge-api --resource-group storyforge-rg \
     --secrets ai-endpoint=<your-endpoint> ai-key=<your-key>
   ```

## Option 2: Azure App Service

**Why:** Simpler if you're not using containers, built-in CI/CD.

### Steps

1. **Create App Service Plan:**
   ```bash
   az appservice plan create --name storyforge-plan --resource-group storyforge-rg --sku B1 --is-linux
   ```

2. **Create Web App:**
   ```bash
   az webapp create --resource-group storyforge-rg --plan storyforge-plan \
     --name storyforge-api --runtime "PYTHON:3.12"
   ```

3. **Configure environment variables:**
   ```bash
   az webapp config appsettings set --resource-group storyforge-rg --name storyforge-api \
     --settings AZURE_AI_ENDPOINT=<your-endpoint> AZURE_AI_API_KEY=<your-key>
   ```

4. **Deploy code:**
   ```bash
   az webapp up --name storyforge-api --resource-group storyforge-rg --runtime "PYTHON:3.12"
   ```

## Dockerfile (needed for Container Apps)

Create this file in your project root:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Security Best Practices

- Use Azure Key Vault for secrets
- Enable Managed Identity for Azure resources
- Set up Azure Front Door for DDoS protection
- Enable Application Insights for monitoring

See [docs/responsible_ai.md](docs/responsible_ai.md) for more security guidance.
