import React, { useState, useEffect, useRef } from 'react';
import {
  CompressionResponse,
  NetworkMetrics,
  SymbolFrequency,
  LiveTelemetryPacket
} from '../types';
import { api } from '../services/api';
import { KpiMetricsRow } from '../components/KpiMetricsRow';
import { HuffmanPrefixTree } from '../components/HuffmanPrefixTree';
import { LiveTelemetryFeedCard } from '../components/LiveTelemetryFeedCard';
import { CodebookTableCard } from '../components/CodebookTableCard';
import { NetworkGauges } from '../components/NetworkGauges';
import { Play, Square } from 'lucide-react';

interface OverviewViewProps {
  frequencies: SymbolFrequency[];
  huffmanData?: CompressionResponse;
  packageMergeData?: CompressionResponse;
  networkMetrics?: NetworkMetrics;
  onNavigate: (tab: string) => void;
}

export const OverviewView: React.FC<OverviewViewProps> = ({
  huffmanData,
  networkMetrics: initialNetworkMetrics
}) => {
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const [livePackets, setLivePackets] = useState<LiveTelemetryPacket[]>([]);
  const [currentMetrics, setCurrentMetrics] = useState<NetworkMetrics | undefined>(initialNetworkMetrics);
  const [wsConnected, setWsConnected] = useState<boolean>(false);
  const wsRef = useRef<WebSocket | null>(null);

  // Sync with initial props
  useEffect(() => {
    if (initialNetworkMetrics) {
      setCurrentMetrics(initialNetworkMetrics);
    }
  }, [initialNetworkMetrics]);

  // Connect to backend WebSocket for live telemetry streaming
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
          if (data.status) {
            setIsSimulating(data.status.is_running && !data.status.is_paused);
          }
          if (data.metrics) {
            setCurrentMetrics(data.metrics);
          }
          if (data.packets && data.packets.length > 0) {
            setLivePackets(prev => [...data.packets.slice(-10), ...prev].slice(0, 50));
          }
        }
      } catch (err) {
        console.error("Overview WS message parse error:", err);
      }
    };

    ws.onclose = () => {
      setWsConnected(false);
    };

    // Initial status check
    api.getSimulationStatus().then(st => {
      setIsSimulating(st.is_running && !st.is_paused);
    }).catch(() => {});

    return () => {
      ws.close();
    };
  }, []);

  // Simulation controls (calls actual backend API)
  const toggleSimulation = async () => {
    try {
      if (!isSimulating) {
        await api.startSimulation();
        setIsSimulating(true);
      } else {
        await api.pauseSimulation();
        setIsSimulating(false);
      }
    } catch (err) {
      console.error("Simulation toggle error:", err);
    }
  };

  return (
    <div className="w-full space-y-5 pb-8">
      {/* ============================================================ */}
      {/* MODULE 1: HEADER                                             */}
      {/* ============================================================ */}
      <section className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-[#F8FAFC] tracking-tight">
            IoTCompress
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="bg-[#141922] border border-[#273244] rounded-lg px-3 py-1.5 flex items-center gap-2.5 text-xs text-[#94A3B8]">
            <span className="font-medium text-[#F8FAFC]">Gateway: IoT-Edge-01</span>
            <span className="text-[#334155]">·</span>
            <span className="font-mono text-[#06B6D4]">Codebook v1.0.1</span>
            <span className="text-[#334155]">·</span>
            <span className="flex items-center gap-1.5 text-[#10B981] font-semibold">
              <span className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-[#10B981] animate-pulse' : 'bg-[#EF4444]'}`}></span>
              {wsConnected ? 'Connected' : 'Offline'}
            </span>
          </div>

          <button
            onClick={toggleSimulation}
            className={`px-4 py-2 font-bold text-xs rounded-lg transition-all flex items-center gap-1.5 cursor-pointer shadow-sm ${
              isSimulating
                ? 'bg-[#EF4444] hover:bg-[#DC2626] text-white'
                : 'bg-[#06B6D4] hover:bg-[#0891B2] text-[#090C12]'
            }`}
          >
            {isSimulating ? (
              <>
                <Square className="w-3.5 h-3.5 fill-current" /> Stop Simulation
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" /> Start Simulation
              </>
            )}
          </button>
        </div>
      </section>

      {/* ============================================================ */}
      {/* MODULE 2: KPI METRICS                                        */}
      {/* ============================================================ */}
      <section className="w-full">
        <KpiMetricsRow
          huffmanData={huffmanData}
          networkMetrics={currentMetrics}
        />
      </section>

      {/* ============================================================ */}
      {/* MODULE 3: HUFFMAN PREFIX TREE                                */}
      {/* ============================================================ */}
      <section className="w-full">
        <HuffmanPrefixTree
          huffmanData={huffmanData}
        />
      </section>

      {/* ============================================================ */}
      {/* MODULE 4: LIVE TELEMETRY FEED                                */}
      {/* ============================================================ */}
      <section className="w-full">
        <LiveTelemetryFeedCard
          packets={livePackets}
          isSimulating={isSimulating}
          originalBitrate={currentMetrics?.original_bitrate || 120}
          compressedBitrate={currentMetrics?.compressed_bitrate || 88}
          bandwidthSavedPct={huffmanData?.bandwidth_savings_pct || 26.67}
        />
      </section>

      {/* ============================================================ */}
      {/* MODULE 5: CODEBOOK TABLE                                     */}
      {/* ============================================================ */}
      <section className="w-full">
        <CodebookTableCard
          huffmanData={huffmanData}
        />
      </section>

      {/* ============================================================ */}
      {/* MODULE 6: NETWORK GAUGES                                     */}
      {/* ============================================================ */}
      <section className="w-full">
        <NetworkGauges
          metrics={currentMetrics}
        />
      </section>
    </div>
  );
};
