const API_BASE = '/api';

function getAuthHeaders() {
  const token = localStorage.getItem('saas_access_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  };
}

export const api = {
  // Auth
  async login(email, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Login failed');
    }
    return res.json();
  },

  async register(email, password, full_name) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, full_name })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Registration failed');
    }
    return res.json();
  },

  async getMe() {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) return null;
    return res.json();
  },

  // Industries & Dynamic Options
  async getIndustries() {
    const res = await fetch(`${API_BASE}/industries`);
    return res.json();
  },

  async getIndustryOptions(industryId) {
    const res = await fetch(`${API_BASE}/industries/${industryId}/options`);
    return res.json();
  },

  // Business & Brand Memory
  async getBusinessProfile() {
    const res = await fetch(`${API_BASE}/business`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) return null;
    return res.json();
  },

  async updateBusinessProfile(profileData) {
    const res = await fetch(`${API_BASE}/business`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(profileData)
    });
    if (!res.ok) throw new Error('Failed to update brand profile');
    return res.json();
  },

  // Content Generation
  async generateContent(payload) {
    const apiKey = localStorage.getItem('user_gemini_key') || '';
    const res = await fetch(`${API_BASE}/content/generate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        ...payload,
        custom_api_key: apiKey
      })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Generation failed');
    }
    return res.json();
  },

  async regenerateContent(contentId, tweaks = {}) {
    const apiKey = localStorage.getItem('user_gemini_key') || '';
    const res = await fetch(`${API_BASE}/content/regenerate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        content_id: contentId,
        ...tweaks,
        custom_api_key: apiKey
      })
    });
    if (!res.ok) throw new Error('Regeneration failed');
    return res.json();
  },

  async updateContent(contentId, updates) {
    const res = await fetch(`${API_BASE}/content/${contentId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(updates)
    });
    if (!res.ok) throw new Error('Failed to update content');
    return res.json();
  },

  async deleteContent(contentId) {
    const res = await fetch(`${API_BASE}/content/${contentId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to delete content');
    return res.json();
  },

  async getHistory(filters = {}) {
    const params = new URLSearchParams();
    if (filters.industry) params.append('industry', filters.industry);
    if (filters.platform) params.append('platform', filters.platform);
    if (filters.search) params.append('search', filters.search);

    const res = await fetch(`${API_BASE}/content/history?${params.toString()}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) return [];
    return res.json();
  },

  async getContentById(contentId) {
    const res = await fetch(`${API_BASE}/content/${contentId}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Content not found');
    return res.json();
  },

  // Image Generation
  async generateAgentPrompt(userInput) {
    const apiKey = localStorage.getItem('user_gemini_key') || '';
    const res = await fetch(`${API_BASE}/content/agent-prompt`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        user_input: userInput,
        custom_api_key: apiKey
      })
    });
    if (!res.ok) throw new Error('Agent prompt generation failed');
    return res.json();
  },

  async generateImage(payload) {
    const apiKey = ''; // Image credentials are configured on the server.
    const res = await fetch(`${API_BASE}/image/generate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        ...payload,
        custom_api_key: apiKey
      })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Image generation failed');
    }
    return res.json();
  },

  // Usage Stats
  async getUsage() {
    const res = await fetch(`${API_BASE}/usage`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) return null;
    return res.json();
  }
};
