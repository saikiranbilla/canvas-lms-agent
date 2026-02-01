import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, Clock, Bot } from 'lucide-react';
import { AgentState } from '../types';
import './AgentInspector.css';

interface AgentInspectorProps {
  agents: AgentState[];
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
}

const getStatusIcon = (status: AgentState['status']) => {
  switch (status) {
    case 'active':
      return <div className="status-dot active" />;
    case 'planning':
      return <Clock size={12} className="status-icon planning" />;
    case 'completed':
      return <CheckCircle size={12} className="status-icon completed" />;
    case 'idle':
    default:
      return <div className="status-dot idle" />;
  }
};

const getStatusText = (status: AgentState['status']) => {
  switch (status) {
    case 'active':
      return 'Active';
    case 'planning':
      return 'Planning';
    case 'completed':
      return 'Completed';
    case 'idle':
      return 'Idle';
    default:
      return 'Unknown';
  }
};

export const AgentInspector: React.FC<AgentInspectorProps> = ({
  agents,
  isCollapsed = false,
  onToggleCollapse
}) => {
  return (
    <motion.div
      className={`agent-inspector ${isCollapsed ? 'collapsed' : ''}`}
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="inspector-header" onClick={onToggleCollapse}>
        <div className="inspector-title">
          <Bot size={16} />
          <span>Agent Inspector</span>
        </div>
        <div className="inspector-toggle">
          {isCollapsed ? '▶' : '▼'}
        </div>
      </div>

      <AnimatePresence>
        {!isCollapsed && (
          <motion.div
            className="inspector-content"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="agents-list">
              {agents.map((agent) => (
                <motion.div
                  key={agent.name}
                  className="agent-item"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="agent-header">
                    <div className="agent-name">
                      {agent.name.replace('_', ' ')}
                    </div>
                    <div className="agent-status">
                      {getStatusIcon(agent.status)}
                      <span>{getStatusText(agent.status)}</span>
                    </div>
                  </div>
                  {agent.lastAction && (
                    <div className="agent-action">
                      {agent.lastAction}
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};