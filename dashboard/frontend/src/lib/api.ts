/**
 * API Client for Backend Communication
 * Type-safe wrapper around fetch API
 */

import type {
  Project,
  ProjectConfiguration,
  Task,
  DashboardStats,
  QualityMetrics,
  PerformanceMetrics,
  CostMetrics,
  ApiResponse,
  PaginatedResponse,
  AgentPerformanceData,
  QualityTrendData,
  CostBreakdownData,
} from './types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      })

      if (!response.ok) {
        const error = await response.json().catch(() => ({ error: 'Unknown error' }))
        return {
          success: false,
          error: error.error || error.detail || `HTTP ${response.status}`,
        }
      }

      const data = await response.json()
      return {
        success: true,
        data,
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      }
    }
  }

  // ==================== PROJECTS ====================

  async getProjects(): Promise<ApiResponse<Project[]>> {
    return this.request<Project[]>('/projects')
  }

  async getProject(id: string): Promise<ApiResponse<Project>> {
    return this.request<Project>(`/projects/${id}`)
  }

  async createProject(data: {
    name: string
    type: Project['type']
    github_repo?: string
    config?: Partial<ProjectConfiguration>
  }): Promise<ApiResponse<Project>> {
    return this.request<Project>('/projects', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateProject(
    id: string,
    data: Partial<Project>
  ): Promise<ApiResponse<Project>> {
    return this.request<Project>(`/projects/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deleteProject(id: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/projects/${id}`, {
      method: 'DELETE',
    })
  }

  async updateProjectConfig(
    id: string,
    config: ProjectConfiguration
  ): Promise<ApiResponse<Project>> {
    return this.request<Project>(`/projects/${id}/config`, {
      method: 'PUT',
      body: JSON.stringify(config),
    })
  }

  // ==================== TASKS ====================

  async getTasks(params?: {
    project_id?: string
    status?: Task['status']
    page?: number
    page_size?: number
  }): Promise<ApiResponse<PaginatedResponse<Task>>> {
    const searchParams = new URLSearchParams()
    if (params?.project_id) searchParams.set('project_id', params.project_id)
    if (params?.status) searchParams.set('status', params.status)
    if (params?.page) searchParams.set('page', params.page.toString())
    if (params?.page_size) searchParams.set('page_size', params.page_size.toString())

    const query = searchParams.toString()
    return this.request<PaginatedResponse<Task>>(
      `/tasks${query ? `?${query}` : ''}`
    )
  }

  async getTask(id: string): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/tasks/${id}`)
  }

  async retryTask(id: string): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/tasks/${id}/retry`, {
      method: 'POST',
    })
  }

  async cancelTask(id: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/tasks/${id}/cancel`, {
      method: 'POST',
    })
  }

  // ==================== METRICS ====================

  async getDashboardStats(): Promise<ApiResponse<DashboardStats>> {
    return this.request<DashboardStats>('/metrics/dashboard')
  }

  async getQualityMetrics(params?: {
    project_id?: string
    start_date?: string
    end_date?: string
  }): Promise<ApiResponse<QualityTrendData[]>> {
    const searchParams = new URLSearchParams()
    if (params?.project_id) searchParams.set('project_id', params.project_id)
    if (params?.start_date) searchParams.set('start_date', params.start_date)
    if (params?.end_date) searchParams.set('end_date', params.end_date)

    const query = searchParams.toString()
    return this.request<QualityTrendData[]>(
      `/metrics/quality${query ? `?${query}` : ''}`
    )
  }

  async getCostMetrics(params?: {
    project_id?: string
    period?: '7d' | '30d' | '90d' | 'all'
  }): Promise<ApiResponse<CostMetrics>> {
    const searchParams = new URLSearchParams()
    if (params?.project_id) searchParams.set('project_id', params.project_id)
    if (params?.period) searchParams.set('period', params.period)

    const query = searchParams.toString()
    return this.request<CostMetrics>(
      `/metrics/cost${query ? `?${query}` : ''}`
    )
  }

  async getAgentPerformance(params?: {
    project_id?: string
    period?: '7d' | '30d' | '90d' | 'all'
  }): Promise<ApiResponse<AgentPerformanceData[]>> {
    const searchParams = new URLSearchParams()
    if (params?.project_id) searchParams.set('project_id', params.project_id)
    if (params?.period) searchParams.set('period', params.period)

    const query = searchParams.toString()
    return this.request<AgentPerformanceData[]>(
      `/metrics/agents${query ? `?${query}` : ''}`
    )
  }

  async getPerformanceMetrics(params?: {
    project_id?: string
  }): Promise<ApiResponse<PerformanceMetrics>> {
    const searchParams = new URLSearchParams()
    if (params?.project_id) searchParams.set('project_id', params.project_id)

    const query = searchParams.toString()
    return this.request<PerformanceMetrics>(
      `/metrics/performance${query ? `?${query}` : ''}`
    )
  }

  // ==================== CONFIGURATION ====================

  async getDefaultConfig(): Promise<ApiResponse<ProjectConfiguration>> {
    return this.request<ProjectConfiguration>('/config/default')
  }

  async validateConfig(
    config: ProjectConfiguration
  ): Promise<ApiResponse<{ valid: boolean; errors?: string[] }>> {
    return this.request<{ valid: boolean; errors?: string[] }>(
      '/config/validate',
      {
        method: 'POST',
        body: JSON.stringify(config),
      }
    )
  }

  // ==================== SYSTEM ====================

  async getSystemHealth(): Promise<
    ApiResponse<{
      status: 'healthy' | 'degraded' | 'down'
      components: Record<string, boolean>
      uptime_seconds: number
    }>
  > {
    return this.request('/health')
  }

  async getCacheStatistics(): Promise<
    ApiResponse<{
      guideline_cache: any
      github_cache: any
      quality_pattern_cache: any
    }>
  > {
    return this.request('/cache-stats')
  }

  async clearCache(layer?: 'guideline' | 'github' | 'quality'): Promise<
    ApiResponse<void>
  > {
    const searchParams = new URLSearchParams()
    if (layer) searchParams.set('layer', layer)

    const query = searchParams.toString()
    return this.request<void>(`/clear-cache${query ? `?${query}` : ''}`, {
      method: 'POST',
    })
  }

  // ==================== TEMPLATES ====================

  async getTemplates(): Promise<
    ApiResponse<{
      templates: Array<{
        id: string
        name: string
        description: string
        icon: string
      }>
    }>
  > {
    return this.request('/templates')
  }

  async getTemplate(id: string): Promise<
    ApiResponse<{
      name: string
      description: string
      guidelines: string[]
      prerequisites: string[]
      tech_stack: string[]
      estimated_duration: string
      complexity: string
    }>
  > {
    return this.request(`/templates/${id}`)
  }
}

// Export singleton instance
export const api = new ApiClient()

// Export class for testing
export default ApiClient
