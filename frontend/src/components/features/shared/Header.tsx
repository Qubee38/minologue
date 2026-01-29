'use client';

import { useAuth } from '@/lib/hooks/useAuth';
import { Button } from '@/components/ui/Button';

export function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="bg-primary text-white shadow-md">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <h1 className="text-xl font-bold">ミノローグ</h1>
        
        {user && (
          <div className="flex items-center gap-4">
            <span className="text-sm">
              {user.display_name || user.email}
            </span>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => logout()}
            >
              ログアウト
            </Button>
          </div>
        )}
      </div>
    </header>
  );
}
