import React, { useState, useRef, useEffect } from 'react';
import { 
  Search, Plus, FileText, RefreshCw, Send, 
  MessageSquare, ChevronRight, Sparkles, ChevronDown, ChevronUp
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { ChatAPI } from '../api/chat';
import { ChatMessage } from '../types';
import './AIAssistantView.css';

// Thinking Process Types
interface ThinkingStep {
  id: string;
  agent: string;
  icon: string;
  title: string;
  action: string;
  debugInfo?: string;
  result?: string;
  duration?: number;
  status: 'running' | 'complete' | 'error';
}

interface ThinkingProcessProps {
  steps: ThinkingStep[];
  expanded: boolean;
  onToggle: () => void;
}

// Thinking Process Component
const ThinkingProcess: React.FC<ThinkingProcessProps> = ({ steps, expanded, onToggle }) => {
  if (steps.length === 0) return null;

  return (
    <div className="thinking-process">
      <div className="thinking-header" onClick={onToggle}>
        <div className="step-icon">🤔</div>
        <div className="thinking-title">Thinking Process</div>
        {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </div>
      
      {expanded && (
        <div className="thinking-steps">
          {steps.map(step => (
            <div key={step.id} className={`step ${step.status}`}>
              <div className="step-header">
                <div className="step-icon">{step.icon}</div>
                <div className="step-title">{step.title}</div>
                {step.duration && <div className="step-time">{step.duration}ms</div>}
              </div>
              
              <div className="step-content">
                <div className="info-row">
                  <span className="info-label">AGENT:</span>
                  <span className="agent-badge">{step.agent}</span>
                </div>
                
                <div className="info-row">
                  <span className="info-label">ACTION:</span>
                  <span className="action-text">{step.action}</span>
                </div>
                
                {step.debugInfo && (
                  <div className="debug-info">
                    {step.debugInfo}
                  </div>
                )}
                
                {step.result && (
                  <div className="result-preview">
                    {step.result}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

interface AIAssistantViewProps {
  courseTitle?: string;
  initialPrompt?: string;
}

export const AIAssistantView: React.FC<AIAssistantViewProps> = ({ courseTitle, initialPrompt }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState(initialPrompt || '');
  const [isLoading, setIsLoading] = useState(false);
  
  // Thinking Process State
  const [thinkingSteps, setThinkingSteps] = useState<ThinkingStep[]>([]);
  const [isThinkingExpanded, setIsThinkingExpanded] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  }, [input]);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, thinkingSteps]);

  // Simulate thinking steps
  const simulateThinking = async () => {
    setThinkingSteps([]);
    setIsThinkingExpanded(true);
    
    // Step 1: Analyze
    const step1: ThinkingStep = {
      id: '1',
      agent: 'Supervisor',
      icon: '🔍',
      title: 'Analyzing user request',
      action: 'Classifying intent and entities',
      status: 'running'
    };
    setThinkingSteps([step1]);
    
    await new Promise(r => setTimeout(r, 800));
    
    setThinkingSteps(prev => prev.map(s => 
      s.id === '1' ? { ...s, status: 'complete', duration: 842, debugInfo: `Intent: QUERY_KNOWLEDGE\nContext: ${courseTitle || 'General'}` } : s
    ));
    
    // Step 2: Plan
    const step2: ThinkingStep = {
      id: '2',
      agent: 'Planner',
      icon: '📝',
      title: 'Formulating execution plan',
      action: 'Selecting tools and agents',
      status: 'running'
    };
    setThinkingSteps(prev => [...prev, step2]);
    
    await new Promise(r => setTimeout(r, 600));
    
    setThinkingSteps(prev => prev.map(s => 
      s.id === '2' ? { ...s, status: 'complete', duration: 520, result: 'Plan: Fetch Canvas data -> Summarize' } : s
    ));
    
    // Step 3: Execute (Canvas)
    const step3: ThinkingStep = {
      id: '3',
      agent: 'Canvas_Executor',
      icon: '🔌',
      title: 'Executing Canvas operations',
      action: 'Calling Canvas API',
      status: 'running',
      debugInfo: 'GET /api/v1/courses?include[]=term'
    };
    setThinkingSteps(prev => [...prev, step3]);
    
    // Return a promise that resolves when the actual API call finishes
    // We'll update step 3 to complete then
    return step3;
  };

  const handleSend = async (text: string = input) => {
    if (!text.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Start simulated thinking
    await simulateThinking();

    try {
      const response = await ChatAPI.sendMessage(text);
      
      // Complete the execution step
      setThinkingSteps(prev => prev.map(s => 
        s.id === '3' ? { ...s, status: 'complete', duration: 1250, result: 'Data retrieved successfully' } : s
      ));
      
      // Add final formatting step
      const step4: ThinkingStep = {
        id: '4',
        agent: 'Response_Specialist',
        icon: '✨',
        title: 'Formatting final response',
        action: 'Generating user-friendly output',
        status: 'running'
      };
      setThinkingSteps(prev => [...prev, step4]);
      
      await new Promise(r => setTimeout(r, 400));
      
      setThinkingSteps(prev => prev.map(s => 
        s.id === '4' ? { ...s, status: 'complete', duration: 380 } : s
      ));

      // Collapse thinking after a moment
      setTimeout(() => setIsThinkingExpanded(false), 1500);

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      // Mark step as error
      setThinkingSteps(prev => prev.map(s => 
        s.status === 'running' ? { ...s, status: 'error', result: 'Failed to execute operation' } : s
      ));
      
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleQuickAction = (action: string) => {
    const prompts: Record<string, string> = {
      'enrollments': 'Check enrollments for this course',
      'assignment': 'Help me create a new assignment',
      'grades': 'Show me a grade summary for the class',
      'sync': 'Sync course data from Canvas'
    };
    
    const prompt = prompts[action] || action;
    handleSend(prompt);
  };

  return (
    <div className="clean-interface ai-assistant-container">
      {/* Quick Actions Header - Always visible at top */}
      <div className="quick-actions-section">
        <div className="quick-actions-grid">
          <div className="action-card" onClick={() => handleQuickAction('enrollments')}>
            <Search size={24} className="action-icon" />
            <span className="action-label">Check Enrollments</span>
          </div>
          <div className="action-card" onClick={() => handleQuickAction('assignment')}>
            <Plus size={24} className="action-icon" />
            <span className="action-label">Add Assignment</span>
          </div>
          <div className="action-card" onClick={() => handleQuickAction('grades')}>
            <FileText size={24} className="action-icon" />
            <span className="action-label">Grade Summary</span>
          </div>
          <div className="action-card" onClick={() => handleQuickAction('sync')}>
            <RefreshCw size={24} className="action-icon" />
            <span className="action-label">Sync Courses</span>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="chat-scroll-area">
        <div className="chat-container">
          
          {/* Empty State / Greeting */}
          {messages.length === 0 && thinkingSteps.length === 0 && (
            <div className="empty-state">
              <div className="greeting-text">Hello! I'm CLAI, your Canvas assistant.</div>
              <div className="subtext">Ask me anything about your courses, students, or assignments</div>
              
              <div className="suggested-chips">
                <button className="chip" onClick={() => handleSend("Find students with missing work")}>
                  Find students with missing work
                </button>
                <button className="chip" onClick={() => handleSend("Show grade distribution")}>
                  Show grade distribution
                </button>
                <button className="chip" onClick={() => handleSend("What assignments are due this week?")}>
                  What assignments are due this week?
                </button>
                <button className="chip" onClick={() => handleSend("Create a new assignment")}>
                  Create a new assignment
                </button>
              </div>
            </div>
          )}

          {/* Message List */}
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.role === 'assistant' ? 'ai' : 'user'}`}>
              <div className="message-bubble message-content">
                <ReactMarkdown
                  components={{
                    // Custom renderers for specific elements if needed
                    a: ({ node, ...props }) => (
                      <a target="_blank" rel="noopener noreferrer" {...props} />
                    ),
                  }}
                >
                  {msg.content}
                </ReactMarkdown>
              </div>
            </div>
          ))}

          {/* Thinking Process Display - Only show when active or has history for current turn */}
          {(isLoading || thinkingSteps.length > 0) && (
            <ThinkingProcess 
              steps={thinkingSteps} 
              expanded={isThinkingExpanded} 
              onToggle={() => setIsThinkingExpanded(!isThinkingExpanded)} 
            />
          )}

          {/* Loading Indicator (Only if thinking is collapsed or empty, to avoid double loader) */}
          {isLoading && thinkingSteps.length === 0 && (
            <div className="message ai">
              <div className="message-bubble">
                <div className="typing-indicator">
                  <span>.</span><span>.</span><span>.</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Fixed Input Area */}
      <div className="input-area">
        <div className="input-container">
          <textarea
            ref={textareaRef}
            className="chat-input"
            placeholder="Ask CLAI anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            rows={1}
          />
          <button 
            className={`send-button ${input.trim() ? 'visible' : ''}`}
            onClick={() => handleSend()}
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};
