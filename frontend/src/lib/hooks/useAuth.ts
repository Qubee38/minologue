import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useAuthStore } from '@/stores/authStore';
import { authAPI, RegisterData } from '@/lib/api/auth';

export function useAuth() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading, setUser, setLoading, logout: logoutStore } = useAuthStore();

  // 現在のユーザー取得
  const { refetch } = useQuery({
    queryKey: ['currentUser'],
    queryFn: authAPI.getCurrentUser,
    enabled: false,
    retry: false,
  });

  // 初期化時にユーザー情報を取得
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    
    if (token) {
      refetch().then(({ data }) => {
        if (data) {
          setUser(data);
        } else {
          setLoading(false);
        }
      }).catch(() => {
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, [refetch, setUser, setLoading]);

  // 登録
  const registerMutation = useMutation({
    mutationFn: (data: RegisterData) => authAPI.register(data),
    onSuccess: (data) => {
      setUser(data.user);
      router.push('/fields');
    },
  });

  // ログイン
  const loginMutation = useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      authAPI.login(email, password),
    onSuccess: (data) => {
      setUser(data.user);
      router.push('/fields');
    },
  });

  // ログアウト
  const logoutMutation = useMutation({
    mutationFn: authAPI.logout,
    onSuccess: () => {
      logoutStore();
      router.push('/login');
    },
  });

  return {
    user,
    isAuthenticated,
    isLoading,
    register: registerMutation.mutate,
    login: loginMutation.mutate,
    logout: logoutMutation.mutate,
    registerError: registerMutation.error,
    loginError: loginMutation.error,
    isRegistering: registerMutation.isPending,
    isLoggingIn: loginMutation.isPending,
  };
}
