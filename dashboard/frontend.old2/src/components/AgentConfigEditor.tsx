/**
 * Agent Configuration Editor Component
 * Direct access to agent config files (Skills, MCP, Instructions, etc.)
 */

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import {
  Settings,
  Save,
  RefreshCw,
  FileText,
  Link,
  Database,
  Code,
  Terminal,
  AlertTriangle,
} from 'lucide-react'
import { api } from '@/lib/api'

interface AgentConnection {
  agent_id: string
  agent_name: string
  connection_type: 'api' | 'local' | 'remote'
  endpoint?: string
  port?: number
  api_key_id?: string
  enabled: boolean
}

interface AgentConfigFile {
  file_path: string
  file_type: 'skill' | 'mcp' | 'instruction' | 'config'
  content: string
  last_modified: string
}

export default function AgentConfigEditor() {
  const queryClient = useQueryClient()
  const [activeTab, setActiveTab] = useState<'connections' | 'files'>('connections')
  const [selectedAgent, setSelectedAgent] = useState<string>('all')
  const [editingFile, setEditingFile] = useState<AgentConfigFile | null>(null)
  const [editedContent, setEditedContent] = useState<string>('')

  // Fetch agent connections
  const { data: connectionsResponse, isLoading: connectionsLoading } = useQuery({
    queryKey: ['agent-connections'],
    queryFn: async () => {
      const result = await api.getAgentConnections()
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
  })

  // Fetch agent config files
  const { data: filesResponse, isLoading: filesLoading } = useQuery({
    queryKey: ['agent-config-files', selectedAgent],
    queryFn: async () => {
      const fileType =
        selectedAgent === 'all' ? undefined :
        selectedAgent === 'skills' ? 'skill' :
        selectedAgent === 'commands' ? 'instruction' :
        selectedAgent === 'mcp' ? 'mcp' :
        undefined
      const result = await api.getAgentConfigFiles(fileType)
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
  })

  // Update agent connection mutation
  const updateConnectionMutation = useMutation({
    mutationFn: async ({ agent_id, enabled }: { agent_id: string; enabled: boolean }) => {
      const result = await api.updateAgentConnection(agent_id, { enabled })
      if (!result.success) throw new Error(result.error)
      return result.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agent-connections'] })
    },
  })

  // Update config file mutation
  const updateFileMutation = useMutation({
    mutationFn: async ({ file_path, content }: { file_path: string; content: string }) => {
      const result = await api.updateAgentConfigFile(file_path, content)
      if (!result.success) throw new Error(result.error)
      return result.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agent-config-files'] })
      setEditingFile(null)
      setEditedContent('')
    },
  })

  const connections = connectionsResponse?.connections || []
  const configFiles = filesResponse?.files || []

  const handleFileEdit = (file: AgentConfigFile) => {
    setEditingFile(file)
    setEditedContent(file.content)
  }

  const handleFileSave = () => {
    if (editingFile) {
      updateFileMutation.mutate({
        file_path: editingFile.file_path,
        content: editedContent,
      })
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <Settings className="w-6 h-6" />
          Agent Configuration
        </h2>
        <p className="text-gray-500 mt-1">
          Manage agent connections, skills, MCP servers, and instructions
        </p>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as any)} className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="connections">Connections & Endpoints</TabsTrigger>
          <TabsTrigger value="files">Config Files & Skills</TabsTrigger>
        </TabsList>

        {/* Connections Tab */}
        <TabsContent value="connections" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Agent Connections</CardTitle>
              <CardDescription>
                Configure endpoints, ports, and API key associations
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {connectionsLoading ? (
                <div className="text-center py-8 text-muted-foreground">
                  Loading connections...
                </div>
              ) : connections.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  No agent connections found
                </div>
              ) : (
                connections.map((conn) => (
                  <div
                    key={conn.agent_id}
                    className="border rounded-lg p-4 bg-muted/30"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-3 h-3 rounded-full ${
                            conn.enabled ? 'bg-green-500' : 'bg-gray-400'
                          }`}
                        />
                        <h3 className="font-semibold">{conn.agent_name}</h3>
                        <Badge variant={conn.connection_type === 'local' ? 'default' : 'secondary'}>
                          {conn.connection_type}
                        </Badge>
                      </div>
                      <Button variant="outline" size="sm">
                        <Settings className="w-4 h-4 mr-2" />
                        Configure
                      </Button>
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      {conn.endpoint && (
                        <div>
                          <div className="text-muted-foreground flex items-center gap-1">
                            <Link className="w-3 h-3" />
                            Endpoint
                          </div>
                          <div className="font-medium font-mono text-xs">
                            {conn.endpoint}
                            {conn.port && `:${conn.port}`}
                          </div>
                        </div>
                      )}
                      {conn.api_key_id && (
                        <div>
                          <div className="text-muted-foreground flex items-center gap-1">
                            <Database className="w-3 h-3" />
                            API Key
                          </div>
                          <div className="font-medium font-mono text-xs">{conn.api_key_id}</div>
                        </div>
                      )}
                      <div>
                        <div className="text-muted-foreground">Agent ID</div>
                        <div className="font-medium font-mono text-xs">{conn.agent_id}</div>
                      </div>
                      <div>
                        <div className="text-muted-foreground">Status</div>
                        <div className={`font-medium ${conn.enabled ? 'text-green-600' : 'text-gray-500'}`}>
                          {conn.enabled ? 'Active' : 'Inactive'}
                        </div>
                      </div>
                    </div>

                    {conn.connection_type === 'local' && (
                      <div className="mt-3 flex items-center gap-2">
                        <Button variant="secondary" size="sm">
                          <Terminal className="w-4 h-4 mr-2" />
                          Test Connection
                        </Button>
                        <Button variant="outline" size="sm">
                          View Logs
                        </Button>
                      </div>
                    )}
                  </div>
                ))
              )}
            </CardContent>
          </Card>

          {/* Connection Templates */}
          <Card>
            <CardHeader>
              <CardTitle>Add New Connection</CardTitle>
              <CardDescription>
                Quick setup for common agent types
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-3">
                <Button variant="outline" className="justify-start">
                  <Code className="w-4 h-4 mr-2" />
                  Local Ollama
                </Button>
                <Button variant="outline" className="justify-start">
                  <Database className="w-4 h-4 mr-2" />
                  API-based Agent
                </Button>
                <Button variant="outline" className="justify-start">
                  <Link className="w-4 h-4 mr-2" />
                  Remote Server
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Config Files Tab */}
        <TabsContent value="files" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Configuration Files</CardTitle>
              <CardDescription>
                Direct access to skills, MCP servers, slash commands, and instructions
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* File Browser */}
              <div className="grid grid-cols-4 gap-2 mb-4">
                <Button
                  variant={selectedAgent === 'all' ? 'default' : 'outline'}
                  onClick={() => setSelectedAgent('all')}
                  size="sm"
                >
                  All Files
                </Button>
                <Button
                  variant={selectedAgent === 'skills' ? 'default' : 'outline'}
                  onClick={() => setSelectedAgent('skills')}
                  size="sm"
                >
                  Skills
                </Button>
                <Button
                  variant={selectedAgent === 'commands' ? 'default' : 'outline'}
                  onClick={() => setSelectedAgent('commands')}
                  size="sm"
                >
                  Commands
                </Button>
                <Button
                  variant={selectedAgent === 'mcp' ? 'default' : 'outline'}
                  onClick={() => setSelectedAgent('mcp')}
                  size="sm"
                >
                  MCP Servers
                </Button>
              </div>

              {/* File List */}
              {filesLoading ? (
                <div className="text-center py-8 text-muted-foreground">
                  Loading config files...
                </div>
              ) : configFiles.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  No config files found
                </div>
              ) : (
                <div className="space-y-2">
                  {configFiles.map((file) => (
                    <div
                      key={file.file_path}
                      className="border rounded-lg p-3 bg-muted/20 hover:bg-muted/40 cursor-pointer transition-colors"
                      onClick={() => handleFileEdit(file)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <FileText className="w-4 h-4 text-blue-500" />
                          <div>
                            <div className="font-medium font-mono text-sm">{file.file_path}</div>
                            <div className="text-xs text-muted-foreground">
                              {file.file_type.toUpperCase()} • Modified:{' '}
                              {new Date(file.last_modified).toLocaleString()}
                            </div>
                          </div>
                        </div>
                        <Button variant="ghost" size="sm">
                          Edit
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* File Editor */}
              {editingFile && (
                <div className="mt-6 border rounded-lg p-4 bg-card">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold">Editing: {editingFile.file_path}</h3>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setEditingFile(null)
                          setEditedContent('')
                        }}
                        disabled={updateFileMutation.isPending}
                      >
                        Cancel
                      </Button>
                      <Button
                        variant="default"
                        size="sm"
                        onClick={handleFileSave}
                        disabled={updateFileMutation.isPending}
                      >
                        <Save className="w-4 h-4 mr-2" />
                        {updateFileMutation.isPending ? 'Saving...' : 'Save Changes'}
                      </Button>
                    </div>
                  </div>
                  <textarea
                    className="w-full h-64 p-4 font-mono text-sm border rounded-lg bg-muted/30 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={editedContent}
                    onChange={(e) => setEditedContent(e.target.value)}
                  />
                  <div className="mt-2 flex items-center gap-2 text-xs text-muted-foreground">
                    <AlertTriangle className="w-3 h-3" />
                    Changes will be applied immediately to the running system
                  </div>
                </div>
              )}

              {/* Add New File */}
              <div className="pt-4 border-t">
                <Button variant="default">
                  <FileText className="w-4 h-4 mr-2" />
                  Create New Config File
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Guidelines & Embeddings */}
          <Card>
            <CardHeader>
              <CardTitle>Guidelines & Embeddings</CardTitle>
              <CardDescription>
                Manage hierarchical guidelines and embedding generation
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 border rounded-lg bg-muted/20">
                  <div>
                    <div className="font-medium">lazy-bird/guidelines/</div>
                    <div className="text-sm text-muted-foreground">
                      Hierarchical guideline system with auto-embedding
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    Browse
                  </Button>
                </div>
                <div className="flex items-center justify-between p-3 border rounded-lg bg-muted/20">
                  <div>
                    <div className="font-medium">embedding_generator.py</div>
                    <div className="text-sm text-muted-foreground">
                      Configure embedding model and parameters
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    Edit
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
