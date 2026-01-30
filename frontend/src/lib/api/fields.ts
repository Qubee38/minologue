import axios from './client';
import { Field, Section } from '@/types';

export interface CreateFieldData {
  name: string;
  location_text?: string;
  latitude?: number;
  longitude?: number;
  memo?: string;
}

export interface UpdateFieldData {
  name?: string;
  location_text?: string;
  latitude?: number;
  longitude?: number;
  memo?: string;
}

export interface CreateSectionData {
  name: string;
  crop_name: string;
  memo?: string;
  display_order?: number;
}

export const fieldsAPI = {
  // 圃場一覧取得
  async getFields(): Promise<Field[]> {
    const response = await axios.get<Field[]>('/fields');
    return response.data;
  },

  // 圃場作成
  async createField(data: CreateFieldData): Promise<Field> {
    const response = await axios.post<Field>('/fields', data);
    return response.data;
  },

  // 圃場詳細取得
  async getField(fieldId: string): Promise<Field> {
    const response = await axios.get<Field>(`/fields/${fieldId}`);
    return response.data;
  },

  // 圃場更新
  async updateField(fieldId: string, data: UpdateFieldData): Promise<Field> {
    const response = await axios.put<Field>(`/fields/${fieldId}`, data);
    return response.data;
  },

  // 圃場削除
  async deleteField(fieldId: string): Promise<void> {
    await axios.delete(`/fields/${fieldId}`);
  },

  // 区画一覧取得
  async getSections(fieldId: string): Promise<Section[]> {
    const response = await axios.get<Section[]>(`/fields/${fieldId}/sections`);
    return response.data;
  },

  // 区画作成
  async createSection(fieldId: string, data: CreateSectionData): Promise<Section> {
    const response = await axios.post<Section>(`/fields/${fieldId}/sections`, data);
    return response.data;
  },

  // 区画削除
  async deleteSection(sectionId: string): Promise<void> {
    await axios.delete(`/sections/${sectionId}`);
  },
}

export const getFieldById = async (id: string): Promise<Field> => {
  const response = await axios.get(`/fields/${id}`);
  return response.data;
};;
