import { ChatRequest, ChatResponse } from '../types';

const API_BASE_URL = 'http://localhost:8001';

export class ChatAPI {
  private static async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  static async sendMessage(message: string, threadId: string = 'demo-1'): Promise<ChatResponse> {
    const request: ChatRequest = {
      message,
      thread_id: threadId,
    };

    return this.post<ChatResponse>('/chat', request);
  }
}