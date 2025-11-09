/**
 * ProjectWizard Component
 * Multi-step AI-assisted project creation with template selection
 */

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ChevronLeft, ChevronRight, Sparkles, CheckCircle2, Circle, X } from 'lucide-react'
import { api } from '@/lib/api'
import type { ProjectType } from '@/lib/types'

interface ProjectWizardProps {
  onSubmit: (data: { name: string; type: ProjectType; github_repo?: string; template_id?: string }) => void
  onCancel: () => void
  isSubmitting: boolean
}

type WizardStep = 'template' | 'details' | 'guidelines' | 'prerequisites'

export default function ProjectWizard({ onSubmit, onCancel, isSubmitting }: ProjectWizardProps) {
  const [currentStep, setCurrentStep] = useState<WizardStep>('template')
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null)
  const [projectName, setProjectName] = useState('')
  const [projectType, setProjectType] = useState<ProjectType>('python')
  const [githubRepo, setGithubRepo] = useState('')
  const [checkedPrerequisites, setCheckedPrerequisites] = useState<Set<number>>(new Set())

  // Fetch templates
  const { data: templatesResponse, isLoading: templatesLoading } = useQuery({
    queryKey: ['templates'],
    queryFn: async () => {
      const result = await api.getTemplates()
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
  })

  // Fetch selected template details
  const { data: templateDetails, isLoading: templateLoading } = useQuery({
    queryKey: ['template', selectedTemplate],
    queryFn: async () => {
      if (!selectedTemplate) return null
      const result = await api.getTemplate(selectedTemplate)
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
    enabled: !!selectedTemplate,
  })

  const templates = templatesResponse?.templates || []

  const steps: { id: WizardStep; label: string }[] = [
    { id: 'template', label: 'Choose Template' },
    { id: 'details', label: 'Project Details' },
    { id: 'guidelines', label: 'Review Guidelines' },
    { id: 'prerequisites', label: 'Prerequisites' },
  ]

  const currentStepIndex = steps.findIndex((s) => s.id === currentStep)

  const handleNext = () => {
    const nextIndex = currentStepIndex + 1
    if (nextIndex < steps.length) {
      setCurrentStep(steps[nextIndex].id)
    }
  }

  const handleBack = () => {
    const prevIndex = currentStepIndex - 1
    if (prevIndex >= 0) {
      setCurrentStep(steps[prevIndex].id)
    }
  }

  const handleSubmit = () => {
    onSubmit({
      name: projectName,
      type: projectType,
      github_repo: githubRepo || undefined,
      template_id: selectedTemplate || undefined,
    })
  }

  const canProceed = () => {
    switch (currentStep) {
      case 'template':
        return selectedTemplate !== null
      case 'details':
        return projectName.trim().length > 0
      case 'guidelines':
        return true
      case 'prerequisites':
        return true
      default:
        return false
    }
  }

  return (
    <div className="border rounded-lg bg-card/60 backdrop-blur-md overflow-hidden">
      {/* Progress Steps */}
      <div className="border-b border-border bg-muted/30 px-6 py-4">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-center gap-2">
              <div
                className={`flex items-center gap-2 ${
                  index === currentStepIndex
                    ? 'text-neon-cyan'
                    : index < currentStepIndex
                    ? 'text-neon-green'
                    : 'text-muted-foreground'
                }`}
              >
                {index < currentStepIndex ? (
                  <CheckCircle2 size={20} />
                ) : (
                  <Circle size={20} fill={index === currentStepIndex ? 'currentColor' : 'none'} />
                )}
                <span className="font-medium text-sm">{step.label}</span>
              </div>
              {index < steps.length - 1 && (
                <ChevronRight size={16} className="text-muted-foreground mx-2" />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Step 1: Template Selection */}
        {currentStep === 'template' && (
          <div className="space-y-4">
            <div className="flex items-center gap-2 mb-6">
              <Sparkles className="text-neon-cyan" size={24} />
              <h3 className="text-xl font-bold">Choose Your Project Template</h3>
            </div>

            {templatesLoading ? (
              <div className="text-center py-8 text-muted-foreground">Loading templates...</div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {templates.map((template) => (
                  <button
                    key={template.id}
                    onClick={() => setSelectedTemplate(template.id)}
                    className={`p-6 border rounded-lg text-left transition-all ${
                      selectedTemplate === template.id
                        ? 'border-neon-cyan bg-neon-cyan/10 shadow-neon-cyan'
                        : 'border-border hover:border-neon-cyan/50'
                    }`}
                  >
                    <div className="text-4xl mb-3">{template.icon}</div>
                    <h4 className="font-semibold mb-2">{template.name}</h4>
                    <p className="text-sm text-muted-foreground">{template.description}</p>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Step 2: Project Details */}
        {currentStep === 'details' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-bold mb-4">Project Details</h3>
              <p className="text-sm text-muted-foreground mb-6">
                Configure your project settings
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Project Name *</label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                className="w-full px-4 py-3 bg-background border border-border rounded-lg focus:border-neon-cyan focus:outline-none"
                placeholder="My Awesome AI Project"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Project Type *</label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { value: 'python', label: 'Python', icon: '🐍' },
                  { value: 'typescript', label: 'TypeScript', icon: '📘' },
                  { value: 'react', label: 'React', icon: '⚛️' },
                  { value: 'node', label: 'Node.js', icon: '🟢' },
                  { value: 'general', label: 'General', icon: '📦' },
                ].map((type) => (
                  <button
                    key={type.value}
                    type="button"
                    onClick={() => setProjectType(type.value as ProjectType)}
                    className={`p-4 border rounded-lg transition-all ${
                      projectType === type.value
                        ? 'border-neon-cyan bg-neon-cyan/10'
                        : 'border-border hover:border-neon-cyan/50'
                    }`}
                  >
                    <div className="text-2xl mb-1">{type.icon}</div>
                    <div className="text-sm font-medium">{type.label}</div>
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
                className="w-full px-4 py-3 bg-background border border-border rounded-lg focus:border-neon-cyan focus:outline-none"
                placeholder="username/repository"
              />
            </div>
          </div>
        )}

        {/* Step 3: Guidelines */}
        {currentStep === 'guidelines' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-bold mb-4">Project Guidelines</h3>
              <p className="text-sm text-muted-foreground mb-6">
                Review best practices for your {templateDetails?.name || 'project'}
              </p>
            </div>

            {templateLoading ? (
              <div className="text-center py-8 text-muted-foreground">Loading guidelines...</div>
            ) : (
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {templateDetails?.guidelines.map((guideline, index) => (
                  <div
                    key={index}
                    className="border rounded-lg p-4 bg-muted/30 prose prose-sm dark:prose-invert max-w-none"
                  >
                    <pre className="whitespace-pre-wrap font-mono text-xs">{guideline}</pre>
                  </div>
                ))}

                <div className="border rounded-lg p-4 bg-neon-cyan/10 border-neon-cyan/30">
                  <h4 className="font-semibold text-neon-cyan mb-2">Tech Stack</h4>
                  <div className="flex flex-wrap gap-2">
                    {templateDetails?.tech_stack.map((tech, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-background rounded-full text-xs font-medium"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="border rounded-lg p-4 bg-neon-purple/10 border-neon-purple/30">
                  <h4 className="font-semibold text-neon-purple mb-2">Estimated Duration</h4>
                  <p className="text-sm">{templateDetails?.estimated_duration}</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Step 4: Prerequisites */}
        {currentStep === 'prerequisites' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-xl font-bold mb-4">Prerequisites Checklist</h3>
              <p className="text-sm text-muted-foreground mb-6">
                Ensure you have everything needed before starting
              </p>
            </div>

            {templateLoading ? (
              <div className="text-center py-8 text-muted-foreground">
                Loading prerequisites...
              </div>
            ) : (
              <div className="space-y-3">
                {templateDetails?.prerequisites.map((prereq, index) => (
                  <label
                    key={index}
                    className="flex items-center gap-3 p-4 border rounded-lg hover:bg-muted/30 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={checkedPrerequisites.has(index)}
                      onChange={(e) => {
                        const newSet = new Set(checkedPrerequisites)
                        if (e.target.checked) {
                          newSet.add(index)
                        } else {
                          newSet.delete(index)
                        }
                        setCheckedPrerequisites(newSet)
                      }}
                      className="w-5 h-5 rounded border-border"
                    />
                    <span className="flex-1">{prereq}</span>
                    {checkedPrerequisites.has(index) && (
                      <CheckCircle2 className="text-neon-green" size={20} />
                    )}
                  </label>
                ))}
              </div>
            )}

            <div className="border-l-4 border-neon-cyan bg-neon-cyan/10 p-4 rounded">
              <p className="text-sm text-muted-foreground">
                <strong className="text-foreground">Pro Tip:</strong> Make sure all prerequisites
                are met before creating the project for the best experience.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="border-t border-border bg-muted/30 px-6 py-4 flex items-center justify-between">
        <button
          onClick={onCancel}
          disabled={isSubmitting}
          className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-accent disabled:opacity-50"
        >
          <X size={16} />
          Cancel
        </button>

        <div className="flex gap-3">
          {currentStepIndex > 0 && (
            <button
              onClick={handleBack}
              disabled={isSubmitting}
              className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-accent disabled:opacity-50"
            >
              <ChevronLeft size={16} />
              Back
            </button>
          )}

          {currentStepIndex < steps.length - 1 ? (
            <button
              onClick={handleNext}
              disabled={!canProceed() || isSubmitting}
              className="flex items-center gap-2 px-4 py-2 bg-neon-cyan text-black rounded-lg hover:bg-neon-cyan/90 disabled:opacity-50"
            >
              Next
              <ChevronRight size={16} />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={!canProceed() || isSubmitting}
              className="flex items-center gap-2 px-6 py-2 bg-neon-green text-black rounded-lg hover:bg-neon-green/90 disabled:opacity-50"
            >
              <Sparkles size={16} />
              {isSubmitting ? 'Creating...' : 'Create Project'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
