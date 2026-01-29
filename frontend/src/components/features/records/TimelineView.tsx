'use client';

import { WorkRecord } from '@/types';

interface TimelineViewProps {
  records: WorkRecord[];
  onRecordClick: (record: WorkRecord) => void;
  onTimeSlotClick?: (hour: number) => void;
}

export function TimelineView({ records, onRecordClick, onTimeSlotClick }: TimelineViewProps) {
  // 時間を分に変換
  const timeToMinutes = (timeStr: string): number => {
    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours * 60 + minutes;
  };

  // 作業の重複グループを計算
  const calculateOverlapGroups = (records: WorkRecord[]) => {
    const sorted = [...records].sort((a, b) => 
      timeToMinutes(a.start_time) - timeToMinutes(b.start_time)
    );

    const groups: WorkRecord[][] = [];
    
    sorted.forEach((record) => {
      const recordStart = timeToMinutes(record.start_time);
      const recordEnd = timeToMinutes(record.end_time);
      
      // 既存のグループで重複するものを探す
      let placed = false;
      for (const group of groups) {
        const hasOverlap = group.some((existing) => {
          const existingStart = timeToMinutes(existing.start_time);
          const existingEnd = timeToMinutes(existing.end_time);
          return recordStart < existingEnd && recordEnd > existingStart;
        });
        
        if (hasOverlap) {
          group.push(record);
          placed = true;
          break;
        }
      }
      
      if (!placed) {
        groups.push([record]);
      }
    });

    return groups;
  };

  // 作業種別に応じた絵文字を取得
  const getWorkEmoji = (workType: string) => {
    const emojiMap: Record<string, string> = {
      '播種': '🌾',
      '定植': '🪴',
      '潅水': '🚿',
      '施肥': '💊',
      '農薬散布': '🪲',
      '防除': '🕸️',
      '整枝': '✂️',
      '除草': '🌿',
      '収穫': '��',
      '出荷準備': '📦',
      '作付け': '🚜',
    };
    return emojiMap[workType] || '📝';
  };

  // 作業種別に応じた色を取得
  const getWorkColor = (workType: string) => {
    const colorMap: Record<string, string> = {
      '潅水': 'bg-blue-500',
      '施肥': 'bg-orange-500',
      '農薬散布': 'bg-red-500',
      '収穫': 'bg-green-500',
      '播種': 'bg-yellow-600',
      '定植': 'bg-purple-500',
      '防除': 'bg-pink-500',
      '整枝': 'bg-indigo-500',
      '除草': 'bg-lime-600',
      '出荷準備': 'bg-cyan-600',
      '作付け': 'bg-amber-600',
    };
    return colorMap[workType] || 'bg-gray-500';
  };

  // 各時間帯（1時間）に対して作業を配置
  const renderHourSlot = (hour: number) => {
    const hourStart = hour * 60;
    const hourEnd = (hour + 1) * 60;

    // この時間帯に重なる作業を検索
    const overlappingRecords = records.filter((record) => {
      const recordStart = timeToMinutes(record.start_time);
      const recordEnd = timeToMinutes(record.end_time);
      return recordStart < hourEnd && recordEnd > hourStart;
    });

    // 重複グループを計算
    const overlapGroups = calculateOverlapGroups(overlappingRecords);
    const columnCount = Math.max(1, ...overlapGroups.map(g => g.length));

    return (
      <div
        key={hour}
        className="border-b border-gray-200 flex hover:bg-gray-50 transition-colors"
        style={{ minHeight: '60px' }}
      >
        {/* 時刻ラベル */}
        <div className="w-16 p-3 text-right text-sm text-gray-500 flex-shrink-0 border-r border-gray-200">
          {hour.toString().padStart(2, '0')}:00
        </div>

        {/* 作業記録エリア */}
        <div
          className="flex-1 relative"
          onClick={() => overlappingRecords.length === 0 && onTimeSlotClick?.(hour)}
          style={{ cursor: overlappingRecords.length === 0 ? 'pointer' : 'default' }}
        >
          {overlappingRecords.map((record, index) => {
            const recordStart = timeToMinutes(record.start_time);
            const recordEnd = timeToMinutes(record.end_time);

            // この時間帯での表示開始・終了位置を計算
            const displayStart = Math.max(recordStart, hourStart);
            const displayEnd = Math.min(recordEnd, hourEnd);

            // 時間帯内でのオフセット（0〜60分）
            const offsetMinutes = displayStart - hourStart;
            const durationMinutes = displayEnd - displayStart;

            // ピクセル位置計算（1時間=60pxとする）
            const topPosition = offsetMinutes;
            const height = durationMinutes;

            // 最初のセグメントかどうか
            const isFirstSegment = recordStart >= hourStart && recordStart < hourEnd;
            const isLastSegment = recordEnd > hourStart && recordEnd <= hourEnd;

            // 重複位置を計算（同じ時間帯の何番目か）
            const groupIndex = overlapGroups.findIndex(g => g.includes(record));
            const group = overlapGroups[groupIndex];
            const positionInGroup = group.indexOf(record);
            const groupSize = group.length;

            // 横幅とオフセットを計算
            const widthPercent = 100 / groupSize;
            const leftPercent = (positionInGroup * widthPercent);

            return (
              <div
                key={`${record.id}-${hour}`}
                className={`${getWorkColor(record.work_type)} text-white absolute cursor-pointer hover:opacity-90 transition-opacity shadow-sm`}
                style={{
                  top: `${topPosition}px`,
                  height: `${height}px`,
                  left: `calc(${leftPercent}% + 4px)`,
                  width: `calc(${widthPercent}% - 8px)`,
                  borderTopLeftRadius: isFirstSegment ? '6px' : '0',
                  borderTopRightRadius: isFirstSegment ? '6px' : '0',
                  borderBottomLeftRadius: isLastSegment ? '6px' : '0',
                  borderBottomRightRadius: isLastSegment ? '6px' : '0',
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  onRecordClick(record);
                }}
              >
                {/* 最初のセグメントにのみ情報を表示 */}
                {isFirstSegment && height >= 40 && (
                  <div className="p-2">
                    <div className="flex items-start gap-1">
                      <span className="text-base">{getWorkEmoji(record.work_type)}</span>
                      <div className="flex-1 min-w-0">
                        <div className="font-semibold text-xs truncate">
                          {record.work_type}
                        </div>
                        <div className="text-[10px] opacity-90">
                          {record.start_time.substring(0, 5)}-{record.end_time.substring(0, 5)}
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                {/* 短い作業の場合は絵文字のみ */}
                {isFirstSegment && height < 40 && (
                  <div className="flex items-center justify-center h-full">
                    <span className="text-base">{getWorkEmoji(record.work_type)}</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
      {Array.from({ length: 24 }, (_, hour) => renderHourSlot(hour))}
    </div>
  );
}
