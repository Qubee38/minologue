import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { fieldsAPI, CreateFieldData, CreateSectionData } from '@/lib/api/fields';

export function useFields() {
  const queryClient = useQueryClient();

  // 圃場一覧取得
  const { data: fields, isLoading, error } = useQuery({
    queryKey: ['fields'],
    queryFn: fieldsAPI.getFields,
  });

  // 圃場作成
  const createFieldMutation = useMutation({
    mutationFn: (data: CreateFieldData) => fieldsAPI.createField(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fields'] });
    },
  });

  // 圃場削除
  const deleteFieldMutation = useMutation({
    mutationFn: (fieldId: string) => fieldsAPI.deleteField(fieldId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fields'] });
    },
  });

  return {
    fields,
    isLoading,
    error,
    createField: createFieldMutation.mutate,
    deleteField: deleteFieldMutation.mutate,
    isCreating: createFieldMutation.isPending,
    isDeleting: deleteFieldMutation.isPending,
  };
}

export function useSections(fieldId: string) {
  const queryClient = useQueryClient();

  // 区画一覧取得
  const { data: sections, isLoading, error } = useQuery({
    queryKey: ['sections', fieldId],
    queryFn: () => fieldsAPI.getSections(fieldId),
    enabled: !!fieldId,
  });

  // 区画作成
  const createSectionMutation = useMutation({
    mutationFn: (data: CreateSectionData) => fieldsAPI.createSection(fieldId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sections', fieldId] });
    },
  });

  // 区画削除
  const deleteSectionMutation = useMutation({
    mutationFn: (sectionId: string) => fieldsAPI.deleteSection(sectionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sections', fieldId] });
    },
  });

  return {
    sections,
    isLoading,
    error,
    createSection: createSectionMutation.mutate,
    deleteSection: deleteSectionMutation.mutate,
    isCreating: createSectionMutation.isPending,
    isDeleting: deleteSectionMutation.isPending,
  };
}
