# Write Your Story

!!! success "Live Production API"
    This interface is connected to the deployed StoryForge API on Azure Container Apps.
    
    - **API Endpoint:** https://storyforge-api.jollyflower-0fc4b005.swedencentral.azurecontainerapps.io
    - **Local Development:** Run `uvicorn app.main:app --reload --port 8001` and change API_BASE in the script section
    - **Deployment Guide:** See [QUICK_DEPLOY.md](https://github.com/codess-aus/storyforge/blob/main/QUICK_DEPLOY.md) for redeployment instructions.

<div id="story-app">
  <div class="prompt-section">
    <h2>📝 Get Inspired</h2>
    <button id="get-prompt-btn" class="btn">Get Writing Prompt</button>
    <div id="prompt-display" class="prompt-box"></div>
  </div>

  <div class="write-section">
    <h2>✍️ Write Your Story</h2>
    <textarea id="story-input" placeholder="Start writing your story here..." rows="15"></textarea>
    <div class="action-buttons">
      <button id="get-suggestions-btn" class="btn">Get Edit Suggestions</button>
      <button id="generate-image-btn" class="btn">Generate Illustration</button>
      <button id="save-story-btn" class="btn btn-primary">Save Story</button>
    </div>
  </div>

  <div class="suggestions-section" id="suggestions-section" style="display:none;">
    <h2>💡 Editor Suggestions</h2>
    <ul id="suggestions-list"></ul>
  </div>

  <div class="image-section" id="image-section" style="display:none;">
    <h2>🎨 Your Illustration</h2>
    <div id="image-display"></div>
  </div>
</div>

<style>
  #story-app {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
  }

  .prompt-section, .write-section, .suggestions-section, .image-section {
    background: #f5f5f5;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
  }

  .prompt-box {
    background: white;
    padding: 15px;
    border-radius: 6px;
    margin-top: 15px;
    min-height: 60px;
    border-left: 4px solid #6f42c1;
    font-style: italic;
  }

  #story-input {
    width: 100%;
    padding: 15px;
    border: 2px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    font-family: 'Georgia', serif;
    margin-bottom: 15px;
    resize: vertical;
  }

  .btn {
    background: #6f42c1;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    margin-right: 10px;
    margin-bottom: 10px;
  }

  .btn:hover {
    background: #5a32a3;
  }

  .btn-primary {
    background: #28a745;
  }

  .btn-primary:hover {
    background: #218838;
  }

  .btn:disabled {
    background: #ccc;
    cursor: not-allowed;
  }

  .action-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  #suggestions-list {
    list-style: none;
    padding: 0;
  }

  #suggestions-list li {
    background: white;
    padding: 12px;
    margin-bottom: 10px;
    border-radius: 6px;
    border-left: 3px solid #ffc107;
  }

  #image-display img {
    max-width: 100%;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }

  .loading {
    opacity: 0.6;
    pointer-events: none;
  }

  .error {
    color: #dc3545;
    padding: 10px;
    background: #f8d7da;
    border-radius: 6px;
    margin-top: 10px;
  }
</style>

