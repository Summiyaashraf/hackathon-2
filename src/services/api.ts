// API service for interacting with the backend
import { getAuthToken } from '../utils/auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8080';

export interface Task {
  id: string;
  user_id: string; // Added user_id for user-specific tasks
  title: string;
  description: string | null;
  status: 'pending' | 'completed';
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  status?: 'pending' | 'completed';
}

// Authentication-related interfaces
export interface User {
  id: string;
  email: string;
  username?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username?: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const apiService = {
  // Helper to get auth headers
  getAuthHeaders(): Record<string, string> {
    const token = getAuthToken();
    if (!token) {
      throw new Error('No authentication token found. Please log in.');
    }

    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  },

  // Authentication methods
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    try {
      // FastAPI expects application/x-www-form-urlencoded with Form fields
      // Backend expects 'email' and 'password' fields (not 'username')
      const params = new URLSearchParams();
      params.append('email', credentials.email);
      params.append('password', credentials.password);

      console.log('Sending login request to:', `${API_BASE_URL}/auth/login`);
      console.log('Login data:', { email: credentials.email, password: '***' });

      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params.toString(),
      });

      console.log('Login response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Login failed:', errorText);
        throw new Error(`Login failed: ${response.status} ${response.statusText}. ${errorText}`);
      }

      const data = await response.json();
      console.log('Login successful, received token');
      return data;
    } catch (error) {
      if (error instanceof TypeError) {
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://127.0.0.1:8080');
      }
      throw error;
    }
  },

  async register(userData: RegisterData): Promise<User> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Registration failed: ${response.status} ${response.statusText}. ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof TypeError) {
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://127.0.0.1:8080');
      }
      throw error;
    }
  },

  async getCurrentUser(): Promise<User> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        method: 'GET',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`Failed to get user profile: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof TypeError) {
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://127.0.0.1:8080');
      }
      throw error;
    }
  },

  // Task methods with user authentication
  async getTasks(): Promise<Task[]> {
    try {
      // Get user ID from the token
      const userId = this.getUserIdFromToken();
      if (!userId) {
        throw new Error('No user ID found in token. Please log in again.');
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`, {
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch tasks: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      // The backend might return the tasks array directly or in a property
      return Array.isArray(data) ? data : data.tasks || [];
    } catch (error) {
      if (error instanceof TypeError) {
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://127.0.0.1:8080');
      }
      throw error;
    }
  },

  async createTask(taskData: CreateTaskRequest): Promise<Task> {
    try {
      // Get user ID from the token
      const userId = this.getUserIdFromToken();
      if (!userId) {
        throw new Error('No user ID found in token. Please log in again.');
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to create task: ${response.status} ${response.statusText}. ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof TypeError) {
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://127.0.0.1:8080');
      }
      throw error;
    }
  },

  async updateTask(taskId: string, taskData: UpdateTaskRequest): Promise<Task> {
    try {
      // Get user ID from the token
      const userId = this.getUserIdFromToken();
      if (!userId) {
        throw new Error('No user ID found in token. Please log in again.');
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
        method: 'PATCH',
        headers: this.getAuthHeaders(),
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to update task: ${response.status} ${response.statusText}. ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof TypeError) {
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://127.0.0.1:8080');
      }
      throw error;
    }
  },

  async deleteTask(taskId: string): Promise<void> {
    try {
      // Get user ID from the token
      const userId = this.getUserIdFromToken();
      if (!userId) {
        throw new Error('No user ID found in token. Please log in again.');
      }

      const response = await fetch(`${API_BASE_URL}/api/${userId}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to delete task: ${response.status} ${response.statusText}. ${errorText}`);
      }
    } catch (error) {
      if (error instanceof TypeError) {
        throw new Error('Network error: Unable to connect to the server. Please make sure the backend is running on http://127.0.0.1:8080');
      }
      throw error;
    }
  },

  // Helper method to get user ID from token
  getUserIdFromToken(): string | null {
    try {
      const token = getAuthToken();
      if (!token) {
        return null;
      }

      // Decode JWT payload to extract user ID
      const parts = token.split('.');
      if (parts.length !== 3) {
        throw new Error('Invalid token format');
      }

      const payload = parts[1];
      // Replace URL-safe base64 characters back to standard base64
      let base64 = payload.replace(/-/g, '+').replace(/_/g, '/');
      // Add padding if needed
      const pad = base64.length % 4;
      if (pad) {
        base64 += '='.repeat(4 - pad);
      }

      const decodedPayload = atob(base64);
      const parsedPayload = JSON.parse(decodedPayload);
      return parsedPayload.sub; // 'sub' typically contains the user ID
    } catch (error) {
      console.error('Error getting user ID from token:', error);
      return null;
    }
  },
};