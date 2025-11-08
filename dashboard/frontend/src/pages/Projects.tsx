import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import ProjectManager from '@/components/ProjectManager'
import ConfigEditor from '@/components/ConfigEditor'
import type { Project } from '@/lib/types'

export default function Projects() {
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)

  const { data: projectsResponse } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const result = await api.getProjects()
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
  })

  const projects = projectsResponse || []

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Projects</h1>
        <p className="text-muted-foreground mt-1">Manage your AI development projects and configurations</p>
      </div>

      <ProjectManager />

      {selectedProject && (
        <div className="mt-8">
          <ConfigEditor
            config={selectedProject.config}
            onChange={(config) => {
              // Update handled by mutation in ConfigEditor
            }}
            onSave={async () => {
              await api.updateProjectConfig(selectedProject.id, selectedProject.config)
            }}
          />
        </div>
      )}
    </div>
  )
}
