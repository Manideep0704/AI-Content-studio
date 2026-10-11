import React, { useState, useEffect } from 'react';
import { 
  Copy, 
  Check, 
  Download, 
  RefreshCw, 
  Edit3, 
  Save, 
  Image as ImageIcon, 
  Heart, 
  MessageCircle, 
  Bookmark, 
  Send,
  ArrowLeft,
  ThumbsUp,
  Share2,
  ExternalLink,
  Film,
  Mail,
  ShoppingBag,
  Sparkles
} from 'lucide-react';
import { api } from '../api';

export default function ResultView({ content, onBack, onContentUpdated, brandProfile }) {
  const [currentContent, setCurrentContent] = useState(content);
  const [isEditing, setIsEditing] = useState(false);
  const [editedCaption, setEditedCaption] = useState(content.caption || '');
  const [editedCta, setEditedCta] = useState(content.cta || '');
  const [copiedSection, setCopiedSection] = useState('');
  const [regenerating, setRegenerating] = useState(false);
  const [generatingImage, setGeneratingImage] = useState(false);
  const [showRegenModal, setShowRegenModal] = useState(false);
  const [tweakTone, setTweakTone] = useState(content.tone || 'premium');
  const [tweakOffer, setTweakOffer] = useState('');
  const [tweakNote, setTweakNote] = useState('');

  useEffect(() => {
    setCurrentContent(content);
    setEditedCaption(content.caption || '');
    setEditedCta(content.cta || '');
  }, [content]);

  const handleCopy = (text, sectionName) => {
    navigator.clipboard.writeText(text);
    setCopiedSection(sectionName);
    setTimeout(() => setCopiedSection(''), 2000);
  };

  const handleCopyFull = () => {
    const fullText = `${currentContent.caption}\n\n${currentContent.cta ? `${currentContent.cta}\n\n` : ''}${currentContent.hashtags?.join(' ') || ''}`;
    handleCopy(fullText, 'full');
  };

  const handleSaveEdit = async () => {
    try {
      const updated = await api.updateContent(currentContent.id, {
        caption: editedCaption,
        cta: editedCta
      });
      setCurrentContent(updated);
      setIsEditing(false);
      if (onContentUpdated) onContentUpdated(updated);
    } catch (err) {
      alert('Failed to save changes');
    }
  };

  const handleCancelEdit = () => {
    setEditedCaption(currentContent.caption);
    setEditedCta(currentContent.cta);
    setIsEditing(false);
  };

  const handleRegenerate = async () => {
    setRegenerating(true);
    setShowRegenModal(false);
    try {
      const updated = await api.regenerateContent(currentContent.id, {
        tone: tweakTone,
        offer: tweakOffer || undefined,
        tweak_instruction: tweakNote || undefined
      });
      setCurrentContent(updated);
      setEditedCaption(updated.caption);
      setEditedCta(updated.cta);
      if (onContentUpdated) onContentUpdated(updated);
    } catch (err) {
      alert('Regeneration failed: ' + err.message);
    } finally {
      setRegenerating(false);
    }
  };

  const handleGenerateImage = async () => {
    setGeneratingImage(true);
    try {
      const res = await api.generateImage({
        content_id: currentContent.id,
        industry: currentContent.industry,
        product: currentContent.product_or_subject,
        offer: currentContent.offer || '',
        business_name: brandProfile?.business_name || ''
      });
      const updated = { ...currentContent, image_url: res.image_url };
      setCurrentContent(updated);
      if (onContentUpdated) onContentUpdated(updated);
    } catch (err) {
      alert('Image update failed: ' + err.message);
    } finally {
      setGeneratingImage(false);
    }
  };

  const downloadTextFile = () => {
    const fullText = `YOUR CAMPAIGN\n${currentContent.industry.toUpperCase()} · ${currentContent.content_type.toUpperCase()}\n\nCaption:\n${currentContent.caption}\n\nCall to action:\n${currentContent.cta}\n\nHashtags:\n${currentContent.hashtags?.join(' ')}\n`;
    const blob = new Blob([fullText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `campaign_${currentContent.content_type}_${Date.now()}.txt`;
    a.click();
  };

  const downloadJsonFile = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(currentContent, null, 2));
    const a = document.createElement('a');
    a.href = dataStr;
    a.download = `campaign_${currentContent.id}.json`;
    a.click();
  };

  // Determine platform type
  const platform = currentContent.platform?.toLowerCase() || 'instagram';
  const contentType = currentContent.content_type?.toLowerCase() || 'instagram_post';
  const brandName = brandProfile?.business_name || 'My Business';
  const brandHandle = brandProfile?.business_name ? brandProfile.business_name.toLowerCase().replace(/\s+/g, '_') : 'my_brand';
  const brandLocation = brandProfile?.location || 'Local Business';

  return (
    <div>
      {/* Top Action Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '1.5rem',
        flexWrap: 'wrap',
        gap: '0.75rem'
      }}>
        <button onClick={onBack} className="btn-secondary" style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}>
          <ArrowLeft size={15} /> Create another
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', flexWrap: 'wrap' }}>
          <div className="quality-meter">
            <Check size={13} />
            <span>Ready for {platform.charAt(0).toUpperCase() + platform.slice(1)}</span>
          </div>

          <button
            onClick={() => setShowRegenModal(true)}
            disabled={regenerating}
            className="btn-secondary"
            style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
          >
            <RefreshCw size={14} className={regenerating ? 'animate-spin' : ''} />
            <span>{regenerating ? 'Rewriting...' : 'Adjust tone'}</span>
          </button>

          <button
            onClick={handleCopyFull}
            className="btn-primary"
            style={{ padding: '0.5rem 1.25rem', fontSize: '0.85rem' }}
          >
            {copiedSection === 'full' ? <Check size={14} /> : <Copy size={14} />}
            <span>{copiedSection === 'full' ? 'Copied' : 'Copy everything'}</span>
          </button>
        </div>
      </div>

      {/* Main Split Layout */}
      <div className="result-split-container">
        {/* LEFT COLUMN: Tailored Platform Mockup */}
        <div>
          <div style={{ marginBottom: '0.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-muted)' }}>
              {contentType.replace(/_/g, ' ').toUpperCase()} PREVIEW
            </span>
            <span style={{
              fontSize: '0.75rem',
              color: 'var(--text-body)',
              background: 'var(--bg-card)',
              border: '1px solid var(--border-warm)',
              padding: '2px 8px',
              borderRadius: 'var(--radius-sm)',
              textTransform: 'capitalize'
            }}>
              {platform} · {currentContent.language || 'English'}
            </span>
          </div>

          {/* 1. WHATSAPP MOCKUP */}
          {platform === 'whatsapp' || contentType === 'whatsapp_message' ? (
            <div className="mockup-whatsapp">
              <div className="wa-header">
                <div className="user-avatar" style={{ width: '34px', height: '34px', background: '#FFFFFF', color: '#128C7E' }}>
                  {brandName.charAt(0)}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '0.92rem', fontWeight: '600', color: 'white', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    {brandName} <span style={{ fontSize: '0.7rem', background: '#25D366', color: 'white', padding: '1px 4px', borderRadius: '4px' }}>Business</span>
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#e0f2fe' }}>online</div>
                </div>
              </div>

              {currentContent.image_url && (
                <div style={{ padding: '0.75rem 0.75rem 0' }}>
                  <img
                    src={currentContent.image_url}
                    alt="Creative Preview"
                    style={{ width: '100%', borderRadius: '8px', maxHeight: '240px', objectFit: 'cover' }}
                  />
                </div>
              )}

              <div className="wa-bubble">
                <div style={{ whiteSpace: 'pre-wrap', fontFamily: currentContent.language === 'telugu' ? 'var(--font-telugu)' : 'inherit' }}>
                  {currentContent.caption}
                </div>
                {currentContent.cta && (
                  <div style={{ marginTop: '0.65rem', paddingTop: '0.65rem', borderTop: '1px dashed #D1D5DB', fontWeight: '600', color: '#075E54' }}>
                    {currentContent.cta}
                  </div>
                )}
                <div style={{ fontSize: '0.68rem', color: 'var(--text-dim)', textAlign: 'right', marginTop: '6px' }}>
                  12:00 PM ✓✓
                </div>
              </div>
            </div>
          ) : platform === 'facebook' || contentType === 'facebook_post' ? (
            /* 2. FACEBOOK MOCKUP */
            <div className="card" style={{ maxWidth: '440px', margin: '0 auto', overflow: 'hidden', boxShadow: 'var(--shadow-float)' }}>
              {/* Header */}
              <div style={{ padding: '0.85rem 1rem', display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                <div className="user-avatar" style={{ width: '36px', height: '36px', background: '#1877F2', color: 'white' }}>
                  {brandName.charAt(0)}
                </div>
                <div>
                  <div style={{ fontSize: '0.88rem', fontWeight: '600', color: 'var(--text-main)' }}>{brandName}</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>Just now · 🌍 Public</div>
                </div>
              </div>

              {/* Body */}
              <div style={{ padding: '0 1rem 0.75rem', fontSize: '0.88rem', lineHeight: '1.5', whiteSpace: 'pre-wrap', fontFamily: currentContent.language === 'telugu' ? 'var(--font-telugu)' : 'inherit' }}>
                {currentContent.caption}
              </div>

              {/* Image */}
              {currentContent.image_url && (
                <div style={{ width: '100%', maxHeight: '280px', overflow: 'hidden', background: 'var(--bg-soft)' }}>
                  <img src={currentContent.image_url} alt="Post Visual" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </div>
              )}

              {/* Action Banner */}
              <div style={{ background: 'var(--bg-soft)', padding: '0.65rem 1rem', borderTop: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>{brandHandle}.com</div>
                  <div style={{ fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-main)' }}>{currentContent.product_or_subject} · Exclusive Deal</div>
                </div>
                <button className="btn-secondary" style={{ padding: '4px 10px', fontSize: '0.78rem' }}>
                  Learn More
                </button>
              </div>

              {/* Social Bar */}
              <div style={{ display: 'flex', justifyContent: 'space-around', padding: '0.5rem 0', borderTop: '1px solid var(--border-subtle)', color: 'var(--text-muted)', fontSize: '0.82rem' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px', cursor: 'pointer' }}><ThumbsUp size={14} /> Like</span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px', cursor: 'pointer' }}><MessageCircle size={14} /> Comment</span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px', cursor: 'pointer' }}><Share2 size={14} /> Share</span>
              </div>
            </div>
          ) : contentType === 'ad_copy' ? (
            /* 3. SPONSORED AD MOCKUP */
            <div className="card" style={{ maxWidth: '440px', margin: '0 auto', overflow: 'hidden', boxShadow: 'var(--shadow-float)' }}>
              <div style={{ padding: '0.75rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-subtle)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div className="user-avatar" style={{ width: '32px', height: '32px' }}>{brandName.charAt(0)}</div>
                  <div>
                    <div style={{ fontSize: '0.85rem', fontWeight: '600' }}>{brandName}</div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Sponsored · ⚡</div>
                  </div>
                </div>
                <span style={{ fontSize: '0.7rem', background: 'var(--accent-terracotta-soft)', color: 'var(--accent-terracotta)', padding: '2px 6px', borderRadius: '4px', fontWeight: '600' }}>AD</span>
              </div>

              <div style={{ padding: '0.75rem 1rem', fontSize: '0.88rem', lineHeight: '1.5', whiteSpace: 'pre-wrap', fontFamily: currentContent.language === 'telugu' ? 'var(--font-telugu)' : 'inherit' }}>
                {currentContent.caption}
              </div>

              {currentContent.image_url && (
                <div style={{ width: '100%', maxHeight: '240px', overflow: 'hidden' }}>
                  <img src={currentContent.image_url} alt="Ad Visual" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </div>
              )}

              <div style={{ padding: '0.85rem 1rem', background: 'var(--bg-soft)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{brandHandle}.com/special</div>
                  <div style={{ fontSize: '0.9rem', fontWeight: '600' }}>{currentContent.offer || 'Special Discount'} Available Now</div>
                </div>
                <button className="btn-primary" style={{ padding: '0.45rem 0.95rem', fontSize: '0.8rem' }}>
                  {currentContent.cta ? currentContent.cta.slice(0, 18) : 'Claim Offer'}
                </button>
              </div>
            </div>
          ) : contentType === 'reel_script' ? (
            /* 4. REEL SCRIPT / VIDEO DIRECTOR MOCKUP */
            <div className="card" style={{ maxWidth: '440px', margin: '0 auto', overflow: 'hidden', boxShadow: 'var(--shadow-float)' }}>
              <div style={{ background: 'var(--text-main)', color: 'white', padding: '0.75rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Film size={17} color="var(--accent-terracotta)" />
                <span style={{ fontWeight: '600', fontSize: '0.9rem' }}>Reel & Video Storyboard</span>
              </div>

              {currentContent.image_url && (
                <div style={{ width: '100%', height: '180px', overflow: 'hidden', position: 'relative' }}>
                  <img src={currentContent.image_url} alt="Concept Hook" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  <div style={{ position: 'absolute', bottom: '8px', left: '8px', background: 'rgba(0,0,0,0.7)', color: 'white', padding: '2px 8px', borderRadius: '4px', fontSize: '0.72rem' }}>
                    0:15 Short Form Concept
                  </div>
                </div>
              )}

              <div style={{ padding: '1rem', maxHeight: '340px', overflowY: 'auto' }}>
                <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.88rem', lineHeight: '1.6', fontFamily: currentContent.language === 'telugu' ? 'var(--font-telugu)' : 'inherit' }}>
                  {currentContent.caption}
                </div>
              </div>
            </div>
          ) : contentType === 'marketing_email' ? (
            /* 5. EMAIL NEWSLETTER MOCKUP */
            <div className="card" style={{ maxWidth: '440px', margin: '0 auto', overflow: 'hidden', boxShadow: 'var(--shadow-float)' }}>
              <div style={{ background: 'var(--bg-soft)', padding: '0.65rem 1rem', borderBottom: '1px solid var(--border-warm)', fontSize: '0.78rem' }}>
                <div style={{ color: 'var(--text-muted)' }}>From: <b style={{ color: 'var(--text-main)' }}>{brandName}</b> &lt;news@{brandHandle}.com&gt;</div>
                <div style={{ color: 'var(--text-main)', fontWeight: '600', marginTop: '2px' }}>
                  {currentContent.product_or_subject} · {currentContent.offer || 'Special Announcement'}
                </div>
              </div>

              {currentContent.image_url && (
                <div style={{ width: '100%', maxHeight: '180px', overflow: 'hidden' }}>
                  <img src={currentContent.image_url} alt="Email Banner" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </div>
              )}

              <div style={{ padding: '1rem', fontSize: '0.88rem', lineHeight: '1.55', whiteSpace: 'pre-wrap', fontFamily: currentContent.language === 'telugu' ? 'var(--font-telugu)' : 'inherit' }}>
                {currentContent.caption}
              </div>

              <div style={{ padding: '0 1rem 1rem', textAlign: 'center' }}>
                <button className="btn-primary" style={{ width: '100%', padding: '0.65rem', justifyContent: 'center' }}>
                  {currentContent.cta || 'Claim VIP Offer →'}
                </button>
              </div>
            </div>
          ) : (
            /* 6. INSTAGRAM POST MOCKUP (DEFAULT) */
            <div className="mockup-phone">
              <div className="mockup-header">
                <div className="mockup-profile">
                  <div className="mockup-avatar">
                    {brandName.charAt(0)}
                  </div>
                  <div>
                    <div style={{ fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-main)' }}>
                      {brandHandle}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                      {brandLocation}
                    </div>
                  </div>
                </div>
                <div style={{ color: 'var(--text-dim)', fontSize: '1rem' }}>•••</div>
              </div>

              <div className="mockup-image-box">
                {currentContent.image_url ? (
                  <img src={currentContent.image_url} alt="Creative Preview" />
                ) : (
                  <div style={{ textAlign: 'center', padding: '1.75rem' }}>
                    <ImageIcon size={36} color="var(--text-dim)" style={{ margin: '0 auto 0.5rem auto' }} />
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginBottom: '0.75rem' }}>
                      Commercial photo preview
                    </div>
                    <button
                      onClick={handleGenerateImage}
                      disabled={generatingImage}
                      className="btn-primary"
                      style={{ padding: '0.45rem 0.95rem', fontSize: '0.8rem' }}
                    >
                      {generatingImage ? 'Updating...' : 'Show image'}
                    </button>
                  </div>
                )}
              </div>

              <div className="mockup-actions">
                <div style={{ display: 'flex', gap: '0.75rem' }}>
                  <Heart size={18} color="var(--color-error)" fill="var(--color-error)" />
                  <MessageCircle size={18} />
                  <Send size={18} />
                </div>
                <Bookmark size={18} />
              </div>

              <div className="mockup-body">
                <div style={{ fontSize: '0.78rem', fontWeight: '600', color: 'var(--text-main)', marginBottom: '4px' }}>
                  512 likes
                </div>
                <div>
                  <span style={{ fontWeight: '600', color: 'var(--text-main)', marginRight: '6px' }}>
                    {brandHandle}
                  </span>
                  <span style={{ whiteSpace: 'pre-wrap', fontFamily: currentContent.language === 'telugu' ? 'var(--font-telugu)' : 'inherit' }}>
                    {currentContent.caption}
                  </span>
                </div>

                {currentContent.cta && (
                  <div style={{ marginTop: '0.65rem', fontWeight: '600', color: 'var(--accent-terracotta)' }}>
                    {currentContent.cta}
                  </div>
                )}

                {currentContent.hashtags && currentContent.hashtags.length > 0 && (
                  <div style={{ marginTop: '0.65rem', color: 'var(--text-muted)', fontSize: '0.8rem', display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                    {currentContent.hashtags.map((tag, i) => (
                      <span key={i}>{tag}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: Editorial Content Inspector */}
        <div>
          <div className="card" style={{ padding: '1.75rem', marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 className="editorial-heading" style={{ fontSize: '1.3rem' }}>
                  Your {contentType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </h3>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  {currentContent.industry} · {currentContent.language} · {currentContent.tone} tone
                </div>
              </div>

              {!isEditing ? (
                <button
                  onClick={() => setIsEditing(true)}
                  className="btn-outline"
                >
                  <Edit3 size={13} /> Edit
                </button>
              ) : (
                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  <button onClick={handleCancelEdit} className="btn-secondary" style={{ padding: '0.35rem 0.65rem', fontSize: '0.78rem' }}>
                    Cancel
                  </button>
                  <button onClick={handleSaveEdit} className="btn-primary" style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}>
                    <Save size={13} /> Save
                  </button>
                </div>
              )}
            </div>

            {/* Main Body / Caption */}
            <div style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                <label className="form-label" style={{ margin: 0, fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  {contentType === 'reel_script' ? 'Script & Scene Direction' : contentType === 'marketing_email' ? 'Email Body' : 'Post Copy & Body'}
                </label>
                <button
                  onClick={() => handleCopy(currentContent.caption, 'caption')}
                  className="btn-outline"
                  style={{ padding: '2px 6px', fontSize: '0.72rem' }}
                >
                  {copiedSection === 'caption' ? <Check size={11} color="var(--color-success)" /> : <Copy size={11} />}
                  <span>{copiedSection === 'caption' ? 'Copied' : 'Copy'}</span>
                </button>
              </div>

              {isEditing ? (
                <textarea
                  className="form-textarea"
                  rows={7}
                  value={editedCaption}
                  onChange={(e) => setEditedCaption(e.target.value)}
                  style={{ fontFamily: currentContent.language === 'telugu' ? 'var(--font-telugu)' : 'inherit' }}
                />
              ) : (
                <div style={{
                  background: 'var(--bg-soft)',
                  border: '1px solid var(--border-warm)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '1rem',
                  fontSize: '0.92rem',
                  lineHeight: '1.6',
                  whiteSpace: 'pre-wrap',
                  fontFamily: currentContent.language === 'telugu' ? 'var(--font-telugu)' : 'inherit'
                }}>
                  {currentContent.caption}
                </div>
              )}
            </div>

            {/* Call to Action */}
            <div style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                <label className="form-label" style={{ margin: 0, fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  Call to action line
                </label>
                <button
                  onClick={() => handleCopy(currentContent.cta, 'cta')}
                  className="btn-outline"
                  style={{ padding: '2px 6px', fontSize: '0.72rem' }}
                >
                  {copiedSection === 'cta' ? <Check size={11} color="var(--color-success)" /> : <Copy size={11} />}
                  <span>{copiedSection === 'cta' ? 'Copied' : 'Copy'}</span>
                </button>
              </div>

              {isEditing ? (
                <input
                  type="text"
                  className="form-input"
                  value={editedCta}
                  onChange={(e) => setEditedCta(e.target.value)}
                />
              ) : (
                <div style={{
                  background: 'var(--bg-soft)',
                  border: '1px solid var(--border-warm)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '0.75rem 1rem',
                  fontWeight: '500',
                  color: 'var(--text-main)',
                  fontSize: '0.88rem'
                }}>
                  {currentContent.cta || 'None'}
                </div>
              )}
            </div>

            {/* Hashtags if applicable */}
            {currentContent.hashtags && currentContent.hashtags.length > 0 && (
              <div style={{ marginBottom: '1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                  <label className="form-label" style={{ margin: 0, fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    Hashtags
                  </label>
                  <button
                    onClick={() => handleCopy(currentContent.hashtags?.join(' ') || '', 'hashtags')}
                    className="btn-outline"
                    style={{ padding: '2px 6px', fontSize: '0.72rem' }}
                  >
                    {copiedSection === 'hashtags' ? <Check size={11} color="var(--color-success)" /> : <Copy size={11} />}
                    <span>{copiedSection === 'hashtags' ? 'Copied' : 'Copy'}</span>
                  </button>
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
                  {currentContent.hashtags.map((tag, i) => (
                    <span
                      key={i}
                      style={{
                        background: 'var(--bg-soft)',
                        border: '1px solid var(--border-warm)',
                        padding: '3px 8px',
                        borderRadius: 'var(--radius-full)',
                        fontSize: '0.78rem',
                        color: 'var(--text-body)'
                      }}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Commercial Photo Actions */}
            <div style={{
              paddingTop: '1.25rem',
              borderTop: '1px solid var(--border-warm)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '0.5rem'
            }}>
              <div>
                <div style={{ fontSize: '0.85rem', fontWeight: '600' }}>Commercial Photography</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  High-resolution photo for {currentContent.product_or_subject}
                </div>
              </div>
              <div style={{ display: 'flex', gap: '0.4rem' }}>
                <button
                  onClick={handleGenerateImage}
                  disabled={generatingImage}
                  className="btn-secondary"
                  style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem' }}
                >
                  <ImageIcon size={13} />
                  <span>{generatingImage ? 'Updating...' : 'Shuffle image'}</span>
                </button>

                {currentContent.image_url && (
                  <a
                    href={currentContent.image_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-outline"
                    style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem', textDecoration: 'none' }}
                  >
                    <ExternalLink size={13} /> Open HD photo
                  </a>
                )}
              </div>
            </div>
          </div>

          {/* Quick Export Formats */}
          <div className="card" style={{ padding: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Export campaign:</span>
            <div style={{ display: 'flex', gap: '0.4rem' }}>
              <button onClick={downloadTextFile} className="btn-outline">
                <Download size={13} /> Text (.txt)
              </button>
              <button onClick={downloadJsonFile} className="btn-outline">
                <Download size={13} /> Data (.json)
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Adjustment Modal */}
      {showRegenModal && (
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
          <div className="card" style={{ width: '100%', maxWidth: '440px', padding: '1.75rem', background: '#FFFFFF', boxShadow: 'var(--shadow-float)' }}>
            <h3 className="editorial-heading" style={{ fontSize: '1.3rem', marginBottom: '0.25rem' }}>
              Adjust Content
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
              Refine the tone or offer details for this campaign.
            </p>

            <div className="form-group">
              <label className="form-label">Voice & Style</label>
              <select
                className="form-select"
                value={tweakTone}
                onChange={(e) => setTweakTone(e.target.value)}
              >
                <option value="premium">Premium</option>
                <option value="friendly">Friendly</option>
                <option value="energetic">Bold</option>
                <option value="minimal">Minimal</option>
                <option value="funny">Playful</option>
                <option value="professional">Elegant</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Update Offer (Optional)</label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. Flat 30% OFF this weekend"
                value={tweakOffer}
                onChange={(e) => setTweakOffer(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="form-label">Custom note (Optional)</label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. Make it punchier, highlight weekend dining"
                value={tweakNote}
                onChange={(e) => setTweakNote(e.target.value)}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem', marginTop: '1.5rem' }}>
              <button onClick={() => setShowRegenModal(false)} className="btn-secondary">
                Cancel
              </button>
              <button onClick={handleRegenerate} className="btn-primary">
                Update content →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
