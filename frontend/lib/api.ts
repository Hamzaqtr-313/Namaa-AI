const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export type TokenPair = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};

type Envelope<T> = { success: true; data: T } | { success: false; error: { code: string; message: string } };

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  });
  const body = (await res.json()) as Envelope<T>;
  if (!body.success) throw new Error(body.error.message);
  return body.data;
}

export function login(tenantSlug: string, email: string, password: string) {
  return request<TokenPair>('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ tenant_slug: tenantSlug, email, password }),
  });
}

export function getToday(accessToken: string) {
  return request<{ pending_approvals: number; open_tasks: number; unassigned_conversations: number }>(
    '/api/v1/dashboard/today',
    { headers: { Authorization: `Bearer ${accessToken}` } }
  );
}
