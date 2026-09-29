'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter, useParams } from 'next/navigation';
import { login } from '@/lib/api';

export default function LoginPage() {
  const t = useTranslations('login');
  const router = useRouter();
  const { locale } = useParams<{ locale: string }>();

  const [tenantSlug, setTenantSlug] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const tokens = await login(tenantSlug, email, password);
      localStorage.setItem('namaa_access_token', tokens.access_token);
      localStorage.setItem('namaa_refresh_token', tokens.refresh_token);
      router.push(`/${locale}/dashboard`);
    } catch {
      setError(t('error'));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <form onSubmit={handleSubmit} className="w-full max-w-sm space-y-4 rounded-xl border bg-white p-8 shadow-sm">
        <h1 className="text-xl font-semibold">{t('title')}</h1>

        <div className="space-y-1">
          <label className="text-sm font-medium">{t('tenantSlug')}</label>
          <input
            className="w-full rounded-md border px-3 py-2"
            value={tenantSlug}
            onChange={(e) => setTenantSlug(e.target.value)}
            required
          />
        </div>

        <div className="space-y-1">
          <label className="text-sm font-medium">{t('email')}</label>
          <input
            type="email"
            className="w-full rounded-md border px-3 py-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="space-y-1">
          <label className="text-sm font-medium">{t('password')}</label>
          <input
            type="password"
            className="w-full rounded-md border px-3 py-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-md bg-gray-900 py-2 text-white disabled:opacity-50"
        >
          {t('submit')}
        </button>
      </form>
    </main>
  );
}
