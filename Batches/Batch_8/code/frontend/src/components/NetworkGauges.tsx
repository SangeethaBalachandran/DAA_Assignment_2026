import React from 'react';
import { BarChart3, Database } from 'lucide-react';
import { NetworkMetrics } from '../types';

interface NetworkGaugesProps {
  metrics?: NetworkMetrics;
}

export const NetworkGauges: React.FC<NetworkGaugesProps> = ({ metrics }) => {
  const linkUtil = metrics?.compressed_utilization_pct !== undefined ? metrics.compressed_utilization_pct : 0.92;
  const msgRate = metrics?.message_rate !== undefined ? metrics.message_rate : 40;

  // Arc length for R=85 is pi * 85 = 267.035
  const ARC_LEN = 267.035;

  // Clamped fractions
  const utilFraction = Math.min(Math.max(linkUtil / 100, 0.015), 1);
  const utilOffset = ARC_LEN * (1 - utilFraction);

  const rateFraction = Math.min(Math.max(msgRate / 100, 0), 1);
  const rateOffset = ARC_LEN * (1 - rateFraction);

  return (
    <div className="bg-[#141922] border border-[#273244] rounded-2xl p-5 shadow-sm space-y-4">
      {/* HEADER */}
      <div className="flex items-center gap-3 pb-3 border-b border-[#273244]/80">
        <div className="p-2 rounded-xl bg-[#06B6D4]/10 text-[#06B6D4] border border-[#06B6D4]/20">
          <BarChart3 className="w-4 h-4" />
        </div>
        <h3 className="text-sm font-bold text-[#F8FAFC]">Network Gauges</h3>
      </div>

      {/* GAUGES CONTENT CONTAINER */}
      <div className="flex flex-col lg:flex-row items-center justify-between gap-6 pt-1">
        {/* TWO GAUGES ROW */}
        <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 gap-6 w-full max-w-2xl">
          {/* GAUGE 1: LINK UTILIZATION */}
          <div className="flex flex-col items-center">
            <div className="relative w-[220px] h-[125px]">
              <svg viewBox="0 0 220 125" className="w-full h-full select-none">
                <path
                  d="M 25 105 A 85 85 0 0 1 195 105"
                  fill="none"
                  stroke="#1E293B"
                  strokeWidth="14"
                  strokeLinecap="round"
                />
                <path
                  d="M 25 105 A 85 85 0 0 1 195 105"
                  fill="none"
                  stroke="#10B981"
                  strokeWidth="14"
                  strokeLinecap="round"
                  strokeDasharray={ARC_LEN}
                  strokeDashoffset={utilOffset}
                  className="transition-all duration-700 ease-out"
                />
                <text x="18" y="122" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">0%</text>
                <text x="50" y="52" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">20%</text>
                <text x="110" y="16" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">40%</text>
                <text x="170" y="52" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">60%</text>
                <text x="195" y="100" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">80%</text>
                <text x="202" y="122" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">100%</text>

                <text x="110" y="85" fill="#94A3B8" fontSize="11" fontWeight="500" textAnchor="middle">
                  Link Utilization
                </text>
                <text x="110" y="112" fill="#10B981" fontSize="20" fontWeight="800" textAnchor="middle" fontFamily="JetBrains Mono">
                  {linkUtil.toFixed(2)}%
                </text>
              </svg>
            </div>
          </div>

          {/* GAUGE 2: MESSAGES / SEC */}
          <div className="flex flex-col items-center">
            <div className="relative w-[220px] h-[125px]">
              <svg viewBox="0 0 220 125" className="w-full h-full select-none">
                <path
                  d="M 25 105 A 85 85 0 0 1 195 105"
                  fill="none"
                  stroke="#1E293B"
                  strokeWidth="14"
                  strokeLinecap="round"
                />
                <path
                  d="M 25 105 A 85 85 0 0 1 195 105"
                  fill="none"
                  stroke="#06B6D4"
                  strokeWidth="14"
                  strokeLinecap="round"
                  strokeDasharray={ARC_LEN}
                  strokeDashoffset={rateOffset}
                  className="transition-all duration-700 ease-out"
                />
                <text x="20" y="122" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">0</text>
                <text x="50" y="52" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">20</text>
                <text x="110" y="16" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">40</text>
                <text x="170" y="52" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">60</text>
                <text x="195" y="100" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">80</text>
                <text x="202" y="122" fill="#64748B" fontSize="9" fontWeight="600" textAnchor="middle">100</text>

                <text x="110" y="85" fill="#94A3B8" fontSize="11" fontWeight="500" textAnchor="middle">
                  Messages/sec
                </text>
                <text x="110" y="112" fill="#06B6D4" fontSize="22" fontWeight="800" textAnchor="middle" fontFamily="JetBrains Mono">
                  {msgRate}
                </text>
              </svg>
            </div>
          </div>
        </div>

        {/* 1-HOUR PROJECTION & ESTIMATED DATA SAVED */}
        <div className="w-full lg:w-72 bg-[#090C12] border border-[#273244] rounded-xl p-4 flex items-center gap-3.5 shadow-2xs">
          <div className="p-2.5 rounded-lg bg-[#10B981]/10 text-[#10B981] border border-[#10B981]/20 shrink-0">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xs text-[#94A3B8] font-medium">1-Hour Projection:</div>
            <div className="text-sm font-bold font-mono text-[#10B981] mt-0.5">
              144,000 msgs · 115.2 kB saved
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
