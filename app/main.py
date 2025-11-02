"""
FastAPI app for StoryForge multi-agent backend.

This file defines endpoints for each agent:
- /prompt: Suggests a creative writing prompt.
- /filter: Runs the safety/content filter.
- /editor: Proposes improvements to submitted stories.
- /illustrate: Generates a vibrant, anime-style illustration.

Each agent is modular, making it easy to scale or swap out as needed.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body

# Load environment variables
load_dotenv()
from app.agents.prompt_agent import generate_prompt
from app.agents.editor_agent import suggest_edits
from app.agents.illustrator_agent import generate_illustration
from app.agents.safety_filter import content_is_safe

app = FastAPI(title="StoryForge Agents API")

@app.get("/prompt")
def get_prompt(user_id: str = "guest"):
    "Prompt Agent: Returns a creative writing prompt."
    return {"prompt": generate_prompt(user_id)}

@app.post("/filter")
def filter_content(story: str = Body(..., embed=True)):
    "Safety Filter Agent: Checks if story is appropriate."
    if not content_is_safe(story):
        raise HTTPException(status_code=400, detail="Content flagged by safety filter.")
    return {"status": "ok"}

@app.post("/editor")
def edit_story(story: str = Body(..., embed=True)):
    "Editor Agent: Suggests improvements/alternatives to the story."
    return {"suggestions": suggest_edits(story)}

@app.post("/illustrate")
def illustrate_story(story: str = Body(..., embed=True)):
    """
    Illustrator Agent: Returns a URL to a generated anime-style illustration.
    Always uses vibrant colors.
    """
    return {"image_url": generate_illustration(story)}