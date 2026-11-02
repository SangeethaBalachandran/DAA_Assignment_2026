import React, { useState, useEffect, useRef } from 'react';
import {
  NetworkMetrics,
  SimulationStatus,
  LiveTelemetryPacket,
  OneHourProjection
} from '../types';
import { api } from '../services/api';
import {
  Play,
  Pause,
  RotateCcw,
  Wifi,
  WifiOff,
  Calendar
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

interface LiveNetworkViewProps {
  initialMetrics?: NetworkMetrics;
}

export const LiveNetworkView: React.FC<LiveNetworkViewProps> = ({
  initialMetrics
}) => {
  const [metrics, setMetrics] = useState<NetworkMetrics | undefined>(initialMetrics);
  const [status, setStatus] = useState<SimulationStatus>({
    is_running: false,
    is_paused: false,
    messages_transmitted: 0,
    cumulative_original_bits: 0,
    cumulative_compressed_bits: 0,
    cumulative_bits_saved: 0,
    current_bitrate_bps: 0,
    elapsed_seconds: 0,
    simulated_duration: "00:00"
  });

  const [packets, setPackets] = useState<LiveTelemetryPacket[]>([]);
  const [throughputHistory, setThroughputHistory] = useState<any[]>([]);
  const [wsConnected, setWsConnected] = useState<boolean>(false);
  const [projection, setProjection] = useState<OneHourProjection | null>(null);
  const [showProjectionModal, setShowProjectionModal] = useState<boolean>(false);

  const [rateConfig, setRateConfig] = useState<number>(40);
  const [seedConfig, setSeedConfig] = useState<string>("");
  const [profileConfig, setProfileConfig] = useState<string>("dynamic");

  const wsRef = useRef<WebSocket | null>(null);

  // Establish WebSocket connection
  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/telemetry`;

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      setWsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'TELEMETRY_UPDATE') {
          if (data.status) setStatus(data.status);
          if (data.metrics) setMetrics(data.metrics);
          if (data.packets && data.packets.length > 0) {
            setPackets(prev => [...data.packets.slice(-10), ...prev].slice(0, 50));

            // Append to throughput chart
            const lastPkt = data.packets[data.packets.length - 1];
            setThroughputHistory(prev => {
              const newEntry = {
                time: new Date(lastPkt.timestamp * 1000).toLocaleTimeString([], { hour12: false, minute: '2-digit', second: '2-digit' }),
                original_bps: data.metrics?.original_bitrate || 120,
                compressed_bps: data.metrics?.compressed_bitrate || 88,
                saved_bps: data.metrics?.bandwidth_saved_bps || 32
              };
              return [...prev.slice(-30), newEntry];
            });
          }
        }
      } catch (err) {
        console.error("WS Parse error:", err);
      }
    };

    ws.onclose = () => {
      setWsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, []);

  const handleStart = async () => {
    await api.startSimulation();
    const st = await api.getSimulationStatus();
    setStatus(st);
  };

  const handlePause = async () => {
    await api.pauseSimulation();
    const st = await api.getSimulationStatus();
    setStatus(st);
  };

  const handleResume = async () => {
    await api.resumeSimulation();
    const st = await api.getSimulationStatus();
    setStatus(st);
  };

  const handleReset = async () => {
    await api.resetSimulation();
    const st = await api.getSimulationStatus();
    setStatus(st);
    setPackets([]);
    setThroughputHistory([]);
  };

  const handleApplyConfig = async () => {
    const updated = await api.configureTelemetry({
      message_rate: rateConfig,
      random_seed: seedConfig ? parseInt(seedConfig) : null,
      traffic_profile: profileConfig
    });
    setMetrics(updated);
  };

  const handleRunOneHour = async () => {
    const proj = await api.getOneHourProjection();
    setProjection(proj);
    setShowProjectionModal(true);
  };

  return (
    <div className="space-y-6">
      {/* SECTION HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-[#F8FAFC] tracking-tight">
            Live Telemetry & Network Dashboard
          </h2>
          <p className="text-xs text-[#94A3B8]">
            Real-time telemetry stream simulation over 9.6 kbps narrowband physical link
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className={`px-2.5 py-1 text-xs font-semibold rounded-lg flex items-center gap-1.5 border ${
            wsConnected
              ? 'bg-[#10B981]/15 text-[#10B981] border-[#10B981]/30'
              : 'bg-[#EF4444]/15 text-[#EF4444] border-[#EF4444]/30'
          }`}>
            {wsConnected ? <Wifi className="w-3.5 h-3.5" /> : <WifiOff className="w-3.5 h-3.5" />}
            {wsConnected ? "WebSocket Connected" : "Connecting..."}
          </div>

          <button
            onClick={handleRunOneHour}
            className="px-3 py-1.5 bg-[#06B6D4]/15 hover:bg-[#06B6D4]/25 text-[#06B6D4] text-xs font-semibold rounded-xl border border-[#06B6D4]/30 transition-colors flex items-center gap-1.5 shadow-2xs cursor-pointer"
          >
            <Calendar className="w-3.5 h-3.5" /> 1-Hour Simulation Projection
          </button>
        </div>
      </div>

      {/* CONTROLS & TELEMETRY CONFIG */}
      <div className="bg-[#141922] p-5 rounded-2xl border border-[#273244] shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          {/* SIMULATION CONTROL BUTTONS */}
          <div className="flex items-center gap-2">
            {!status.is_running ? (
              <button
                onClick={handleStart}
                className="px-4 py-2 bg-[#06B6D4] hover:bg-[#0891B2] text-[#090C12] text-xs font-bold rounded-xl transition-all flex items-center gap-1.5 shadow-xs cursor-pointer"
              >
                <Play className="w-3.5 h-3.5 fill-current" /> Start Simulation
              </button>
            ) : status.is_paused ? (
              <button
                onClick={handleResume}
                className="px-4 py-2 bg-[#06B6D4] hover:bg-[#0891B2] text-[#090C12] text-xs font-bold rounded-xl transition-all flex items-center gap-1.5 shadow-xs cursor-pointer"
              >
                <Play className="w-3.5 h-3.5 fill-current" /> Resume
              </button>
            ) : (
              <button
                onClick={handlePause}
                className="px-4 py-2 bg-[#F59E0B] hover:bg-[#D97706] text-[#090C12] text-xs font-bold rounded-xl transition-all flex items-center gap-1.5 shadow-xs cursor-pointer"
              >
                <Pause className="w-3.5 h-3.5 fill-current" /> Pause
              </button>
            )}

            <button
              onClick={handleReset}
              className="px-3.5 py-2 bg-[#090C12] hover:bg-[#1E293B] text-[#94A3B8] border border-[#273244] text-xs font-semibold rounded-xl transition-all flex items-center gap-1.5 cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" /> Reset
            </button>

            <div className="ml-2 px-3 py-1.5 bg-[#090C12] border border-[#273244] rounded-xl text-xs font-mono text-[#94A3B8]">
              Elapsed: <strong className="text-[#F8FAFC]">{status.simulated_duration}</strong>
            </div>
          </div>

          {/* PARAMETER CONTROLS */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-1.5 text-xs">
              <span className="text-[#94A3B8] font-medium">Profile:</span>
              <select
                value={profileConfig}
                onChange={(e) => {
                  setProfileConfig(e.target.value);
                  api.configureTelemetry({
                    message_rate: rateConfig,
                    random_seed: seedConfig ? parseInt(seedConfig) : null,
                    traffic_profile: e.target.value
                  }).then(setMetrics);
                }}
                className="px-2 py-1 bg-[#090C12] border border-[#273244] rounded-lg font-mono text-xs text-[#06B6D4] cursor-pointer"
              >
                <option value="dynamic">Dynamic Drift</option>
                <option value="normal">Normal (52% OK)</option>
                <option value="high_temp">High Temp Warning</option>
                <option value="high_vib">High Vibration Alert</option>
                <option value="fault_heavy">Fault Crisis</option>
              </select>
            </div>

            <div className="flex items-center gap-1.5 text-xs">
              <span className="text-[#94A3B8] font-medium">Aggregate Rate:</span>
              <input
                type="number"
                min="1"
                max="200"
                value={rateConfig}
                onChange={(e) => setRateConfig(parseInt(e.target.value) || 40)}
                className="w-16 px-2 py-1 bg-[#090C12] border border-[#273244] rounded-lg font-mono text-xs text-center font-bold text-[#06B6D4]"
              />
              <span className="text-[#64748B]">msgs/s</span>
            </div>

            <div className="flex items-center gap-1.5 text-xs">
              <span className="text-[#94A3B8] font-medium">Seed:</span>
              <input
                type="text"
                placeholder="None"
                value={seedConfig}
                onChange={(e) => setSeedConfig(e.target.value)}
                className="w-16 px-2 py-1 bg-[#090C12] border border-[#273244] rounded-lg font-mono text-xs text-center text-[#F8FAFC]"
              />
            </div>

            <button
              onClick={handleApplyConfig}
              className="px-3 py-1 bg-[#0E3A43] hover:bg-[#155e75] text-[#06B6D4] text-xs font-semibold rounded-lg border border-[#06B6D4]/30 transition-colors cursor-pointer"
            >
              Apply
            </button>
          </div>
        </div>
      </div>

      {/* METRIC STRIP */}
      {metrics && (
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
          <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
            <span className="text-xs text-[#94A3B8]">Messages Transmitted</span>
            <div className="text-xl font-bold font-mono text-[#F8FAFC] mt-1">
              {status.messages_transmitted.toLocaleString()}
            </div>
            <span className="text-[10px] text-[#64748B]">Target: {metrics.message_rate} msgs/s</span>
          </div>

          <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
            <span className="text-xs text-[#94A3B8]">Original Bitrate</span>
            <div className="text-xl font-bold font-mono text-[#F8FAFC] mt-1">
              {metrics.original_bitrate} <span className="text-xs font-sans text-[#94A3B8]">bps</span>
            </div>
            <span className="text-[10px] text-[#64748B]">3-bit fixed word</span>
          </div>

          <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
            <span className="text-xs text-[#94A3B8]">Compressed Bitrate</span>
            <div className="text-xl font-bold font-mono text-[#10B981] mt-1">
              {metrics.compressed_bitrate} <span className="text-xs font-sans text-[#94A3B8]">bps</span>
            </div>
            <span className="text-[10px] text-[#10B981] font-medium">{metrics.percentage_savings.toFixed(2)}% savings</span>
          </div>

          <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
            <span className="text-xs text-[#94A3B8]">Cumulative Bits Freed</span>
            <div className="text-xl font-bold font-mono text-[#06B6D4] mt-1">
              {status.cumulative_bits_saved.toLocaleString()} <span className="text-xs font-sans text-[#94A3B8]">b</span>
            </div>
            <span className="text-[10px] text-[#64748B]">{(status.cumulative_bits_saved / 8).toFixed(1)} Bytes saved</span>
          </div>

          <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
            <span className="text-xs text-[#94A3B8]">Link Utilization</span>
            <div className="text-xl font-bold font-mono text-[#F8FAFC] mt-1">
              {metrics.compressed_utilization_pct}%
            </div>
            <span className="text-[10px] text-[#10B981] font-semibold">Status: {metrics.congestion_status}</span>
          </div>
        </div>
      )}

      {/* THROUGHPUT LIVE CHART */}
      <div className="bg-[#141922] p-5 rounded-2xl border border-[#273244] shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-[#273244]">
          <div>
            <h3 className="text-sm font-bold text-[#F8FAFC]">Real-Time Channel Throughput</h3>
            <p className="text-xs text-[#94A3B8]">Original vs Compressed traffic bitrate over the 9.6 kbps physical carrier</p>
          </div>
          <span className="text-xs font-mono font-semibold text-[#10B981] bg-[#10B981]/15 px-2 py-0.5 rounded border border-[#10B981]/30">
            Headroom: {metrics?.available_capacity_bps || 9508} bps
          </span>
        </div>

        <div className="h-64 w-full">
          {throughputHistory.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={throughputHistory} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorOrig" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#94a3b8" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorComp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.5}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.05}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#273244" />
                <XAxis dataKey="time" stroke="#64748B" />
                <YAxis domain={[0, 'auto']} stroke="#64748B" label={{ value: 'Bitrate (bps)', angle: -90, position: 'insideLeft', fill: '#94A3B8' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#090C12', borderColor: '#273244', borderRadius: '12px', color: '#F8FAFC' }}
                />
                <Legend wrapperStyle={{ color: '#94A3B8' }} />
                <Area type="monotone" dataKey="original_bps" name="Original Bitrate (bps)" stroke="#94a3b8" fillOpacity={1} fill="url(#colorOrig)" />
                <Area type="monotone" dataKey="compressed_bps" name="Compressed Bitrate (bps)" stroke="#10b981" fillOpacity={1} fill="url(#colorComp)" />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center bg-[#090C12] rounded-xl text-[#64748B] text-xs italic border border-[#273244]">
              Press "Start Simulation" to stream real-time throughput metrics.
            </div>
          )}
        </div>
      </div>

      {/* RECENT PACKET STREAM TABLE */}
      <div className="bg-[#141922] p-5 rounded-2xl border border-[#273244] shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-[#273244]">
          <div>
            <h3 className="text-sm font-bold text-[#F8FAFC]">Incoming Telemetry Packet Stream</h3>
            <p className="text-xs text-[#94A3B8]">Live burst inspection sampled according to empirical distribution</p>
          </div>
          <span className="text-xs text-[#94A3B8] font-mono">Showing last 50 packets</span>
        </div>

        <div className="overflow-x-auto max-h-64 overflow-y-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="sticky top-0 bg-[#090C12]">
              <tr className="border-b border-[#273244] text-[#94A3B8] font-sans font-semibold uppercase text-[10px]">
                <th className="py-2 px-3">Seq #</th>
                <th className="py-2 px-3">Sensor ID</th>
                <th className="py-2 px-3">Symbol</th>
                <th className="py-2 px-3">Codeword</th>
                <th className="py-2 px-3">Orig Bits</th>
                <th className="py-2 px-3">Comp Bits</th>
                <th className="py-2 px-3">Instant Load</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#273244]/60">
              {packets.length > 0 ? (
                packets.map((pkt) => (
                  <tr key={pkt.sequence_id} className="hover:bg-[#1E293B]/40">
                    <td className="py-1.5 px-3 text-[#64748B]">#{pkt.sequence_id}</td>
                    <td className="py-1.5 px-3 font-semibold text-[#94A3B8]">Sensor-{pkt.sensor_id}</td>
                    <td className="py-1.5 px-3 font-bold text-[#F8FAFC]">{pkt.symbol}</td>
                    <td className="py-1.5 px-3">
                      <span className="px-1.5 py-0.5 bg-[#06B6D4]/15 text-[#06B6D4] font-bold rounded border border-[#06B6D4]/30">
                        {pkt.codeword}
                      </span>
                    </td>
                    <td className="py-1.5 px-3 text-[#64748B]">3 b</td>
                    <td className="py-1.5 px-3 font-bold text-[#10B981]">{pkt.compressed_bits} b</td>
                    <td className="py-1.5 px-3 text-[#94A3B8]">{pkt.channel_load_bps} bps</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-[#64748B] font-sans italic">
                    Simulation paused or inactive. Press "Start Simulation" above.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* 1-HOUR SIMULATION MODAL */}
      {showProjectionModal && projection && (
        <div className="fixed inset-0 z-50 bg-[#090C12]/80 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-[#141922] rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-[#273244] space-y-5 animate-in fade-in zoom-in-95 duration-150 text-[#F8FAFC]">
            <div className="flex items-center justify-between pb-3 border-b border-[#273244]">
              <div className="flex items-center gap-2">
                <Calendar className="w-5 h-5 text-[#06B6D4]" />
                <h3 className="text-base font-bold text-[#F8FAFC]">1-Hour Network Projection</h3>
              </div>
              <button
                onClick={() => setShowProjectionModal(false)}
                className="text-[#94A3B8] hover:text-[#F8FAFC] font-bold text-lg cursor-pointer"
              >
                &times;
              </button>
            </div>

            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Calculates the cumulative telemetry transmission across a full 1-hour window (3,600 seconds) at the aggregate rate of 40 messages per second.
            </p>

            <div className="space-y-3 font-mono text-xs">
              <div className="p-3 bg-[#090C12] border border-[#273244] rounded-xl flex justify-between">
                <span className="text-[#94A3B8] font-sans">Total Transmitted Messages:</span>
                <strong className="text-[#F8FAFC]">{projection.total_messages.toLocaleString()} msgs</strong>
              </div>

              <div className="p-3 bg-[#090C12] border border-[#273244] rounded-xl flex justify-between">
                <span className="text-[#94A3B8] font-sans">Legacy Uncompressed Volume:</span>
                <strong className="text-[#F8FAFC]">{projection.original_bits.toLocaleString()} bits ({projection.original_bytes.toLocaleString()} B)</strong>
              </div>

              <div className="p-3 bg-[#10B981]/15 border border-[#10B981]/30 rounded-xl flex justify-between text-[#10B981]">
                <span className="font-sans">Package-Merge (L&le;4) Volume:</span>
                <strong>{projection.package_merge_bits.toLocaleString()} bits ({projection.package_merge_bytes.toLocaleString()} B)</strong>
              </div>

              <div className="p-3 bg-[#10B981]/25 border border-[#10B981]/40 rounded-xl flex justify-between text-[#10B981] font-bold">
                <span className="font-sans">Bandwidth Freed per Hour:</span>
                <span>+{projection.package_merge_bits_saved.toLocaleString()} bits ({projection.package_merge_savings_pct}%)</span>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setShowProjectionModal(false)}
                className="px-4 py-2 bg-[#06B6D4] hover:bg-[#0891B2] text-[#090C12] font-bold text-xs rounded-xl cursor-pointer"
              >
                Close Projection
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
