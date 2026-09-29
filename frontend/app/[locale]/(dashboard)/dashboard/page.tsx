'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter, useParams } from 'next/navigation';
import { getToday } from '@/lib/api';

export default function DashboardPage() {
  const t = useTranslations('dashboard');
  const router = useRouter();
  const { locale } = useParams<{ locale: string }>();

  const [stats, setStats] = useState<{
    pending_approvals: number;
    open_tasks: number;
    unassigned_conversations: number;
  } | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('namaa_access_token');
    if (!token) {
      router.push(`/${locale}/login`);
      return;
    }
    getToday(token)
      .then(setStats)
      .catch(() => router.push(`/${locale}/login`));
  }, [locale, router]);

  if (!stats) return null;

  const isEmpty = stats.pending_approvals === 0 && stats.open_tasks === 0 && stats.unassigned_conversations === 0;

  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="mb-6 text-2xl font-semibold">{t('title')}</h1>

      {isEmpty ? (
        <p className="text-gray-500">{t('empty')}</p>
      ) : (
        <div className="grid grid-cols-3 gap-4">
          <StatCard label={t('pendingApprovals')} value={stats.pending_approvals} />
          <StatCard label={t('openTasks')} value={stats.open_tasks} />
          <StatCard label={t('unassignedConversations')} value={stats.unassigned_conversations} />
        </div>
      )}
    </main>
  );
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-xl border bg-white p-4 shadow-sm">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-semibold">{value}</p>
    </div>
  );
}
