import React from 'react';
import { 
  ArrowRight, 
  Utensils, 
  Shirt, 
  Building, 
  Scissors, 
  Smartphone,
  Instagram,
  Facebook,
  MessageCircle,
  Megaphone,
  Mail,
  FileText,
  Video,
  Clock
} from 'lucide-react';

const industryIcons = {
  restaurant: Utensils,
  clothing: Shirt,
  real_estate: Building,
  salon: Scissors,
  electronics: Smartphone
};

export default function DashboardView({ 
  industries, 
  usage, 
  recentHistory, 
  onSelectIndustry, 
  onViewContent,
  setView 
}) {
  const quickFormats = [
    { id: 'instagram_post', label: 'Instagram post', icon: Instagram, desc: 'Photo caption & hashtags' },
    { id: 'whatsapp_message', label: 'WhatsApp message', icon: MessageCircle, desc: 'Direct broadcast offer' },
    { id: 'ad_copy', label: 'Advertisement', icon: Megaphone, desc: 'Promotional ad text' },
    { id: 'reel_script', label: 'Reel script', icon: Video, desc: 'Short video concept' },
    { id: 'facebook_post', label: 'Facebook post', icon: Facebook, desc: 'Community update' },
    { id: 'marketing_email', label: 'Marketing email', icon: Mail, desc: 'Customer newsletter' }
  ];

  return (
    <div>
      {/* Editorial Welcome Card */}
      <div className="card" style={{ padding: '2.25rem 2.5rem', marginBottom: '2.5rem', background: '#FFFFFF' }}>
        <div style={{ maxWidth: '640px' }}>
          <h2 className="editorial-heading" style={{ fontSize: '2rem', lineHeight: '1.25', marginBottom: '0.65rem' }}>
            Create content your customers notice.
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginBottom: '1.5rem', lineHeight: '1.6' }}>
            Choose your business, campaign and style. We'll handle the rest.
          </p>
          <button
            onClick={() => setView('create')}
            className="btn-primary"
            style={{ padding: '0.75rem 1.6rem', fontSize: '0.95rem' }}
          >
            Create a post →
          </button>
        </div>
      </div>

      {/* Format Selection Cards: "What would you like to create?" */}
      <div style={{ marginBottom: '2.75rem' }}>
        <div style={{ marginBottom: '1rem' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: '600' }}>What would you like to create?</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            Select a format to start with pre-tuned structures.
          </p>
        </div>

        <div className="option-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))' }}>
          {quickFormats.map((fmt) => {
            const Icon = fmt.icon;
            return (
              <div
                key={fmt.id}
                onClick={() => setView('create')}
                className="card card-hover"
                style={{ padding: '1rem', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}
              >
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: 'var(--radius-xs)',
                  background: 'var(--bg-soft)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--text-main)',
                  marginBottom: '0.25rem'
                }}>
                  <Icon size={16} />
                </div>
                <div style={{ fontWeight: '600', fontSize: '0.9rem', color: 'var(--text-main)' }}>
                  {fmt.label}
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                  {fmt.desc}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Business Sectors */}
      <div style={{ marginBottom: '2.75rem' }}>
        <div style={{ marginBottom: '1rem' }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: '600' }}>Industries</h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            Questionnaires adapt to the specific needs of your business type.
          </p>
        </div>

        <div className="option-grid">
          {industries.map((ind) => {
            const Icon = industryIcons[ind.id] || Utensils;
            return (
              <div
                key={ind.id}
                onClick={() => onSelectIndustry(ind.id)}
                className="card card-hover"
                style={{ padding: '1.15rem', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{
                    width: '34px',
                    height: '34px',
                    borderRadius: 'var(--radius-xs)',
                    background: 'var(--bg-soft)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--text-main)'
                  }}>
                    <Icon size={17} />
                  </div>
                  <ArrowRight size={13} color="var(--text-muted)" />
                </div>
                <div style={{ fontWeight: '600', fontSize: '0.95rem', color: 'var(--text-main)', marginTop: '0.35rem' }}>
                  {ind.name}
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                  {ind.description}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Work */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: '600' }}>Recent work</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              Your latest created posts and campaign drafts.
            </p>
          </div>
          {recentHistory && recentHistory.length > 0 && (
            <button
              onClick={() => setView('history')}
              className="btn-outline"
            >
              View library <ArrowRight size={13} />
            </button>
          )}
        </div>

        {recentHistory && recentHistory.length > 0 ? (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '1rem'
          }}>
            {recentHistory.slice(0, 3).map((item) => (
              <div
                key={item.id}
                onClick={() => onViewContent(item)}
                className="card card-hover"
                style={{ padding: '1.25rem', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
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
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                    Language: {item.language ? item.language.toUpperCase() : 'EN'}
                  </span>
                  <span style={{ fontSize: '0.78rem', color: 'var(--accent-terracotta)', fontWeight: '500', display: 'flex', alignItems: 'center', gap: '3px' }}>
                    Open →
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="card" style={{ padding: '3rem 2rem', textAlign: 'center' }}>
            <Clock size={28} color="var(--text-dim)" style={{ margin: '0 auto 0.75rem auto' }} />
            <div style={{ fontSize: '1rem', fontWeight: '500', marginBottom: '0.25rem' }}>No campaigns created yet</div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
              Pick an industry or format above to write your first post.
            </p>
            <button
              onClick={() => setView('create')}
              className="btn-primary"
            >
              Create content →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
