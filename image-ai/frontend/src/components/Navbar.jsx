import React from 'react';
import { Building2, Globe, Sparkles } from 'lucide-react';

export default function Navbar({ brandProfile, setView }) {
  return (
    <header style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: '2rem',
      paddingBottom: '1.15rem',
      borderBottom: '1px solid var(--border-warm)',
      flexWrap: 'wrap',
      gap: '1rem'
    }}>
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <h1 className="editorial-heading" style={{ fontSize: '1.75rem', fontWeight: '600', letterSpacing: '-0.02em' }}>
            Content Studio
          </h1>
          <span style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            gap: '0.35rem', 
            padding: '0.2rem 0.55rem', 
            borderRadius: 'var(--radius-full)', 
            background: 'var(--accent-sage-soft)', 
            color: 'var(--color-success)', 
            fontSize: '0.72rem', 
            fontWeight: '600' 
          }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--color-success)', display: 'inline-block' }} />
            Live
          </span>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginTop: '3px' }}>
          Autonomous multimodal content & visual generator for modern brands.
        </p>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
        {brandProfile && brandProfile.business_name && (
          <button
            onClick={() => setView('brand')}
            className="btn-outline"
            style={{ 
              fontSize: '0.82rem', 
              padding: '0.45rem 0.95rem',
              borderRadius: 'var(--radius-full)',
              background: '#FFFFFF',
              boxShadow: 'var(--shadow-subtle)'
            }}
          >
            <Building2 size={14} color="var(--primary)" />
            <span style={{ fontWeight: '600' }}>{brandProfile.business_name}</span>
          </button>
        )}

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.45rem',
          padding: '0.4rem 0.85rem',
          background: '#FFFFFF',
          border: '1px solid var(--border-warm)',
          borderRadius: 'var(--radius-full)',
          fontSize: '0.8rem',
          color: 'var(--text-muted)',
          boxShadow: 'var(--shadow-subtle)'
        }}>
          <Globe size={13} color="var(--primary)" />
          <span style={{ fontWeight: '500' }}>Telugu · Hindi · English</span>
        </div>
      </div>
    </header>
  );
}
