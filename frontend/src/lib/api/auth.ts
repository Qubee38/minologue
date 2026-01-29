import axios from './client';
import { apiClient } from './client';
import { AuthToken, User } from '@/types';

export interface RegisterData {
  email: string;
  password: string;
  display_name?: string;
  farm_name?: string;
}

export interface LoginData {
  username: string; // OAuth2PasswordRequestForm用
  password: string;
}

export const authAPI = {
  // ユーザー登録
  async register(data: RegisterData): Promise<AuthToken> {
    const response = await axios.post<AuthToken>('/auth/register', data);
    apiClient.setToken(response.data.access_token);
    return response.data;
  },

  // ログイン
  async login(email: string, password: string): Promise<AuthToken> {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await axios.post<AuthToken>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    apiClient.setToken(response.data.access_token);
    return response.data;
  },

  // ログアウト
  async logout(): Promise<void> {
    await axios.post('/auth/logout');
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  },

  // 現在のユーザー取得
  async getCurrentUser(): Promise<User> {
    const response = await axios.get<User>('/users/me');
    return response.data;
  },

  // ユーザー情報更新
  async updateUser(data: Partial<User>): Promise<User> {
    const response = await axios.patch<User>('/users/me', data);
    return response.data;
  },
};
