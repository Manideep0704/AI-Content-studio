import React from 'react';
import { 
  Home, 
  Plus, 
  Layers, 
  Building2, 
  Settings, 
  LogOut, 
  User as UserIcon,
  Check,
  X
} from 'lucide-react';

export default function Sidebar({ currentView, setView, user, onLogout, onOpenAuth, mobileOpen, onCloseMobile }) {
  const navItems = [
    { id: 'agent', label: 'Image Agent', icon: Home },
    { id: 'dashboard', label: 'Dashboard', icon: Layers },
    { id: 'create', label: 'Create Content', icon: Plus },
    { id: 'history', label: 'History', icon: Layers },
    { id: 'brand', label: 'Brand', icon: Building2 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const handleNavClick = (viewId) => {
    if (!user && ['create', 'history', 'brand'].includes(viewId)) {
      onOpenAuth();
      if (onCloseMobile) onCloseMobile();
      return;
    }
    setView(viewId);
    if (onCloseMobile) onCloseMobile();
  };

  return (
    <>
      {/* Mobile Backdrop Overlay */}
      {mobileOpen && (
        <div 
          className="sidebar-overlay" 
          onClick={onCloseMobile}
          aria-hidden="true"
        />
      )}

      <aside className={`app-sidebar ${mobileOpen ? 'mobile-open' : ''}`}>
        {/* Brand Header */}
        <div className="sidebar-logo" style={{ justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <div className="logo-badge">
              <Layers size={17} />
            </div>
            <div>
              <div className="logo-title">Content Studio</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>You choose. We create.</div>
            </div>
          </div>

          {/* Close button on mobile */}
          {mobileOpen && (
            <button
              onClick={onCloseMobile}
              style={{ background: 'transparent', border: 'none', color: 'var(--text-dim)', cursor: 'pointer', padding: '4px' }}
              aria-label="Close navigation"
            >
              <X size={18} />
            </button>
          )}
        </div>

        {/* Primary Action Button */}
        <div style={{ marginBottom: '1.25rem' }}>
          <button
            onClick={() => handleNavClick('agent')}
            className="btn-primary"
            style={{ width: '100%', padding: '0.65rem 0.85rem', fontSize: '0.88rem', justifyContent: 'center' }}
          >
            <Plus size={16} /> New Image Prompt →
          </button>
        </div>

        {/* Navigation */}
        <nav className="nav-links">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`nav-item ${isActive ? 'active' : ''}`}
              >
                <Icon size={17} color={isActive ? 'var(--text-main)' : 'var(--text-muted)'} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Footer User Info */}
        <div className="sidebar-footer">
          {user ? (
            <div className="user-badge">
              <div className="user-avatar">
                {user.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: '0.82rem', fontWeight: '500', color: 'var(--text-main)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {user.full_name || user.email}
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--accent-sage)', display: 'flex', alignItems: 'center', gap: '3px' }}>
                  <Check size={11} /> Ready
                </div>
              </div>
              <button
                onClick={onLogout}
                title="Sign Out"
                style={{ background: 'transparent', border: 'none', color: 'var(--text-dim)', cursor: 'pointer', padding: '4px' }}
              >
                <LogOut size={15} />
              </button>
            </div>
          ) : (
            <button
              onClick={() => { onOpenAuth(); if (onCloseMobile) onCloseMobile(); }}
              className="btn-secondary"
              style={{ width: '100%', padding: '0.55rem', fontSize: '0.82rem', justifyContent: 'center' }}
            >
              <UserIcon size={15} /> Sign In
            </button>
          )}
        </div>
      </aside>
    </>
  );
}
