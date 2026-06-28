import type { AuthenticationSession, AuthenticationTokens } from '@/domains/auth/contracts'
import type { Organization } from '@/domains/organizations/contracts'
import type { components } from '@/shared/api/schema'

type Account = components['schemas']['AccountOutputSerializerV1']

type MockData = {
  account: Account
  authentication?: Partial<AuthenticationTokens> & {
    session?: Partial<AuthenticationSession>
  }
  organization: Organization
}

let mockDataPromise: Promise<MockData> | null = null

export const isMockDataEnabled = import.meta.env.VITE_USE_MOCK_DATA === 'true'

export async function getMockAccount() {
  const mockData = await getMockData()
  return mockData.account
}

export async function getMockAuthenticationTokens(): Promise<AuthenticationTokens> {
  const mockData = await getMockData()
  const sessionId = mockData.authentication?.session_id ?? '00000000-0000-4000-8000-000000000001'

  return {
    access_expires_in: mockData.authentication?.access_expires_in ?? 3600,
    access_token: mockData.authentication?.access_token ?? 'mock-access-token',
    refresh_expires_at: mockData.authentication?.refresh_expires_at ?? getDateInDays(30),
    refresh_token: mockData.authentication?.refresh_token ?? 'mock-refresh-token',
    session_id: sessionId,
    token_type: mockData.authentication?.token_type ?? 'Bearer',
  }
}

export async function getMockAuthenticationSessions(): Promise<AuthenticationSession[]> {
  const mockData = await getMockData()
  const tokens = await getMockAuthenticationTokens()
  const now = new Date().toISOString()

  return [
    {
      created_at: mockData.authentication?.session?.created_at ?? now,
      expires_at: mockData.authentication?.session?.expires_at ?? getDateInDays(30),
      id: tokens.session_id,
      is_current: true,
      last_used_at: mockData.authentication?.session?.last_used_at ?? now,
    },
  ]
}

export async function getMockOrganization() {
  const mockData = await getMockData()
  return mockData.organization
}

export async function getMockOrganizations() {
  return [await getMockOrganization()]
}

async function getMockData() {
  if (!mockDataPromise) {
    mockDataPromise = fetch(`${import.meta.env.BASE_URL}mock-data.json`, {
      cache: 'no-cache',
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Unable to load mock data: ${response.status}`)
        }

        return response.json() as Promise<MockData>
      })
      .then(validateMockData)
  }

  return mockDataPromise
}

function validateMockData(mockData: MockData) {
  if (!mockData.account?.id || !mockData.organization?.id || !mockData.organization?.name) {
    throw new Error('mock-data.json must include account and organization records.')
  }

  return mockData
}

function getDateInDays(days: number) {
  const date = new Date()
  date.setDate(date.getDate() + days)
  return date.toISOString()
}
