import React, { useState } from 'react';
import { Mail, Lock, User, ArrowRight, X, Layers } from 'lucide-react';
import { api } from '../api';

export default function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      let data;
      if (isLogin) {
        data = await api.login(email, password);
      } else {
        data = await api.register(email, password, fullName);
      }
      localStorage.setItem('saas_access_token', data.access_token);
      onAuthSuccess(data.user);
      onClose();
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(23, 32, 51, 0.4)',
      backdropFilter: 'blur(4px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '1rem'
    }}>
      <div className="card" style={{
        width: '100%',
        maxWidth: '400px',
        padding: '2.25rem',
        position: 'relative',
        background: '#FFFFFF',
        boxShadow: 'var(--shadow-float)'
      }}>
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '1rem',
            right: '1rem',
            background: 'transparent',
            border: 'none',
            color: 'var(--text-dim)',
            cursor: 'pointer'
          }}
        >
          <X size={18} />
        </button>

        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <div className="logo-badge" style={{ margin: '0 auto 0.65rem auto' }}>
            <Layers size={17} />
          </div>
          <h2 className="editorial-heading" style={{ fontSize: '1.4rem' }}>
            {isLogin ? 'Sign in to Content Studio' : 'Create an Account'}
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            {isLogin ? 'Access your saved brand profile & campaigns' : 'Get started in seconds'}
          </p>
        </div>

        {error && (
          <div style={{
            background: '#FDF2F2',
            border: '1px solid #F8B4B4',
            borderRadius: 'var(--radius-xs)',
            padding: '0.65rem',
            color: 'var(--color-error)',
            fontSize: '0.82rem',
            marginBottom: '1rem'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="form-group">
              <label className="form-label">Full Name</label>
              <input
                type="text"
                required
                placeholder="e.g. Rahul Sharma"
                className="form-input"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>
          )}

          <div className="form-group">
            <label className="form-label">Email Address</label>
            <input
              type="email"
              required
              placeholder="owner@example.com"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              required
              placeholder="••••••••"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary"
            style={{ width: '100%', padding: '0.7rem', marginTop: '0.5rem', justifyContent: 'center' }}
          >
            {loading ? 'Please wait...' : isLogin ? 'Sign in →' : 'Create account →'}
          </button>
        </form>



        <div style={{ textAlign: 'center', marginTop: '1.25rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button
            type="button"
            onClick={() => { setIsLogin(!isLogin); setError(''); }}
            style={{ background: 'transparent', border: 'none', color: 'var(--accent-terracotta)', fontWeight: '600', cursor: 'pointer' }}
          >
            {isLogin ? 'Register' : 'Sign in'}
          </button>
        </div>
      </div>
    </div>
  );
}

