import React, { useState, useEffect } from 'react';
import {
  SymbolFrequency,
  TwoQueueResponse,
  AlgorithmComparisonResponse,
  BenchmarkResult
} from '../types';
import { api } from '../services/api';
import { TreeVisualizer } from '../components/TreeVisualizer';
import { TwoQueueStepper } from '../components/TwoQueueStepper';
import {
  GitCompare,
  Layers,
  BarChart3,
  Sparkles,
  CheckCircle2
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface AlgorithmLabViewProps {
  frequencies: SymbolFrequency[];
  comparisonData?: AlgorithmComparisonResponse;
  twoQueueData?: TwoQueueResponse;
  onLoadFrequencies: (freqs: SymbolFrequency[]) => void;
}

export const AlgorithmLabView: React.FC<AlgorithmLabViewProps> = ({
  comparisonData,
  twoQueueData,
  onLoadFrequencies
}) => {
  const [activeTab, setActiveTab] = useState<'comparison' | 'two-queue' | 'benchmark'>('comparison');
  const [benchmarks, setBenchmarks] = useState<BenchmarkResult[]>([]);
  const [loadingBenchmark, setLoadingBenchmark] = useState(false);

  useEffect(() => {
    if (activeTab === 'benchmark' && benchmarks.length === 0) {
      loadBenchmarks();
    }
  }, [activeTab]);

  const loadBenchmarks = async () => {
    try {
      setLoadingBenchmark(true);
      const data = await api.getBenchmarks();
      setBenchmarks(data);
    } catch (err) {
      console.error("Benchmark load error:", err);
    } finally {
      setLoadingBenchmark(false);
    }
  };

  const handleLoadCounterexample = async (variant: '5-symbol' | '8-symbol') => {
    try {
      const res = await api.getCounterexample(variant);
      onLoadFrequencies(res.distribution);
    } catch (err) {
      console.error("Failed to load counterexample:", err);
    }
  };

  return (
    <div className="space-y-6">
      {/* HEADER & TAB SELECTOR */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-[#F8FAFC] tracking-tight">
            Algorithm Laboratory
          </h2>
          <p className="text-xs text-[#94A3B8]">
            Comparative analysis of Huffman, Shannon-Fano, and Two-Queue linear-time construction
          </p>
        </div>
        <div className="flex items-center gap-1.5 p-1 bg-[#090C12] rounded-xl border border-[#273244]">
          <button
            onClick={() => setActiveTab('comparison')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 cursor-pointer ${
              activeTab === 'comparison'
                ? 'bg-[#0E3A43] text-[#06B6D4] shadow-xs'
                : 'text-[#94A3B8] hover:text-[#F8FAFC]'
            }`}
          >
            <GitCompare className="w-3.5 h-3.5" /> Huffman vs Shannon-Fano
          </button>
          <button
            onClick={() => setActiveTab('two-queue')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 cursor-pointer ${
              activeTab === 'two-queue'
                ? 'bg-[#0E3A43] text-[#06B6D4] shadow-xs'
                : 'text-[#94A3B8] hover:text-[#F8FAFC]'
            }`}
          >
            <Layers className="w-3.5 h-3.5" /> Two-Queue Animation (O(N))
          </button>
          <button
            onClick={() => setActiveTab('benchmark')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 cursor-pointer ${
              activeTab === 'benchmark'
                ? 'bg-[#0E3A43] text-[#06B6D4] shadow-xs'
                : 'text-[#94A3B8] hover:text-[#F8FAFC]'
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5" /> Empirical Benchmarks
          </button>
        </div>
      </div>

      {/* TAB 1: COMPARISON */}
      {activeTab === 'comparison' && comparisonData && (
        <div className="space-y-6">
          {/* COUNTEREXAMPLE ACTION BANNER */}
          <div className={`p-5 rounded-2xl border transition-all ${
            comparisonData.is_counterexample
              ? 'bg-[#451A03]/30 border-[#F59E0B]/50 text-[#F8FAFC]'
              : 'bg-[#141922] border-[#273244] text-[#F8FAFC] shadow-sm'
          }`}>
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                    comparisonData.is_counterexample
                      ? 'bg-[#F59E0B]/20 text-[#F59E0B] border border-[#F59E0B]/40'
                      : 'bg-[#10B981]/20 text-[#10B981] border border-[#10B981]/40'
                  }`}>
                    {comparisonData.is_counterexample ? "STRICT SUBOPTIMALITY DETECTED" : "COINCIDENTAL EQUALITY"}
                  </span>
                  <span className="text-xs text-[#94A3B8] font-mono">
                    Δ = {comparisonData.length_difference > 0 ? `+${comparisonData.length_difference.toFixed(4)}` : '0.0000'} bits/msg
                  </span>
                </div>
                <p className="text-xs text-[#94A3B8] leading-relaxed max-w-3xl">
                  {comparisonData.explanation}
                </p>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => handleLoadCounterexample('8-symbol')}
                  className="px-3 py-2 bg-[#F59E0B] hover:bg-[#D97706] text-[#090C12] font-bold text-xs rounded-xl transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer"
                >
                  <Sparkles className="w-3.5 h-3.5" /> Load 8-Symbol IoT Counterexample
                </button>
                <button
                  onClick={() => handleLoadCounterexample('5-symbol')}
                  className="px-3 py-2 bg-[#090C12] hover:bg-[#1E293B] text-[#F8FAFC] border border-[#273244] font-medium text-xs rounded-xl transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer"
                >
                  Load Classic 5-Symbol Case
                </button>
              </div>
            </div>
          </div>

          {/* STAT COMPARISON CARDS */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
              <span className="text-xs text-[#94A3B8]">Huffman Avg Length</span>
              <div className="text-xl font-bold font-mono text-[#10B981] mt-1">
                {comparisonData.huffman.average_length.toFixed(4)} b
              </div>
              <span className="text-[10px] text-[#64748B]">Optimal (Bottom-Up)</span>
            </div>

            <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
              <span className="text-xs text-[#94A3B8]">Shannon-Fano Avg Length</span>
              <div className={`text-xl font-bold font-mono mt-1 ${
                comparisonData.is_counterexample ? 'text-[#F59E0B]' : 'text-[#F8FAFC]'
              }`}>
                {comparisonData.shannon_fano.average_length.toFixed(4)} b
              </div>
              <span className="text-[10px] text-[#64748B]">Heuristic (Top-Down)</span>
            </div>

            <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
              <span className="text-xs text-[#94A3B8]">Huffman Efficiency</span>
              <div className="text-xl font-bold font-mono text-[#06B6D4] mt-1">
                {comparisonData.huffman.efficiency.toFixed(2)}%
              </div>
              <span className="text-[10px] text-[#64748B]">H(X) / L_Huff</span>
            </div>

            <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
              <span className="text-xs text-[#94A3B8]">Shannon-Fano Efficiency</span>
              <div className="text-xl font-bold font-mono text-[#F8FAFC] mt-1">
                {comparisonData.shannon_fano.efficiency.toFixed(2)}%
              </div>
              <span className="text-[10px] text-[#64748B]">H(X) / L_SF</span>
            </div>
          </div>

          {/* SIDE-BY-SIDE TREE VISUALIZATIONS */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <TreeVisualizer
              treeData={comparisonData.huffman.tree}
              title="Huffman Binary Tree"
              algorithmName="Min-Heap (Optimal)"
            />
            <TreeVisualizer
              treeData={comparisonData.shannon_fano.tree}
              title="Shannon-Fano Binary Tree"
              algorithmName="Shannon-Fano (Bipartition)"
            />
          </div>

          {/* CODEBOOK COMPARISON TABLE */}
          <div className="bg-[#141922] rounded-2xl border border-[#273244] p-5 shadow-sm space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-[#273244]">
              <h3 className="text-sm font-bold text-[#F8FAFC]">Direct Codebook Comparison</h3>
              <span className="text-xs text-[#94A3B8]">Sorted by empirical frequency</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead>
                  <tr className="border-b border-[#273244] text-[#94A3B8] font-sans font-semibold uppercase text-[10px]">
                    <th className="py-2.5 px-3">Symbol</th>
                    <th className="py-2.5 px-3">Weight</th>
                    <th className="py-2.5 px-3">Huffman Codeword</th>
                    <th className="py-2.5 px-3">Huffman Length</th>
                    <th className="py-2.5 px-3">SF Codeword</th>
                    <th className="py-2.5 px-3">SF Length</th>
                    <th className="py-2.5 px-3 font-sans">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#273244]/60">
                  {comparisonData.huffman.codebook.map((hEntry, i) => {
                    const sfEntry = comparisonData.shannon_fano.codebook[i];
                    const diff = sfEntry.length - hEntry.length;
                    return (
                      <tr key={hEntry.symbol} className="hover:bg-[#1E293B]/40 transition-colors">
                        <td className="py-2.5 px-3 font-bold text-[#F8FAFC]">{hEntry.symbol}</td>
                        <td className="py-2.5 px-3 text-[#94A3B8]">{hEntry.frequency}</td>
                        <td className="py-2.5 px-3">
                          <span className="px-2 py-0.5 bg-[#10B981]/15 text-[#10B981] rounded font-bold border border-[#10B981]/30">
                            {hEntry.codeword}
                          </span>
                        </td>
                        <td className="py-2.5 px-3 font-semibold text-[#F8FAFC]">{hEntry.length} b</td>
                        <td className="py-2.5 px-3">
                          <span className="px-2 py-0.5 bg-[#06B6D4]/15 text-[#06B6D4] rounded font-bold border border-[#06B6D4]/30">
                            {sfEntry?.codeword}
                          </span>
                        </td>
                        <td className="py-2.5 px-3 font-semibold text-[#F8FAFC]">{sfEntry?.length} b</td>
                        <td className="py-2.5 px-3 font-sans">
                          {diff === 0 ? (
                            <span className="text-[#64748B] text-[11px]">Equal</span>
                          ) : diff > 0 ? (
                            <span className="text-[#F59E0B] font-bold text-[11px]">SF +{diff} bit longer</span>
                          ) : (
                            <span className="text-[#10B981] font-bold text-[11px]">SF {diff} bit shorter</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: TWO-QUEUE ANIMATION */}
      {activeTab === 'two-queue' && twoQueueData && comparisonData && (
        <TwoQueueStepper
          steps={twoQueueData.steps}
          huffmanOps={comparisonData.huffman.operations_count}
          twoQueueOps={twoQueueData.operations_count}
        />
      )}

      {/* TAB 3: BENCHMARK */}
      {activeTab === 'benchmark' && (
        <div className="bg-[#141922] rounded-2xl border border-[#273244] p-5 shadow-sm space-y-6">
          <div className="flex items-center justify-between pb-3 border-b border-[#273244]">
            <div>
              <h3 className="text-sm font-bold text-[#F8FAFC]">Empirical Complexity & Runtime Benchmark</h3>
              <p className="text-xs text-[#94A3B8]">
                Measured execution time and operation counts comparing Min-Heap (O(N log N)) vs Two-Queue (O(N))
              </p>
            </div>
            <button
              onClick={loadBenchmarks}
              disabled={loadingBenchmark}
              className="px-3 py-1.5 text-xs font-semibold bg-[#06B6D4]/15 text-[#06B6D4] hover:bg-[#06B6D4]/25 rounded-lg border border-[#06B6D4]/30 transition-colors cursor-pointer"
            >
              {loadingBenchmark ? "Running Real Tests..." : "Re-Run Benchmarks"}
            </button>
          </div>

          {benchmarks.length > 0 && (
            <div className="space-y-6">
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={benchmarks} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#273244" />
                    <XAxis dataKey="alphabet_size" stroke="#64748B" label={{ value: 'Alphabet Size (N)', position: 'insideBottom', offset: -5, fill: '#94A3B8' }} />
                    <YAxis stroke="#64748B" label={{ value: 'Runtime (ms)', angle: -90, position: 'insideLeft', fill: '#94A3B8' }} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#090C12', borderColor: '#273244', borderRadius: '12px', color: '#F8FAFC' }}
                    />
                    <Legend wrapperStyle={{ color: '#94A3B8' }} />
                    <Bar dataKey="min_heap_time_ms" name="Min-Heap O(N log N) ms" fill="#06B6D4" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="two_queue_time_ms" name="Two-Queue O(N) ms" fill="#10B981" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs font-mono">
                  <thead>
                    <tr className="border-b border-[#273244] text-[#94A3B8] font-sans font-semibold uppercase text-[10px]">
                      <th className="py-2.5 px-3">Alphabet (N)</th>
                      <th className="py-2.5 px-3">Min-Heap Time (ms)</th>
                      <th className="py-2.5 px-3">Two-Queue Time (ms)</th>
                      <th className="py-2.5 px-3">Speedup</th>
                      <th className="py-2.5 px-3">Min-Heap Ops</th>
                      <th className="py-2.5 px-3">Two-Queue Ops</th>
                      <th className="py-2.5 px-3 font-sans">Cost Equivalence</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#273244]/60">
                    {benchmarks.map((b) => (
                      <tr key={b.alphabet_size} className="hover:bg-[#1E293B]/40">
                        <td className="py-2.5 px-3 font-bold text-[#F8FAFC]">N = {b.alphabet_size}</td>
                        <td className="py-2.5 px-3 text-[#94A3B8]">{b.min_heap_time_ms} ms</td>
                        <td className="py-2.5 px-3 text-[#10B981] font-bold">{b.two_queue_time_ms} ms</td>
                        <td className="py-2.5 px-3 text-[#06B6D4] font-bold">{b.speedup_factor}x</td>
                        <td className="py-2.5 px-3 text-[#94A3B8]">{b.min_heap_ops}</td>
                        <td className="py-2.5 px-3 text-[#94A3B8]">{b.two_queue_ops}</td>
                        <td className="py-2.5 px-3 font-sans">
                          {b.costs_equivalent ? (
                            <span className="text-[#10B981] flex items-center gap-1 font-semibold text-[11px]">
                              <CheckCircle2 className="w-3.5 h-3.5" /> Exact Equivalent
                            </span>
                          ) : (
                            <span className="text-[#EF4444] font-bold text-[11px]">Mismatch</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
