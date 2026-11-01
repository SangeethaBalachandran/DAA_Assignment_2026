export interface SymbolFrequency {
  symbol: string;
  frequency: number;
}

export interface CodebookEntry {
  symbol: string;
  frequency: number;
  probability: number;
  codeword: string;
  length: number;
  register_compatible: boolean;
}

export interface TreeNode {
  id: string;
  name: string;
  weight: number;
  symbol?: string;
  code?: string;
  bit?: string;
  depth: number;
  children?: TreeNode[];
}

export interface CompressionResponse {
  algorithm: string;
  codebook: CodebookEntry[];
  codebook_map: Record<string, string>;
  tree?: TreeNode;
  average_length: number;
  entropy: number;
  efficiency: number;
  redundancy: number;
  compression_ratio: number;
  bandwidth_savings_pct: number;
  kraft_sum: number;
  max_codeword_length: number;
  hardware_compatible: boolean;
  operations_count: number;
  execution_time_ms: number;
}

export interface TwoQueueStep {
  step_number: number;
  q1_before: string[];
  q2_before: string[];
  popped: string[];
  merged_weight: number;
  result_node: string;
  description: string;
}

export interface TwoQueueResponse extends CompressionResponse {
  steps: TwoQueueStep[];
}

export interface AlgorithmComparisonResponse {
  huffman: CompressionResponse;
  shannon_fano: CompressionResponse;
  two_queue: CompressionResponse;
  is_counterexample: boolean;
  length_difference: number;
  explanation: string;
}

export interface NetworkMetrics {
  message_rate: number;
  channel_capacity: number;
  original_bitrate: number;
  compressed_bitrate: number;
  bandwidth_saved_bps: number;
  bandwidth_saved_bph: number;
  original_utilization_pct: number;
  compressed_utilization_pct: number;
  percentage_savings: number;
  available_capacity_bps: number;
  congestion_status: 'OPTIMAL' | 'CONGESTED' | 'CRITICAL';
  overhead_framing_bps: number;
  overhead_broadcast_bps: number;
}

export interface SimulationStatus {
  is_running: boolean;
  is_paused: boolean;
  messages_transmitted: number;
  cumulative_original_bits: number;
  cumulative_compressed_bits: number;
  cumulative_bits_saved: number;
  current_bitrate_bps: number;
  elapsed_seconds: number;
  simulated_duration: string;
}

export interface LiveTelemetryPacket {
  timestamp: number;
  sequence_id: number;
  sensor_id: number;
  symbol: string;
  original_bits: number;
  codeword: string;
  compressed_bits: number;
  channel_load_bps: number;
  utilization_pct: number;
  value?: number;
}

export interface ReceiverStatus {
  receiver_id: number;
  synchronized: boolean;
  current_version: string;
  latency_ms: number;
  retries: number;
}

export interface CodebookBroadcastResponse {
  version: string;
  algorithm: string;
  broadcast_timestamp: number;
  payload_bits: number;
  framing_bits: number;
  total_broadcast_bits: number;
  amortized_bps: number;
  receivers_total: number;
  receivers_acked: number;
  receivers_failed: number;
  sync_percentage: number;
  sample_receivers: ReceiverStatus[];
}

export interface OneHourProjection {
  duration_hours: number;
  total_messages: number;
  original_bits: number;
  original_bytes: number;
  huffman_bits: number;
  huffman_bytes: number;
  huffman_bits_saved: number;
  huffman_savings_pct: number;
  package_merge_bits: number;
  package_merge_bytes: number;
  package_merge_bits_saved: number;
  package_merge_savings_pct: number;
  hardware_compatible_savings_pct: number;
  channel_capacity_bph: number;
}

export interface BenchmarkResult {
  alphabet_size: number;
  min_heap_time_ms: number;
  two_queue_time_ms: number;
  min_heap_ops: number;
  two_queue_ops: number;
  huffman_avg_len: number;
  two_queue_avg_len: number;
  costs_equivalent: boolean;
  speedup_factor: number;
}

