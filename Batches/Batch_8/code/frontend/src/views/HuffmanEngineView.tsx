import React from 'react';
import { CompressionResponse, SymbolFrequency } from '../types';
import { FrequencyEditor } from '../components/FrequencyEditor';
import { TreeVisualizer } from '../components/TreeVisualizer';
import { MessageCodec } from '../components/MessageCodec';
import { Download, AlertTriangle, CheckCircle } from 'lucide-react';

interface HuffmanEngineViewProps {
  frequencies: SymbolFrequency[];
  huffmanData?: CompressionResponse;
  onFrequencyChange: (newFreqs: SymbolFrequency[]) => void;
  onResetFrequencies: () => void;
  onLoadPreset?: (name: string) => void;
}

export const HuffmanEngineView: React.FC<HuffmanEngineViewProps> = ({
  frequencies,
  huffmanData,
  onFrequencyChange,
  onResetFrequencies,
  onLoadPreset
}) => {
  const exportCodebookJSON = () => {
    if (!huffmanData) return;
    const blob = new Blob([JSON.stringify(huffmanData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `huffman_codebook_${Date.now()}.json`;
    a.click();
  };

  const exportCodebookCSV = () => {
    if (!huffmanData) return;
    const headers = "Symbol,Frequency,Probability,Codeword,Length_Bits,Hardware_Compatible\n";
    const rows = huffmanData.codebook
      .map(c => `${c.symbol},${c.frequency},${c.probability},${c.codeword},${c.length},${c.register_compatible ? 'PASS' : 'FAIL'}`)
      .join("\n");
    const blob = new Blob([headers + rows], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `huffman_codebook_${Date.now()}.csv`;
    a.click();
  };

  return (
    <div className="space-y-6">
      {/* SECTION HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-bold text-[#F8FAFC] tracking-tight">
            Huffman Tree & Codebook Engine
          </h2>
          <p className="text-xs text-[#94A3B8]">
            Constructs optimal prefix-free binary tree via bottom-up min-heap priority queue
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={exportCodebookJSON}
            className="px-3 py-1.5 text-xs font-medium text-[#F8FAFC] bg-[#141922] hover:bg-[#1E293B] border border-[#273244] rounded-xl transition-colors flex items-center gap-1.5 shadow-2xs cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" /> Export JSON
          </button>
          <button
            onClick={exportCodebookCSV}
            className="px-3 py-1.5 text-xs font-medium text-[#F8FAFC] bg-[#141922] hover:bg-[#1E293B] border border-[#273244] rounded-xl transition-colors flex items-center gap-1.5 shadow-2xs cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" /> Export CSV
          </button>
        </div>
      </div>

      {/* FREQUENCY EDITOR */}
      <FrequencyEditor
        frequencies={frequencies}
        onChange={onFrequencyChange}
        onReset={onResetFrequencies}
        onLoadPreset={onLoadPreset}
      />

      {/* MATHEMATICAL METRICS BAR */}
      {huffmanData && (
        <div className="grid grid-cols-2 sm:grid-cols-6 gap-3">
          <div className="bg-[#141922] p-3.5 rounded-xl border border-[#273244] shadow-2xs">
            <div className="text-[11px] font-medium text-[#94A3B8]">Average Length (L)</div>
            <div className="text-base font-black text-[#06B6D4] font-mono mt-0.5">
              {huffmanData.average_length.toFixed(4)} <span className="text-[10px] text-[#64748B] font-sans">bits</span>
            </div>
            <div className="text-[10px] text-[#64748B] mt-0.5">Σ p(i) × l(i)</div>
          </div>

          <div className="bg-[#141922] p-3.5 rounded-xl border border-[#273244] shadow-2xs">
            <div className="text-[11px] font-medium text-[#94A3B8]">Entropy H(X)</div>
            <div className="text-base font-black text-[#06B6D4] font-mono mt-0.5">
              {huffmanData.entropy.toFixed(4)} <span className="text-[10px] text-[#64748B] font-sans">bits</span>
            </div>
            <div className="text-[10px] text-[#64748B] mt-0.5">Shannon lower bound</div>
          </div>

          <div className="bg-[#141922] p-3.5 rounded-xl border border-[#273244] shadow-2xs">
            <div className="text-[11px] font-medium text-[#94A3B8]">Coding Efficiency</div>
            <div className="text-base font-black text-[#10B981] font-mono mt-0.5">
              {huffmanData.efficiency.toFixed(2)}%
            </div>
            <div className="text-[10px] text-[#64748B] mt-0.5">H(X) / L</div>
          </div>

          <div className="bg-[#141922] p-3.5 rounded-xl border border-[#273244] shadow-2xs">
            <div className="text-[11px] font-medium text-[#94A3B8]">Bandwidth Savings</div>
            <div className="text-base font-black text-[#10B981] font-mono mt-0.5">
              {huffmanData.bandwidth_savings_pct.toFixed(2)}%
            </div>
            <div className="text-[10px] text-[#64748B] mt-0.5">vs 3-bit fixed</div>
          </div>

          <div className="bg-[#141922] p-3.5 rounded-xl border border-[#273244] shadow-2xs">
            <div className="text-[11px] font-medium text-[#94A3B8]">Kraft Inequality</div>
            <div className="text-base font-black text-[#F8FAFC] font-mono mt-0.5">
              {huffmanData.kraft_sum.toFixed(4)}
            </div>
            <div className="text-[10px] text-[#10B981] font-semibold mt-0.5">Full tree (=1.0)</div>
          </div>

          <div className="bg-[#141922] p-3.5 rounded-xl border border-[#273244] shadow-2xs">
            <div className="text-[11px] font-medium text-[#94A3B8]">Max Codeword</div>
            <div className={`text-base font-black font-mono mt-0.5 ${huffmanData.max_codeword_length > 4 ? 'text-[#EF4444]' : 'text-[#F8FAFC]'}`}>
              {huffmanData.max_codeword_length} <span className="text-[10px] text-[#64748B] font-sans">bits</span>
            </div>
            <div className="text-[10px] mt-0.5 font-semibold">
              {huffmanData.max_codeword_length > 4 ? (
                <span className="text-[#EF4444] flex items-center gap-0.5"><AlertTriangle className="w-2.5 h-2.5" /> Exceeds 4b</span>
              ) : (
                <span className="text-[#10B981] flex items-center gap-0.5"><CheckCircle className="w-2.5 h-2.5" /> Fits 4b</span>
              )}
            </div>
          </div>
        </div>
      )}

      {/* CODEBOOK TABLE & TREE SPLIT */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* TABLE */}
        <div className="lg:col-span-6 bg-[#141922] rounded-2xl border border-[#273244] p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-[#273244]">
            <div>
              <h3 className="text-sm font-bold text-[#F8FAFC]">Generated Huffman Codebook</h3>
              <p className="text-xs text-[#94A3B8]">Instantaneous prefix-free codewords derived from tree traversal</p>
            </div>
            <span className="text-xs font-mono font-medium text-[#64748B]">
              Min-Heap: {huffmanData?.operations_count || 0} ops
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-[#273244] text-[#94A3B8] font-sans font-semibold uppercase tracking-wider text-[10px]">
                  <th className="py-2.5 px-3">Symbol</th>
                  <th className="py-2.5 px-3">Freq</th>
                  <th className="py-2.5 px-3">Prob p(i)</th>
                  <th className="py-2.5 px-3">Codeword</th>
                  <th className="py-2.5 px-3">Length</th>
                  <th className="py-2.5 px-3 font-sans">Hardware (&le;4)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E293B]/70">
                {huffmanData?.codebook.map((entry) => (
                  <tr key={entry.symbol} className="hover:bg-[#1E293B]/40 transition-colors">
                    <td className="py-2.5 px-3 font-bold text-[#F8FAFC]">{entry.symbol}</td>
                    <td className="py-2.5 px-3 text-[#94A3B8]">{entry.frequency}</td>
                    <td className="py-2.5 px-3 text-[#94A3B8]">{entry.probability.toFixed(3)}</td>
                    <td className="py-2.5 px-3">
                      <span className="px-2 py-0.5 bg-[#06B6D4]/15 text-[#06B6D4] font-bold rounded border border-[#06B6D4]/30">
                        {entry.codeword}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 font-semibold text-[#94A3B8]">{entry.length} b</td>
                    <td className="py-2.5 px-3 font-sans">
                      {entry.register_compatible ? (
                        <span className="px-2 py-0.5 text-[10px] font-bold bg-[#10B981]/15 text-[#10B981] rounded-full border border-[#10B981]/30">
                          PASS
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 text-[10px] font-bold bg-[#EF4444]/15 text-[#EF4444] rounded-full border border-[#EF4444]/30">
                          OVERFLOW ({entry.length}b &gt; 4b)
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="pt-3 border-t border-[#273244] flex items-center justify-between text-xs text-[#94A3B8]">
            <span>Weighted Length: <strong className="font-mono text-[#F8FAFC]">{huffmanData?.average_length.toFixed(4)} bits/msg</strong></span>
            <span>Compression: <strong className="text-[#10B981] font-mono">{huffmanData?.compression_ratio}:1</strong></span>
          </div>
        </div>

        {/* TREE VISUALIZER */}
        <div className="lg:col-span-6">
          <TreeVisualizer
            treeData={huffmanData?.tree}
            title="Interactive Huffman Binary Tree"
            algorithmName="Min-Heap Huffman"
          />
        </div>
      </div>

      {/* MESSAGE ENCODER / DECODER */}
      {huffmanData && (
        <MessageCodec
          codebookMap={huffmanData.codebook_map}
          algorithmName="Huffman"
        />
      )}
    </div>
  );
};
