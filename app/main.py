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

# Load environment variables FIRST before any other imports
load_dotenv()

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.agents.prompt_agent import generate_prompt
from app.agents.editor_agent import suggest_edits
from app.agents.illustrator_agent import generate_illustration
from app.agents.safety_filter import content_is_safe
from app.story_manager import (
    save_story,
    list_stories,
    get_story,
    update_story,
    delete_story
)

app = FastAPI(title="StoryForge Agents API")

# Enable CORS for local development and GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/prompt")
def get_prompt(user_id: str = "guest"):
    "Prompt Agent: Returns a creative writing prompt."
    # Debug: print endpoint being used
    endpoint = os.getenv("AZURE_AI_ENDPOINT", "NOT_SET")
    print(f"DEBUG: Using endpoint: {endpoint}")
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


# Story Management Models
class StoryCreate(BaseModel):
    title: str
    content: str
    author: str = "anonymous"

class StoryUpdate(BaseModel):
    title: str
    content: str
    author: str = "anonymous"


# Story Management Endpoints
@app.post("/stories")
def create_story(story: StoryCreate):
    """Save a new story to GitHub repository."""
    try:
        result = save_story(
            title=story.title,
            content=story.content,
            author=story.author
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stories")
def get_stories():
    """List all stories from the repository."""
    try:
        stories = list_stories()
        return {"stories": stories, "count": len(stories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stories/{story_id}")
def get_story_by_id(story_id: str):
    """Retrieve a specific story by ID."""
    try:
        story = get_story(story_id)
        if not story:
            raise HTTPException(status_code=404, detail="Story not found")
        return story
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/stories/{story_id}")
def update_story_by_id(story_id: str, story: StoryUpdate):
    """Update an existing story."""
    try:
        result = update_story(
            story_id=story_id,
            title=story.title,
            content=story.content,
            author=story.author
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/stories/{story_id}")
def delete_story_by_id(story_id: str):
    """Delete a story."""
    try:
        success = delete_story(story_id)
        if not success:
            raise HTTPException(status_code=404, detail="Story not found")
        return {"message": "Story deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))