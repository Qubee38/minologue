// ユーザー型
export interface User {
  id: number;
  email: string;
  display_name: string | null;
  farm_name: string | null;
  is_active: boolean;
  created_at: string;
  last_login_at: string | null;
}

// 認証トークン型
export interface AuthToken {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

// 圃場型
export interface Field {
  id: number;
  name: string;
  location_text: string | null;
  latitude: number | null;
  longitude: number | null;
  memo: string | null;
  owner_user_id: number;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

// 区画型
export interface Section {
  id: number;
  field_id: number;
  name: string;
  crop_name: string;
  memo: string | null;
  display_order: number;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

// スケジュール型
export interface Schedule {
  id: number;
  section_id: number;
  month: number;
  work_content: string;
  created_at: string;
  updated_at: string;
}

// 作業記録型
export interface WorkRecord {
  id: number;
  field_id: number;
  section_id: number | null;
  recorder_user_id: number;
  record_target: 'section' | 'field';
  work_date: string;
  start_time: string;
  end_time: string;
  work_type: string;
  custom_work_name: string | null;
  quantity: number | null;
  quantity_unit: string | null;
  memo: string | null;
  photos: Photo[];
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
}

// 写真型
export interface Photo {
  id: number;
  work_record_id: number;
  file_path: string;
  file_size: number;
  display_order: number;
  created_at: string;
}

// 共有型
export interface Share {
  id: number;
  field_id: number;
  shared_user_id: number;
  role: 'admin' | 'recorder';
  status: 'pending' | 'approved' | 'rejected';
  invited_by_user_id: number;
  created_at: string;
  updated_at: string;
  approved_at: string | null;
}

// 天候型
export interface Weather {
  id: number;
  date: string;
  location_text: string;
  latitude: number;
  longitude: number;
  weather: '晴れ' | '曇り' | '雨' | '雪' | '台風';
  max_temperature: number | null;
  min_temperature: number | null;
  precipitation: number | null;
  wind_speed: number | null;
  is_manual: boolean;
  created_at: string;
}

// APIエラー型
export interface APIError {
  error: string;
  message: string;
  details?: Record<string, string[]>;
}

// ページネーション型
export interface PaginationMeta {
  current_page: number;
  per_page: number;
  total_pages: number;
  total_count: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: PaginationMeta;
}
