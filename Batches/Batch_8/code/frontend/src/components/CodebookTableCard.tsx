import React from 'react';
import { Database } from 'lucide-react';
import { CompressionResponse } from '../types';

interface CodebookTableCardProps {
  huffmanData?: CompressionResponse;
}

export const CodebookTableCard: React.FC<CodebookTableCardProps> = ({ huffmanData }) => {
  // Ground truth symbol data matching reference table
  const defaultTableData = [
    { symbol: "OK", prob: 0.52, code: "1", length: 1, compliant: true },
    { symbol: "TEMP_HI", prob: 0.12, code: "010", length: 3, compliant: true },
    { symbol: "TEMP_LO", prob: 0.10, code: "011", length: 3, compliant: true },
    { symbol: "HUM", prob: 0.08, code: "1000", length: 4, compliant: true },
    { symbol: "VIB", prob: 0.06, code: "1001", length: 4, compliant: true },
    { symbol: "DOOR", prob: 0.05, code: "10100", length: 5, compliant: false },
    { symbol: "FAULT", prob: 0.04, code: "10101", length: 5, compliant: false },
    { symbol: "RESET", prob: 0.03, code: "10110", length: 6, compliant: false },
  ];

  // If huffmanData is present, use its mapped entries or fallback to standard
  const rows = huffmanData?.codebook && huffmanData.codebook.length === 8
    ? huffmanData.codebook.map(c => ({
        symbol: c.symbol,
        prob: c.probability,
        code: c.codeword,
        length: c.length,
        compliant: c.length <= 4
      }))
    : defaultTableData;

  return (
    <div className="bg-[#141922] border border-[#273244] rounded-2xl p-5 shadow-sm space-y-4">
      {/* HEADER */}
      <div className="flex items-center gap-3 pb-3 border-b border-[#273244]/80">
        <div className="p-2 rounded-xl bg-[#06B6D4]/10 text-[#06B6D4] border border-[#06B6D4]/20">
          <Database className="w-4 h-4" />
        </div>
        <h3 className="text-sm font-bold text-[#F8FAFC]">Codebook Table</h3>
      </div>

      {/* TABLE */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-[#273244] text-[#94A3B8] font-sans font-semibold uppercase text-[10px] tracking-wider">
              <th className="py-2 px-4">Symbol</th>
              <th className="py-2 px-4">Probability</th>
              <th className="py-2 px-4">Huffman Code</th>
              <th className="py-2 px-4">Length</th>
              <th className="py-2 px-4 font-sans text-right">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#1E293B]/70">
            {rows.map((row) => (
              <tr key={row.symbol} className="hover:bg-[#1E293B]/40 transition-colors">
                <td className="py-2.5 px-4 font-bold text-[#F8FAFC]">{row.symbol}</td>
                <td className="py-2.5 px-4 text-[#94A3B8]">{row.prob.toFixed(2)}</td>
                <td className="py-2.5 px-4">
                  <span className="px-2 py-0.5 bg-[#06B6D4]/15 text-[#06B6D4] font-bold rounded border border-[#06B6D4]/30 text-xs">
                    {row.code}
                  </span>
                </td>
                <td className="py-2.5 px-4 text-[#94A3B8]">
                  {row.length} {row.length === 1 ? 'bit' : 'bits'}
                </td>
                <td className="py-2.5 px-4 text-right font-sans">
                  {row.compliant ? (
                    <span className="inline-flex items-center px-2.5 py-0.5 bg-[#10B981]/15 text-[#10B981] font-semibold text-[11px] rounded-full border border-[#10B981]/30">
                      Compliant
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2.5 py-0.5 bg-[#EF4444]/15 text-[#EF4444] font-semibold text-[11px] rounded-full border border-[#EF4444]/30">
                      Overflow
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
