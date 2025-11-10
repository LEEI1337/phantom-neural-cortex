/**
 * Spec-Kit Workflow Component
 *
 * Visual interface for GitHub Spec-Kit integration with UltraThink optimizations.
 * Displays spec-driven development pipeline: Constitution → Specify → Plan → Tasks → Implement
 */

import React, { useState, useEffect } from 'react';
import { apiClient } from '../lib/api';

interface Feature {
  feature_id: string;
  name: string;
  description: string;
  current_phase: string;
  completed_phases: string[];
  estimated_iterations?: number;
  optimal_agent?: string;
  complexity_score?: number;
  latent_compression?: {
    compression_ratio: number;
    original_tokens: number;
    compressed_tokens: number;
  };
}

interface SpecKitWorkflowProps {
  projectId: string;
}

const PHASES = [
  { id: 'constitution', name: 'Constitution', icon: '📜', description: 'Governing principles' },
  { id: 'specify', name: 'Specify', icon: '📋', description: 'Requirements & user stories' },
  { id: 'clarify', name: 'Clarify', icon: '❓', description: 'Resolve ambiguities' },
  { id: 'plan', name: 'Plan', icon: '📐', description: 'Technical architecture' },
  { id: 'analyze', name: 'Analyze', icon: '🔍', description: 'Consistency validation' },
  { id: 'tasks', name: 'Tasks', icon: '✅', description: 'Task breakdown' },
  { id: 'implement', name: 'Implement', icon: '⚙️', description: 'Execute implementation' },
];

