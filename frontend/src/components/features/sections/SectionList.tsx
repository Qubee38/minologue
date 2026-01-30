'use client';

import { useRouter } from 'next/navigation';
import { useSections } from '@/lib/hooks/useFields';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';

interface SectionListProps {
  fieldId: string;
}

export function SectionList({ fieldId }: SectionListProps) {
  const router = useRouter();
  const { sections, isLoading, deleteSection, isDeleting } = useSections(fieldId);

  const handleDelete = (e: React.MouseEvent, id: string, name: string) => {
    e.stopPropagation();
    console.log('Delete button clicked:', id, name);
    if (confirm(`区画「${name}」を削除しますか？`)) {
      deleteSection(id);
    }
  };

  const handleSectionClick = (sectionId: string) => {
    console.log('Section clicked, navigating to:', `/sections/${sectionId}/records`);
    router.push(`/sections/${sectionId}/records`);
  };

  if (isLoading) {
    return <div className="text-center py-4 text-gray-600">読み込み中...</div>;
  }

  if (!sections || sections.length === 0) {
    return (
      <div className="text-center py-6 text-gray-500">
        区画がありません
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {sections.map((section) => (
        <Card 
          key={section.id} 
          className="bg-white hover:border-teal-600 transition-colors cursor-pointer"
          onClick={() => handleSectionClick(section.id)}
        >
          <div className="flex items-center justify-between p-4">
            <div className="flex-1">
              <h4 className="font-semibold text-gray-900">{section.name}</h4>
              <p className="text-sm text-gray-600 mt-1">
                🌱 {section.crop_name}
              </p>
              {section.memo && (
                <p className="text-sm text-gray-500 mt-1">{section.memo}</p>
              )}
            </div>
            <div className="flex gap-2">
              <Button
                variant="secondary"
                size="sm"
                onClick={(e) => {
                  e.stopPropagation();
                  console.log('Edit button clicked');
                }}
              >
                📝
              </Button>
              <Button
                variant="danger"
                size="sm"
                onClick={(e) => handleDelete(e, section.id, section.name)}
                isLoading={isDeleting}
              >
                🗑️
              </Button>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
