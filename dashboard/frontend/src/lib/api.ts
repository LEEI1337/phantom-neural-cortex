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

  // ==================== HRM CONFIGURATION ====================

  async getHRMConfig(params: {
    project_id?: string
    task_id?: string
  }): Promise<ApiResponse<any>> {
    const searchParams = new URLSearchParams()
    if (params.project_id) searchParams.set('project_id', params.project_id)
    if (params.task_id) searchParams.set('task_id', params.task_id)

    const query = searchParams.toString()
    return this.request(`/hrm/config${query ? `?${query}` : ''}`)
  }

  async updateHRMConfig(data: {
    project_id?: string
    task_id?: string
    config: any
    apply_immediately?: boolean
    persist?: boolean
  }): Promise<ApiResponse<{
    status: string
    config_id: string
    applied_at: string
    impact_estimate: {
      cost_change: number
      speed_change: number
      quality_change: number
      token_reduction: number
    }
    active_tasks_affected: number
    future_tasks_affected: boolean
  }>> {
    return this.request('/hrm/config', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async simulateHRMImpact(data: {
    current_config: any
    proposed_config: any
    task_context: {
      complexity?: number
      estimated_duration?: number
      current_quality?: number
    }
  }): Promise<ApiResponse<{
    impact_analysis: {
      cost: { current: number; predicted: number; change_percent: number; confidence: number }
      speed: { current: number; predicted: number; change_percent: number; confidence: number }
      quality: { current: number; predicted: number; change_percent: number; confidence: number }
      tokens: { current: number; predicted: number; change_percent: number; confidence: number }
    }
    warnings: string[]
    recommendations: string[]
  }>> {
    return this.request('/hrm/simulate', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async getHRMPresets(params?: {
    include_builtin?: boolean
    visibility?: string
  }): Promise<ApiResponse<{
    presets: Array<{
      id: string
      name: string
      description: string
      icon: string
      color: string
      builtin: boolean
      config: any
      usage_stats: {
        usage_count: number
        avg_quality: number | null
        avg_cost: number | null
        avg_duration: number | null
      }
    }>
  }>> {
    const searchParams = new URLSearchParams()
    if (params?.include_builtin !== undefined)
      searchParams.set('include_builtin', params.include_builtin.toString())
    if (params?.visibility)
      searchParams.set('visibility', params.visibility)

    const query = searchParams.toString()
    return this.request(`/hrm/config/presets${query ? `?${query}` : ''}`)
  }

  async createHRMPreset(data: {
    name: string
    description: string
    icon: string
    color: string
    config: any
    visibility: string
  }): Promise<ApiResponse<any>> {
    return this.request('/hrm/config/presets', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async applyHRMPreset(
    preset_id: string,
    params: {
      project_id: string
      apply_immediately?: boolean
    }
  ): Promise<ApiResponse<{
    status: string
    config_id: string
    applied_at: string
    impact_estimate: {
      cost_change: number
      speed_change: number
      quality_change: number
      token_reduction: number
    }
    active_tasks_affected: number
    future_tasks_affected: boolean
  }>> {
    const searchParams = new URLSearchParams()
    searchParams.set('project_id', params.project_id)
    if (params.apply_immediately !== undefined)
      searchParams.set('apply_immediately', params.apply_immediately.toString())

    const query = searchParams.toString()
    return this.request(`/hrm/config/presets/${preset_id}/apply?${query}`, {
      method: 'POST',
    })
  }

  async getHRMConfigHistory(config_id: string): Promise<ApiResponse<{
    history: Array<{
      id: string
      config_id: string
      changed_by: string
      changed_at: string
      change_type: string
      old_config: any
      new_config: any
      task_id: string | null
      impact_metrics: {
        cost_change: number
        speed_change: number
        quality_change: number
        token_reduction: number
      }
    }>
  }>> {
    return this.request(`/hrm/config/history/${config_id}`)
  }

  // ==================== AGENT CONFIGURATION ====================

  async getAgentConnections(): Promise<ApiResponse<{
    connections: Array<{
      agent_id: string
      agent_name: string
      connection_type: 'api' | 'local' | 'remote'
      endpoint?: string
      port?: number
      api_key_id?: string
      enabled: boolean
    }>
  }>> {
    return this.request('/agents/connections')
  }

  async getAgentConnection(agent_id: string): Promise<ApiResponse<{
    agent_id: string
    agent_name: string
    connection_type: 'api' | 'local' | 'remote'
    endpoint?: string
    port?: number
    api_key_id?: string
    enabled: boolean
  }>> {
    return this.request(`/agents/connections/${agent_id}`)
  }

  async createAgentConnection(data: {
    agent_id: string
    agent_name: string
    connection_type: 'api' | 'local' | 'remote'
    endpoint?: string
    port?: number
    api_key_id?: string
    enabled?: boolean
  }): Promise<ApiResponse<{
    agent_id: string
    agent_name: string
    connection_type: 'api' | 'local' | 'remote'
    endpoint?: string
    port?: number
    api_key_id?: string
    enabled: boolean
  }>> {
    return this.request('/agents/connections', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateAgentConnection(
    agent_id: string,
    data: {
      agent_name?: string
      endpoint?: string
      port?: number
      api_key_id?: string
      enabled?: boolean
    }
  ): Promise<ApiResponse<{
    agent_id: string
    agent_name: string
    connection_type: 'api' | 'local' | 'remote'
    endpoint?: string
    port?: number
    api_key_id?: string
    enabled: boolean
  }>> {
    return this.request(`/agents/connections/${agent_id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deleteAgentConnection(agent_id: string): Promise<ApiResponse<{
    message: string
  }>> {
    return this.request(`/agents/connections/${agent_id}`, {
      method: 'DELETE',
    })
  }

  async getAgentConfigFiles(file_type?: string): Promise<ApiResponse<{
    files: Array<{
      file_path: string
      file_type: 'skill' | 'mcp' | 'instruction' | 'config'
      content: string
      last_modified: string
    }>
  }>> {
    const query = file_type ? `?file_type=${file_type}` : ''
    return this.request(`/agents/files${query}`)
  }

  async getAgentConfigFile(file_path: string): Promise<ApiResponse<{
    file_path: string
    file_type: 'skill' | 'mcp' | 'instruction' | 'config'
    content: string
    last_modified: string
  }>> {
    return this.request(`/agents/files/${encodeURIComponent(file_path)}`)
  }

  async updateAgentConfigFile(
    file_path: string,
    content: string
  ): Promise<ApiResponse<{
    file_path: string
    file_type: 'skill' | 'mcp' | 'instruction' | 'config'
    content: string
    last_modified: string
  }>> {
    return this.request(`/agents/files/${encodeURIComponent(file_path)}`, {
      method: 'PUT',
      body: JSON.stringify({ content }),
    })
  }

  async createAgentConfigFile(data: {
    file_path: string
    file_type: 'skill' | 'mcp' | 'instruction' | 'config'
    content: string
  }): Promise<ApiResponse<{
    file_path: string
    file_type: 'skill' | 'mcp' | 'instruction' | 'config'
    content: string
    last_modified: string
  }>> {
    return this.request('/agents/files', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async deleteAgentConfigFile(file_path: string): Promise<ApiResponse<{
    message: string
  }>> {
    return this.request(`/agents/files/${encodeURIComponent(file_path)}`, {
      method: 'DELETE',
    })
  }
}

// Export singleton instance
export const api = new ApiClient()

// Export class for testing
export default ApiClient
