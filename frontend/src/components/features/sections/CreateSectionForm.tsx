'use client';

import { useState } from 'react';
import { useSections } from '@/lib/hooks/useFields';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';

interface CreateSectionFormProps {
  fieldId: string;
  onClose: () => void;
}

export function CreateSectionForm({ fieldId, onClose }: CreateSectionFormProps) {
  const { createSection, isCreating } = useSections(fieldId);
  const [formData, setFormData] = useState({
    name: '',
    crop_name: '',
    memo: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createSection(formData);
    onClose();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="区画名"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        required
        placeholder="例: A区画"
      />
      
      <Input
        label="作物名"
        value={formData.crop_name}
        onChange={(e) => setFormData({ ...formData, crop_name: e.target.value })}
        required
        placeholder="例: トマト"
      />
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          メモ
        </label>
        <textarea
          value={formData.memo}
          onChange={(e) => setFormData({ ...formData, memo: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
          rows={3}
          placeholder="品種、栽培方法など"
        />
      </div>

      <div className="flex gap-2">
        <Button type="submit" isLoading={isCreating} className="flex-1">
          作成
        </Button>
        <Button type="button" variant="secondary" onClick={onClose} className="flex-1">
          キャンセル
        </Button>
      </div>
    </form>
  );
}
