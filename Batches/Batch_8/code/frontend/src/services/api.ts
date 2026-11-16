import {
  SymbolFrequency,
  CompressionResponse,
  TwoQueueResponse,
  AlgorithmComparisonResponse,
  NetworkMetrics,
  SimulationStatus,
  CodebookBroadcastResponse,
  OneHourProjection,
  BenchmarkResult
} from '../types';

const API_BASE = '/api';

export const api = {
  // Huffman
  async getDefaultHuffman(): Promise<CompressionResponse> {
    const res = await fetch(`${API_BASE}/huffman/default`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async generateHuffman(frequencies: SymbolFrequency[]): Promise<CompressionResponse> {
    const res = await fetch(`${API_BASE}/huffman/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frequencies })
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Shannon-Fano
  async generateShannonFano(frequencies: SymbolFrequency[]): Promise<CompressionResponse> {
    const res = await fetch(`${API_BASE}/shannon-fano/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frequencies })
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Two-Queue
  async generateTwoQueue(frequencies: SymbolFrequency[]): Promise<TwoQueueResponse> {
    const res = await fetch(`${API_BASE}/huffman/two-queue`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frequencies })
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Package-Merge
  async generatePackageMerge(frequencies: SymbolFrequency[], maxLength = 4): Promise<CompressionResponse> {
    const res = await fetch(`${API_BASE}/package-merge/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frequencies, max_length: maxLength })
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Comparison & Counterexample
  async compareAlgorithms(frequencies: SymbolFrequency[]): Promise<AlgorithmComparisonResponse> {
    const res = await fetch(`${API_BASE}/algorithms/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frequencies })
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getCounterexample(variant: '5-symbol' | '8-symbol' = '8-symbol'): Promise<{
    variant: string;
    distribution: SymbolFrequency[];
    comparison: AlgorithmComparisonResponse;
  }> {
    const res = await fetch(`${API_BASE}/algorithms/counterexample?variant=${variant}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getBenchmarks(): Promise<BenchmarkResult[]> {
    const res = await fetch(`${API_BASE}/algorithms/benchmark`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Encoder & Decoder
  async encode(messages: string[], codebookMap?: Record<string, string>, algorithm = 'huffman') {
    const res = await fetch(`${API_BASE}/encoder/encode`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages, codebook_map: codebookMap, algorithm })
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async decode(bitstream: string, codebookMap: Record<string, string>, codebookVersion?: string) {
    const res = await fetch(`${API_BASE}/encoder/decode`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        bitstream,
        codebook_map: codebookMap,
        codebook_version: codebookVersion
      })
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Telemetry & Network
  async getNetworkMetrics(): Promise<NetworkMetrics> {
    const res = await fetch(`${API_BASE}/telemetry/metrics`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getSimulationStatus(): Promise<SimulationStatus> {
    const res = await fetch(`${API_BASE}/telemetry/status`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async configureTelemetry(config: any): Promise<NetworkMetrics> {
    const res = await fetch(`${API_BASE}/telemetry/configure`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config)
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async startSimulation() {
    const res = await fetch(`${API_BASE}/telemetry/start`, { method: 'POST' });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async pauseSimulation() {
    const res = await fetch(`${API_BASE}/telemetry/pause`, { method: 'POST' });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async resumeSimulation() {
    const res = await fetch(`${API_BASE}/telemetry/resume`, { method: 'POST' });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async resetSimulation() {
    const res = await fetch(`${API_BASE}/telemetry/reset`, { method: 'POST' });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getOneHourProjection(): Promise<OneHourProjection> {
    const res = await fetch(`${API_BASE}/telemetry/one-hour`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  // Codebook Management
  async getCurrentCodebook() {
    const res = await fetch(`${API_BASE}/codebook/current`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async broadcastCodebook(targetVersion?: string, algorithm = 'package_merge', lossRate = 0.015): Promise<CodebookBroadcastResponse> {
    const res = await fetch(`${API_BASE}/codebook/broadcast`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_version: targetVersion,
        algorithm,
        receiver_count: 5000,
        simulated_loss_rate: lossRate
      })
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getBroadcastHistory() {
    const res = await fetch(`${API_BASE}/codebook/history`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }
};

