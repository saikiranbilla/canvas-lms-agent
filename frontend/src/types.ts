export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface AgentState {
  name: string;
  status: 'planning' | 'active' | 'idle' | 'completed';
  lastAction?: string;
  timestamp: Date;
}

export interface Delegation {
  id: string;
  agent: string;
  task: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  timestamp: Date;
}

export interface AuditEntry {
  id: string;
  action: string;
  agent: string;
  details: string;
  timestamp: Date;
}

export interface ChatRequest {
  message: string;
  thread_id?: string;
}

export interface ChatResponse {
  response: string;
  error?: string;
}

export interface UserProfile {
  id: number;
  name: string;
  short_name: string;
  sortable_name: string;
  avatar_url: string;
  primary_email?: string;
  title?: string;
}