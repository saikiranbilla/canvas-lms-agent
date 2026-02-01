import React, { useEffect, useState } from 'react';
import { 
  Activity, Server, Database, Cpu, CheckCircle2, AlertCircle, 
  RefreshCw, Play, MessageSquare, Terminal, Zap, Clock, 
  BarChart2, Shield, Settings, ChevronDown, ExternalLink
} from 'lucide-react';
import { UserProfile, AgentState } from '../types';
import { AgentInspector } from './AgentInspector';
import './AgentDashboard.css';

interface AgentStatusData {
  system_status: {
    supervisor: string;
    canvas_mcp: string;
    tool_execution: string;
    memory: string;
    last_run: string;
  };
  canvas_integration: {
    status: string;
    token_valid: boolean;
    mcp_health: string;
    available_tools: number;
    last_successful_call: string;
  };
  metrics: {
    conversations_today: number;
    agent_runs_today: number;
    avg_response_time: number;
    most_used_tool: string;
  };
  recent_runs: Array<{
    id: string;
    intent: string;
    tools: string[];
    duration: string;
    status: string;
    timestamp: string;
  }>;
}

interface AgentDashboardProps {
  token: string;
  user: UserProfile | null;
  agents: AgentState[];
  onAction: (action: string, payload?: any) => void;
}

