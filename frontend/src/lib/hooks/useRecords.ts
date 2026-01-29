import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { recordsAPI, CreateWorkRecordData } from '@/lib/api/records';

export function useSectionRecords(
  sectionId: number,
  params?: {
    start_date?: string;
    end_date?: string;
    work_type?: string;
  }
) {
  const queryClient = useQueryClient();

  // 作業記録一覧取得
  const { data: records, isLoading, error } = useQuery({
    queryKey: ['records', sectionId, params],
    queryFn: () => recordsAPI.getSectionRecords(sectionId, params),
    enabled: !!sectionId,
  });

  // 作業記録作成
  const createRecordMutation = useMutation({
    mutationFn: (data: CreateWorkRecordData) =>
      recordsAPI.createSectionRecord(sectionId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['records', sectionId] });
    },
  });

  // 作業記録削除
  const deleteRecordMutation = useMutation({
    mutationFn: (recordId: number) => recordsAPI.deleteRecord(recordId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['records', sectionId] });
    },
  });

  return {
    records,
    isLoading,
    error,
    createRecord: createRecordMutation.mutate,
    deleteRecord: deleteRecordMutation.mutate,
    isCreating: createRecordMutation.isPending,
    isDeleting: deleteRecordMutation.isPending,
  };
}
