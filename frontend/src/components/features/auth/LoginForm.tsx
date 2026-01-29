'use client';

import { useState } from 'react';
import { useAuth } from '@/lib/hooks/useAuth';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card } from '@/components/ui/Card';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, isLoggingIn, loginError } = useAuth();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login({ email, password });
  };

  return (
    <Card className="max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-center mb-6">ログイン</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          type="email"
          label="メールアドレス"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete="email"
        />
        
        <Input
          type="password"
          label="パスワード"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete="current-password"
        />

        {loginError && (
          <div className="text-red-600 text-sm">
            ログインに失敗しました。メールアドレスとパスワードを確認してください。
          </div>
        )}

        <Button type="submit" className="w-full" isLoading={isLoggingIn}>
          ログイン
        </Button>
      </form>

      <div className="mt-4 text-center text-sm text-gray-600">
        <a href="/register" className="text-primary hover:underline">
          アカウントをお持ちでない方はこちら
        </a>
      </div>
    </Card>
  );
}
