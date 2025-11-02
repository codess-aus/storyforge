# Setup Guide

## Prerequisites

- Python 3.12+
- Git
- Azure AI Foundry account (or Azure OpenAI)
- GitHub account

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

3. **Get your Azure AI credentials (text/chat models):**
   - Go to [Azure AI Foundry](https://ai.azure.com/)
   - Create a project or use an existing one
   - Get your endpoint and API key from the project settings
   - Update `AZURE_AI_ENDPOINT` and `AZURE_AI_API_KEY` in `.env`

4. **(If image model is in a different region) Add image endpoint/key:**
   - Deploy `gpt-image-1` (or chosen image model) in any supported region.
   - Copy its endpoint & key into `AZURE_IMAGE_ENDPOINT` and `AZURE_IMAGE_API_KEY`.
   - If image model shares the same resource, you can leave these blank.

5. **Get your GitHub token (optional, for auto-committing stories):**
   - Go to [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
   - Create a new token with `repo` scope
   - Update `GITHUB_TOKEN` in `.env`

## Running the Application

### Start the FastAPI backend:
```bash
uvicorn app.main:app --reload --port 8001
```

API will be available at: http://localhost:8001
API docs at: http://localhost:8001/docs

### Start the MkDocs site:
```bash
mkdocs serve
```

Documentation site will be available at: http://localhost:8000

## Testing the Agents

Once the API is running, test each agent:

- **Prompt Agent:** `GET http://localhost:8001/prompt?user_id=guest`
- **Safety Filter:** `POST http://localhost:8001/filter` with JSON body: `{"story": "your text"}`
- **Editor Agent:** `POST http://localhost:8001/editor` with JSON body: `{"story": "your story"}`
- **Illustrator Agent:** `POST http://localhost:8001/illustrate` with JSON body: `{"story": "your story"}`

If you have a separate image endpoint/key, the illustrator agent code will need to choose which base URL to call (text vs image). For now it's stubbed; later replace with real SDK calls using:
```python
image_endpoint = os.getenv("AZURE_IMAGE_ENDPOINT") or os.getenv("AZURE_AI_ENDPOINT")
image_key = os.getenv("AZURE_IMAGE_API_KEY") or os.getenv("AZURE_AI_API_KEY")
```

## Next Steps

- Add your first story as a markdown file in `docs/chapters/`
- Integrate real AI Foundry SDK calls in the agent files
- Deploy to GitHub Pages (documentation)
- Deploy API to Azure (App Service or Container Apps)

See [docs/MVP.md](docs/MVP.md) for architecture details.
