'use client';

import { useState } from 'react';
import { useSectionRecords } from '@/lib/hooks/useRecords';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { WorkRecord } from '@/types';

interface EditRecordFormProps {
  record: WorkRecord;
  sectionId: string;
  onClose: () => void;
}

export function EditRecordForm({ record, sectionId, onClose }: EditRecordFormProps) {
  const { updateRecord, deleteRecord, isUpdating, isDeleting } = useSectionRecords(sectionId);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  
  const [formData, setFormData] = useState({
    work_type: record.work_type,
    start_time: record.start_time.substring(0, 5),
    end_time: record.end_time.substring(0, 5),
    quantity: record.quantity?.toString() || '',
    quantity_unit: record.quantity_unit || '',
    memo: record.memo || '',
  });

  const workTypes = [
    '作付け',
    '播種',
    '定植',
    '潅水',
    '施肥',
    '農薬散布',
    '防除',
    '整枝',
    '除草',
    '収穫',
    '出荷準備',
    'その他',
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const updateData = {
      work_type: formData.work_type,
      start_time: formData.start_time + ':00',
      end_time: formData.end_time + ':00',
      quantity: formData.quantity ? parseFloat(formData.quantity) : undefined,
      quantity_unit: formData.quantity_unit || undefined,
      memo: formData.memo || undefined,
    };

    updateRecord(
      { recordId: record.id, data: updateData },
      {
        onSuccess: () => {
          onClose();
        },
        onError: (error) => {
          console.error('更新エラー:', error);
          alert('作業記録の更新に失敗しました');
        },
      }
    );
  };

  const handleDelete = () => {
    deleteRecord(record.id, {
      onSuccess: () => {
        onClose();
      },
      onError: (error) => {
        console.error('削除エラー:', error);
        alert('作業記録の削除に失敗しました');
      },
    });
  };

  const needsQuantity = ['潅水', '施肥', '農薬散布', '収穫'].includes(formData.work_type);
  
  const getDefaultUnit = (workType: string) => {
    const unitMap: Record<string, string> = {
      '潅水': 'L',
      '施肥': 'kg',
      '農薬散布': 'ml',
      '収穫': 'kg',
    };
    return unitMap[workType] || '';
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          作業種別 *
        </label>
        <select
          value={formData.work_type}
          onChange={(e) => {
            const workType = e.target.value;
            setFormData({
              ...formData,
              work_type: workType,
              quantity_unit: getDefaultUnit(workType),
            });
          }}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
          required
        >
          {workTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="開始時刻 *"
          type="time"
          value={formData.start_time}
          onChange={(e) => setFormData({ ...formData, start_time: e.target.value })}
          required
        />
        <Input
          label="終了時刻 *"
          type="time"
          value={formData.end_time}
          onChange={(e) => setFormData({ ...formData, end_time: e.target.value })}
          required
        />
      </div>

      {needsQuantity && (
        <div className="grid grid-cols-2 gap-4">
          <Input
            label="数量"
            type="number"
            step="0.1"
            value={formData.quantity}
            onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
            placeholder="例: 50"
          />
          <Input
            label="単位"
            value={formData.quantity_unit}
            onChange={(e) => setFormData({ ...formData, quantity_unit: e.target.value })}
            placeholder={getDefaultUnit(formData.work_type)}
          />
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          メモ
        </label>
        <textarea
          value={formData.memo}
          onChange={(e) => setFormData({ ...formData, memo: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
          rows={3}
          placeholder="作業内容の詳細"
        />
      </div>

      {showDeleteConfirm ? (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-sm text-red-800 mb-3">本当に削除しますか？この操作は取り消せません。</p>
          <div className="flex gap-2">
            <Button
              type="button"
              variant="danger"
              onClick={handleDelete}
              isLoading={isDeleting}
              className="flex-1"
            >
              削除する
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => setShowDeleteConfirm(false)}
              className="flex-1"
            >
              キャンセル
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex gap-2">
          <Button type="submit" isLoading={isUpdating} className="flex-1">
            💾 保存
          </Button>
          <Button 
            type="button" 
            variant="danger"
            onClick={() => setShowDeleteConfirm(true)}
            className="flex-1"
          >
            🗑️ 削除
          </Button>
          <Button 
            type="button" 
            variant="secondary" 
            onClick={onClose}
            className="flex-1"
          >
            キャンセル
          </Button>
        </div>
      )}
    </form>
  );
}