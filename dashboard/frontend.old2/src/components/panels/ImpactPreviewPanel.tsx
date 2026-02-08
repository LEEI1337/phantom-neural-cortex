import React, { useState } from 'react';
import { Card } from '../ui/card';

interface ImpactOption {
    priority: string;
    selected_agent: string;
    est_cost: number;
    est_speed: number;
    est_quality: number;
    token_efficiency: number;
}

interface ImpactReport {
    task_id: string;
    options: ImpactOption[];
    recommendation: string;
    overall_savings_potential: number;
}

const ImpactPreviewPanel: React.FC = () => {
    const [description, setDescription] = useState('');
    const [report, setReport] = useState<ImpactReport | null>(null);
    const [loading, setLoading] = useState(false);

    const fetchPreview = async () => {
        if (!description) return;
        setLoading(true);
        try {
            const response = await fetch('http://localhost:1336/api/swarm/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description })
            });
            const data = await response.json();
            setReport(data);
        } catch (error) {
            console.error('Failed to fetch impact preview:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-4 p-4 text-white">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-cyan-400">Impact Analysis (Phase 6)</h3>
                <div className="text-xs px-2 py-1 bg-cyan-900/50 rounded border border-cyan-700">DRY RUN MODE</div>
            </div>

            <div className="space-y-2">
                <div className="text-sm font-medium text-gray-400">Describe your task:</div>
                <textarea
                    className="w-full h-24 bg-slate-900 border border-slate-700 rounded p-2 text-sm focus:border-cyan-500 outline-none transition-colors"
                    placeholder="e.g. Implement a secure payment gateway with Stripe integration..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
                <button
                    onClick={fetchPreview}
                    disabled={loading || !description}
                    className="w-full py-2 bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 disabled:cursor-not-allowed rounded font-bold transition-all"
                >
                    {loading ? 'Simulating...' : 'Predict Impact 🚀'}
                </button>
            </div>

            {report && (
                <div className="mt-6 space-y-4">
                    <div className="p-3 bg-cyan-950/30 border border-cyan-800 rounded-lg">
                        <div className="text-xs text-cyan-400 font-bold mb-1">AI RECOMMENDATION</div>
                        <p className="text-sm italic text-gray-200">{report.recommendation}</p>
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                        {report.options.map((opt) => (
                            <Card key={opt.priority} className={`p-3 bg-slate-900/80 border-2 ${opt.priority === 'balanced' ? 'border-cyan-500' : 'border-slate-800'}`}>
                                <div className="flex justify-between items-start mb-2">
                                    <span className="text-[10px] font-bold uppercase tracking-wider px-1 bg-slate-800 rounded">{opt.priority}</span>
                                    <span className="text-xs text-gray-400">${opt.est_cost.toFixed(3)}</span>
                                </div>
                                <div className="text-sm font-bold truncate mb-1">{opt.selected_agent}</div>
                                <div className="w-full bg-slate-800 h-1 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-cyan-500"
                                        style={{ width: `${opt.est_quality * 100}%` }}
                                    />
                                </div>
                                <div className="flex justify-between mt-1 text-[10px] text-gray-500">
                                    <span>Quality: {(opt.est_quality * 100).toFixed(0)}%</span>
                                    <span>{opt.est_speed.toFixed(0)}s</span>
                                </div>
                            </Card>
                        ))}
                    </div>

                    <div className="flex items-center gap-3 p-3 bg-green-900/20 border border-green-900/50 rounded-lg">
                        <div className="text-2xl">💰</div>
                        <div>
                            <div className="text-sm font-bold text-green-400">Total Savings Potential</div>
                            <div className="text-lg font-black text-white">{report.overall_savings_potential.toFixed(1)}% efficiency gain</div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ImpactPreviewPanel;
