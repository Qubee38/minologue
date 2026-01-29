'use client';

import { FieldList } from '@/components/features/fields/FieldList';
import { CreateFieldForm } from '@/components/features/fields/CreateFieldForm';

export default function FieldsPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">圃場・区画管理</h1>
      
      <div className="mb-6">
        <CreateFieldForm />
      </div>
      
      <FieldList />
    </div>
  );
}
