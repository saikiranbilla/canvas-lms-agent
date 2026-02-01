import React, { useState, useEffect } from 'react';
import { Sidebar } from './Sidebar';
import { CourseList } from './CourseList';
import { HomeView } from './HomeView';
import { AgentDashboard } from './AgentDashboard';
import { AIAssistantView } from './AIAssistantView';
import { AgentState, UserProfile } from '../types';

interface Course {
  id: number;
  name: string;
  course_code: string;
  total_students?: number;
  term?: { name: string };
}

interface DashboardProps {
  token: string;
  onLogout: () => void;
  onSelectCourse: (course: Course) => void;
  agents: AgentState[];
}

export const Dashboard: React.FC<DashboardProps> = ({ 
  token, 
  onLogout, 
  onSelectCourse,
  agents 
}) => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [initialPrompt, setInitialPrompt] = useState<string>('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        console.log('Fetching user profile...');
        const response = await fetch('http://localhost:8001/api/user/me', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        if (response.ok) {
          const data = await response.json();
          console.log('User profile fetched:', data);
          setUserProfile(data);
        } else {
          console.error('Failed to fetch user profile:', response.status);
        }
      } catch (error) {
        console.error('Failed to fetch user profile:', error);
      }
    };

    if (token) {
      fetchProfile();
    }
  }, [token]);

  const handleAgentAction = (action: string, payload?: any) => {
    switch (action) {
      case 'open_assistant':
      case 'new_session':
        setActiveTab('ai-assistant');
        break;
      case 'prompt':
        setInitialPrompt(payload);
        setActiveTab('ai-assistant');
        break;
      case 'run_test':
        console.log('Running tool test...');
        // Could trigger a toast here
        break;
      case 'test_connection':
        // Trigger connection test
        break;
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <AgentDashboard 
          token={token} 
          user={userProfile}
          agents={agents}
          onAction={handleAgentAction}
        />;
      case 'ai-assistant':
        return <AIAssistantView initialPrompt={initialPrompt} />;
      case 'courses':
        return <CourseList token={token} onSelectCourse={onSelectCourse} />;
      default:
        return (
          <div className="flex items-center justify-center h-full text-gray-500">
            Section under construction
          </div>
        );
    }
  };

  return (
    <div className="flex h-screen bg-parchment overflow-hidden" style={{ display: 'flex', flexDirection: 'row', height: '100vh', width: '100%' }}>
      {/* Left Sidebar */}
      <Sidebar 
        user={userProfile}
        activeTab={activeTab}
        onTabChange={setActiveTab}
        onLogout={onLogout}
      />

      {/* Main Content Area */}
      <div className="main-content flex-1 flex flex-col min-w-0 overflow-hidden">
        {renderContent()}
      </div>
    </div>
  );
};
