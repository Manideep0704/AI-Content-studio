import React, { useState, useEffect } from 'react';
import { 
  Layers, 
  Search, 
  Trash2, 
  Copy, 
  Check, 
  Plus, 
  Eye,
  ArrowRight
} from 'lucide-react';
import { api } from '../api';

export default function HistoryView({ onViewContent, onEditContent, setView }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedIndustry, setSelectedIndustry] = useState('all');
  const [selectedPlatform, setSelectedPlatform] = useState('all');
  const [copiedId, setCopiedId] = useState('');

  const loadHistory = async () => {
    setLoading(true);
    try {
      const data = await api.getHistory({
        industry: selectedIndustry,
        platform: selectedPlatform,
        search: searchTerm
      });
      setHistory(data);
    } catch (err) {
      console.error('Failed to load history', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [selectedIndustry, selectedPlatform]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    loadHistory();
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Delete this saved campaign?')) return;
    try {
      await api.deleteContent(id);
      setHistory(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      alert('Failed to delete content item');
    }
  };

  const handleQuickCopy = (item, e) => {
    e.stopPropagation();
    const text = `${item.caption}\n\n${item.cta ? `${item.cta}\n\n` : ''}${item.hashtags?.join(' ') || ''}`;
    navigator.clipboard.writeText(text);
    setCopiedId(item.id);
    setTimeout(() => setCopiedId(''), 2000);
  };

  return (
    <div>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.75rem', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div>
          <h2 className="editorial-heading" style={{ fontSize: '1.75rem' }}>
            Library
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginTop: '2px' }}>
            All your generated marketing copy, visuals, and campaigns.
          </p>
        </div>

        <button
          onClick={() => setView('create')}
          className="btn-primary"
        >
          <Plus size={15} /> Create a post →
        </button>
      </div>

      {/* Filters Toolbar */}
      <div className="card" style={{ padding: '1rem', marginBottom: '1.5rem' }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <div style={{ position: 'relative', flex: 1, minWidth: '220px' }}>
            <input
              type="text"
              placeholder="Search library..."
              className="form-input"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ paddingLeft: '2.25rem' }}
            />
            <Search size={15} style={{ position: 'absolute', left: '0.85rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-dim)' }} />
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <select
              className="form-select"
              value={selectedIndustry}
              onChange={(e) => setSelectedIndustry(e.target.value)}
              style={{ width: 'auto', minWidth: '140px' }}
            >
              <option value="all">All industries</option>
              <option value="restaurant">Restaurant</option>
              <option value="clothing">Clothing</option>
              <option value="real_estate">Real Estate</option>
              <option value="salon">Salon</option>
              <option value="electronics">Electronics</option>
            </select>

            <select
              className="form-select"
              value={selectedPlatform}
              onChange={(e) => setSelectedPlatform(e.target.value)}
              style={{ width: 'auto', minWidth: '140px' }}
            >
              <option value="all">All formats</option>
              <option value="instagram">Instagram</option>
              <option value="facebook">Facebook</option>
              <option value="whatsapp">WhatsApp</option>
              <option value="email">Email</option>
            </select>

            <button type="submit" className="btn-secondary" style={{ padding: '0.55rem 0.85rem' }}>
              Search
            </button>
          </div>
        </form>
      </div>

      {/* Grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <div className="animate-spin" style={{ width: '24px', height: '24px', border: '2px solid var(--accent-terracotta)', borderTopColor: 'transparent', borderRadius: '50%', margin: '0 auto 0.75rem auto' }} />
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Loading library…</p>
        </div>
      ) : history.length > 0 ? (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
          gap: '1.25rem'
        }}>
          {history.map((item) => (
            <div
              key={item.id}
              onClick={() => onViewContent(item)}
              className="card card-hover"
              style={{ padding: '1.25rem', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', gap: '0.35rem' }}>
                  <span style={{
                    fontSize: '0.7rem',
                    fontWeight: '500',
                    textTransform: 'uppercase',
                    padding: '2px 8px',
                    borderRadius: 'var(--radius-full)',
                    background: 'var(--bg-soft)',
                    color: 'var(--text-body)',
                    border: '1px solid var(--border-warm)'
                  }}>
                    {item.industry} · {item.platform}
                  </span>
                </div>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>
                  {new Date(item.created_at).toLocaleDateString()}
                </span>
              </div>

              <div style={{ fontWeight: '600', fontSize: '0.95rem', color: 'var(--text-main)' }}>
                {item.product_or_subject || 'Marketing Post'}
              </div>

              <p style={{
                color: 'var(--text-muted)',
                fontSize: '0.82rem',
                lineHeight: '1.45',
                display: '-webkit-box',
                WebkitLineClamp: 3,
                WebkitBoxOrient: 'vertical',
                overflow: 'hidden',
                fontFamily: item.language === 'telugu' ? 'var(--font-telugu)' : 'inherit'
              }}>
                {item.caption}
              </p>

              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginTop: 'auto',
                paddingTop: '0.65rem',
                borderTop: '1px solid var(--border-warm)'
              }}>
                <button
                  onClick={(e) => handleQuickCopy(item, e)}
                  className="btn-outline"
                  style={{ padding: '3px 8px', fontSize: '0.75rem' }}
                >
                  {copiedId === item.id ? <Check size={11} color="var(--color-success)" /> : <Copy size={11} />}
                  <span>{copiedId === item.id ? 'Copied' : 'Copy'}</span>
                </button>

                <div style={{ display: 'flex', gap: '0.35rem' }}>
                  <button
                    onClick={(e) => { e.stopPropagation(); onViewContent(item); }}
                    className="btn-outline"
                    title="Open"
                    style={{ padding: '3px 6px' }}
                  >
                    <Eye size={13} />
                  </button>
                  <button
                    onClick={(e) => handleDelete(item.id, e)}
                    className="btn-outline"
                    title="Delete"
                    style={{ padding: '3px 6px', color: 'var(--color-error)' }}
                  >
                    <Trash2 size={13} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card" style={{ padding: '3rem 1.5rem', textAlign: 'center' }}>
          <Layers size={32} color="var(--text-dim)" style={{ margin: '0 auto 0.75rem auto' }} />
          <h3 style={{ fontSize: '1.1rem', marginBottom: '0.25rem', fontWeight: '600' }}>No campaigns found</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
            Try resetting your search or create a new post.
          </p>
          <button onClick={() => setView('create')} className="btn-primary">
            Create a post →
          </button>
        </div>
      )}
    </div>
  );
}
