'use client';

import { useState } from 'react';
import { useFields } from '@/lib/hooks/useFields';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card } from '@/components/ui/Card';

interface CreateFieldFormProps {
  onSuccess?: () => void;
}

export function CreateFieldForm({ onSuccess }: CreateFieldFormProps) {
  const [name, setName] = useState('');
  const [locationText, setLocationText] = useState('');
  const [memo, setMemo] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  
  const { createField, isCreating } = useFields();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createField(
      {
        name,
        location_text: locationText || undefined,
        memo: memo || undefined,
      },
      {
        onSuccess: () => {
          setName('');
          setLocationText('');
          setMemo('');
          setIsOpen(false);
          onSuccess?.();
        },
      }
    );
  };

  if (!isOpen) {
    return (
      <Button onClick={() => setIsOpen(true)} className="w-full">
        ➕ 圃場を追加
      </Button>
    );
  }

  return (
    <Card>
      <h3 className="text-lg font-semibold mb-4">新しい圃場を追加</h3>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="圃場名"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="例: 第一圃場"
          required
        />
        
        <Input
          label="位置情報（任意）"
          value={locationText}
          onChange={(e) => setLocationText(e.target.value)}
          placeholder="例: 愛知県岡崎市"
        />

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            メモ（任意）
          </label>
          <textarea
            value={memo}
            onChange={(e) => setMemo(e.target.value)}
            placeholder="圃場の特徴、土壌情報など"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            rows={3}
          />
        </div>

        <div className="flex gap-2">
          <Button type="submit" className="flex-1" isLoading={isCreating}>
            作成
          </Button>
          <Button
            type="button"
            variant="secondary"
            onClick={() => setIsOpen(false)}
            className="flex-1"
          >
            キャンセル
          </Button>
        </div>
      </form>
    </Card>
  );
}
