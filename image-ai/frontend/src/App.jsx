import React, { useState, useEffect } from 'react';
import { Menu, Layers } from 'lucide-react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import AuthModal from './components/AuthModal';
import DashboardView from './components/DashboardView';
import CreateWizard from './components/CreateWizard';
import ResultView from './components/ResultView';
import HistoryView from './components/HistoryView';
import BrandProfileView from './components/BrandProfileView';
import SettingsView from './components/SettingsView';
import PromptAgentView from './components/PromptAgentView';
import { api } from './api';

export default function App() {
  const [currentView, setCurrentView] = useState('agent');
  const [user, setUser] = useState(null);
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [brandProfile, setBrandProfile] = useState(null);
  const [industries, setIndustries] = useState([]);
  const [usage, setUsage] = useState(null);
  const [recentHistory, setRecentHistory] = useState([]);
  const [selectedContent, setSelectedContent] = useState(null);
  const [wizardIndustry, setWizardIndustry] = useState('restaurant');
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  // Load user, profile, industries, usage and recent history on mount
  useEffect(() => {
    async function initData() {
      try {
        const [me, profile, inds, usg, hist] = await Promise.all([
          api.getMe().catch(() => null),
          api.getBusinessProfile().catch(() => null),
          api.getIndustries().catch(() => []),
          api.getUsage().catch(() => null),
          api.getHistory().catch(() => [])
        ]);

        if (me) setUser(me);
        if (profile) setBrandProfile(profile);
        if (inds) setIndustries(inds);
        if (usg) setUsage(usg);
        if (hist) setRecentHistory(hist);
      } catch (err) {
        console.error('Initialization error', err);
      }
    }
    initData();
  }, []);

  const refreshAllData = async () => {
    try {
      const [profile, usg, hist] = await Promise.all([
        api.getBusinessProfile().catch(() => null),
        api.getUsage().catch(() => null),
        api.getHistory().catch(() => [])
      ]);
      if (profile) setBrandProfile(profile);
      if (usg) setUsage(usg);
      if (hist) setRecentHistory(hist);
    } catch (e) {}
  };

  const handleAuthSuccess = (userData) => {
    setUser(userData);
    refreshAllData();
  };

  const handleLogout = () => {
    localStorage.removeItem('saas_access_token');
    setUser(null);
    window.location.reload();
  };

  const handleLaunchIndustry = (industryId) => {
    setWizardIndustry(industryId);
    setCurrentView('create');
  };

  const handleGenerationComplete = (generatedContent) => {
    setSelectedContent(generatedContent);
    setCurrentView('result');
    refreshAllData();
  };

  const handleViewContent = (contentItem) => {
    setSelectedContent(contentItem);
    setCurrentView('result');
  };

  return (
    <div className="app-container">
      {/* Mobile Top Bar */}
      <div className="mobile-top-bar" style={{ width: '100%' }}>
        <button
          onClick={() => setMobileNavOpen(true)}
          style={{ background: 'transparent', border: 'none', color: 'var(--text-main)', cursor: 'pointer', padding: '6px', display: 'flex', alignItems: 'center' }}
          aria-label="Open menu"
        >
          <Menu size={22} />
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div className="logo-badge" style={{ width: '26px', height: '26px' }}>
            <Layers size={14} />
          </div>
          <span style={{ fontFamily: 'var(--font-serif)', fontWeight: '600', fontSize: '1.05rem', color: 'var(--text-main)' }}>
            Content Studio
          </span>
        </div>

        <div style={{ width: '28px' }} /> {/* Spacer for balance */}
      </div>

      {/* Sidebar Navigation */}
      <Sidebar
        currentView={currentView}
        setView={setCurrentView}
        user={user}
        onLogout={handleLogout}
        onOpenAuth={() => setIsAuthOpen(true)}
        mobileOpen={mobileNavOpen}
        onCloseMobile={() => setMobileNavOpen(false)}
      />

      {/* Main Workspace Area */}
      <main className="app-main">
        <Navbar
          brandProfile={brandProfile}
          setView={setCurrentView}
        />

        {currentView === 'agent' && (
          <PromptAgentView user={user} onOpenAuth={() => setIsAuthOpen(true)} onImageGenerated={refreshAllData} />
        )}

        {currentView === 'dashboard' && (
          <DashboardView
            industries={industries}
            usage={usage}
            recentHistory={recentHistory}
            onSelectIndustry={handleLaunchIndustry}
            onViewContent={handleViewContent}
            setView={setCurrentView}
          />
        )}

        {currentView === 'create' && (
          <CreateWizard
            initialIndustry={wizardIndustry}
            brandProfile={brandProfile}
            onGenerationComplete={handleGenerationComplete}
          />
        )}

        {currentView === 'result' && selectedContent && (
          <ResultView
            content={selectedContent}
            brandProfile={brandProfile}
            onBack={() => setCurrentView('agent')}
            onContentUpdated={(updated) => {
              setSelectedContent(updated);
              refreshAllData();
            }}
          />
        )}

        {currentView === 'history' && (
          <HistoryView
            onViewContent={handleViewContent}
            setView={setCurrentView}
          />
        )}

        {currentView === 'brand' && (
          <BrandProfileView
            brandProfile={brandProfile}
            onProfileUpdated={(updated) => setBrandProfile(updated)}
          />
        )}

        {currentView === 'settings' && (
          <SettingsView
            usage={usage}
          />
        )}
      </main>

      {/* Auth Modal */}
      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        onAuthSuccess={handleAuthSuccess}
      />
    </div>
  );
}
