import React from 'react';
import { 
  LayoutDashboard, 
  MessageSquare, 
  BookOpen, 
  Settings, 
  LogOut, 
  ChevronDown,
  CheckCircle2,
  RefreshCw
} from 'lucide-react';
import { UserProfile } from '../types';
import './Sidebar.css';

interface SidebarProps {
  user: UserProfile | null;
  activeTab: string;
  onTabChange: (tab: string) => void;
  onLogout: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  user, 
  activeTab, 
  onTabChange, 
  onLogout 
}) => {
  return (
    <div className="sidebar">
      {/* Header */}
      <div className="sidebar-header">
        <div className="logo-container">
          <div className="logo-icon"></div>
          <span className="logo-text">CLAI</span>
        </div>
      </div>

      {/* Workspace Selector */}
      <div className="sidebar-section">
        <div className="section-label">WORKSPACE</div>
        <button className="workspace-selector">
          <span>Fall 2024 Semester</span>
          <ChevronDown size={16} />
        </button>
      </div>

      {/* Navigation */}
      <div className="sidebar-section">
        <div className="section-label">NAVIGATION</div>
        <nav className="sidebar-nav">
          <button 
            className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => onTabChange('dashboard')}
          >
            <LayoutDashboard size={20} />
            <span>Dashboard</span>
          </button>
          
          <button 
            className={`nav-item ${activeTab === 'ai-assistant' ? 'active' : ''}`}
            onClick={() => onTabChange('ai-assistant')}
          >
            <MessageSquare size={20} />
            <span>AI Assistant</span>
          </button>
          
          <button 
            className={`nav-item ${activeTab === 'courses' ? 'active' : ''}`}
            onClick={() => onTabChange('courses')}
          >
            <BookOpen size={20} />
            <span>Courses</span>
          </button>
          
          <button 
            className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`}
            onClick={() => onTabChange('settings')}
          >
            <Settings size={20} />
            <span>Settings</span>
          </button>
        </nav>
      </div>

      {/* Integrations */}
      <div className="sidebar-section">
        <div className="section-label">INTEGRATIONS</div>
        <div className="integration-item">
          <div className="integration-info">
            <span className="integration-name">Canvas LMS</span>
            <div className="status-badge connected">
              <div className="status-dot"></div>
              <span>Connected</span>
            </div>
          </div>
        </div>
        
        <div className="integration-item">
          <div className="integration-info">
            <span className="integration-name">Student Gateway</span>
            <div className="status-badge syncing">
              <div className="status-dot"></div>
              <span>Syncing</span>
            </div>
          </div>
        </div>
      </div>

      {/* User Profile (Bottom) */}
      <div className="sidebar-footer">
        <div className="user-profile">
          <div className="user-avatar">
            {user?.avatar_url ? (
              <img src={user.avatar_url} alt={user.name} />
            ) : (
              <div className="avatar-placeholder">
                {user?.name?.charAt(0) || 'U'}
              </div>
            )}
          </div>
          <div className="user-info">
            <div className="user-name">{user?.name || 'Loading...'}</div>
            <div className="user-role">{user?.title || 'Faculty'}</div>
          </div>
          <button className="logout-btn" onClick={onLogout} title="Sign Out">
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};
