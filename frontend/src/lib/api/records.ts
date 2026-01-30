import axios from './client';
import { WorkRecord, PaginatedResponse } from '@/types';

export interface CreateWorkRecordData {
  record_target: 'section' | 'field';
  work_date: string;
  start_time: string;
  end_time: string;
  work_type: string;
  custom_work_name?: string;
  quantity?: number;
  quantity_unit?: string;
  memo?: string;
}

export interface UpdateWorkRecordData {
  work_date?: string;
  start_time?: string;
  end_time?: string;
  work_type?: string;
  custom_work_name?: string;
  quantity?: number;
  quantity_unit?: string;
  memo?: string;
}

export const recordsAPI = {
  // 区画の作業記録一覧取得
  async getSectionRecords(
    sectionId: string,
    params?: {
      start_date?: string;
      end_date?: string;
      work_type?: string;
      page?: number;
      per_page?: number;
    }
  ): Promise<WorkRecord[]> {
    const response = await axios.get<PaginatedResponse<WorkRecord>>(
      `/sections/${sectionId}/records`,
      { params }
    );
    return response.data.data; // dataプロパティから配列を取得
  },

  // 作業記録作成（区画）
  async createSectionRecord(
    sectionId: string,
    data: CreateWorkRecordData
  ): Promise<WorkRecord> {
    const response = await axios.post<WorkRecord>(
      `/sections/${sectionId}/records`,
      data
    );
    return response.data;
  },

  // 作業記録詳細取得
  async getRecord(recordId: string): Promise<WorkRecord> {
    const response = await axios.get<WorkRecord>(`/records/${recordId}`);
    return response.data;
  },

  // 作業記録更新
  async updateRecord(
    recordId: string,
    data: UpdateWorkRecordData
  ): Promise<WorkRecord> {
    const response = await axios.put<WorkRecord>(
      `/records/${recordId}`,
      data
    );
    return response.data;
  },

  // 作業記録削除
  async deleteRecord(recordId: string): Promise<void> {
    await axios.delete(`/records/${recordId}`);
  },
};
