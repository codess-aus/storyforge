# StoryForge

A collaborative, AI-powered story writing and illustration platform.

## Features

- **Creative Prompts:** Powered by Generative AI (AI Foundry).
- **Multi-Agent:** Prompt, Editor, and Illustrator agents, each powered by AI.
- **Safe & Responsible:** Content moderation and versioned edits.
- **Modern Look:** Styled after GitHub Universe.
- **Simple & Extensible:** MkDocs for docs, FastAPI for agents, ready for Azure.

## Quickstart

1. **Install Python dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

2. **Run the FastAPI app:**
    ```sh
    uvicorn app.main:app --reload
    ```

3. **Build and serve the MkDocs site:**
    ```sh
    mkdocs serve
    ```

4. **Edit stories in `/docs/chapters/` as Markdown files.**

## Responsible AI & Security

See [docs/responsible_ai.md](docs/responsible_ai.md) and [SECURITY.md](SECURITY.md) for details and upgrade paths.

## Interesting Facts

- Each story is a Markdown file, versioned in GitHub—making edits and collaboration transparent and safe.
- Agents are modular for easy AI upgrades.
- The GitHub Universe-inspired style makes the app both modern and familiar.

---