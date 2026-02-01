import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Play } from 'lucide-react';
import './Hero.css';

interface HeroProps {
  onConnectCanvas: () => void;
  onWatchDemo: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onConnectCanvas, onWatchDemo }) => {
  return (
    <motion.div 
      className="hero-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
    >
      <div className="hero-content">
        <motion.h1 
          className="hero-title text-serif"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          CLAI
        </motion.h1>
        
        <motion.p 
          className="hero-subtitle text-serif"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          The intelligent layer for Canvas.
        </motion.p>
        
        <motion.div 
          className="hero-actions"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          <button 
            className="btn-primary hero-cta"
            onClick={onConnectCanvas}
          >
            Connect Your Canvas
            <ArrowRight size={16} className="cta-icon" />
          </button>
          
          <button 
            className="btn-secondary hero-demo"
            onClick={onWatchDemo}
          >
            <Play size={16} className="demo-icon" />
            Watch 2-min demo
          </button>
        </motion.div>
        
        <motion.div 
          className="trust-badges"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.8 }}
        >
          <div className="badge">
            <div className="badge-icon">✓</div>
            <span>SOC 2</span>
          </div>
          <div className="badge">
            <div className="badge-icon">✓</div>
            <span>FERPA</span>
          </div>
          <div className="badge">
            <div className="badge-icon">✓</div>
            <span>500+ Universities</span>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};