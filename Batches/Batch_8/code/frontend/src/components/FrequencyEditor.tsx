import React from 'react';
import { SymbolFrequency } from '../types';
import { RotateCcw, Sparkles } from 'lucide-react';

interface FrequencyEditorProps {
  frequencies: SymbolFrequency[];
  onChange: (newFreqs: SymbolFrequency[]) => void;
  onReset: () => void;
  onLoadPreset?: (presetName: string) => void;
}

export const FrequencyEditor: React.FC<FrequencyEditorProps> = ({
  frequencies,
  onChange,
  onReset,
  onLoadPreset
}) => {
  const total = frequencies.reduce((acc, curr) => acc + (Number(curr.frequency) || 0), 0);

  const handleFrequencyChange = (index: number, val: string) => {
    const num = Math.max(0, parseFloat(val) || 0);
    const updated = frequencies.map((item, i) =>
      i === index ? { ...item, frequency: num } : item
    );
    onChange(updated);
  };

  return (
    <div className="bg-[#141922] rounded-2xl border border-[#273244] p-5 shadow-sm">
      <div className="flex items-center justify-between pb-4 border-b border-[#273244]">
        <div>
          <h3 className="text-sm font-bold text-[#F8FAFC]">Telemetry Frequency Distribution</h3>
          <p className="text-xs text-[#94A3B8]">
            Observed status counts per 100 messages • Normalized automatically
          </p>
        </div>
        <div className="flex items-center gap-2">
          {onLoadPreset && (
            <div className="flex items-center gap-1.5">
              <button
                onClick={() => onLoadPreset('counterexample')}
                className="px-2.5 py-1 text-xs font-medium text-[#F59E0B] bg-[#451A03]/60 hover:bg-[#451A03] rounded-lg border border-[#F59E0B]/40 transition-colors flex items-center gap-1 cursor-pointer"
                title="Load proven Shannon-Fano counterexample"
              >
                <Sparkles className="w-3.5 h-3.5" /> Counterexample
              </button>
            </div>
          )}
          <button
            onClick={onReset}
            className="px-2.5 py-1 text-xs font-medium text-[#94A3B8] hover:text-[#F8FAFC] bg-[#090C12] hover:bg-[#1E293B] border border-[#273244] rounded-lg transition-colors flex items-center gap-1 cursor-pointer"
          >
            <RotateCcw className="w-3 h-3" /> Reset Default
          </button>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-3">
        {frequencies.map((item, index) => {
          const prob = total > 0 ? (item.frequency / total) : 0;
          return (
            <div
              key={item.symbol}
              className="p-3 bg-[#090C12] border border-[#273244] rounded-xl hover:border-[#06B6D4]/50 transition-colors"
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-mono text-xs font-bold text-[#F8FAFC]">{item.symbol}</span>
                <span className="text-[11px] font-mono text-[#06B6D4]">p={prob.toFixed(3)}</span>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="number"
                  min="0"
                  step="1"
                  value={item.frequency}
                  onChange={(e) => handleFrequencyChange(index, e.target.value)}
                  className="w-full px-2.5 py-1 bg-[#141922] border border-[#273244] rounded-lg text-xs font-mono font-semibold text-[#F8FAFC] focus:outline-none focus:ring-1 focus:ring-[#06B6D4] focus:border-[#06B6D4]"
                />
                <span className="text-xs text-[#64748B] font-medium">%</span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-4 pt-3 border-t border-[#273244] flex items-center justify-between text-xs">
        <div className="flex items-center gap-4 text-[#94A3B8]">
          <span>Total Frequency: <strong className="font-mono text-[#F8FAFC]">{total}</strong></span>
          <span>Sum of Probabilities: <strong className="font-mono text-[#10B981]">{total > 0 ? (1.0).toFixed(4) : '0.0000'}</strong></span>
        </div>
        <span className="text-[11px] text-[#64748B]">
          Source: Calibrated 1-Hour Operational Sample (5,000 sensors)
        </span>
      </div>
    </div>
  );
};