<script>
  const API_BASE = 'https://storyforge-api.jollyflower-0fc4b005.swedencentral.azurecontainerapps.io';
  
  // Check if we're editing an existing story
  let editingStory = null;
  let generatedImage = null; // Store the generated image
  
  const editData = sessionStorage.getItem('editStory');
  if (editData) {
    editingStory = JSON.parse(editData);
    sessionStorage.removeItem('editStory');
    
    // Populate the editor
    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('story-input').value = editingStory.content;
      document.querySelector('h1').textContent = `Edit: ${editingStory.title}`;
      
      // Load existing image if available
      if (editingStory.image) {
        const section = document.getElementById('image-section');
        const display = document.getElementById('image-display');
        section.style.display = 'block';
        display.innerHTML = `<img src="${editingStory.image}" alt="Story illustration">`;
        generatedImage = editingStory.image;
      }
    });
  }

  document.getElementById('get-prompt-btn').addEventListener('click', async () => {
    const btn = document.getElementById('get-prompt-btn');
    const display = document.getElementById('prompt-display');
    
    btn.disabled = true;
    btn.textContent = 'Loading...';
    display.innerHTML = '<em>Generating creative prompt...</em>';
    
    try {
      const response = await fetch(`${API_BASE}/prompt?user_id=web-user`);
      const data = await response.json();
      display.textContent = data.prompt;
    } catch (error) {
      display.innerHTML = '<span class="error">Failed to load prompt. Make sure the API server is running.</span>';
    } finally {
      btn.disabled = false;
      btn.textContent = 'Get Writing Prompt';
    }
  });

  document.getElementById('get-suggestions-btn').addEventListener('click', async () => {
    const story = document.getElementById('story-input').value;
    const btn = document.getElementById('get-suggestions-btn');
    const section = document.getElementById('suggestions-section');
    const list = document.getElementById('suggestions-list');
    
    if (!story.trim()) {
      alert('Please write some story content first!');
      return;
    }
    
    btn.disabled = true;
    btn.textContent = 'Analyzing...';
    section.style.display = 'block';
    list.innerHTML = '<li>Getting suggestions...</li>';
    
    try {
      const response = await fetch(`${API_BASE}/editor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ story })
      });
      const data = await response.json();
      
      list.innerHTML = data.suggestions.map(s => `<li>${s}</li>`).join('');
    } catch (error) {
      list.innerHTML = '<li class="error">Failed to get suggestions. Make sure the API server is running.</li>';
    } finally {
      btn.disabled = false;
      btn.textContent = 'Get Edit Suggestions';
    }
  });

  document.getElementById('generate-image-btn').addEventListener('click', async () => {
    const story = document.getElementById('story-input').value;
    const btn = document.getElementById('generate-image-btn');
    const section = document.getElementById('image-section');
    const display = document.getElementById('image-display');
    
    if (!story.trim()) {
      alert('Please write some story content first!');
      return;
    }
    
    btn.disabled = true;
    btn.textContent = 'Generating Image (30-60s)...';
    section.style.display = 'block';
    display.innerHTML = '<p>Creating your anime-style illustration...</p>';
    
    try {
      const response = await fetch(`${API_BASE}/illustrate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ story })
      });
      const data = await response.json();
      
      display.innerHTML = `<img src="${data.image_url}" alt="Story illustration">`;
      // Store the generated image to save with story
      generatedImage = data.image_url;
    } catch (error) {
      display.innerHTML = '<p class="error">Failed to generate image. Make sure the API server is running.</p>';
    } finally {
      btn.disabled = false;
      btn.textContent = 'Generate Illustration';
    }
  });

  document.getElementById('save-story-btn').addEventListener('click', async () => {
    const story = document.getElementById('story-input').value;
    const btn = document.getElementById('save-story-btn');
    
    if (!story.trim()) {
      alert('Please write some story content first!');
      return;
    }
    
    // Get story title from user
    const defaultTitle = editingStory ? editingStory.title : 'My Story';
    const title = prompt('Enter a title for your story:', defaultTitle);
    if (!title) return;
    
    // Get author name (optional)
    const defaultAuthor = editingStory ? editingStory.author : 'anonymous';
    const author = prompt('Enter your name (optional):', defaultAuthor) || 'anonymous';
    
    btn.disabled = true;
    btn.textContent = 'Saving...';
    
    try {
      // Prepare story data with optional image
      const storyData = {
        title: title,
        content: story,
        author: author
      };
      
      // Add image if one was generated
      if (generatedImage) {
        storyData.image = generatedImage;
      }
      
      if (editingStory) {
        // Update existing story
        response = await fetch(`${API_BASE}/stories/${editingStory.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(storyData)
        });
      } else {
        // Create new story
        response = await fetch(`${API_BASE}/stories`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(storyData)
        });
      }
      
      if (!response.ok) {
        throw new Error('Failed to save story');
      }
      
      const data = await response.json();
      
      // Show success message with link
      const viewUrl = data.url;
      const action = editingStory ? 'updated' : 'saved';
      alert(`Story ${action} successfully!\n\nIt will be published at:\n${viewUrl}\n\n(Note: It may take 1-2 minutes for GitHub Pages to deploy)`);
      
      // Clear editing state
      editingStory = null;
      generatedImage = null;
      document.querySelector('h1').textContent = 'Write Your Story';
      
      // Clear the textarea and image
      if (confirm('Clear the editor?')) {
        document.getElementById('story-input').value = '';
        document.getElementById('image-section').style.display = 'none';
        document.getElementById('image-display').innerHTML = '';
      }
      
    } catch (error) {
      alert('Failed to save story. Please try again.');
      console.error(error);
    } finally {
      btn.disabled = false;
      btn.textContent = 'Save Story';
    }
  });
</script>
