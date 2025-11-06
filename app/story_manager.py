"""
Story management using GitHub as storage backend.
Saves stories to docs/chapters/ folder for automatic MkDocs publishing.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from github import Github, GithubException
import re

def get_github_client():
    """Initialize and return GitHub client."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not set in environment")
    return Github(token)

def get_repo():
    """Get the configured repository."""
    repo_name = os.getenv("GITHUB_REPO")
    if not repo_name:
        raise ValueError("GITHUB_REPO not set in environment")
    
    client = get_github_client()
    return client.get_repo(repo_name)

def slugify(title: str) -> str:
    """Convert title to URL-safe slug."""
    # Remove special characters and convert to lowercase
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    # Replace spaces with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def save_story(title: str, content: str, author: str = "anonymous") -> Dict:
    """
    Save a story to GitHub repository.
    
    Args:
        title: Story title
        content: Story content (markdown)
        author: Author name/identifier
        
    Returns:
        Dict with story metadata including URL
    """
    repo = get_repo()
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = slugify(title)
    filename = f"{timestamp}-{slug}.md"
    filepath = f"docs/chapters/{filename}"
    
    # Create markdown content with frontmatter
    frontmatter = f"""---
title: "{title}"
author: "{author}"
date: "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
---

"""
    full_content = frontmatter + content
    
    # Commit to repository
    try:
        repo.create_file(
            path=filepath,
            message=f"Add story: {title}",
            content=full_content,
            branch="main"
        )
        
        # Return metadata
        return {
            "id": filename.replace('.md', ''),
            "title": title,
            "author": author,
            "filename": filename,
            "filepath": filepath,
            "url": f"https://codess-aus.github.io/storyforge/chapters/{filename.replace('.md', '')}",
            "created_at": datetime.now().isoformat()
        }
    except GithubException as e:
        raise Exception(f"Failed to save story to GitHub: {str(e)}")

def list_stories() -> List[Dict]:
    """
    List all stories from the chapters folder.
    
    Returns:
        List of story metadata dicts
    """
    repo = get_repo()
    
    try:
        contents = repo.get_contents("docs/chapters")
        stories = []
        
        for content_file in contents:
            if content_file.name.endswith('.md') and content_file.name != 'index.md':
                # Get file content to parse frontmatter
                file_content = content_file.decoded_content.decode('utf-8')
                
                # Parse frontmatter
                metadata = parse_frontmatter(file_content)
                metadata['id'] = content_file.name.replace('.md', '')
                metadata['filename'] = content_file.name
                metadata['url'] = f"https://codess-aus.github.io/storyforge/chapters/{content_file.name.replace('.md', '')}"
                
                stories.append(metadata)
        
        # Sort by date, newest first
        stories.sort(key=lambda x: x.get('date', ''), reverse=True)
        return stories
        
    except GithubException as e:
        if e.status == 404:
            return []  # Directory doesn't exist or is empty
        raise Exception(f"Failed to list stories: {str(e)}")

def get_story(story_id: str) -> Optional[Dict]:
    """
    Retrieve a specific story by ID.
    
    Args:
        story_id: Story identifier (filename without .md)
        
    Returns:
        Dict with story content and metadata, or None if not found
    """
    repo = get_repo()
    filename = f"{story_id}.md"
    filepath = f"docs/chapters/{filename}"
    
    try:
        file_content = repo.get_contents(filepath)
        content = file_content.decoded_content.decode('utf-8')
        
        # Split frontmatter and content
        metadata = parse_frontmatter(content)
        story_content = content.split('---', 2)[2].strip() if content.count('---') >= 2 else content
        
        return {
            "id": story_id,
            "filename": filename,
            "title": metadata.get('title', 'Untitled'),
            "author": metadata.get('author', 'anonymous'),
            "date": metadata.get('date', ''),
            "content": story_content,
            "url": f"https://codess-aus.github.io/storyforge/chapters/{story_id}"
        }
        
    except GithubException as e:
        if e.status == 404:
            return None
        raise Exception(f"Failed to retrieve story: {str(e)}")

def update_story(story_id: str, title: str, content: str, author: str = "anonymous") -> Dict:
    """
    Update an existing story.
    
    Args:
        story_id: Story identifier (filename without .md)
        title: Updated title
        content: Updated content
        author: Author name
        
    Returns:
        Dict with updated story metadata
    """
    repo = get_repo()
    filename = f"{story_id}.md"
    filepath = f"docs/chapters/{filename}"
    
    # Create updated content with frontmatter
    frontmatter = f"""---
title: "{title}"
author: "{author}"
date: "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
updated: "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
---

"""
    full_content = frontmatter + content
    
    try:
        # Get current file to get its SHA
        existing_file = repo.get_contents(filepath)
        
        # Update file
        repo.update_file(
            path=filepath,
            message=f"Update story: {title}",
            content=full_content,
            sha=existing_file.sha,
            branch="main"
        )
        
        return {
            "id": story_id,
            "title": title,
            "author": author,
            "filename": filename,
            "filepath": filepath,
            "url": f"https://codess-aus.github.io/storyforge/chapters/{story_id}",
            "updated_at": datetime.now().isoformat()
        }
        
    except GithubException as e:
        raise Exception(f"Failed to update story: {str(e)}")

def delete_story(story_id: str) -> bool:
    """
    Delete a story.
    
    Args:
        story_id: Story identifier (filename without .md)
        
    Returns:
        True if deleted successfully
    """
    repo = get_repo()
    filename = f"{story_id}.md"
    filepath = f"docs/chapters/{filename}"
    
    try:
        # Get current file to get its SHA
        existing_file = repo.get_contents(filepath)
        
        # Delete file
        repo.delete_file(
            path=filepath,
            message=f"Delete story: {story_id}",
            sha=existing_file.sha,
            branch="main"
        )
        
        return True
        
    except GithubException as e:
        if e.status == 404:
            return False
        raise Exception(f"Failed to delete story: {str(e)}")

def parse_frontmatter(content: str) -> Dict:
    """
    Parse YAML frontmatter from markdown content.
    
    Args:
        content: Markdown content with frontmatter
        
    Returns:
        Dict of frontmatter key-value pairs
    """
    metadata = {}
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            frontmatter = parts[1].strip()
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    # Remove quotes and whitespace
                    value = value.strip().strip('"').strip("'")
                    metadata[key.strip()] = value
    
    return metadata
