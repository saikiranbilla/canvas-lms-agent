import React from 'react';
import { motion } from 'framer-motion';
import { Users, CheckCircle, Clock, TrendingUp } from 'lucide-react';
import { Delegation } from '../types';
import './ObservabilitySidebar.css';

interface ObservabilitySidebarProps {
  delegations: Delegation[];
  totalDelegations: number;
  activeDelegations: number;
  completedDelegations: number;
}

export const ObservabilitySidebar: React.FC<ObservabilitySidebarProps> = ({
  delegations,
  totalDelegations,
  activeDelegations,
  completedDelegations
}) => {
  const getStatusIcon = (status: Delegation['status']) => {
    switch (status) {
      case 'running':
        return <Clock size={12} className="status-icon running" />;
      case 'completed':
        return <CheckCircle size={12} className="status-icon completed" />;
      case 'failed':
        return <div className="status-dot failed" />;
      default:
        return <div className="status-dot pending" />;
    }
  };

  const getStatusColor = (status: Delegation['status']) => {
    switch (status) {
      case 'running':
        return 'running';
      case 'completed':
        return 'completed';
      case 'failed':
        return 'failed';
      default:
        return 'pending';
    }
  };

  return (
    <motion.div
      className="observability-sidebar"
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      {/* Stats Overview */}
      <div className="stats-overview">
        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp size={16} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{totalDelegations}</div>
            <div className="stat-label">Total Tasks</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <Clock size={16} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{activeDelegations}</div>
            <div className="stat-label">Active</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">
            <CheckCircle size={16} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{completedDelegations}</div>
            <div className="stat-label">Completed</div>
          </div>
        </div>
      </div>

      {/* Delegations List */}
      <div className="delegations-section">
        <div className="section-header">
          <Users size={16} />
          <h4>Delegations</h4>
        </div>
        
        <div className="delegations-list">
          {delegations.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🤖</div>
              <p>No active delegations</p>
            </div>
          ) : (
            delegations.map((delegation) => (
              <motion.div
                key={delegation.id}
                className={`delegation-item ${getStatusColor(delegation.status)}`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <div className="delegation-header">
                  <div className="delegation-agent">
                    {delegation.agent.replace('_', ' ')}
                  </div>
                  <div className="delegation-status">
                    {getStatusIcon(delegation.status)}
                  </div>
                </div>
                <div className="delegation-task">
                  {delegation.task}
                </div>
                <div className="delegation-time">
                  {delegation.timestamp.toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </div>
              </motion.div>
            ))
          )}
        </div>
      </div>

      {/* Audit Trail */}
      <div className="audit-section">
        <div className="section-header">
          <CheckCircle size={16} />
          <h4>Audit Trail</h4>
        </div>
        
        <div className="audit-list">
          <div className="audit-item">
            <div className="audit-time">2m ago</div>
            <div className="audit-action">Supervisor initialized</div>
          </div>
          <div className="audit-item">
            <div className="audit-time">1m ago</div>
            <div className="audit-action">Canvas Executor activated</div>
          </div>
          <div className="audit-item">
            <div className="audit-time">30s ago</div>
            <div className="audit-action">Content Specialist ready</div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};