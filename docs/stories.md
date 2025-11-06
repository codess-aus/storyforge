# Story Gallery

Browse all the stories created with StoryForge!

<div id="stories-container">
  <p>Loading stories...</p>
</div>

<style>
  #stories-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }

  .story-card {
    background: #f5f5f5;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    border-left: 4px solid #6f42c1;
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .story-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }

  .story-title {
    font-size: 24px;
    font-weight: bold;
    color: #6f42c1;
    margin-bottom: 10px;
  }

  .story-meta {
    color: #666;
    font-size: 14px;
    margin-bottom: 15px;
  }

  .story-preview {
    color: #333;
    line-height: 1.6;
    margin-bottom: 15px;
  }

  .story-actions {
    display: flex;
    gap: 10px;
  }

  .btn {
    background: #6f42c1;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
  }

  .btn:hover {
    background: #5a32a3;
  }

  .btn-secondary {
    background: #28a745;
  }

  .btn-secondary:hover {
    background: #218838;
  }

  .loading {
    text-align: center;
    padding: 40px;
    color: #666;
  }

  .error {
    background: #f8d7da;
    color: #721c24;
    padding: 15px;
    border-radius: 6px;
    margin: 20px 0;
  }

  .no-stories {
    text-align: center;
    padding: 40px;
    color: #666;
  }

  .filter-bar {
    background: white;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .filter-bar input {
    width: 100%;
    padding: 10px;
    border: 2px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
  }
</style>

<script>
  const API_BASE = 'https://storyforge-api.jollyflower-0fc4b005.swedencentral.azurecontainerapps.io';

  async function loadStories() {
    const container = document.getElementById('stories-container');
    
    try {
      const response = await fetch(`${API_BASE}/stories`);
      const data = await response.json();
      
      if (!data.stories || data.stories.length === 0) {
        container.innerHTML = `
          <div class="no-stories">
            <h2>No stories yet!</h2>
            <p>Be the first to write a story.</p>
            <a href="/storyforge/write/" class="btn">Start Writing</a>
          </div>
        `;
        return;
      }
      
      // Create filter bar
      let html = `
        <div class="filter-bar">
          <input type="text" id="search-input" placeholder="Search stories by title or author..." onkeyup="filterStories()">
        </div>
        <div id="stories-list">
      `;
      
      // Add story cards
      for (const story of data.stories) {
        const title = story.title || 'Untitled';
        const author = story.author || 'anonymous';
        const date = story.date ? new Date(story.date).toLocaleDateString() : 'Unknown date';
        
        html += `
          <div class="story-card" data-title="${title.toLowerCase()}" data-author="${author.toLowerCase()}">
            <div class="story-title">${escapeHtml(title)}</div>
            <div class="story-meta">
              By <strong>${escapeHtml(author)}</strong> • ${date}
            </div>
            <div class="story-actions">
              <a href="${story.url}" class="btn" target="_blank">Read Story</a>
              <button onclick="editStory('${story.id}')" class="btn btn-secondary">Edit</button>
            </div>
          </div>
        `;
      }
      
      html += '</div>';
      container.innerHTML = html;
      
    } catch (error) {
      container.innerHTML = `
        <div class="error">
          Failed to load stories. Please try again later.
        </div>
      `;
      console.error('Error loading stories:', error);
    }
  }

  function filterStories() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const cards = document.querySelectorAll('.story-card');
    
    cards.forEach(card => {
      const title = card.getAttribute('data-title');
      const author = card.getAttribute('data-author');
      
      if (title.includes(searchTerm) || author.includes(searchTerm)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  }

  async function editStory(storyId) {
    try {
      const response = await fetch(`${API_BASE}/stories/${storyId}`);
      const story = await response.json();
      
      // Store in sessionStorage and redirect to write page
      sessionStorage.setItem('editStory', JSON.stringify(story));
      window.location.href = '/storyforge/write/';
      
    } catch (error) {
      alert('Failed to load story for editing');
      console.error(error);
    }
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Load stories on page load
  loadStories();
</script>
