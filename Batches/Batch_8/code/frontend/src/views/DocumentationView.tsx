import React from 'react';
import { BookOpen, ShieldAlert, Download } from 'lucide-react';

export const DocumentationView: React.FC = () => {
  return (
    <div className="space-y-6 max-w-5xl mx-auto text-[#F8FAFC]">
      {/* HEADER */}
      <div className="bg-[#141922] rounded-2xl border border-[#273244] p-6 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-[#06B6D4]/15 text-[#06B6D4] text-xs font-semibold mb-2 border border-[#06B6D4]/30">
            <BookOpen className="w-3.5 h-3.5" /> University DAA Engineering Specification
          </div>
          <h2 className="text-xl font-bold text-[#F8FAFC] tracking-tight">
            Mathematical Specification & Algorithmic Analysis
          </h2>
          <p className="text-xs text-[#94A3B8]">
            Formal proofs, complexity bounds, and network capacity equations for Industrial IoT telemetry
          </p>
        </div>

        <a
          href="/docs/MATHEMATICAL_SPECIFICATION.pdf"
          target="_blank"
          rel="noopener noreferrer"
          className="px-4 py-2 bg-[#06B6D4] hover:bg-[#0891B2] text-[#090C12] font-bold text-xs rounded-xl transition-colors flex items-center gap-1.5 shadow-xs shrink-0 cursor-pointer"
        >
          <Download className="w-3.5 h-3.5" /> Download Full PDF Document
        </a>
      </div>

      {/* SECTION 1 */}
      <div className="bg-[#141922] rounded-2xl border border-[#273244] p-6 shadow-sm space-y-3">
        <h3 className="text-sm font-bold text-[#F8FAFC] border-b border-[#273244] pb-2 flex items-center gap-2">
          <span className="w-6 h-6 rounded-lg bg-[#090C12] text-[#06B6D4] border border-[#273244] flex items-center justify-center text-xs font-bold font-mono">1</span>
          Problem Definition & Information Entropy Bound
        </h3>
        <p className="text-xs text-[#94A3B8] leading-relaxed">
          An industrial edge gateway forwards status codes from 5,000 sensors over a 9.6 kbps narrowband physical communication link. Under legacy fixed-length encoding, 8 discrete events require <code className="px-1.5 py-0.5 bg-[#090C12] border border-[#273244] rounded text-[#06B6D4] font-mono text-[11px]">l_fixed = ceil(log2(8)) = 3 bits/message</code>.
        </p>
        <p className="text-xs text-[#94A3B8] leading-relaxed">
          Shannon's Source Coding Theorem establishes the theoretical limit on compression for any lossless symbol-by-symbol code:
        </p>
        <div className="p-3 bg-[#090C12] rounded-xl font-mono text-xs text-[#10B981] border border-[#273244]">
          H(X) = - Σ p(i) log2(p(i)) = 2.1843 bits/message
        </div>
        <p className="text-xs text-[#64748B]">
          No prefix-free symbol code can achieve an average code length lower than 2.1843 bits without multi-symbol block grouping.
        </p>
      </div>

      {/* SECTION 2 */}
      <div className="bg-[#141922] rounded-2xl border border-[#273244] p-6 shadow-sm space-y-3">
        <h3 className="text-sm font-bold text-[#F8FAFC] border-b border-[#273244] pb-2 flex items-center gap-2">
          <span className="w-6 h-6 rounded-lg bg-[#090C12] text-[#06B6D4] border border-[#273244] flex items-center justify-center text-xs font-bold font-mono">2</span>
          Huffman Optimality & Sibling Exchange Argument
        </h3>
        <p className="text-xs text-[#94A3B8] leading-relaxed">
          The Huffman min-heap algorithm constructs an optimal binary tree bottom-up. The proof of optimality rests on two foundational lemmas:
        </p>
        <div className="space-y-2 text-xs">
          <div className="p-3 bg-[#090C12] rounded-xl border border-[#273244]">
            <strong className="text-[#F8FAFC] block mb-1">Lemma 1 (Greedy-Choice Property / Exchange Argument):</strong>
            <span className="text-[#94A3B8]">
              Let x and y be the two least frequent symbols in alphabet Σ. There exists an optimal prefix code tree in which x and y are sibling leaves at maximum depth. Swapping higher-frequency nodes with deeper lower-frequency nodes cannot decrease the weighted path length B(T) = Σ f(s) d(s).
            </span>
          </div>
          <div className="p-3 bg-[#090C12] rounded-xl border border-[#273244]">
            <strong className="text-[#F8FAFC] block mb-1">Lemma 2 (Optimal Substructure):</strong>
            <span className="text-[#94A3B8]">
              Replacing the two sibling leaves x and y with a composite parent node z having weight w(z) = w(x) + w(y) reduces the problem to an alphabet of size N - 1. An optimal tree for the reduced alphabet yields an optimal tree for the original alphabet by induction.
            </span>
          </div>
        </div>
      </div>

      {/* SECTION 3 */}
      <div className="bg-[#141922] rounded-2xl border border-[#273244] p-6 shadow-sm space-y-3">
        <h3 className="text-sm font-bold text-[#F8FAFC] border-b border-[#273244] pb-2 flex items-center gap-2">
          <span className="w-6 h-6 rounded-lg bg-[#090C12] text-[#06B6D4] border border-[#273244] flex items-center justify-center text-xs font-bold font-mono">3</span>
          Shannon-Fano Heuristic & Suboptimality Counterexample
        </h3>
        <p className="text-xs text-[#94A3B8] leading-relaxed">
          Shannon-Fano operates top-down, greedily partitioning sorted symbols into two groups with minimal weight difference. Because decisions made at higher levels are irreversible, it is globally suboptimal.
        </p>
        <div className="p-4 bg-[#451A03]/30 border border-[#F59E0B]/40 rounded-xl text-xs space-y-2 text-[#F8FAFC]">
          <div className="font-bold flex items-center gap-1.5 text-[#F59E0B]">
            <ShieldAlert className="w-4 h-4 text-[#F59E0B]" /> Mathematically Proven Counterexample:
          </div>
          <div>Alphabet: <strong className="text-[#F8FAFC]">Σ = [A: 35, B: 17, C: 17, D: 16, E: 15]</strong> (Sum = 100)</div>
          <div className="font-mono text-[11px] space-y-1 text-[#94A3B8]">
            <div>• Shannon-Fano top split: &#123;A, B&#125; (sum 52) vs &#123;C, D, E&#125; (sum 48) &rarr; A receives 2-bit codeword ("00") &rarr; <strong className="text-[#F59E0B]">L_SF = 2.3100 bits</strong></div>
            <div>• Huffman bottom-up merges: (15+16=31), (17+17=34), (31+34=65), (35+65=100) &rarr; A receives 1-bit codeword ("0") &rarr; <strong className="text-[#10B981]">L_Huff = 2.3000 bits</strong></div>
            <div>• Strict difference: <strong className="text-[#F59E0B]">+0.0100 bits/message deficit</strong> in Shannon-Fano.</div>
          </div>
        </div>
      </div>

      {/* SECTION 4 */}
      <div className="bg-[#141922] rounded-2xl border border-[#273244] p-6 shadow-sm space-y-3">
        <h3 className="text-sm font-bold text-[#F8FAFC] border-b border-[#273244] pb-2 flex items-center gap-2">
          <span className="w-6 h-6 rounded-lg bg-[#090C12] text-[#06B6D4] border border-[#273244] flex items-center justify-center text-xs font-bold font-mono">4</span>
          Linear-Time Huffman via Two Queues (van Leeuwen, 1976)
        </h3>
        <p className="text-xs text-[#94A3B8] leading-relaxed">
          Standard binary min-heap Huffman requires O(N log N) time due to heap adjustment operations. When initial frequencies are pre-sorted, Jan van Leeuwen proved that maintaining two FIFO queues—Queue 1 for initial leaves and Queue 2 for merged internal nodes—allows extracting the two minimum elements in O(1) time. Tree construction is strictly <strong className="text-[#06B6D4]">O(N) linear time</strong>.
        </p>
      </div>

      {/* SECTION 5 */}
      <div className="bg-[#141922] rounded-2xl border border-[#273244] p-6 shadow-sm space-y-3">
        <h3 className="text-sm font-bold text-[#F8FAFC] border-b border-[#273244] pb-2 flex items-center gap-2">
          <span className="w-6 h-6 rounded-lg bg-[#090C12] text-[#06B6D4] border border-[#273244] flex items-center justify-center text-xs font-bold font-mono">5</span>
          Length-Limited Huffman via Package-Merge (Larmore & Hirschberg, 1990)
        </h3>
        <p className="text-xs text-[#94A3B8] leading-relaxed">
          Receiver hardware registers cannot process codewords longer than 4 bits. Unconstrained Huffman produces 5-bit (`DOOR`) and 6-bit (`FAULT`, `RESET`) codewords, violating firmware register boundaries.
        </p>
        <p className="text-xs text-[#94A3B8] leading-relaxed">
          The Package-Merge algorithm reduces the length-limited prefix code problem to an integer knapsack on coin collection across L_max levels in O(N · L_max) time. Tested against an exhaustive 4^8 brute force search, Package-Merge finds the globally optimal 4-bit constrained codebook (L = 2.3000 bits/msg) with zero register overflow risk.
        </p>
      </div>
    </div>
  );
};
