import React, { useState, useEffect } from 'react';
import { 
  Building2, 
  Save, 
  Check
} from 'lucide-react';
import { api } from '../api';

export default function BrandProfileView({ brandProfile, onProfileUpdated }) {
  const [profile, setProfile] = useState({
    business_name: '',
    industry: 'restaurant',
    description: '',
    location: '',
    phone: '',
    website: '',
    brand_colors: '#D97757, #172033',
    preferred_language: 'telugu',
    preferred_tone: 'premium',
    default_cta: 'Order Now or Visit Us Today!'
  });
  const [saving, setSaving] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    if (brandProfile) {
      setProfile({
        business_name: brandProfile.business_name || '',
        industry: brandProfile.industry || 'restaurant',
        description: brandProfile.description || '',
        location: brandProfile.location || '',
        phone: brandProfile.phone || '',
        website: brandProfile.website || '',
        brand_colors: brandProfile.brand_colors || '#D97757, #172033',
        preferred_language: brandProfile.preferred_language || 'telugu',
        preferred_tone: brandProfile.preferred_tone || 'premium',
        default_cta: brandProfile.default_cta || 'Order Now or Visit Us Today!'
      });
    }
  }, [brandProfile]);

  const handleChange = (field, val) => {
    setProfile(prev => ({ ...prev, [field]: val }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSuccessMessage('');
    try {
      const updated = await api.updateBusinessProfile(profile);
      onProfileUpdated(updated);
      setSuccessMessage('Brand profile saved. All future campaigns will automatically include this context.');
      setTimeout(() => setSuccessMessage(''), 4000);
    } catch (err) {
      alert('Failed to save brand profile');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{ maxWidth: '780px', margin: '0 auto' }}>
      <div style={{ marginBottom: '1.75rem' }}>
        <h2 className="editorial-heading" style={{ fontSize: '1.75rem' }}>
          Brand Profile
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginTop: '2px' }}>
          Save your business information once to have it automatically included in every marketing campaign.
        </p>
      </div>

      {successMessage && (
        <div style={{
          background: 'var(--accent-sage-soft)',
          border: '1px solid rgba(120, 146, 122, 0.3)',
          borderRadius: 'var(--radius-sm)',
          padding: '0.75rem 1rem',
          color: 'var(--color-success)',
          marginBottom: '1.25rem',
          fontSize: '0.85rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          <Check size={16} />
          <span>{successMessage}</span>
        </div>
      )}

      <form onSubmit={handleSave} className="card" style={{ padding: '2rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.25rem', marginBottom: '1.25rem' }}>
          <div className="form-group">
            <label className="form-label">Business / Brand Name *</label>
            <input
              type="text"
              required
              className="form-input"
              value={profile.business_name}
              onChange={(e) => handleChange('business_name', e.target.value)}
              placeholder="e.g. Royal Spice Restaurant"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Primary Industry</label>
            <select
              className="form-select"
              value={profile.industry}
              onChange={(e) => handleChange('industry', e.target.value)}
            >
              <option value="restaurant">Restaurant & Food</option>
              <option value="clothing">Clothing & Fashion</option>
              <option value="real_estate">Real Estate & Housing</option>
              <option value="salon">Salon & Spa</option>
              <option value="electronics">Electronics & Gadgets</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Business Description / Specialization</label>
          <textarea
            className="form-textarea"
            rows={3}
            value={profile.description}
            onChange={(e) => handleChange('description', e.target.value)}
            placeholder="e.g. Authentic Hyderabadi Dum Biryani, royal spices, and family dining."
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem', marginBottom: '1.25rem' }}>
          <div className="form-group">
            <label className="form-label">Location / Address</label>
            <input
              type="text"
              className="form-input"
              value={profile.location}
              onChange={(e) => handleChange('location', e.target.value)}
              placeholder="e.g. Jubilee Hills, Hyderabad"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Phone / WhatsApp</label>
            <input
              type="text"
              className="form-input"
              value={profile.phone}
              onChange={(e) => handleChange('phone', e.target.value)}
              placeholder="e.g. +91 98765 43210"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Website</label>
            <input
              type="text"
              className="form-input"
              value={profile.website}
              onChange={(e) => handleChange('website', e.target.value)}
              placeholder="https://example.com"
            />
          </div>
        </div>

        <div style={{ paddingTop: '1.25rem', borderTop: '1px solid var(--border-warm)', marginBottom: '1.25rem' }}>
          <h4 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.85rem' }}>
            Defaults
          </h4>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
            <div className="form-group">
              <label className="form-label">Default Language</label>
              <select
                className="form-select"
                value={profile.preferred_language}
                onChange={(e) => handleChange('preferred_language', e.target.value)}
              >
                <option value="telugu">Telugu (తెలుగు)</option>
                <option value="hindi">Hindi (हिन्दी)</option>
                <option value="english">English</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Default Voice & Style</label>
              <select
                className="form-select"
                value={profile.preferred_tone}
                onChange={(e) => handleChange('preferred_tone', e.target.value)}
              >
                <option value="premium">Premium</option>
                <option value="friendly">Friendly</option>
                <option value="energetic">Bold</option>
                <option value="professional">Elegant</option>
                <option value="funny">Playful</option>
                <option value="minimal">Minimal</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Default Call To Action</label>
              <input
                type="text"
                className="form-input"
                value={profile.default_cta}
                onChange={(e) => handleChange('default_cta', e.target.value)}
                placeholder="e.g. Call to Book Your Table or Order Online!"
              />
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button
            type="submit"
            disabled={saving}
            className="btn-primary"
          >
            <Save size={15} />
            <span>{saving ? 'Saving...' : 'Save Profile'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
