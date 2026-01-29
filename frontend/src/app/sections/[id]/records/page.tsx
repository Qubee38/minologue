'use client';

import { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useSectionRecords } from '@/lib/hooks/useRecords';
import { Button } from '@/components/ui/Button';
import { TimelineView } from '@/components/features/records/TimelineView';
import { CreateRecordForm } from '@/components/features/records/CreateRecordForm';
import { EditRecordForm } from '@/components/features/records/EditRecordForm';
import { WorkRecord } from '@/types';

export default function SectionRecordsPage() {
  const params = useParams();
  const router = useRouter();
  const sectionId = Number(params.id);
  
  const [currentDate, setCurrentDate] = useState(new Date());
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedWorkType, setSelectedWorkType] = useState('');
  const [selectedStartTime, setSelectedStartTime] = useState('09:00');
  const [selectedRecord, setSelectedRecord] = useState<WorkRecord | null>(null);
  const [showMenu, setShowMenu] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  
  const dateStr = currentDate.toISOString().split('T')[0];
  const { records, isLoading, error } = useSectionRecords(sectionId, {
    start_date: dateStr,
    end_date: dateStr,
  });

  const handleWorkIconClick = (workType: string) => {
    setSelectedWorkType(workType);
    setSelectedStartTime('09:00');
    setShowCreateForm(true);
  };

  const handleTimeSlotClick = (hour: number) => {
    setSelectedWorkType('');
    setSelectedStartTime(`${hour.toString().padStart(2, '0')}:00`);
    setShowCreateForm(true);
  };

  const handleRecordClick = (record: WorkRecord) => {
    setSelectedRecord(record);
  };

  const workIcons = [
    { emoji: '🌾', label: '播種' },
    { emoji: '🪴', label: '定植' },
    { emoji: '🚿', label: '潅水' },
    { emoji: '💊', label: '施肥' },
    { emoji: '🪲', label: '農薬散布' },
    { emoji: '🕸️', label: '防除' },
    { emoji: '✂️', label: '整枝' },
    { emoji: '🌿', label: '除草' },
    { emoji: '🍅', label: '収穫' },
    { emoji: '📦', label: '出荷準備' },
    { emoji: '🚜', label: '作付け' },
    { emoji: '📝', label: 'その他' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <header className="bg-teal-600 text-white p-4 shadow-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold">ミノローグ</h1>
          <button
            onClick={() => setShowUserMenu(!showUserMenu)}
            className="text-2xl hover:bg-teal-700 px-3 py-1 rounded"
          >
            👤▼
          </button>
        </div>
      </header>

      {/* ユーザードロップダウン */}
      {showUserMenu && (
        <>
          <div 
            className="fixed inset-0 z-40" 
            onClick={() => setShowUserMenu(false)}
          />
          <div className="fixed top-14 right-4 bg-white rounded-lg shadow-lg z-50 min-w-[200px] border border-gray-200">
            <button
              className="w-full text-left px-4 py-3 hover:bg-gray-100 border-b border-gray-200"
              onClick={() => {
                alert('プロフィール画面へ');
                setShowUserMenu(false);
              }}
            >
              プロフィール
            </button>
            <button
              className="w-full text-left px-4 py-3 hover:bg-gray-100 border-b border-gray-200"
              onClick={() => {
                router.push('/fields');
                setShowUserMenu(false);
              }}
            >
              圃場切替
            </button>
            <button
              className="w-full text-left px-4 py-3 hover:bg-gray-100"
              onClick={() => {
                alert('ログアウト');
                setShowUserMenu(false);
              }}
            >
              ログアウト
            </button>
          </div>
        </>
      )}

      {/* サブヘッダー */}
      <div className="bg-white border-b border-gray-200 p-4 sticky top-14 z-30">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="text-sm text-gray-600">
            圃場A &gt; 区画{sectionId}
          </div>
          <div className="flex gap-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => router.back()}
            >
              📊
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setShowMenu(!showMenu)}
            >
              ≡
            </Button>
          </div>
        </div>
      </div>

      {/* メニューサイドバー */}
      {showMenu && (
        <>
          <div 
            className="fixed inset-0 bg-black bg-opacity-50 z-40" 
            onClick={() => setShowMenu(false)}
          />
          <div className="fixed top-0 right-0 h-full w-80 bg-white shadow-xl z-50 transform transition-transform">
            <div className="bg-teal-600 text-white p-4 font-bold text-lg">
              メニュー
            </div>
            <button
              className="w-full text-left px-4 py-4 hover:bg-gray-100 border-b border-gray-200 flex items-center gap-3"
              onClick={() => {
                alert('区画詳細画面へ');
                setShowMenu(false);
              }}
            >
              <span className="text-xl">📝</span>
              <span>区画詳細</span>
            </button>
            <button
              className="w-full text-left px-4 py-4 hover:bg-gray-100 border-b border-gray-200 flex items-center gap-3"
              onClick={() => {
                router.back();
                setShowMenu(false);
              }}
            >
              <span className="text-xl">🔄</span>
              <span>区画切替</span>
            </button>
            <button
              className="w-full text-left px-4 py-4 hover:bg-gray-100 border-b border-gray-200 flex items-center gap-3"
              onClick={() => {
                alert('共有設定画面へ');
                setShowMenu(false);
              }}
            >
              <span className="text-xl">👥</span>
              <span>共有設定</span>
            </button>
            <button
              className="w-full text-left px-4 py-4 hover:bg-gray-100 flex items-center gap-3"
              onClick={() => {
                alert('エクスポート画面へ');
                setShowMenu(false);
              }}
            >
              <span className="text-xl">📥</span>
              <span>エクスポート</span>
            </button>
          </div>
        </>
      )}

      {/* 日付・天候バー */}
      <div className="bg-white border-b border-gray-200 p-4 sticky top-[7.5rem] z-20">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-4">
              <button
                className="text-2xl hover:bg-gray-100 p-2 rounded"
                onClick={() => {
                  const newDate = new Date(currentDate);
                  newDate.setDate(newDate.getDate() - 1);
                  setCurrentDate(newDate);
                }}
              >
                ‹
              </button>
              <div className="font-semibold cursor-pointer hover:bg-gray-100 px-3 py-2 rounded">
                {currentDate.toLocaleDateString('ja-JP', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  weekday: 'short',
                })}
              </div>
              <button
                className="text-2xl hover:bg-gray-100 p-2 rounded"
                onClick={() => {
                  const newDate = new Date(currentDate);
                  newDate.setDate(newDate.getDate() + 1);
                  setCurrentDate(newDate);
                }}
              >
                ›
              </button>
            </div>

            <div className="flex items-center gap-4 text-sm text-gray-600">
              <div className="flex items-center gap-1">
                <span>☀️</span>
                <span>12℃ / 3℃</span>
              </div>
            </div>
          </div>

          <div className="text-sm text-gray-500">
            今月: 種蒔き
          </div>
        </div>
      </div>

      {/* メインコンテンツ */}
      <main className="max-w-7xl mx-auto p-4 pb-24">
        {showCreateForm ? (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-bold mb-4">作業記録を追加</h2>
            <CreateRecordForm
              sectionId={sectionId}
              workDate={dateStr}
              defaultStartTime={selectedStartTime}
              defaultWorkType={selectedWorkType}
              onClose={() => setShowCreateForm(false)}
            />
          </div>
        ) : selectedRecord ? (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-bold mb-4">作業記録を編集</h2>
            <EditRecordForm
              record={selectedRecord}
              sectionId={sectionId}
              onClose={() => setSelectedRecord(null)}
            />
          </div>
        ) : isLoading ? (
          <div className="text-center py-8 text-gray-600">読み込み中...</div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            エラー: {error instanceof Error ? error.message : 'データの取得に失敗しました'}
          </div>
        ) : (
          <>
            {records && records.length > 0 && (
              <div className="mb-4 text-sm text-gray-600 bg-white px-4 py-2 rounded-md shadow-sm">
                📝 {records.length}件の作業記録
              </div>
            )}
            <TimelineView 
              records={records || []} 
              onRecordClick={handleRecordClick}
              onTimeSlotClick={handleTimeSlotClick}
            />
          </>
        )}
      </main>

      {/* 作業アイコンバー */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-3 overflow-x-auto shadow-lg z-30">
        <div className="flex gap-2 justify-start">
          {workIcons.map((work) => (
            <button
              key={work.label}
              className="flex flex-col items-center min-w-[70px] p-2 rounded-lg hover:bg-gray-100 transition-colors flex-shrink-0"
              onClick={() => handleWorkIconClick(work.label)}
            >
              <span className="text-2xl mb-1">{work.emoji}</span>
              <span className="text-xs text-gray-600">{work.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
