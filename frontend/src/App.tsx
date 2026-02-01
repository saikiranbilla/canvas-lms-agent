import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, ArrowRight, Play, CheckCircle, Zap, Shield, BarChart3, BookOpen, Star } from 'lucide-react';
import { Dashboard } from './components/Dashboard';
import { AgentState, Delegation } from './types';
import './App.css';

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('canvas_token'));
  const [showChat, setShowChat] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState<any>(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [agents, setAgents] = useState<AgentState[]>([
    {
      name: 'Supervisor',
      status: 'active',
      lastAction: 'Routing tasks to workers',
      timestamp: new Date()
    },
    {
      name: 'Canvas_Executor',
      status: 'idle',
      lastAction: 'Ready to process Canvas operations',
      timestamp: new Date()
    },
    {
      name: 'Content_Specialist',
      status: 'idle',
      lastAction: 'Ready to draft content',
      timestamp: new Date()
    }
  ]);
  
  // Delegations state is kept here if we need to pass it down later
  const [delegations, setDelegations] = useState<Delegation[]>([
    {
      id: '1',
      agent: 'Supervisor',
      task: 'Initialize multi-agent system',
      status: 'completed',
      timestamp: new Date(Date.now() - 30000)
    }
  ]);

  useEffect(() => {
    // Check if we're returning from authentication
    const params = new URLSearchParams(window.location.search);
    const urlToken = params.get('token');
    
    if (urlToken) {
      localStorage.setItem('canvas_token', urlToken);
      setToken(urlToken);
      setIsLoggingIn(false); // Reset loading state
      window.history.replaceState({}, '', window.location.pathname);
    } else {
      // Reset loading state if no token in URL (normal page load)
      setIsLoggingIn(false);
    }
  }, []);

  const [isLoggingIn, setIsLoggingIn] = useState(false);

  const handleLogin = () => {
    setIsLoggingIn(true);
    window.location.href = 'http://localhost:8001/auth/login';
  };

  const handleLogout = () => {
    localStorage.removeItem('canvas_token');
    setToken(null);
    setSelectedCourse(null);
    setShowChat(false);
  };

  const handleWatchDemo = () => {
    // Demo simulation logic
    // For demo, we might want to just log in with mock token
    handleLogin();
  };

  if (token) {
    return (
      <div className="app page-wrapper">
        <Dashboard 
          token={token}  
          onLogout={handleLogout}
          onSelectCourse={(course) => {
            setSelectedCourse(course);
          }}
          agents={agents}
        />
      </div>
    );
  }

  return (
    <div className="app page-wrapper">
      {isLoggingIn && (
        <div className="login-loading-overlay">
          <div className="login-loading-content">
            <div className="spinner"></div>
            <p>Logging in to Canvas using API...</p>
          </div>
        </div>
      )}
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <motion.div 
            className="nav-logo"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="logo-text text-serif">CLAI</span>
          </motion.div>
          
          <div className="nav-links">
            <a href="#features" className="nav-link">Features</a>
            <a href="#pricing" className="nav-link">Pricing</a>
            <a href="#about" className="nav-link">About</a>
            <a href="#contact" className="nav-link">Contact</a>
          </div>
          
          <div className="nav-actions">
            <button className="btn-secondary nav-btn">Sign In</button>
            <button 
              className="btn-primary nav-btn"
              onClick={handleLogin}
            >
              Get Started
            </button>
          </div>
          
          <button 
            className="nav-toggle"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
        
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div
              className="nav-mobile"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
            >
              <a href="#features" className="nav-link-mobile">Features</a>
              <a href="#pricing" className="nav-link-mobile">Pricing</a>
              <a href="#about" className="nav-link-mobile">About</a>
              <a href="#contact" className="nav-link-mobile">Contact</a>
              <div className="nav-actions-mobile">
                <button className="btn-secondary nav-btn">Sign In</button>
                <button 
                  className="btn-primary nav-btn"
                  onClick={handleLogin}
                >
                  Get Started
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-container">
          <div className="hero-content">
            <motion.div 
              className="hero-badge"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              <Zap size={16} />
              <span>AI-Powered Canvas Integration</span>
            </motion.div>
            
            <motion.h1 
              className="hero-title text-serif"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              Transform Your Canvas Experience with
              <span className="hero-title-highlight">Intelligent Automation</span>
            </motion.h1>
            
            <motion.p 
              className="hero-description"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              CLAI connects seamlessly to your Canvas LMS, automating course management, 
              content creation, and student engagement with advanced AI agents that work 24/7.
            </motion.p>
            
            <motion.div 
              className="hero-actions"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <button 
                className="btn-primary hero-cta"
                onClick={handleLogin}
              >
                Connect Your Canvas
                <ArrowRight size={16} className="cta-icon" />
              </button>
              
              <button 
                className="btn-secondary hero-demo"
                onClick={handleWatchDemo}
              >
                <Play size={16} className="demo-icon" />
                Watch Demo
              </button>
            </motion.div>
            
            <motion.div 
              className="hero-stats"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
            >
              <div className="stat-item">
                <div className="stat-number">500+</div>
                <div className="stat-label">Universities</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">50K+</div>
                <div className="stat-label">Educators</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">99.9%</div>
                <div className="stat-label">Uptime</div>
              </div>
            </motion.div>
          </div>
          
          <motion.div 
            className="hero-visual"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            <div className="floating-card">
              <div className="card-header">
                <div className="card-title">
                  <BookOpen size={16} />
                  <span>Course Management</span>
                </div>
                <div className="status-indicator active"></div>
              </div>
              <div className="card-content">
                <div className="task-item">
                  <CheckCircle size={12} className="task-icon" />
                  <span>Assignments auto-graded</span>
                </div>
                <div className="task-item">
                  <CheckCircle size={12} className="task-icon" />
                  <span>Content personalized</span>
                </div>
                <div className="task-item">
                  <CheckCircle size={12} className="task-icon" />
                  <span>Analytics generated</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="container">
          <motion.div 
            className="section-header"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="section-title text-serif">Built for Modern Education</h2>
            <p className="section-description">
              Powerful features that transform how educators manage their Canvas courses
            </p>
          </motion.div>
          
          <div className="features-grid">
            <motion.div 
              className="feature-card"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              viewport={{ once: true }}
            >
              <div className="feature-icon">
                <Zap size={24} />
              </div>
              <h3 className="feature-title">Intelligent Automation</h3>
              <p className="feature-description">
                AI agents work 24/7 to manage assignments, grade submissions, and personalize learning experiences.
              </p>
              <ul className="feature-list">
                <li>Auto-grade assignments</li>
                <li>Personalize content delivery</li>
                <li>Generate detailed analytics</li>
              </ul>
            </motion.div>
            
            <motion.div 
              className="feature-card"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
            >
              <div className="feature-icon">
                <Shield size={24} />
              </div>
              <h3 className="feature-title">Enterprise Security</h3>
              <p className="feature-description">
                Built with enterprise-grade security and compliance standards that universities trust.
              </p>
              <ul className="feature-list">
                <li>SOC 2 Type II certified</li>
                <li>FERPA compliant</li>
                <li>End-to-end encryption</li>
              </ul>
            </motion.div>
            
            <motion.div 
              className="feature-card"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              viewport={{ once: true }}
            >
              <div className="feature-icon">
                <BarChart3 size={24} />
              </div>
              <h3 className="feature-title">Advanced Analytics</h3>
              <p className="feature-description">
                Gain deep insights into student engagement and course performance with AI-powered analytics.
              </p>
              <ul className="feature-list">
                <li>Student engagement tracking</li>
                <li>Predictive performance insights</li>
                <li>Custom reporting dashboards</li>
              </ul>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="testimonials-section">
        <div className="container">
          <motion.div 
            className="section-header"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="section-title text-serif">Trusted by Educators Worldwide</h2>
            <p className="section-description">
              See how CLAI is transforming education at leading institutions
            </p>
          </motion.div>
          
          <div className="testimonials-grid">
            <motion.div 
              className="testimonial-card"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              viewport={{ once: true }}
            >
              <div className="testimonial-content">
                <div className="testimonial-rating">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} size={16} className="star-filled" />
                  ))}
                </div>
                <p className="testimonial-text">
                  "CLAI has revolutionized how we manage our online courses. The AI automation saves us hours every week."
                </p>
              </div>
              <div className="testimonial-author">
                <div className="author-info">
                  <div className="author-name">Dr. Sarah Johnson</div>
                  <div className="author-title">Professor of Psychology, Stanford University</div>
                </div>
              </div>
            </motion.div>
            
            <motion.div 
              className="testimonial-card"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
            >
              <div className="testimonial-content">
                <div className="testimonial-rating">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} size={16} className="star-filled" />
                  ))}
                </div>
                <p className="testimonial-text">
                  "The intelligent automation has improved student engagement by 40%. It's like having a teaching assistant that never sleeps."
                </p>
              </div>
              <div className="testimonial-author">
                <div className="author-info">
                  <div className="author-name">Prof. Michael Chen</div>
                  <div className="author-title">Director of Online Learning, MIT</div>
                </div>
              </div>
            </motion.div>
            
            <motion.div 
              className="testimonial-card"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              viewport={{ once: true }}
            >
              <div className="testimonial-content">
                <div className="testimonial-rating">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} size={16} className="star-filled" />
                  ))}
                </div>
                <p className="testimonial-text">
                  "CLAI's analytics have given us insights we never had before. We can now predict and prevent student dropouts."
                </p>
              </div>
              <div className="testimonial-author">
                <div className="author-info">
                  <div className="author-name">Dr. Emily Rodriguez</div>
                  <div className="author-title">Dean of Digital Education, Harvard University</div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <motion.div 
            className="cta-content"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="cta-title text-serif">Ready to Transform Your Canvas Experience?</h2>
            <p className="cta-description">
              Join thousands of educators who are already using CLAI to automate their courses and improve student outcomes.
            </p>
            <div className="cta-actions">
              <button 
                className="btn-primary cta-btn"
                onClick={handleLogin}
              >
                Start Free Trial
                <ArrowRight size={16} />
              </button>
              <p className="cta-note">No credit card required • 14-day free trial</p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-brand">
              <div className="footer-logo text-serif">CLAI</div>
              <p className="footer-description">
                The intelligent layer for Canvas LMS. Automating education, one course at a time.
              </p>
              <div className="footer-social">
                <a href="#" className="social-link">LinkedIn</a>
                <a href="#" className="social-link">Twitter</a>
                <a href="#" className="social-link">GitHub</a>
              </div>
            </div>
            
            <div className="footer-links">
              <div className="footer-column">
                <h4 className="footer-title">Product</h4>
                <a href="#features" className="footer-link">Features</a>
                <a href="#pricing" className="footer-link">Pricing</a>
                <a href="#" className="footer-link">Integrations</a>
                <a href="#" className="footer-link">API</a>
              </div>
              
              <div className="footer-column">
                <h4 className="footer-title">Company</h4>
                <a href="#about" className="footer-link">About</a>
                <a href="#" className="footer-link">Blog</a>
                <a href="#" className="footer-link">Careers</a>
                <a href="#contact" className="footer-link">Contact</a>
              </div>
              
              <div className="footer-column">
                <h4 className="footer-title">Support</h4>
                <a href="#" className="footer-link">Documentation</a>
                <a href="#" className="footer-link">Help Center</a>
                <a href="#" className="footer-link">Privacy</a>
                <a href="#" className="footer-link">Terms</a>
              </div>
              
              <div className="footer-column">
                <h4 className="footer-title">Compliance</h4>
                <div className="compliance-badges">
                  <div className="compliance-badge">
                    <CheckCircle size={12} />
                    <span>SOC 2 Type II</span>
                  </div>
                  <div className="compliance-badge">
                    <CheckCircle size={12} />
                    <span>FERPA Compliant</span>
                  </div>
                  <div className="compliance-badge">
                    <CheckCircle size={12} />
                    <span>GDPR Ready</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="footer-bottom">
            <p className="footer-copyright">
              © 2024 CLAI. All rights reserved. Built with ❤️ for educators worldwide.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
