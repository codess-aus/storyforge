I want to create a MVP Azure App. It should initially be created using mkdocs and published to pages - but as we build it out, it should be deployed to Azure. It must use Generative AI via AI Foundry to prompt the user to write stories, which should be stored in GitHub, as chapters in mkdocs, and they should be editable after they have been recorded. The app should be multi-agent, because after the story is written, another agent should propose different versions of the story, to upgrade or improve what the writer has submitted. Another agent could provide an illustration for the story. The illustration should always be in anime style, using vibrant colours. So a prompt agent, a editor agent and an illustrator agent. The app should be responsive, it should look modern, it should be accessible. I would also like the app to use content and safety filters from AI Foundry and it's architecture should demonstrate how it is a responsible, trustworthy app. The app should be as simple as possible, be built as cheaply as possible. It should be secure, but in a simple way - with docs explaining how it could be upgraded to enterprise ready. The design of the website should mimic the GitHub Universe website for styling and colour scheme, as closely as possible. 

1. MVP Overview & Context
Purpose:
A collaborative, story-writing web app using Generative AI to prompt, review, and illustrate user submissions, all managed as chapters in an mkdocs-based documentation site.
Workflow:
Prompt Agent: Asks user to write a story, leveraging AI Foundry for creative prompts & content filtering.
Editor Agent: Reviews and suggests improvements/alternate versions.
Illustrator Agent: Generates vibrant anime-style illustrations for each chapter.
Storage: Each story/chapter is stored as a Markdown file in GitHub, rendered by mkdocs.
Editability: Users can edit their stories post-submission.
Modern UI: Styled after GitHub Universe, responsive, accessible.
Responsible AI: Content/safety filters and clear documentation on trustworthiness.
Azure-Ready: Initial deployment to GitHub Pages; transition plan for Azure.
2. Tech Stack Choices
Frontend:
mkdocs-material (theme: matches GitHub Universe style, responsive, accessible)
Custom JS/CSS for enhanced UI/UX
Azure Static Web Apps (future deployment)
Backend (for AI & multi-agent orchestration):
Python FastAPI (lightweight, async, easy Azure deployment)
AI Foundry SDK for Generative AI, content/safety filtering, multi-agent orchestration
Note: MVP can start with GitHub Actions/Workflows to simulate agent orchestration.
Storage:
Stories as Markdown in GitHub repo (managed by mkdocs)
Images stored in same repo or Azure Blob (future-proof)
Security:
GitHub authentication for contributors (MVP)
Docs for upgrading to OAuth/Enterprise security
3. Architecture Diagram (MVP)
Mermaid
flowchart TD
    A[User] -->|Story Prompt| B(Prompt Agent <br>AI Foundry)
    B -->|Prompt| C[User]
    C -->|Story| D[GitHub - Mkdocs]
    D -->|New Chapter| E[Editor Agent]
    E -->|Suggestions| C
    D -->|Chapter| F[Illustrator Agent]
    F -->|Anime Illustration| D
    D -->|Published| G[mkdocs-material Site]
4. MVP Implementation Plan
a) Mkdocs Setup
Initialize a new repo with mkdocs-material theme.
Set up GitHub Pages for deployment.
Example mkdocs.yml for GitHub Universe-like look:
YAML
site_name: StoryForge
theme:
  name: material
  custom_dir: theme
  palette:
    - scheme: default
      primary: blue
      accent: indigo
      toggle:
        icon: material/lightbulb
        name: Switch to dark mode
    - scheme: slate
      primary: deep purple
      accent: pink
      toggle:
        icon: material/lightbulb-outline
        name: Switch to light mode
extra_css:
  - styles/github-universe.css
Interesting Fact:
mkdocs-material is one of the most customizable and accessible doc themes, making it perfect for mimicking GitHub Universe and building modern, responsive sites.

b) Agent Orchestration (Python FastAPI Example)
Each agent is a FastAPI endpoint:
/prompt – uses AI Foundry to generate creative prompts and filter input
/editor – proposes alternate/improved versions
/illustrator – generates anime images (calls AI Foundry image API)

app/main.py
v1
from fastapi import FastAPI, HTTPException
from ai_foundry_sdk import AIFPrompt, AIFEditor, AIFIllustrator, AIFSafetyFilter

app = FastAPI()

@app.post("/prompt")
Interesting Fact:
Using separate endpoints for each agent allows for easy scaling—each agent can be upgraded, swapped, or run independently as you move toward Azure or more advanced orchestration.

c) GitHub Integration for Chapters
Use PyGithub or GitHub API to push new/updated chapters (Markdown files) into the repo.
Example function to add a chapter:

app/github_utils.py
v1
from github import Github

def add_chapter(repo_name, token, chapter_title, content_md):
    g = Github(token)
    repo = g.get_repo(repo_name)
    file_path = f"docs/chapters/{chapter_title.replace(' ', '_')}.md"
d) Frontend (mkdocs) UX Enhancements
Custom JS for interactive prompts, edits, and image display.
Use mkdocs-macros-plugin for dynamic content (e.g., listing recent stories).
Accessibility: Use ARIA labels, high contrast, keyboard navigation.
e) Responsible AI & Safety
Every input/output run through AI Foundry’s safety filters.
Display “AI-generated, content filtered” badges.
MVP docs: Section on “Responsible AI” and security, with upgrade paths to SSO, audit logging, etc.
5. Docs: How to Upgrade to Enterprise Security
Add a SECURITY.md doc with:
How to integrate Azure Active Directory for SSO
Enabling Azure Key Vault for secrets
Audit log hooks for all agent actions
API rate limiting and monitoring
Guidelines for regular AI model evaluations
6. Deployment Plan
MVP:
Deploy mkdocs to GitHub Pages (free, fast)
Agents can run as Azure Functions or small FastAPI app (Azure App Service/Container Apps for future scaling)
Future:
Deploy entire app as Azure Static Web App + Azure API Management + Azure Functions
Use Azure Blob for illustration/image storage
7. Modern Look: GitHub Universe Styling
GitHub Universe’s color palette: blue, deep purple, pink accents, dark/light toggle.
Use mkdocs-material palette settings and custom CSS for extra polish.
8. Next Steps: Kickoff Files
Would you like to see:

The initial mkdocs.yml, sample homepage, and a minimal FastAPI agent backend scaffold?
Or the full repo structure and a sample agent workflow