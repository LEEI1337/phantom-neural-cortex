/**
 * ProjectManager Component
 * CRUD Operations für Projekte mit Template-Support
 */

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Edit2, Trash2, Archive, Play, Pause } from 'lucide-react'
import { api } from '@/lib/api'
import type { Project, ProjectType } from '@/lib/types'

const PROJECT_TYPES: { value: ProjectType; label: string; icon: string }[] = [
  { value: 'python', label: 'Python', icon: '🐍' },
  { value: 'typescript', label: 'TypeScript', icon: '📘' },
  { value: 'react', label: 'React', icon: '⚛️' },
  { value: 'node', label: 'Node.js', icon: '🟢' },
  { value: 'general', label: 'General', icon: '📦' },
]

export default function ProjectManager() {
  const queryClient = useQueryClient()
  const [isCreating, setIsCreating] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)

  // Fetch Projects
  const { data: response, isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const result = await api.getProjects()
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
  })

  const projects = response || []

  // Create Project Mutation
  const createMutation = useMutation({
    mutationFn: async (data: { name: string; type: ProjectType; github_repo?: string }) => {
      const result = await api.createProject(data)
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setIsCreating(false)
    },
  })

  // Update Project Mutation
  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<Project> }) => {
      const result = await api.updateProject(id, data)
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setEditingId(null)
    },
  })

  // Delete Project Mutation
  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      const result = await api.deleteProject(id)
      if (!result.success) throw new Error(result.error)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
    },
  })

  if (isLoading) {
    return <div className="p-8 text-center">Loading projects...</div>
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Projects</h2>
          <p className="text-sm text-muted-foreground mt-1">
            Manage your AI development projects ({projects.length}/4 slots)
          </p>
        </div>
        <button
          onClick={() => setIsCreating(true)}
          disabled={projects.length >= 4}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Plus size={20} />
          New Project
        </button>
      </div>

      {/* Create Form */}
      {isCreating && (
        <CreateProjectForm
          onSubmit={(data) => createMutation.mutate(data)}
          onCancel={() => setIsCreating(false)}
          isSubmitting={createMutation.isPending}
        />
      )}

      {/* Project Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {projects.map((project) => (
          <ProjectCard
            key={project.id}
            project={project}
            isEditing={editingId === project.id}
            onEdit={() => setEditingId(project.id)}
            onCancelEdit={() => setEditingId(null)}
            onUpdate={(data) => updateMutation.mutate({ id: project.id, data })}
            onDelete={() => {
              if (confirm(`Delete project "${project.name}"?`)) {
                deleteMutation.mutate(project.id)
              }
            }}
          />
        ))}
      </div>

      {/* Empty State */}
      {projects.length === 0 && !isCreating && (
        <div className="text-center py-12 border-2 border-dashed rounded-lg">
          <p className="text-lg text-muted-foreground mb-4">No projects yet</p>
          <button
            onClick={() => setIsCreating(true)}
            className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90"
          >
            Create Your First Project
          </button>
        </div>
      )}
    </div>
  )
}

function CreateProjectForm({
  onSubmit,
  onCancel,
  isSubmitting,
}: {
  onSubmit: (data: { name: string; type: ProjectType; github_repo?: string }) => void
  onCancel: () => void
  isSubmitting: boolean
}) {
  const [name, setName] = useState('')
  const [type, setType] = useState<ProjectType>('python')
  const [githubRepo, setGithubRepo] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      name,
      type,
      github_repo: githubRepo || undefined,
    })
  }

  return (
    <div className="border rounded-lg p-6 bg-card">
      <h3 className="text-lg font-semibold mb-4">Create New Project</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Project Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary"
            placeholder="My Awesome Project"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Project Type</label>
          <div className="grid grid-cols-3 gap-2">
            {PROJECT_TYPES.map((pt) => (
              <button
                key={pt.value}
                type="button"
                onClick={() => setType(pt.value)}
                className={`px-4 py-3 border rounded-lg text-left ${
                  type === pt.value
                    ? 'border-primary bg-primary/10'
                    : 'border-border hover:border-primary/50'
                }`}
              >
                <div className="text-2xl mb-1">{pt.icon}</div>
                <div className="text-sm font-medium">{pt.label}</div>
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            GitHub Repository (Optional)
          </label>
          <input
            type="text"
            value={githubRepo}
            onChange={(e) => setGithubRepo(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-primary"
            placeholder="owner/repo"
          />
        </div>

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={isSubmitting || !name}
            className="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 disabled:opacity-50"
          >
            {isSubmitting ? 'Creating...' : 'Create Project'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className="px-4 py-2 border rounded-lg hover:bg-accent"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}

function ProjectCard({
  project,
  isEditing,
  onEdit,
  onCancelEdit,
  onUpdate,
  onDelete,
}: {
  project: Project
  isEditing: boolean
  onEdit: () => void
  onCancelEdit: () => void
  onUpdate: (data: Partial<Project>) => void
  onDelete: () => void
}) {
  const typeInfo = PROJECT_TYPES.find((t) => t.value === project.type) || PROJECT_TYPES[4]

  const successRate =
    project.total_tasks > 0
      ? (project.successful_tasks / project.total_tasks) * 100
      : 0

  const toggleStatus = () => {
    const newStatus = project.status === 'active' ? 'paused' : 'active'
    onUpdate({ status: newStatus })
  }

  const archiveProject = () => {
    onUpdate({ status: 'archived' })
  }

  return (
    <div className="border rounded-lg p-5 bg-card hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="text-3xl">{typeInfo.icon}</div>
          <div>
            <h3 className="font-semibold text-lg">{project.name}</h3>
            <p className="text-sm text-muted-foreground">{project.slot}</p>
          </div>
        </div>
        <div className="flex gap-1">
          {project.status === 'active' && (
            <button
              onClick={toggleStatus}
              className="p-2 hover:bg-accent rounded"
              title="Pause"
            >
              <Pause size={16} />
            </button>
          )}
          {project.status === 'paused' && (
            <button
              onClick={toggleStatus}
              className="p-2 hover:bg-accent rounded"
              title="Resume"
            >
              <Play size={16} />
            </button>
          )}
          <button
            onClick={onEdit}
            className="p-2 hover:bg-accent rounded"
            title="Edit"
          >
            <Edit2 size={16} />
          </button>
          <button
            onClick={archiveProject}
            className="p-2 hover:bg-accent rounded"
            title="Archive"
          >
            <Archive size={16} />
          </button>
          <button
            onClick={onDelete}
            className="p-2 hover:bg-destructive/10 text-destructive rounded"
            title="Delete"
          >
            <Trash2 size={16} />
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="space-y-3">
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Tasks</span>
          <span className="font-medium">
            {project.successful_tasks}/{project.total_tasks}
          </span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Success Rate</span>
          <span className="font-medium">{successRate.toFixed(0)}%</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Avg Quality</span>
          <span className="font-medium">{(project.avg_quality * 100).toFixed(0)}%</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-muted-foreground">Total Cost</span>
          <span className="font-medium">${project.total_cost.toFixed(2)}</span>
        </div>
      </div>

      {/* Status Badge */}
      <div className="mt-4 pt-4 border-t">
        <span
          className={`inline-block px-2 py-1 text-xs font-medium rounded ${
            project.status === 'active'
              ? 'bg-green-100 text-green-800'
              : project.status === 'paused'
              ? 'bg-yellow-100 text-yellow-800'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
        </span>
        {project.github_repo && (
          <span className="ml-2 text-xs text-muted-foreground">
            📦 {project.github_repo}
          </span>
        )}
      </div>
    </div>
  )
}
