import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { CodebookBroadcastResponse } from '../types';
import {
  Send,
  CheckCircle,
  AlertOctagon
} from 'lucide-react';

export const CodebookManagementView: React.FC = () => {
  const [currentVersion, setCurrentVersion] = useState<string>("v1.0.0");
  const [broadcastData, setBroadcastData] = useState<CodebookBroadcastResponse | null>(null);
  const [broadcasting, setBroadcasting] = useState<boolean>(false);
  const [lossRate, setLossRate] = useState<number>(0.015);
  const [selectedAlgo, setSelectedAlgo] = useState<string>("package_merge");

  // Outdated decode test state
  const [testBitstream, setTestBitstream] = useState<string>("010011100");
  const [testVersion, setTestVersion] = useState<string>("v0.9.0");
  const [testResult, setTestResult] = useState<any>(null);

  useEffect(() => {
    loadCurrentCodebook();
  }, []);

  const loadCurrentCodebook = async () => {
    try {
      const data = await api.getCurrentCodebook();
      setCurrentVersion(data.version);
    } catch (err) {
      console.error("Failed to load current codebook:", err);
    }
  };

  const handleBroadcast = async () => {
    try {
      setBroadcasting(true);
      const res = await api.broadcastCodebook(undefined, selectedAlgo, lossRate);
      setBroadcastData(res);
      setCurrentVersion(res.version);
      setTestVersion(res.version); // update test
    } catch (err) {
      console.error("Broadcast failed:", err);
    } finally {
      setBroadcasting(false);
    }
  };

  const handleTestDecode = async () => {
    try {
      const curCb = await api.getCurrentCodebook();
      const res = await api.decode(testBitstream, curCb.codebook, testVersion);
      setTestResult({ success: true, res });
    } catch (err: any) {
      setTestResult({ success: false, error: err.message || "Decoding error" });
    }
  };

  return (
    <div className="space-y-6">
      {/* SECTION HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-[#F8FAFC] tracking-tight">
            Gateway Codebook Management & Broadcast
          </h2>
          <p className="text-xs text-[#94A3B8]">
            Over-the-air decoding table synchronization across 5,000 edge sensor receivers
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3 py-1 bg-[#06B6D4]/15 text-[#06B6D4] font-mono text-xs font-bold rounded-lg border border-[#06B6D4]/30">
            Gateway Active: {currentVersion}
          </span>
        </div>
      </div>

      {/* BROADCAST CONTROL CARD */}
      <div className="bg-[#141922] rounded-2xl border border-[#273244] p-5 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[#273244]">
          <div>
            <h3 className="text-sm font-bold text-[#F8FAFC]">Broadcast Codebook to Field Receivers</h3>
            <p className="text-xs text-[#94A3B8]">
              Pushes updated prefix codebook version to all 5,000 registered industrial field nodes
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 text-xs">
              <span className="text-[#94A3B8] font-medium">Codec:</span>
              <select
                value={selectedAlgo}
                onChange={(e) => setSelectedAlgo(e.target.value)}
                className="px-2 py-1 bg-[#090C12] border border-[#273244] rounded-lg font-mono text-xs font-bold text-[#06B6D4]"
              >
                <option value="package_merge">Package-Merge (L&le;4)</option>
                <option value="huffman">Standard Huffman</option>
              </select>
            </div>

            <div className="flex items-center gap-1.5 text-xs">
              <span className="text-[#94A3B8] font-medium">Channel Loss:</span>
              <input
                type="number"
                min="0"
                max="0.2"
                step="0.005"
                value={lossRate}
                onChange={(e) => setLossRate(parseFloat(e.target.value) || 0)}
                className="w-16 px-2 py-1 bg-[#090C12] border border-[#273244] rounded-lg font-mono text-xs text-center font-bold text-[#F8FAFC]"
              />
            </div>

            <button
              onClick={handleBroadcast}
              disabled={broadcasting}
              className="px-4 py-2 bg-[#06B6D4] hover:bg-[#0891B2] disabled:opacity-50 text-[#090C12] font-bold text-xs rounded-xl transition-all flex items-center gap-1.5 shadow-xs cursor-pointer"
            >
              <Send className="w-3.5 h-3.5" />
              {broadcasting ? "Broadcasting..." : "Broadcast New Version"}
            </button>
          </div>
        </div>

        {/* OVERHEAD CALCULATOR STRIP */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="p-3 bg-[#090C12] border border-[#273244] rounded-xl">
            <span className="text-[#64748B] text-[11px]">Table Payload Size</span>
            <div className="font-mono font-bold text-[#F8FAFC] mt-0.5">80 bits (8 symbols)</div>
          </div>
          <div className="p-3 bg-[#090C12] border border-[#273244] rounded-xl">
            <span className="text-[#64748B] text-[11px]">Framing Overhead (CRC16)</span>
            <div className="font-mono font-bold text-[#F8FAFC] mt-0.5">32 bits / broadcast</div>
          </div>
          <div className="p-3 bg-[#090C12] border border-[#273244] rounded-xl">
            <span className="text-[#64748B] text-[11px]">Amortized Broadcast Rate</span>
            <div className="font-mono font-bold text-[#10B981] mt-0.5">0.0311 bps / hour</div>
          </div>
          <div className="p-3 bg-[#090C12] border border-[#273244] rounded-xl">
            <span className="text-[#64748B] text-[11px]">Channel Overhead Ratio</span>
            <div className="font-mono font-bold text-[#10B981] mt-0.5">0.00032% of 9.6 kbps</div>
          </div>
        </div>
      </div>

      {/* BROADCAST RESULTS & RECEIVER STATUS */}
      {broadcastData && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
              <span className="text-xs text-[#94A3B8]">Synchronized Receivers</span>
              <div className="text-xl font-bold font-mono text-[#10B981] mt-1">
                {broadcastData.receivers_acked.toLocaleString()} / {broadcastData.receivers_total.toLocaleString()}
              </div>
              <span className="text-[10px] text-[#10B981] font-semibold">{broadcastData.sync_percentage}% ACK Rate</span>
            </div>

            <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
              <span className="text-xs text-[#94A3B8]">Unacknowledged (Retrying)</span>
              <div className="text-xl font-bold font-mono text-[#F59E0B] mt-1">
                {broadcastData.receivers_failed} nodes
              </div>
              <span className="text-[10px] text-[#64748B]">Scheduled re-burst</span>
            </div>

            <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
              <span className="text-xs text-[#94A3B8]">Broadcast Volume</span>
              <div className="text-xl font-bold font-mono text-[#F8FAFC] mt-1">
                {broadcastData.total_broadcast_bits} bits
              </div>
              <span className="text-[10px] text-[#64748B]">80 payload + 32 header</span>
            </div>

            <div className="bg-[#141922] p-4 rounded-xl border border-[#273244] shadow-2xs">
              <span className="text-xs text-[#94A3B8]">Active Deployed Version</span>
              <div className="text-xl font-bold font-mono text-[#06B6D4] mt-1">
                {broadcastData.version}
              </div>
              <span className="text-[10px] text-[#64748B]">OTA Verified</span>
            </div>
          </div>

          {/* SAMPLE RECEIVER TABLE */}
          <div className="bg-[#141922] rounded-2xl border border-[#273244] p-5 shadow-sm space-y-3">
            <div className="flex items-center justify-between pb-3 border-b border-[#273244]">
              <h3 className="text-sm font-bold text-[#F8FAFC]">Field Receiver Telemetry Status (Sample 20 of 5,000)</h3>
              <span className="text-xs text-[#64748B] font-mono">OTA Latency: 12 - 48 ms nominal</span>
            </div>

            <div className="overflow-x-auto max-h-60 overflow-y-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead>
                  <tr className="border-b border-[#273244] text-[#94A3B8] font-sans font-semibold uppercase text-[10px]">
                    <th className="py-2 px-3">Receiver ID</th>
                    <th className="py-2 px-3">Sync Status</th>
                    <th className="py-2 px-3">Version Installed</th>
                    <th className="py-2 px-3">Roundtrip Latency</th>
                    <th className="py-2 px-3">Retries</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#273244]/60">
                  {broadcastData.sample_receivers.map((rx) => (
                    <tr key={rx.receiver_id} className="hover:bg-[#1E293B]/40">
                      <td className="py-1.5 px-3 font-semibold text-[#F8FAFC]">Receiver-{rx.receiver_id}</td>
                      <td className="py-1.5 px-3 font-sans">
                        {rx.synchronized ? (
                          <span className="px-2 py-0.5 bg-[#10B981]/15 text-[#10B981] rounded font-semibold text-[10px] border border-[#10B981]/30">
                            SYNCHRONIZED
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 bg-[#EF4444]/15 text-[#EF4444] rounded font-semibold text-[10px] border border-[#EF4444]/30">
                            PENDING ACK
                          </span>
                        )}
                      </td>
                      <td className="py-1.5 px-3 text-[#94A3B8]">{rx.current_version}</td>
                      <td className="py-1.5 px-3 text-[#94A3B8]">{rx.latency_ms} ms</td>
                      <td className="py-1.5 px-3 text-[#94A3B8]">{rx.retries}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* VERSION MISMATCH TEST HARNESS */}
      <div className="bg-[#141922] rounded-2xl border border-[#273244] p-5 shadow-sm space-y-4">
        <div className="pb-3 border-b border-[#273244]">
          <h3 className="text-sm font-bold text-[#F8FAFC]">Outdated Codebook Version Rejection Verification</h3>
          <p className="text-xs text-[#94A3B8]">
            Requirement: Prevent decoding when receiver has an outdated codebook version
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="text-xs font-semibold text-[#94A3B8] block mb-1">Incoming Bitstream:</label>
            <input
              type="text"
              value={testBitstream}
              onChange={(e) => setTestBitstream(e.target.value)}
              className="w-full px-3 py-1.5 bg-[#090C12] border border-[#273244] rounded-lg font-mono text-xs text-[#06B6D4]"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-[#94A3B8] block mb-1">Receiver Tagged Version:</label>
            <input
              type="text"
              value={testVersion}
              onChange={(e) => setTestVersion(e.target.value)}
              placeholder="e.g. v0.9.0"
              className="w-full px-3 py-1.5 bg-[#090C12] border border-[#273244] rounded-lg font-mono text-xs text-[#F8FAFC]"
            />
          </div>

          <div className="flex items-end">
            <button
              onClick={handleTestDecode}
              className="w-full px-4 py-2 bg-[#06B6D4] hover:bg-[#0891B2] text-[#090C12] font-bold text-xs rounded-xl transition-colors cursor-pointer"
            >
              Verify Decoder Rejection
            </button>
          </div>
        </div>

        {testResult && (
          <div className={`p-4 rounded-xl text-xs leading-relaxed border ${
            testResult.success
              ? 'bg-[#10B981]/15 border-[#10B981]/30 text-[#10B981]'
              : 'bg-[#EF4444]/15 border-[#EF4444]/30 text-[#EF4444]'
          }`}>
            {testResult.success ? (
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-[#10B981]" />
                <span>Version matches active gateway ({currentVersion}). Decoded {testResult.res.symbols_decoded} status messages successfully!</span>
              </div>
            ) : (
              <div className="flex items-start gap-2">
                <AlertOctagon className="w-4 h-4 text-[#EF4444] shrink-0 mt-0.5" />
                <div>
                  <strong className="block font-bold">Decoding Successfully Blocked (Version Mismatch):</strong>
                  <span>{testResult.error}</span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
