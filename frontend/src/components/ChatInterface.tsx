import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Clock } from 'lucide-react';
import { ChatMessage } from '../types';
import { ChatAPI } from '../api/chat';
import './ChatInterface.css';

interface ChatInterfaceProps {
  courseTitle: string;
  onClose: () => void;
  isMinimized?: boolean;
  onToggleMinimize?: () => void;
  embedded?: boolean;
  initialInput?: string;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  courseTitle,
  onClose,
  isMinimized = false,
  onToggleMinimize,
  embedded = false,
  initialInput = ''
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m CLAI, your Canvas assistant. How can I help you with your course today?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState(initialInput);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (initialInput) {
      setInput(initialInput);
    }
  }, [initialInput]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await ChatAPI.sendMessage(input);
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
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

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (isMinimized && !embedded) {
    return (
      <motion.div
        className="chat-interface-minimized"
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
      >
        <div className="minimized-header" onClick={onToggleMinimize}>
          <div className="minimized-title">
            <span className="status-dot live"></span>
            CLAI Assistant
          </div>
          <div className="minimized-actions">
            <button onClick={(e) => { e.stopPropagation(); onClose(); }}>×</button>
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      className={`chat-interface ${embedded ? 'embedded' : ''}`}
      initial={!embedded ? { scale: 0.8, opacity: 0, y: 20 } : { opacity: 1, scale: 1, y: 0 }}
      animate={{ scale: 1, opacity: 1, y: 0 }}
      exit={{ scale: 0.8, opacity: 0, y: 20 }}
      transition={{ type: 'spring', damping: 20 }}
    >
      {/* Header */}
      {!embedded && (
        <div className="chat-header">
          <div className="chat-header-left">
            <span className="status-dot live"></span>
            <h3 className="course-title">{courseTitle}</h3>
          </div>
          <div className="chat-header-right">
            <button 
              className="minimize-btn" 
              onClick={onToggleMinimize}
              title="Minimize"
            >
              −
            </button>
            <button 
              className="close-btn" 
              onClick={onClose}
              title="Close"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="chat-messages">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              className={`message ${message.role}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="message-header">
                <div className="message-author">
                  {message.role === 'assistant' ? (
                    <Bot size={16} className="author-icon" />
                  ) : (
                    <User size={16} className="author-icon" />
                  )}
                  <span>{message.role === 'assistant' ? 'CLAI' : 'You'}</span>
                </div>
                <div className="message-time">
                  <Clock size={12} />
                  {formatTime(message.timestamp)}
                </div>
              </div>
              <div className="message-content">
                {message.content}
              </div>
            </motion.div>
          ))}
          
          {isLoading && (
            <motion.div
              className="message assistant loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <div className="message-header">
                <div className="message-author">
                  <Bot size={16} className="author-icon" />
                  <span>CLAI</span>
                </div>
              </div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask CLAI anything about your course..."
            disabled={isLoading}
            rows={1}
          />
          <button
            className={`send-btn ${!input.trim() || isLoading ? 'disabled' : ''}`}
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </motion.div>
  );
};