/**
 * HRM (Hierarchical Reasoning Module) Page
 * Complete HRM configuration and monitoring interface
 */

import { useState, useEffect } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/card'
import { Badge } from '../components/ui/badge'
import { HRMControlPanelV2 } from '../components/HRMControlPanelV2'
import { HRMPresetGallery } from '../components/HRMPresetGallery'
import { ws } from '../lib/websocket'
import {
  Settings,
  Layers,
  Zap,
  Bell,
  Info,
} from 'lucide-react'

export function HRM() {
  const [selectedProjectId] = useState<string>('default') // Use 'default' for global config
  const [notifications, setNotifications] = useState<any[]>([])

  useEffect(() => {
    // Subscribe to HRM updates
    const unsubscribe = ws.subscribeToHRMUpdates(selectedProjectId, (data) => {
      addNotification({
        type: data.event || 'info',
        message: `HRM ${data.event || 'updated'}`,
        timestamp: new Date().toISOString(),
        data,
      })
    })

    // Subscribe to system alerts
    const unsubscribeAlerts = ws.subscribeToSystemAlerts((data) => {
      if (data.message && data.message.includes('HRM')) {
        addNotification({
          type: data.severity,
          message: data.message,
          timestamp: new Date().toISOString(),
        })
      }
    })

    return () => {
      unsubscribe()
      unsubscribeAlerts()
    }
  }, [selectedProjectId])

  const addNotification = (notification: any) => {
    setNotifications((prev) => [notification, ...prev].slice(0, 10)) // Keep last 10
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <Layers className="w-8 h-8 text-primary" />
            Hierarchical Reasoning Module
          </h1>
          <p className="text-muted-foreground mt-2">
            Real-time ML/RL optimization controls with instant persistence
          </p>
        </div>

        {/* Connection Status */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg border border-border">
            <div
              className={`w-2 h-2 rounded-full ${
                ws.isConnected() ? 'bg-green-500 animate-pulse' : 'bg-red-500'
              }`}
            />
            <span className="text-sm font-medium">
              {ws.isConnected() ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {/* Notifications Badge */}
          {notifications.length > 0 && (
            <Badge className="flex items-center gap-1">
              <Bell className="w-3 h-3" />
              {notifications.length}
            </Badge>
          )}
        </div>
      </div>

      {/* Main Tabs */}
      <Tabs defaultValue="control" className="w-full">
        <TabsList className="grid w-full grid-cols-3 max-w-md">
          <TabsTrigger value="control" className="flex items-center gap-2">
            <Settings className="w-4 h-4" />
            Control Panel
          </TabsTrigger>
          <TabsTrigger value="presets" className="flex items-center gap-2">
            <Layers className="w-4 h-4" />
            Presets
          </TabsTrigger>
          <TabsTrigger value="monitoring" className="flex items-center gap-2">
            <Zap className="w-4 h-4" />
            Activity
          </TabsTrigger>
        </TabsList>

        {/* Control Panel Tab */}
        <TabsContent value="control" className="mt-6">
          <HRMControlPanelV2 projectId={selectedProjectId} />
        </TabsContent>

        {/* Presets Tab */}
        <TabsContent value="presets" className="mt-6">
          <HRMPresetGallery
            projectId={selectedProjectId}
            onPresetApplied={(preset) => {
              addNotification({
                type: 'success',
                message: `Preset "${preset.name}" applied successfully`,
                timestamp: new Date().toISOString(),
              })
            }}
          />
        </TabsContent>

        {/* Activity Monitoring Tab */}
        <TabsContent value="monitoring" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="w-5 h-5" />
                Recent Activity
              </CardTitle>
              <CardDescription>
                Real-time updates from HRM system
              </CardDescription>
            </CardHeader>
            <CardContent>
              {notifications.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <Info className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>No recent activity</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {notifications.map((notif, i) => (
                    <NotificationItem key={i} notification={notif} />
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

function InfoCard({
  title,
  value,
  description,
  icon: Icon,
  color,
  bgColor,
}: {
  title: string
  value: string
  description: string
  icon: any
  color: string
  bgColor: string
}) {
  return (
    <Card className="p-6">
      <div className="flex items-start gap-3">
        <div className={`p-2 rounded-lg ${bgColor}`}>
          <Icon className={`w-5 h-5 ${color}`} />
        </div>
        <div className="flex-1">
          <div className="text-2xl font-bold">{value}</div>
          <div className="text-sm font-medium">{title}</div>
          <div className="text-xs text-muted-foreground mt-1">{description}</div>
        </div>
      </div>
    </Card>
  )
}

function NotificationItem({ notification }: { notification: any }) {
  const typeColors = {
    success: 'border-green-200 bg-green-50 text-green-800',
    warning: 'border-yellow-200 bg-yellow-50 text-yellow-800',
    error: 'border-red-200 bg-red-50 text-red-800',
    info: 'border-blue-200 bg-blue-50 text-blue-800',
  }

  const color = typeColors[notification.type as keyof typeof typeColors] || typeColors.info

  return (
    <div className={`p-3 rounded-lg border ${color}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="font-medium">{notification.message}</div>
          {notification.data && (
            <div className="text-xs mt-1 opacity-75">
              {JSON.stringify(notification.data, null, 2).slice(0, 100)}...
            </div>
          )}
        </div>
        <div className="text-xs opacity-75">
          {new Date(notification.timestamp).toLocaleTimeString()}
        </div>
      </div>
    </div>
  )
}
