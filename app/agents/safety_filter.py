"""
Safety Filter Agent

Basic keyword-based filter for demonstration.
In production, use AI Foundry's robust moderation/content safety API.
"""
def content_is_safe(story: str) -> bool:
    # Example: Simple banned word check. Replace with advanced AI moderation.
    banned_words = ["violence", "hate", "explicit"]
    return not any(word in story.lower() for word in banned_words)