import React from 'react';
import { GitFork } from 'lucide-react';
import { CompressionResponse } from '../types';

interface HuffmanPrefixTreeProps {
  huffmanData?: CompressionResponse;
}

export const HuffmanPrefixTree: React.FC<HuffmanPrefixTreeProps> = ({ huffmanData }) => {
  // Map or fallback codes
  const codeMap: Record<string, string> = {
    OK: huffmanData?.codebook_map?.OK || "1",
    TEMP_HI: huffmanData?.codebook_map?.TEMP_HI || "010",
    TEMP_LO: huffmanData?.codebook_map?.TEMP_LO || "011",
    HUM: huffmanData?.codebook_map?.HUM || "1000",
    VIB: huffmanData?.codebook_map?.VIB || "1001",
    DOOR: huffmanData?.codebook_map?.DOOR || "10100",
    FAULT: huffmanData?.codebook_map?.FAULT || "10101",
    RESET: huffmanData?.codebook_map?.RESET || "10110"
  };

  return (
    <div className="bg-[#141922] border border-[#273244] rounded-2xl p-5 shadow-sm space-y-4">
      {/* HEADER */}
      <div className="flex items-center gap-3 pb-3 border-b border-[#273244]/80">
        <div className="p-2 rounded-xl bg-[#06B6D4]/10 text-[#06B6D4] border border-[#06B6D4]/20">
          <GitFork className="w-4 h-4" />
        </div>
        <h3 className="text-sm font-bold text-[#F8FAFC]">Huffman Prefix Tree</h3>
      </div>

      {/* TREE CANVAS */}
      <div className="relative bg-[#090C12]/90 rounded-xl border border-[#273244]/60 bg-grid-dots overflow-x-auto overflow-y-hidden py-8 px-4 flex justify-center items-center min-h-[300px]">
        <svg
          viewBox="0 0 1020 280"
          className="w-full max-w-[960px] h-auto select-none"
          style={{ minWidth: '780px' }}
        >
          <defs>
            <filter id="cyanGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="2" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* ================= SVG EDGES ================= */}
          <g stroke="#334155" strokeWidth="1.75" strokeLinecap="round">
            {/* Root (510, 30) -> Left OK (310, 100), Right N1 (680, 80) */}
            <line x1="510" y1="30" x2="310" y2="100" />
            <line x1="510" y1="30" x2="680" y2="80" />

            {/* N1 (680, 80) -> Left N2 (410, 140), Right N3 (780, 130) */}
            <line x1="680" y1="80" x2="410" y2="140" />
            <line x1="680" y1="80" x2="780" y2="130" />

            {/* N2 (410, 140) -> TEMP_HI (380, 215), TEMP_LO (465, 215) */}
            <line x1="410" y1="140" x2="380" y2="215" />
            <line x1="410" y1="140" x2="465" y2="215" />

            {/* N3 (780, 130) -> Left N4 (600, 180), Right N5 (800, 180) */}
            <line x1="780" y1="130" x2="600" y2="180" />
            <line x1="780" y1="130" x2="800" y2="180" />

            {/* N4 (600, 180) -> HUM (555, 245), VIB (635, 245) */}
            <line x1="600" y1="180" x2="555" y2="245" />
            <line x1="600" y1="180" x2="635" y2="245" />

            {/* N5 (800, 180) -> DOOR (720, 245), N6 (840, 215) */}
            <line x1="800" y1="180" x2="720" y2="245" />
            <line x1="800" y1="180" x2="840" y2="215" />

            {/* N6 (840, 215) -> FAULT (805, 260), RESET (885, 260) */}
            <line x1="840" y1="215" x2="805" y2="260" />
            <line x1="840" y1="215" x2="885" y2="260" />
          </g>

          {/* ================= BINARY EDGE LABELS (0 and 1) ================= */}
          <g fontSize="11" fontFamily="Inter, sans-serif" fontWeight="700" fill="#06B6D4" textAnchor="middle">
            <text x="390" y="55">0</text>
            <text x="610" y="45">1</text>

            <text x="525" y="105">0</text>
            <text x="740" y="100">1</text>

            <text x="385" y="175">0</text>
            <text x="445" y="175">1</text>
            <text x="680" y="150">0</text>
            <text x="800" y="150">1</text>

            <text x="568" y="210">0</text>
            <text x="625" y="210">1</text>
            <text x="750" y="210">0</text>
            <text x="830" y="195">1</text>

            <text x="815" y="238">0</text>
            <text x="870" y="238">1</text>
          </g>

          {/* ================= INTERNAL NODES ================= */}
          <circle cx="510" cy="30" r="10" fill="#090C12" stroke="#06B6D4" strokeWidth="2" filter="url(#cyanGlow)" />
          <text x="510" y="34" fill="#F8FAFC" fontSize="10" fontWeight="700" textAnchor="middle" fontFamily="JetBrains Mono">Ø</text>

          <circle cx="680" cy="80" r="6" fill="#090C12" stroke="#06B6D4" strokeWidth="2" />
          <circle cx="410" cy="140" r="6" fill="#090C12" stroke="#06B6D4" strokeWidth="2" />
          <circle cx="780" cy="130" r="6" fill="#090C12" stroke="#06B6D4" strokeWidth="2" />
          <circle cx="600" cy="180" r="6" fill="#090C12" stroke="#06B6D4" strokeWidth="2" />
          <circle cx="800" cy="180" r="6" fill="#090C12" stroke="#06B6D4" strokeWidth="2" />
          <circle cx="840" cy="215" r="5" fill="#090C12" stroke="#06B6D4" strokeWidth="2" />

          {/* ================= LEAF NODES (Symbol, Code, Length) ================= */}
          {/* 1. OK (1 bit) - GREEN */}
          <g transform="translate(275, 80)">
            <rect width="70" height="36" rx="18" fill="#064E3B" stroke="#10B981" strokeWidth="1.75" />
            <text x="35" y="16" fill="#10B981" fontSize="11" fontWeight="700" textAnchor="middle" fontFamily="Inter, sans-serif">OK</text>
            <text x="35" y="28" fill="#A7F3D0" fontSize="9" fontWeight="600" textAnchor="middle" fontFamily="JetBrains Mono">{codeMap.OK} (1 bit)</text>
          </g>

          {/* 2. TEMP_HI (3 bits) - GREEN */}
          <g transform="translate(340, 195)">
            <rect width="78" height="38" rx="8" fill="#064E3B" stroke="#10B981" strokeWidth="1.75" />
            <text x="39" y="16" fill="#10B981" fontSize="10" fontWeight="700" textAnchor="middle" fontFamily="Inter, sans-serif">TEMP_HI</text>
            <text x="39" y="28" fill="#A7F3D0" fontSize="8.5" fontWeight="600" textAnchor="middle" fontFamily="JetBrains Mono">{codeMap.TEMP_HI} (3b)</text>
          </g>

          {/* 3. TEMP_LO (3 bits) - GREEN */}
          <g transform="translate(425, 195)">
            <rect width="78" height="38" rx="8" fill="#064E3B" stroke="#10B981" strokeWidth="1.75" />
            <text x="39" y="16" fill="#10B981" fontSize="10" fontWeight="700" textAnchor="middle" fontFamily="Inter, sans-serif">TEMP_LO</text>
            <text x="39" y="28" fill="#A7F3D0" fontSize="8.5" fontWeight="600" textAnchor="middle" fontFamily="JetBrains Mono">{codeMap.TEMP_LO} (3b)</text>
          </g>

          {/* 4. HUM (4 bits) - AMBER */}
          <g transform="translate(525, 225)">
            <rect width="66" height="38" rx="8" fill="#451A03" stroke="#F59E0B" strokeWidth="1.75" />
            <text x="33" y="16" fill="#F59E0B" fontSize="10" fontWeight="700" textAnchor="middle" fontFamily="Inter, sans-serif">HUM</text>
            <text x="33" y="28" fill="#FDE68A" fontSize="8.5" fontWeight="600" textAnchor="middle" fontFamily="JetBrains Mono">{codeMap.HUM} (4b)</text>
          </g>

          {/* 5. VIB (4 bits) - AMBER */}
          <g transform="translate(605, 225)">
            <rect width="66" height="38" rx="8" fill="#451A03" stroke="#F59E0B" strokeWidth="1.75" />
            <text x="33" y="16" fill="#F59E0B" fontSize="10" fontWeight="700" textAnchor="middle" fontFamily="Inter, sans-serif">VIB</text>
            <text x="33" y="28" fill="#FDE68A" fontSize="8.5" fontWeight="600" textAnchor="middle" fontFamily="JetBrains Mono">{codeMap.VIB} (4b)</text>
          </g>

          {/* 6. DOOR (5 bits) - RED */}
          <g transform="translate(685, 225)">
            <rect width="72" height="38" rx="8" fill="#450A0A" stroke="#EF4444" strokeWidth="1.75" />
            <text x="36" y="16" fill="#EF4444" fontSize="10" fontWeight="700" textAnchor="middle" fontFamily="Inter, sans-serif">DOOR ▲</text>
            <text x="36" y="28" fill="#FECACA" fontSize="8.5" fontWeight="600" textAnchor="middle" fontFamily="JetBrains Mono">{codeMap.DOOR} (5b)</text>
          </g>

          {/* 7. FAULT (5 bits) - RED */}
          <g transform="translate(770, 240)">
            <rect width="72" height="38" rx="8" fill="#450A0A" stroke="#EF4444" strokeWidth="1.75" />
            <text x="36" y="16" fill="#EF4444" fontSize="10" fontWeight="700" textAnchor="middle" fontFamily="Inter, sans-serif">FAULT ▲</text>
            <text x="36" y="28" fill="#FECACA" fontSize="8.5" fontWeight="600" textAnchor="middle" fontFamily="JetBrains Mono">{codeMap.FAULT} (5b)</text>
          </g>

          {/* 8. RESET (6 bits) - RED */}
          <g transform="translate(850, 240)">
            <rect width="72" height="38" rx="8" fill="#450A0A" stroke="#EF4444" strokeWidth="1.75" />
            <text x="36" y="16" fill="#EF4444" fontSize="10" fontWeight="700" textAnchor="middle" fontFamily="Inter, sans-serif">RESET ▲</text>
            <text x="36" y="28" fill="#FECACA" fontSize="8.5" fontWeight="600" textAnchor="middle" fontFamily="JetBrains Mono">{codeMap.RESET} (6b)</text>
          </g>
        </svg>
      </div>
    </div>
  );
};
