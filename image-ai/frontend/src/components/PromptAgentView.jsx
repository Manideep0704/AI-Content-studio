import React, { useState } from 'react';
import { Bot, Send, Sparkles, Image as ImageIcon, Loader2, ArrowRight, Check, Copy } from 'lucide-react';
import { api } from '../api';

export default function PromptAgentView({ user, onOpenAuth, onImageGenerated }) {
  const [input, setInput] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [imageLoading, setImageLoading] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [copied, setCopied] = useState(false);

  const suggestions = [
    { label: '🍗 Dum Biryani Promo', prompt: 'Festive promotion banner for spicy Hyderabadi Dum Biryani with 20% discount' },
    { label: '🥻 Silk Saree Collection', prompt: 'Elegant showcase of Kanchipuram pure silk saree with traditional gold zari work' },
    { label: '☕ Artisanal Cafe', prompt: 'Steaming gourmet cappuccino with latte art on a rustic wooden cafe table' },
    { label: '🏠 Luxury 3BHK Villa', prompt: 'Modern architectural interior of a sunlit luxury living room with panoramic balcony view' }
  ];

  const handleSend = async (overridePrompt) => {
    const textToSend = typeof overridePrompt === 'string' ? overridePrompt : input;
    if (!textToSend.trim() || loading || imageLoading) return;
    if (!user) { onOpenAuth(); return; }
    
    const userMsg = { role: 'user', content: textToSend };
    setChatLog(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setGeneratedImage(null);
    
    try {
      const response = await api.generateAgentPrompt(userMsg.content);
      const agentMsg = {
        role: 'agent',
        content: `I've analyzed your request. I identified the product as **${response.product || 'General'}** in the **${response.industry || 'General'}** industry. Generating image...`,
        promptData: response
      };
      setChatLog(prev => [...prev, agentMsg]);
      
      setImageLoading(true);
      const imageResponse = await api.generateImage({
        prompt: response.suggested_prompt,
        industry: response.industry,
        product: response.product,
        offer: response.offer
      });
      
      setGeneratedImage(imageResponse.image_url);
      onImageGenerated?.();
    } catch (err) {
      setChatLog(prev => [...prev, { role: 'agent', content: `Error: ${err.message}` }]);
    } finally {
      setLoading(false);
      setImageLoading(false);
    }
  };

  const copyPromptText = (text) => {
    navigator.clipboard?.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="view-container">
      {/* Studio Header */}
      <div className="view-header" style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.3rem 0.75rem', borderRadius: 'var(--radius-full)', background: 'var(--primary-soft)', color: 'var(--primary)', fontSize: '0.78rem', fontWeight: '600', marginBottom: '0.5rem' }}>
            <Sparkles size={13} />
            <span>AI Creative Studio</span>
          </div>
          <h2 className="editorial-heading" style={{ fontSize: '1.85rem' }}>Prompt Library Agent</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', marginTop: '0.2rem' }}>
            Describe your marketing idea or select a template below. We'll engineer the prompt and render the visual.
          </p>
        </div>
      </div>

      {/* Main Studio Console */}
      <div className="agent-container card" style={{ display: 'flex', flexDirection: 'column', minHeight: '620px', height: 'auto', padding: 0, overflow: 'hidden' }}>
        
        {/* Chat / Generation Canvas */}
        <div className="chat-window" style={{ flex: 1, padding: '1.75rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1.25rem', background: '#FAFAFD', minHeight: '440px' }}>
          
          {/* Empty State Hero */}
          {chatLog.length === 0 && (
            <div style={{ margin: 'auto', textAlign: 'center', maxWidth: '520px', padding: '2rem 1rem' }}>
              <div style={{ 
                width: '64px', 
                height: '64px', 
                borderRadius: 'var(--radius-md)', 
                background: 'var(--primary-gradient)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center', 
                color: 'white',
                margin: '0 auto 1.25rem',
                boxShadow: '0 8px 20px rgba(79, 70, 229, 0.3)'
              }}>
                <Bot size={32} />
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: '0.5rem', color: 'var(--text-main)' }}>
                What would you like to create today?
              </h3>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: '1.6', marginBottom: '1.5rem' }}>
                Type in natural language or click any quick template below to instantly generate high-converting promotional banners.
              </p>

              {/* Quick Inspiration Chips */}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', justifyContent: 'center' }}>
                {suggestions.map((item, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setInput(item.prompt);
                      handleSend(item.prompt);
                    }}
                    style={{
                      background: '#FFFFFF',
                      border: '1px solid var(--border-warm)',
                      borderRadius: 'var(--radius-full)',
                      padding: '0.45rem 0.95rem',
                      fontSize: '0.82rem',
                      fontWeight: '500',
                      color: 'var(--text-body)',
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.35rem',
                      boxShadow: 'var(--shadow-subtle)',
                      transition: 'all var(--transition-fast)'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor = 'var(--primary)';
                      e.currentTarget.style.transform = 'translateY(-1px)';
                      e.currentTarget.style.color = 'var(--primary)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor = 'var(--border-warm)';
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.color = 'var(--text-body)';
                    }}
                  >
                    <span>{item.label}</span>
                    <ArrowRight size={12} />
                  </button>
                ))}
              </div>
            </div>
          )}
          
          {/* Message Stream */}
          {chatLog.map((msg, i) => (
            <div 
              key={i} 
              className={`chat-message ${msg.role}`} 
              style={{
                alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                background: msg.role === 'user' ? 'var(--primary-gradient)' : '#FFFFFF',
                color: msg.role === 'user' ? '#FFFFFF' : 'var(--text-main)',
                padding: '0.95rem 1.25rem',
                borderRadius: msg.role === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
                maxWidth: '85%',
                boxShadow: msg.role === 'user' ? '0 4px 14px rgba(79, 70, 229, 0.25)' : 'var(--shadow-card)',
                border: msg.role === 'user' ? 'none' : '1px solid var(--border-warm)'
              }}
            >
              {msg.role === 'agent' && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', marginBottom: '0.5rem', color: 'var(--primary)', fontWeight: '600', fontSize: '0.8rem' }}>
                  <Sparkles size={14} />
                  <span>Studio Copilot</span>
                </div>
              )}

              <div style={{ whiteSpace: "pre-wrap", lineHeight: '1.6', fontSize: '0.92rem' }}>
                {msg.content}
              </div>
              
              {/* Prompt Analysis Box */}
              {msg.promptData && (
                <div style={{ 
                  marginTop: '0.85rem', 
                  padding: '0.75rem 0.95rem',
                  background: 'var(--bg-soft)',
                  border: '1px solid var(--border-warm)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.84rem'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                    <strong style={{ color: 'var(--text-main)', fontSize: '0.78rem', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                      Engineered Prompt
                    </strong>
                    <button 
                      onClick={() => copyPromptText(msg.promptData.suggested_prompt)}
                      style={{ background: 'none', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.25rem', color: 'var(--text-muted)', fontSize: '0.75rem' }}
                      title="Copy Prompt"
                    >
                      {copied ? <Check size={12} color="var(--color-success)" /> : <Copy size={12} />}
                      <span>{copied ? 'Copied' : 'Copy'}</span>
                    </button>
                  </div>
                  <div style={{ color: 'var(--text-body)', fontStyle: 'italic', lineHeight: '1.5' }}>
                    "{msg.promptData.suggested_prompt}"
                  </div>
                </div>
              )}
            </div>
          ))}
          
          {/* Thinking State */}
          {loading && (
            <div style={{ alignSelf: 'flex-start', background: '#FFFFFF', padding: '0.75rem 1.15rem', borderRadius: '14px', border: '1px solid var(--border-warm)', boxShadow: 'var(--shadow-subtle)', display: 'flex', alignItems: 'center', gap: '0.65rem', color: 'var(--text-muted)', fontSize: '0.88rem' }}>
              <Loader2 className="spin" size={17} color="var(--primary)" />
              <span>Analyzing intent & engineering optimal lighting prompt...</span>
            </div>
          )}
          
          {/* Generating Visual State */}
          {imageLoading && (
            <div style={{ alignSelf: 'center', margin: '1.5rem 0', background: '#FFFFFF', padding: '1.5rem 2rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-warm)', boxShadow: 'var(--shadow-card)', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.85rem', textAlign: 'center' }}>
              <div style={{ width: '48px', height: '48px', borderRadius: 'var(--radius-full)', background: 'var(--primary-soft)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)' }}>
                <Loader2 className="spin" size={26} />
              </div>
              <div>
                <div style={{ fontWeight: '600', color: 'var(--text-main)', fontSize: '0.95rem' }}>Synthesizing Studio Visual</div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>Rendering high-resolution creative via AI engine...</div>
              </div>
            </div>
          )}
          
          {/* Showcase Generated Output */}
          {generatedImage && (
            <div style={{ 
              alignSelf: 'center', 
              margin: '1.5rem 0', 
              background: '#FFFFFF', 
              borderRadius: 'var(--radius-md)', 
              border: '1px solid var(--border-warm)', 
              overflow: 'hidden', 
              boxShadow: 'var(--shadow-float)', 
              maxWidth: '560px',
              width: '100%'
            }}>
              <div style={{ padding: '0.75rem 1rem', background: '#FFFFFF', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', fontSize: '0.82rem', fontWeight: '600', color: 'var(--text-main)' }}>
                  <ImageIcon size={15} color="var(--primary)" />
                  <span>High-Resolution Generation Output</span>
                </div>
                <span className="quality-meter">AI Verified</span>
              </div>
              <div style={{ width: '100%', background: '#0F172A', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <img 
                  src={generatedImage} 
                  alt="Generated" 
                  style={{ width: '100%', maxHeight: '520px', objectFit: 'contain', display: 'block' }} 
                />
              </div>
              <div style={{ padding: '1rem', background: '#FFFFFF', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'flex-end', gap: '0.65rem' }}>
                <a 
                  className="btn-secondary" 
                  href={generatedImage} 
                  download
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '0.45rem' }}
                >
                  Download image
                </a>
              </div>
            </div>
          )}
        </div>
        
        {/* Modern Prompt Input Dock */}
        <div className="chat-input-area" style={{ padding: '1.15rem 1.5rem', borderTop: '1px solid var(--border-warm)', background: '#FFFFFF', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          
          {/* Suggestions row if chat has items */}
          {chatLog.length > 0 && (
            <div style={{ display: 'flex', gap: '0.4rem', overflowX: 'auto', paddingBottom: '0.2rem' }}>
              {suggestions.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setInput(item.prompt);
                    handleSend(item.prompt);
                  }}
                  style={{
                    background: 'var(--bg-soft)',
                    border: '1px solid var(--border-warm)',
                    borderRadius: 'var(--radius-full)',
                    padding: '0.25rem 0.75rem',
                    fontSize: '0.75rem',
                    color: 'var(--text-body)',
                    cursor: 'pointer',
                    whiteSpace: 'nowrap'
                  }}
                >
                  {item.label}
                </button>
              ))}
            </div>
          )}

          <div style={{ display: 'flex', gap: '0.65rem', alignItems: 'center' }}>
            <div style={{ flex: 1, position: 'relative', display: 'flex', alignItems: 'center' }}>
              <input
                type="text"
                className="form-input"
                aria-label="Describe your image"
                style={{ 
                  flex: 1, 
                  padding: '0.8rem 1rem 0.8rem 2.5rem', 
                  borderRadius: 'var(--radius-full)', 
                  fontSize: '0.92rem',
                  border: '1px solid var(--border-warm)',
                  boxShadow: 'var(--shadow-subtle)'
                }}
                placeholder="E.g., I need a high-end photo of a silk saree for a festival offer..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                disabled={loading || imageLoading}
              />
              <Sparkles size={16} color="var(--primary)" style={{ position: 'absolute', left: '1rem', pointerEvents: 'none' }} />
            </div>

            <button 
              aria-label="Generate image" 
              className="btn-primary" 
              onClick={() => handleSend()} 
              disabled={loading || imageLoading || !input.trim()}
              style={{ borderRadius: 'var(--radius-full)', padding: '0.8rem 1.4rem', gap: '0.5rem' }}
            >
              <span>Generate</span>
              <Send size={15} />
            </button>
          </div>
        </div>
        
      </div>
    </div>
  );
}
