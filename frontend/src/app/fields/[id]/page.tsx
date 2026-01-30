'use client';

import { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { getFieldById } from '@/lib/api/fields';
import { Button } from '@/components/ui/Button';
import { SectionList } from '@/components/features/sections/SectionList';
import { CreateSectionForm } from '@/components/features/sections/CreateSectionForm';

export default function FieldDetailPage() {
  const params = useParams();
  const router = useRouter();
  const fieldId = params.id as string;
  const [showCreateForm, setShowCreateForm] = useState(false);

  const { data: field, isLoading, error } = useQuery({
    queryKey: ['field', fieldId],
    queryFn: () => getFieldById(fieldId),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-600">読み込み中...</div>
      </div>
    );
  }

  if (error || !field) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4">
        <div className="text-red-600">圃場が見つかりません</div>
        <Button onClick={() => router.push('/fields')}>
          圃場一覧に戻る
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-6">
        <Button 
          variant="secondary" 
          onClick={() => router.push('/fields')}
        >
          ← 戻る
        </Button>
      </div>

      {/* 圃場情報 */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          {field.name}
        </h1>

        <div className="space-y-4">
          <div>
            <h2 className="text-sm font-medium text-gray-500">位置情報</h2>
            <p className="mt-1 text-gray-900">
              {field.location_text || '未設定'}
            </p>
            {field.latitude && field.longitude && (
              <p className="mt-1 text-sm text-gray-600">
                緯度: {field.latitude}, 経度: {field.longitude}
              </p>
            )}
          </div>

          {field.memo && (
            <div>
              <h2 className="text-sm font-medium text-gray-500">メモ</h2>
              <p className="mt-1 text-gray-900 whitespace-pre-wrap">
                {field.memo}
              </p>
            </div>
          )}

          <div>
            <h2 className="text-sm font-medium text-gray-500">作成日時</h2>
            <p className="mt-1 text-gray-900">
              {new Date(field.created_at).toLocaleString('ja-JP')}
            </p>
          </div>
        </div>
      </div>

      {/* 区画セクション */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">区画</h2>
          <Button onClick={() => setShowCreateForm(!showCreateForm)}>
            {showCreateForm ? 'キャンセル' : '➕ 区画を追加'}
          </Button>
        </div>

        {showCreateForm && (
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <CreateSectionForm 
              fieldId={fieldId} 
              onClose={() => setShowCreateForm(false)} 
            />
          </div>
        )}

        <SectionList fieldId={fieldId} />
      </div>
    </div>
  );
}
