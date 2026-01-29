'use client';

import { useState } from 'react';
import { useAuth } from '@/lib/hooks/useAuth';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card } from '@/components/ui/Card';

export function RegisterForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [farmName, setFarmName] = useState('');
  const { register, isRegistering, registerError } = useAuth();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    register({
      email,
      password,
      display_name: displayName || undefined,
      farm_name: farmName || undefined,
    });
  };

  return (
    <Card className="max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-center mb-6">アカウント登録</h2>
      
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
          autoComplete="new-password"
          minLength={8}
        />

        <Input
          type="text"
          label="表示名（任意）"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          autoComplete="name"
        />

        <Input
          type="text"
          label="農園名（任意）"
          value={farmName}
          onChange={(e) => setFarmName(e.target.value)}
        />

        {registerError && (
          <div className="text-red-600 text-sm">
            登録に失敗しました。入力内容を確認してください。
          </div>
        )}

        <Button type="submit" className="w-full" isLoading={isRegistering}>
          登録
        </Button>
      </form>

      <div className="mt-4 text-center text-sm text-gray-600">
        <a href="/login" className="text-primary hover:underline">
          既にアカウントをお持ちの方はこちら
        </a>
      </div>
    </Card>
  );
}
