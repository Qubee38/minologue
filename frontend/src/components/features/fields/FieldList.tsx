'use client';

import { useFields } from '@/lib/hooks/useFields';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Field } from '@/types';

export function FieldList() {
  const { fields, isLoading, deleteField, isDeleting } = useFields();

  if (isLoading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        <p className="mt-4 text-gray-600">読み込み中...</p>
      </div>
    );
  }

  if (!fields || fields.length === 0) {
    return (
      <Card>
        <div className="text-center py-8">
          <p className="text-gray-600 mb-4">圃場が登録されていません</p>
          <p className="text-sm text-gray-500">「圃場を追加」ボタンから最初の圃場を登録してください</p>
        </div>
      </Card>
    );
  }

  const handleDelete = (fieldId: string, fieldName: string) => {
    if (window.confirm(`「${fieldName}」を削除しますか？`)) {
      deleteField(fieldId);
    }
  };

  return (
    <div className="space-y-4">
      {fields.map((field: Field) => (
        <Card key={field.id} className="hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900">{field.name}</h3>
              {field.location_text && (
                <p className="text-sm text-gray-600 mt-1">📍 {field.location_text}</p>
              )}
              {field.memo && (
                <p className="text-sm text-gray-500 mt-2">{field.memo}</p>
              )}
            </div>
            
            <div className="flex gap-2 ml-4">
              <Button
                variant="secondary"
                size="sm"
                onClick={() => window.location.href = `/fields/${field.id}`}
              >
                詳細
              </Button>
              <Button
                variant="danger"
                size="sm"
                onClick={() => handleDelete(field.id, field.name)}
                disabled={isDeleting}
              >
                削除
              </Button>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