export const SpecKitWorkflow: React.FC<SpecKitWorkflowProps> = ({ projectId }) => {
  const [features, setFeatures] = useState<Feature[]>([]);
  const [selectedFeature, setSelectedFeature] = useState<Feature | null>(null);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Form states
  const [newFeature, setNewFeature] = useState({
    feature_id: '',
    name: '',
    description: '',
  });

  useEffect(() => {
    loadFeatures();
  }, [projectId]);

  const loadFeatures = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get(`/api/speckit/features?project_id=${projectId}`);
      setFeatures(response.data);
    } catch (error) {
      console.error('Failed to load features:', error);
    } finally {
      setLoading(false);
    }
  };

  const createFeature = async () => {
    try {
      setLoading(true);
      const response = await apiClient.post(
        `/api/speckit/features?project_id=${projectId}`,
        newFeature
      );
      setFeatures([...features, response.data]);
      setShowCreateModal(false);
      setNewFeature({ feature_id: '', name: '', description: '' });
    } catch (error) {
      console.error('Failed to create feature:', error);
      alert('Failed to create feature');
    } finally {
      setLoading(false);
    }
  };

  const getPhaseStatus = (feature: Feature, phaseId: string): 'completed' | 'current' | 'pending' => {
    if (feature.completed_phases.includes(phaseId)) {
      return 'completed';
    }
    if (feature.current_phase === phaseId) {
      return 'current';
    }
    return 'pending';
  };

  const getPhaseColor = (status: string): string => {
    switch (status) {
      case 'completed':
        return 'bg-green-500';
      case 'current':
        return 'bg-blue-500';
      default:
        return 'bg-gray-300';
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Spec-Kit Workflow</h2>
          <p className="text-gray-600 mt-1">
            Spec-Driven Development with UltraThink Optimizations
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Create New Feature
        </button>
      </div>

      {/* Features List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {features.map((feature) => (
          <div
            key={feature.feature_id}
            onClick={() => setSelectedFeature(feature)}
            className={`p-4 border-2 rounded-lg cursor-pointer transition ${
              selectedFeature?.feature_id === feature.feature_id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <h3 className="font-semibold text-lg mb-2">{feature.name}</h3>
            <p className="text-sm text-gray-600 mb-3">{feature.description}</p>

            {/* Progress Bar */}
            <div className="mb-3">
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>Progress</span>
                <span>{Math.round((feature.completed_phases.length / 7) * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{ width: `${(feature.completed_phases.length / 7) * 100}%` }}
                />
              </div>
            </div>

            {/* UltraThink Metrics */}
            <div className="grid grid-cols-2 gap-2 text-xs">
              {feature.estimated_iterations && (
                <div className="bg-gray-100 p-2 rounded">
                  <div className="text-gray-500">Iterations</div>
                  <div className="font-semibold">{feature.estimated_iterations}</div>
                </div>
              )}
              {feature.optimal_agent && (
                <div className="bg-gray-100 p-2 rounded">
                  <div className="text-gray-500">Agent</div>
                  <div className="font-semibold capitalize">{feature.optimal_agent}</div>
                </div>
              )}
              {feature.complexity_score && (
                <div className="bg-gray-100 p-2 rounded">
                  <div className="text-gray-500">Complexity</div>
                  <div className="font-semibold">{feature.complexity_score.toFixed(1)}</div>
                </div>
              )}
              {feature.latent_compression && (
                <div className="bg-gray-100 p-2 rounded">
                  <div className="text-gray-500">Compression</div>
                  <div className="font-semibold">
                    {feature.latent_compression.compression_ratio.toFixed(1)}x
                  </div>
                </div>
              )}
            </div>

            {/* Current Phase Badge */}
            <div className="mt-3">
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {PHASES.find((p) => p.id === feature.current_phase)?.icon}{' '}
                {PHASES.find((p) => p.id === feature.current_phase)?.name || feature.current_phase}
              </span>
            </div>
          </div>
        ))}

        {features.length === 0 && !loading && (
          <div className="col-span-full text-center py-12 text-gray-500">
            <p className="text-lg mb-2">No features yet</p>
            <p>Create your first feature to get started</p>
          </div>
        )}
      </div>

      {/* Selected Feature Detail */}
      {selectedFeature && (
        <div className="mt-8 border-2 border-gray-200 rounded-lg p-6">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h3 className="text-xl font-bold">{selectedFeature.name}</h3>
              <p className="text-gray-600 mt-1">{selectedFeature.description}</p>
            </div>
            <button
              onClick={() => setSelectedFeature(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>

          {/* Phase Pipeline */}
          <div className="mb-6">
            <h4 className="font-semibold mb-4">Workflow Pipeline</h4>
            <div className="flex items-center space-x-2 overflow-x-auto pb-4">
              {PHASES.map((phase, index) => {
                const status = getPhaseStatus(selectedFeature, phase.id);
                return (
                  <React.Fragment key={phase.id}>
                    <div className="flex flex-col items-center min-w-[120px]">
                      <div
                        className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl ${getPhaseColor(
                          status
                        )} text-white transition-all ${
                          status === 'current' ? 'ring-4 ring-blue-300 animate-pulse' : ''
                        }`}
                      >
                        {phase.icon}
                      </div>
                      <div className="mt-2 text-center">
                        <div className="text-sm font-medium">{phase.name}</div>
                        <div className="text-xs text-gray-500">{phase.description}</div>
                      </div>
                    </div>
                    {index < PHASES.length - 1 && (
                      <div className="flex-1 min-w-[40px]">
                        <div
                          className={`h-1 ${
                            selectedFeature.completed_phases.includes(phase.id)
                              ? 'bg-green-500'
                              : 'bg-gray-300'
                          } transition-all`}
                        />
                      </div>
                    )}
                  </React.Fragment>
                );
              })}
            </div>
          </div>

          {/* UltraThink Optimizations Summary */}
          <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4">
            <h4 className="font-semibold mb-3 flex items-center">
              <span className="mr-2">🧠</span>
              UltraThink Optimizations
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white rounded p-3">
                <div className="text-xs text-gray-500 mb-1">ML Iteration Prediction</div>
                <div className="text-2xl font-bold text-blue-600">
                  {selectedFeature.estimated_iterations || 'N/A'}
                </div>
                <div className="text-xs text-gray-500">predicted iterations</div>
              </div>
              <div className="bg-white rounded p-3">
                <div className="text-xs text-gray-500 mb-1">Optimal Agent</div>
                <div className="text-2xl font-bold text-green-600 capitalize">
                  {selectedFeature.optimal_agent || 'N/A'}
                </div>
                <div className="text-xs text-gray-500">auto-selected</div>
              </div>
              <div className="bg-white rounded p-3">
                <div className="text-xs text-gray-500 mb-1">Complexity Score</div>
                <div className="text-2xl font-bold text-orange-600">
                  {selectedFeature.complexity_score?.toFixed(1) || 'N/A'}
                </div>
                <div className="text-xs text-gray-500">cyclomatic</div>
              </div>
              {selectedFeature.latent_compression && (
                <div className="bg-white rounded p-3">
                  <div className="text-xs text-gray-500 mb-1">Token Compression</div>
                  <div className="text-2xl font-bold text-purple-600">
                    {selectedFeature.latent_compression.compression_ratio.toFixed(1)}x
                  </div>
                  <div className="text-xs text-gray-500">
                    {selectedFeature.latent_compression.original_tokens} →{' '}
                    {selectedFeature.latent_compression.compressed_tokens}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="mt-6 flex space-x-3">
            <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
              Continue to Next Phase
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 transition">
              View Artifacts
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 transition">
              Export Spec
            </button>
          </div>
        </div>
      )}

      {/* Create Feature Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-bold mb-4">Create New Feature</h3>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Feature ID
                </label>
                <input
                  type="text"
                  value={newFeature.feature_id}
                  onChange={(e) =>
                    setNewFeature({ ...newFeature, feature_id: e.target.value })
                  }
                  placeholder="e.g., user-authentication"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={newFeature.name}
                  onChange={(e) => setNewFeature({ ...newFeature, name: e.target.value })}
                  placeholder="e.g., User Authentication System"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={newFeature.description}
                  onChange={(e) =>
                    setNewFeature({ ...newFeature, description: e.target.value })
                  }
                  placeholder="Describe the feature and its purpose..."
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <div className="text-sm font-medium text-blue-900 mb-1">
                  🧠 UltraThink Analysis
                </div>
                <div className="text-xs text-blue-700">
                  Upon creation, ML models will automatically analyze complexity, predict optimal
                  iteration count, and select the best AI agent for this feature.
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end space-x-3">
              <button
                onClick={() => setShowCreateModal(false)}
                className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 transition"
              >
                Cancel
              </button>
              <button
                onClick={createFeature}
                disabled={!newFeature.feature_id || !newFeature.name || loading}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Creating...' : 'Create Feature'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