export const AgentDashboard: React.FC<AgentDashboardProps> = ({ token, user, agents, onAction }) => {
  const [data, setData] = useState<AgentStatusData | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/agent/status', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const result = await response.json();
        setData(result);
      }
    } catch (error) {
      console.error('Failed to fetch agent status:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Auto-refresh every 30s
    return () => clearInterval(interval);
  }, [token]);

  const handleRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  const formatDate = (isoString: string) => {
    return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  if (loading) {
    return <div className="dashboard-loading">Loading Agent System...</div>;
  }

  return (
    <div className="agent-dashboard">
      {/* Top Header Bar */}
      <header className="dashboard-header">
        <div className="header-left">
          <h1 className="welcome-text">
            Welcome back, <span className="user-name">{user?.short_name || 'Instructor'}</span>
          </h1>
          <div className="workspace-selector">
            <span>Fall 2024 Semester</span>
            <ChevronDown size={14} />
          </div>
        </div>
        <div className="header-right">
          <div className="status-badge success">
            <div className="dot"></div>
            Canvas Connected
          </div>
          <div className="status-badge success">
            <div className="dot"></div>
            Agent Active
          </div>
        </div>
      </header>

      <div className="dashboard-grid">
        {/* Column 1: System Health */}
        <div className="dashboard-column">
          {/* Agent System Status Card */}
          <div className="dashboard-card">
            <div className="card-header">
              <h3><Cpu size={18} /> System Status</h3>
              <div className="live-indicator"></div>
            </div>
            <div className="status-list">
              <div className="status-item">
                <span className="label">Supervisor Agent</span>
                <span className="value ready"><div className="dot"></div> Ready</span>
              </div>
              <div className="status-item">
                <span className="label">Canvas MCP Tools</span>
                <span className="value connected"><div className="dot"></div> Connected</span>
              </div>
              <div className="status-item">
                <span className="label">Tool Execution</span>
                <span className="value available"><div className="dot"></div> Available</span>
              </div>
              <div className="status-item">
                <span className="label">Memory</span>
                <span className="value active"><div className="dot"></div> Active</span>
              </div>
              <div className="status-item last-run">
                <span className="label">Last Run</span>
                <span className="value">{data?.system_status.last_run ? formatDate(data.system_status.last_run) : '-'}</span>
              </div>
            </div>
          </div>

          {/* Canvas Integration Card */}
          <div className="dashboard-card">
            <div className="card-header">
              <h3><Database size={18} /> Canvas Integration</h3>
            </div>
            <div className="integration-stats">
              <div className="stat-row">
                <span className="label">Token Status</span>
                <span className="value valid"><CheckCircle2 size={14} /> Valid</span>
              </div>
              <div className="stat-row">
                <span className="label">MCP Health</span>
                <span className="value healthy">Healthy</span>
              </div>
              <div className="stat-row">
                <span className="label">Available Tools</span>
                <span className="value number">{data?.canvas_integration.available_tools}</span>
              </div>
              <div className="stat-row">
                <span className="label">Last Call</span>
                <span className="value">{data?.canvas_integration.last_successful_call ? formatDate(data.canvas_integration.last_successful_call) : '-'}</span>
              </div>
            </div>
            <button className="card-action-btn" onClick={() => onAction('test_connection')}>
              Test Connection
            </button>
          </div>

          {/* Capabilities Overview */}
          <div className="dashboard-card">
            <div className="card-header">
              <h3><Shield size={18} /> Capabilities</h3>
            </div>
            <div className="capabilities-list">
              {['Courses', 'Assignments', 'Submissions', 'Enrollments', 'Announcements'].map(cap => (
                <div key={cap} className="capability-item">
                  <CheckCircle2 size={14} className="text-success" />
                  <span>{cap}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Column 2: Activity & Actions */}
        <div className="dashboard-column main-column">
          {/* AI Assistant Activity Snapshot */}
          <div className="metrics-grid">
            <div className="metric-tile">
              <div className="metric-label">Conversations Today</div>
              <div className="metric-value">{data?.metrics.conversations_today}</div>
              <MessageSquare size={16} className="metric-icon" />
            </div>
            <div className="metric-tile">
              <div className="metric-label">Agent Runs</div>
              <div className="metric-value">{data?.metrics.agent_runs_today}</div>
              <Zap size={16} className="metric-icon" />
            </div>
            <div className="metric-tile">
              <div className="metric-label">Avg Response</div>
              <div className="metric-value">{data?.metrics.avg_response_time}s</div>
              <Clock size={16} className="metric-icon" />
            </div>
            <div className="metric-tile">
              <div className="metric-label">Top Tool</div>
              <div className="metric-value small">{data?.metrics.most_used_tool.replace('Canvas_', '')}</div>
              <Terminal size={16} className="metric-icon" />
            </div>
          </div>

          {/* Quick Actions Panel */}
          <div className="dashboard-card">
            <div className="card-header">
              <h3><Zap size={18} /> Quick Actions</h3>
            </div>
            <div className="actions-grid">
              <button className="action-btn primary" onClick={() => onAction('open_assistant')}>
                <MessageSquare size={18} />
                Open Assistant
              </button>
              <button className="action-btn" onClick={() => onAction('new_session')}>
                <Play size={18} />
                New Session
              </button>
              <button className="action-btn" onClick={() => onAction('run_test')}>
                <Terminal size={18} />
                Run Tool Test
              </button>
              <button className="action-btn" onClick={handleRefresh} disabled={refreshing}>
                <RefreshCw size={18} className={refreshing ? 'spin' : ''} />
                Refresh Data
              </button>
            </div>
          </div>

          {/* Guided Prompt Panel */}
          <div className="dashboard-card">
            <div className="card-header">
              <h3><BarChart2 size={18} /> Try Asking the Assistant</h3>
            </div>
            <div className="prompts-grid">
              {[
                "Find students with missing work",
                "Draft an announcement",
                "Summarize course activity",
                "Help with grading",
                "Check assignment stats"
              ].map((prompt) => (
                <button 
                  key={prompt} 
                  className="prompt-chip"
                  onClick={() => onAction('prompt', prompt)}
                >
                  {prompt} <ArrowIcon />
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Column 3: Inspector & Recent Runs */}
        <div className="dashboard-column">
          {/* Agent Inspector */}
          <AgentInspector agents={agents} isCollapsed={false} />

          <div className="dashboard-card">
            <div className="card-header">
              <h3><Activity size={18} /> Recent Agent Runs</h3>
              <button className="icon-btn"><ExternalLink size={14} /></button>
            </div>
            <div className="recent-runs-feed">
              {data?.recent_runs.map((run) => (
                <div key={run.id} className="run-item">
                  <div className="run-header">
                    <span className={`status-dot ${run.status}`}></span>
                    <span className="run-time">{formatDate(run.timestamp)}</span>
                    <span className="run-duration">{run.duration}</span>
                  </div>
                  <div className="run-intent">{run.intent}</div>
                  <div className="run-tools">
                    {run.tools.map(tool => (
                      <span key={tool} className="tool-badge">{tool}</span>
                    ))}
                  </div>
                </div>
              ))}
              {(!data?.recent_runs || data.recent_runs.length === 0) && (
                <div className="empty-state">No recent activity</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ArrowIcon = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="5" y1="12" x2="19" y2="12"></line>
    <polyline points="12 5 19 12 12 19"></polyline>
  </svg>
);
