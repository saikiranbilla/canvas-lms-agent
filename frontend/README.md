# CLAI Frontend

The intelligent layer for Canvas LMS - Frontend

## Features

- **Warm Parchment Design**: Elegant UI with terracotta accents and serif typography
- **Supervisor-Worker Visualization**: Real-time agent state monitoring
- **Chat Interface**: Seamless communication with the AI assistant
- **Observability Dashboard**: Track delegations and audit trails
- **Responsive Design**: Mobile-first approach with smooth animations

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Architecture

The frontend integrates with the backend API at `http://localhost:8001/chat` and maps the LangGraph Supervisor-Worker states to the UI components:

- **Supervisor**: Routes tasks between Canvas_Executor and Content_Specialist
- **Canvas_Executor**: Handles Canvas LMS operations
- **Content_Specialist**: Drafts academic content and assignments

## Design System

- **Colors**: Warm parchment (#F5EEE2), deep charcoal (#2A2B2F), terracotta (#B05B36)
- **Typography**: Playfair Display (serif) for branding, Inter (sans-serif) for UI
- **Animations**: Smooth transitions using Framer Motion

## Components

- `Hero`: Landing page with CLAI branding and CTAs
- `ChatInterface`: Floating chat card with message history
- `AgentInspector`: Real-time agent status monitoring
- `ObservabilitySidebar`: Delegations tracking and audit trail