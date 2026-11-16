import React, { useState, useEffect } from 'react';
import { Activity } from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { LiveTelemetryPacket } from '../types';

interface LiveTelemetryFeedCardProps {
  packets: LiveTelemetryPacket[];
  isSimulating: boolean;
  originalBitrate?: number;
  compressedBitrate?: number;
  bandwidthSavedPct?: number;
}

export const LiveTelemetryFeedCard: React.FC<LiveTelemetryFeedCardProps> = ({
  packets,
  originalBitrate = 120,
  compressedBitrate = 88,
  bandwidthSavedPct = 26.67
}) => {
  // Chart history
  const [chartData, setChartData] = useState<any[]>([
    { time: '15:20', original: 120, compressed: 88, band: [88, 120], savings: 32 },
    { time: '15:21', original: 120, compressed: 88, band: [88, 120], savings: 32 },
    { time: '15:22', original: 120, compressed: 88, band: [88, 120], savings: 32 },
    { time: '15:23', original: 120, compressed: 88, band: [88, 120], savings: 32 },
    { time: '15:24', original: 120, compressed: 88, band: [88, 120], savings: 32 },
    { time: '15:25', original: 120, compressed: 88, band: [88, 120], savings: 32 },
  ]);

  // Terminal log items
  const [logItems, setLogItems] = useState<any[]>([
    { time: "15:25:13.482", json: '{"id":8427,"type":"TEMP_LO","ts":1761981313,"value":27.9}', badge: "RX" },
    { time: "15:25:13.107", json: '{"id":8426,"type":"HUM","ts":1761981313,"value":56.2}', badge: "RX" },
    { time: "15:25:12.684", json: '{"id":8425,"type":"OK","ts":1761981312,"value":0}', badge: "RX" },
    { time: "15:25:12.191", json: '{"id":8424,"type":"VIB","ts":1761981312,"value":0.012}', badge: "RX" },
    { time: "15:25:11.709", json: '{"id":8423,"type":"DOOR","ts":1761981311,"value":1}', badge: "RX" },
  ]);

  // Append new packets when live telemetry updates
  useEffect(() => {
    if (packets.length > 0) {
      const latest = packets.slice(0, 5);
      const newLogs = latest.map(p => {
        const d = new Date(p.timestamp * 1000);
        const timeStr = `${d.toTimeString().split(' ')[0]}.${String(d.getMilliseconds()).padStart(3, '0')}`;
        const valMap: Record<string, any> = {
          OK: 0,
          TEMP_HI: 68.4,
          TEMP_LO: 14.2,
          HUM: 58.1,
          VIB: 0.018,
          DOOR: 1,
          FAULT: 501,
          RESET: 1
        };
        const val = p.value !== undefined && p.value !== null ? p.value : (valMap[p.symbol] ?? 0);
        const jsonStr = `{"id":${p.sensor_id},"type":"${p.symbol}","ts":${Math.floor(p.timestamp)},"value":${val}}`;
        return { time: timeStr, json: jsonStr, badge: "RX" };
      });
      setLogItems(newLogs);

      // Update chart
      const now = new Date();
      const nowStr = `${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
      setChartData(prev => [
        ...prev.slice(-15),
        {
          time: nowStr,
          original: Math.round(originalBitrate),
          compressed: Math.round(compressedBitrate),
          band: [Math.round(compressedBitrate), Math.round(originalBitrate)],
          savings: Math.round(originalBitrate - compressedBitrate)
        }
      ]);
    }
  }, [packets, originalBitrate, compressedBitrate]);

  return (
    <div className="bg-[#141922] border border-[#273244] rounded-2xl p-5 shadow-sm space-y-4">
      {/* HEADER & BITRATE STATS */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#273244]/80">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-[#06B6D4]/10 text-[#06B6D4] border border-[#06B6D4]/20">
            <Activity className="w-4 h-4" />
          </div>
          <h3 className="text-sm font-bold text-[#F8FAFC]">Live Telemetry Feed</h3>
        </div>

        {/* BITRATE STATS (Original, Compressed, Savings) */}
        <div className="flex flex-wrap items-center gap-4 text-xs font-mono">
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-[#94A3B8]"></span>
            <span className="text-[#94A3B8]">Original: <strong className="text-[#F8FAFC]">{originalBitrate} bps</strong></span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-[#06B6D4]"></span>
            <span className="text-[#06B6D4]">Compressed: <strong>{compressedBitrate} bps</strong></span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-[#10B981]"></span>
            <span className="text-[#10B981]">Savings: <strong>{bandwidthSavedPct.toFixed(2)}%</strong></span>
          </div>
        </div>
      </div>

      {/* TWO-COLUMN GRID INSIDE THE FULL-WIDTH CARD */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-1">
        {/* LEFT: THROUGHPUT AREA CHART (7 cols) */}
        <div className="lg:col-span-7 flex flex-col justify-between">
          <div className="h-48 w-full mt-1">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="savingsFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0.05}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#273244" vertical={false} />
                <XAxis dataKey="time" stroke="#64748B" fontSize={10} tickLine={false} />
                <YAxis domain={[0, 'auto']} stroke="#64748B" fontSize={10} tickLine={false} />
                <Tooltip
                  content={({ active, payload, label }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-[#090C12]/95 border border-[#273244] rounded-xl p-3 shadow-xl text-xs space-y-1.5 backdrop-blur-md">
                          <div className="text-[#94A3B8] font-mono text-[11px] mb-1">{label}</div>
                          <div className="flex items-center gap-2 text-[#E2E8F0]">
                            <span className="w-2 h-2 rounded-full bg-[#94A3B8]"></span>
                            <span>Original: <span className="font-mono font-bold text-[#F8FAFC]">{originalBitrate} bps</span></span>
                          </div>
                          <div className="flex items-center gap-2 text-[#06B6D4]">
                            <span className="w-2 h-2 rounded-full bg-[#06B6D4]"></span>
                            <span>Compressed: <span className="font-mono font-bold text-[#06B6D4]">{compressedBitrate} bps</span></span>
                          </div>
                          <div className="flex items-center gap-2 text-[#10B981]">
                            <span className="w-2 h-2 rounded-full bg-[#10B981]"></span>
                            <span>Savings: <span className="font-mono font-bold text-[#10B981]">{bandwidthSavedPct.toFixed(2)}%</span></span>
                          </div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Area type="monotone" dataKey="band" stroke="none" fill="url(#savingsFill)" />
                <Area type="monotone" dataKey="original" stroke="#94A3B8" strokeWidth={2} fill="none" dot={false} />
                <Area type="monotone" dataKey="compressed" stroke="#06B6D4" strokeWidth={2} fill="none" dot={{ r: 3, fill: '#06B6D4' }} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* RIGHT: LATEST TELEMETRY PACKETS WITH TIMESTAMPS (5 cols) */}
        <div className="lg:col-span-5 bg-[#090C12] rounded-xl border border-[#273244]/80 p-3 font-mono text-xs flex flex-col justify-between overflow-hidden">
          <div className="space-y-2">
            {logItems.map((item, idx) => (
              <div key={idx} className="flex items-center justify-between text-[11px] gap-2 border-b border-[#1E293B]/50 pb-1.5 last:border-none">
                <span className="text-[#64748B] shrink-0">{item.time}</span>
                <span className="text-[#E2E8F0] truncate select-all">{item.json}</span>
                <span className="px-1.5 py-0.2 bg-[#10B981]/20 text-[#10B981] font-bold text-[10px] rounded border border-[#10B981]/40 shrink-0">
                  {item.badge}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
