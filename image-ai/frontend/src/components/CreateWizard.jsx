import React, { useState, useEffect } from 'react';
import { 
  Utensils, 
  Shirt, 
  Building, 
  Scissors, 
  Smartphone, 
  Instagram, 
  Facebook, 
  MessageCircle, 
  FileText, 
  Megaphone, 
  Video, 
  Mail, 
  ArrowRight, 
  ArrowLeft, 
  Check, 
  Image as ImageIcon,
  Tag
} from 'lucide-react';
import { api } from '../api';

const industryIconMap = {
  restaurant: Utensils,
  clothing: Shirt,
  real_estate: Building,
  salon: Scissors,
  electronics: Smartphone
};

const contentTypeIconMap = {
  instagram_post: Instagram,
  facebook_post: Facebook,
  whatsapp_message: MessageCircle,
  product_description: FileText,
  ad_copy: Megaphone,
  reel_script: Video,
  marketing_email: Mail
};

export default function CreateWizard({ initialIndustry, onGenerationComplete, brandProfile }) {
  const [step, setStep] = useState(1);
  const [industries, setIndustries] = useState([]);
  const [industryOptions, setIndustryOptions] = useState(null);
  const [loadingOptions, setLoadingOptions] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [generationPhase, setGenerationPhase] = useState('');
  const [error, setError] = useState('');

  // Form state
  const [selectedIndustry, setSelectedIndustry] = useState(initialIndustry || 'restaurant');
  const [selectedContentType, setSelectedContentType] = useState('instagram_post');
  const [product, setProduct] = useState('Biryani');
  const [objective, setObjective] = useState('promotion');
  const [offer, setOffer] = useState('20% OFF');
  const [tone, setTone] = useState(brandProfile?.preferred_tone || 'premium');
  const [language, setLanguage] = useState(brandProfile?.preferred_language || 'telugu');
  const [generateImage, setGenerateImage] = useState(true);
  const [includeCta, setIncludeCta] = useState(true);
  const [extraFields, setExtraFields] = useState({});

  const toneLabels = [
    { id: 'premium', label: 'Premium', desc: 'Refined & sophisticated' },
    { id: 'friendly', label: 'Friendly', desc: 'Warm & conversational' },
    { id: 'energetic', label: 'Bold', desc: 'High-energy & urgent' },
    { id: 'minimal', label: 'Minimal', desc: 'Clean & direct' },
    { id: 'funny', label: 'Playful', desc: 'Engaging & light-hearted' },
    { id: 'professional', label: 'Elegant', desc: 'Polished & trustworthy' }
  ];

  useEffect(() => {
    async function loadIndustries() {
      try {
        const data = await api.getIndustries();
        setIndustries(data);
      } catch (err) {
        console.error('Failed to load industries', err);
      }
    }
    loadIndustries();
  }, []);

  useEffect(() => {
    async function loadOptions() {
      if (!selectedIndustry) return;
      setLoadingOptions(true);
      try {
        const data = await api.getIndustryOptions(selectedIndustry);
        setIndustryOptions(data);
        
        if (data.fields && data.fields.length > 0) {
          const prodField = data.fields.find(f => f.key === 'product');
          if (prodField && prodField.options && prodField.options.length > 0) {
            if (selectedIndustry === 'restaurant') {
              setProduct('Biryani');
              setOffer('20% OFF');
            } else {
              setProduct(prodField.options[0]);
            }
          }
        }
      } catch (err) {
        console.error('Failed to load industry options', err);
      } finally {
        setLoadingOptions(false);
      }
    }
    loadOptions();
  }, [selectedIndustry]);

  const handleExtraFieldChange = (key, val) => {
    setExtraFields(prev => ({ ...prev, [key]: val }));
  };

  const handleGenerate = async () => {
    if (!product.trim()) {
      setError('Please enter what you are creating content for.');
      return;
    }

    setError('');
    setGenerating(true);
    setGenerationPhase('Creating your post...');
    setTimeout(() => setGenerationPhase('Choosing the right words...'), 500);
    setTimeout(() => setGenerationPhase('Preparing your message...'), 1000);

    try {
      const payload = {
        industry: selectedIndustry,
        content_type: selectedContentType,
        product: product.trim(),
        objective: objective,
        offer: offer.trim(),
        tone: tone,
        language: language,
        platform: industryOptions?.content_types?.find(c => c.id === selectedContentType)?.platform || 'instagram',
        length: 'medium',
        include_cta: includeCta,
        generate_image: generateImage,
        extra_fields: extraFields
      };

      const result = await api.generateContent(payload);
      onGenerationComplete(result);
    } catch (err) {
      setError(err.message || 'Could not generate content. Please try again.');
      setGenerating(false);
    }
  };

  return (
    <div style={{ maxWidth: '820px', margin: '0 auto' }}>
      {/* Editorial Header */}
      <div style={{ marginBottom: '1.75rem' }}>
        <h2 className="editorial-heading" style={{ fontSize: '1.75rem' }}>
          Create Content
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '2px' }}>
          Step {step} of 3: {step === 1 ? 'Select format' : step === 2 ? 'Campaign details' : 'Voice & language'}
        </p>
      </div>

      {/* Stepper */}
      <div className="stepper-container">
        <div 
          className={`stepper-step ${step === 1 ? 'active' : step > 1 ? 'completed' : ''}`}
          onClick={() => step > 1 && setStep(1)}
        >
          <div className="step-circle">{step > 1 ? <Check size={13} /> : '1'}</div>
          <div className="step-label">1. What are you creating?</div>
        </div>

        <div style={{ flex: 1, height: '1px', background: 'var(--border-warm)', margin: '0 1rem' }} />

        <div 
          className={`stepper-step ${step === 2 ? 'active' : step > 2 ? 'completed' : ''}`}
          onClick={() => step > 2 && setStep(2)}
        >
          <div className="step-circle">{step > 2 ? <Check size={13} /> : '2'}</div>
          <div className="step-label">2. What's it about?</div>
        </div>

        <div style={{ flex: 1, height: '1px', background: 'var(--border-warm)', margin: '0 1rem' }} />

        <div 
          className={`stepper-step ${step === 3 ? 'active' : ''}`}
        >
          <div className="step-circle">3</div>
          <div className="step-label">3. How should it feel?</div>
        </div>
      </div>

      {error && (
        <div style={{
          background: '#FDF2F2',
          border: '1px solid #F8B4B4',
          borderRadius: 'var(--radius-sm)',
          padding: '0.75rem 1rem',
          color: 'var(--color-error)',
          marginBottom: '1.25rem',
          fontSize: '0.85rem'
        }}>
          {error}
        </div>
      )}

      {/* STEP 1: Format & Industry */}
      {step === 1 && (
        <div className="card" style={{ padding: '2rem' }}>
          <div style={{ marginBottom: '2rem' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: '600', marginBottom: '0.35rem' }}>
              Select your business sector
            </h3>

            <div className="option-grid">
              {industries.map((ind) => {
                const Icon = industryIconMap[ind.id] || Utensils;
                const isSelected = selectedIndustry === ind.id;
                return (
                  <div
                    key={ind.id}
                    onClick={() => setSelectedIndustry(ind.id)}
                    className={`option-card ${isSelected ? 'selected' : ''}`}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <div className="option-badge">
                        <Icon size={17} />
                      </div>
                      {isSelected && <Check size={15} color="var(--accent-terracotta)" />}
                    </div>
                    <div style={{ fontWeight: '600', fontSize: '0.95rem' }}>{ind.name}</div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>{ind.description}</div>
                  </div>
                );
              })}
            </div>
          </div>

          <div style={{ paddingTop: '1.75rem', borderTop: '1px solid var(--border-warm)' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: '600', marginBottom: '0.35rem' }}>
              What format are you creating?
            </h3>

            <div className="option-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))' }}>
              {industryOptions?.content_types?.map((ct) => {
                const Icon = contentTypeIconMap[ct.id] || Instagram;
                const isSelected = selectedContentType === ct.id;
                return (
                  <div
                    key={ct.id}
                    onClick={() => setSelectedContentType(ct.id)}
                    className={`option-card ${isSelected ? 'selected' : ''}`}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <div className="option-badge">
                        <Icon size={16} />
                      </div>
                      {isSelected && <Check size={15} color="var(--accent-terracotta)" />}
                    </div>
                    <div style={{ fontWeight: '600', fontSize: '0.9rem' }}>{ct.label}</div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>{ct.desc}</div>
                  </div>
                );
              })}
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '2rem' }}>
            <button
              onClick={() => setStep(2)}
              className="btn-primary"
            >
              Continue →
            </button>
          </div>
        </div>
      )}

      {/* STEP 2: Questionnaire Details */}
      {step === 2 && (
        <div className="card" style={{ padding: '2rem' }}>
          <div style={{ marginBottom: '1.5rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: '600' }}>
              What are you highlighting?
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              Enter the main item or dish for your {industryOptions?.name?.toLowerCase()}.
            </p>
          </div>

          {/* Product / Dish */}
          <div className="form-group">
            <label className="form-label">
              Product, dish, or service name *
            </label>
            <input
              type="text"
              className="form-input"
              value={product}
              onChange={(e) => setProduct(e.target.value)}
              placeholder="e.g. Hyderabadi Dum Biryani, Kanchipuram Saree, 3 BHK Luxury Flat"
            />
            <div className="pill-group">
              <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', alignSelf: 'center' }}>Suggestions:</span>
              {industryOptions?.fields?.find(f => f.key === 'product')?.options?.map((opt, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => setProduct(opt)}
                  className={`pill-item ${product === opt ? 'active' : ''}`}
                >
                  {opt}
                </button>
              ))}
            </div>
          </div>

          {/* Offer / Occasion */}
          <div className="form-group" style={{ marginTop: '1.5rem' }}>
            <label className="form-label">
              What's the occasion or offer?
            </label>
            <input
              type="text"
              className="form-input"
              value={offer}
              onChange={(e) => setOffer(e.target.value)}
              placeholder="e.g. 20% OFF this weekend, Buy 1 Get 1 Free, Festival Special"
            />
            <div className="pill-group">
              <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', alignSelf: 'center' }}>Common offers:</span>
              {["20% OFF", "Buy 1 Get 1 Free", "Flat ₹100 OFF", "Weekend Special", "No discount (Quality focus)"].map((off, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => setOffer(off === "No discount (Quality focus)" ? "" : off)}
                  className={`pill-item ${offer === off ? 'active' : (off.startsWith('No') && !offer ? 'active' : '')}`}
                >
                  {off}
                </button>
              ))}
            </div>
          </div>

          {/* Dynamic Extra Fields */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.25rem', marginTop: '1.5rem' }}>
            {industryOptions?.fields?.filter(f => f.key !== 'product' && f.key !== 'offer').map((field) => (
              <div key={field.key} className="form-group">
                <label className="form-label">{field.label}</label>
                {field.type === 'select' ? (
                  <select
                    className="form-select"
                    value={extraFields[field.key] || field.default || ''}
                    onChange={(e) => handleExtraFieldChange(field.key, e.target.value)}
                  >
                    {field.options?.map((opt) => (
                      <option key={typeof opt === 'string' ? opt : opt.id} value={typeof opt === 'string' ? opt : opt.id}>
                        {typeof opt === 'string' ? opt : opt.label}
                      </option>
                    ))}
                  </select>
                ) : (
                  <div>
                    <input
                      type="text"
                      className="form-input"
                      value={extraFields[field.key] || ''}
                      onChange={(e) => handleExtraFieldChange(field.key, e.target.value)}
                      placeholder={field.placeholder || 'Type or choose below'}
                    />
                    {field.options && (
                      <div className="pill-group">
                        {field.options.slice(0, 3).map((opt, i) => (
                          <button
                            key={i}
                            type="button"
                            onClick={() => handleExtraFieldChange(field.key, opt)}
                            className={`pill-item ${extraFields[field.key] === opt ? 'active' : ''}`}
                          >
                            {opt}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Brand profile preview note */}
          {brandProfile && brandProfile.business_name && (
            <div style={{
              background: 'var(--bg-soft)',
              border: '1px solid var(--border-warm)',
              borderRadius: 'var(--radius-sm)',
              padding: '0.75rem 1rem',
              marginTop: '1.5rem',
              fontSize: '0.82rem',
              color: 'var(--text-body)'
            }}>
              Including details for <b>{brandProfile.business_name}</b> ({brandProfile.location || 'Local'})
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '2rem' }}>
            <button
              onClick={() => setStep(1)}
              className="btn-secondary"
            >
              <ArrowLeft size={15} /> Back
            </button>
            <button
              onClick={() => setStep(3)}
              className="btn-primary"
            >
              Continue →
            </button>
          </div>
        </div>
      )}

      {/* STEP 3: Voice, Language & Generate */}
      {step === 3 && (
        <div className="card" style={{ padding: '2rem' }}>
          {/* Tone: How should it feel? */}
          <div style={{ marginBottom: '2rem' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: '600', marginBottom: '0.35rem' }}>
              How should it feel?
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '0.85rem' }}>
              Select the voice and personality of this campaign.
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: '0.75rem' }}>
              {toneLabels.map((t) => {
                const isSelected = tone === t.id;
                return (
                  <div
                    key={t.id}
                    onClick={() => setTone(t.id)}
                    className={`option-card ${isSelected ? 'selected' : ''}`}
                    style={{ padding: '0.85rem' }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontWeight: '600', fontSize: '0.9rem' }}>{t.label}</span>
                      {isSelected && <Check size={14} color="var(--accent-terracotta)" />}
                    </div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>{t.desc}</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Language */}
          <div style={{ marginBottom: '2rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border-warm)' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: '600', marginBottom: '0.35rem' }}>
              Language
            </h3>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.75rem' }}>
              {industryOptions?.languages?.map((lang) => {
                const isSelected = language === lang.id;
                return (
                  <div
                    key={lang.id}
                    onClick={() => setLanguage(lang.id)}
                    className={`option-card ${isSelected ? 'selected' : ''}`}
                    style={{ padding: '0.85rem' }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '1.2rem' }}>{lang.flag}</span>
                      {isSelected && <Check size={14} color="var(--accent-terracotta)" />}
                    </div>
                    <div style={{ fontWeight: '600', fontSize: '0.95rem' }}>{lang.label}</div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>{lang.native}</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Output Toggles */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
            gap: '1rem',
            paddingTop: '1.5rem',
            borderTop: '1px solid var(--border-warm)',
            marginBottom: '2rem'
          }}>
            <div
              onClick={() => setGenerateImage(!generateImage)}
              className="card"
              style={{
                padding: '0.9rem 1.15rem',
                cursor: 'pointer',
                border: generateImage ? '1px solid var(--accent-terracotta)' : '1px solid var(--border-warm)',
                background: generateImage ? 'var(--accent-terracotta-soft)' : '#FFFFFF'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', fontWeight: '500', fontSize: '0.88rem' }}>
                  <ImageIcon size={16} />
                  <span>Generate companion image</span>
                </div>
                <input
                  type="checkbox"
                  checked={generateImage}
                  onChange={() => {}}
                  style={{ width: '16px', height: '16px', accentColor: 'var(--accent-terracotta)' }}
                />
              </div>
            </div>

            <div
              onClick={() => setIncludeCta(!includeCta)}
              className="card"
              style={{
                padding: '0.9rem 1.15rem',
                cursor: 'pointer',
                border: includeCta ? '1px solid var(--accent-terracotta)' : '1px solid var(--border-warm)',
                background: includeCta ? 'var(--accent-terracotta-soft)' : '#FFFFFF'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', fontWeight: '500', fontSize: '0.88rem' }}>
                  <Tag size={16} />
                  <span>Include call to action line</span>
                </div>
                <input
                  type="checkbox"
                  checked={includeCta}
                  onChange={() => {}}
                  style={{ width: '16px', height: '16px', accentColor: 'var(--accent-terracotta)' }}
                />
              </div>
            </div>
          </div>

          {/* Action Footer */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <button
              onClick={() => setStep(2)}
              className="btn-secondary"
            >
              <ArrowLeft size={15} /> Back
            </button>

            <button
              onClick={handleGenerate}
              disabled={generating}
              className="btn-primary"
              style={{ padding: '0.8rem 2.25rem', fontSize: '0.95rem' }}
            >
              {generating ? (
                <>
                  <div className="animate-spin" style={{ width: '16px', height: '16px', border: '2px solid white', borderTopColor: 'transparent', borderRadius: '50%' }} />
                  <span>Creating content…</span>
                </>
              ) : (
                <>
                  <span>Create content →</span>
                </>
              )}
            </button>
          </div>

          {generating && (
            <div style={{
              marginTop: '1.25rem',
              padding: '0.85rem',
              background: 'var(--bg-soft)',
              border: '1px solid var(--border-warm)',
              borderRadius: 'var(--radius-sm)',
              textAlign: 'center',
              fontSize: '0.85rem',
              color: 'var(--text-muted)'
            }}>
              {generationPhase}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
