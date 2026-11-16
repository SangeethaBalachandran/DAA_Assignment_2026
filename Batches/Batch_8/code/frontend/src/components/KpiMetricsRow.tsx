import React from 'react';
import { CompressionResponse, NetworkMetrics } from '../types';

interface KpiMetricsRowProps {
  huffmanData?: CompressionResponse;
  networkMetrics?: NetworkMetrics;
}

export const KpiMetricsRow: React.FC<KpiMetricsRowProps> = ({
  huffmanData
}) => {
  const avgLen = huffmanData?.average_length ? huffmanData.average_length.toFixed(2) : "2.20";
  const entropy = huffmanData?.entropy ? huffmanData.entropy.toFixed(2) : "2.18";
  const efficiency = huffmanData?.efficiency ? huffmanData.efficiency.toFixed(2) : "99.29";
  const savingsPct = huffmanData?.bandwidth_savings_pct ? huffmanData.bandwidth_savings_pct.toFixed(2) : "26.67";

  const cards = [
    {
      name: "Average Code Length",
      value: avgLen,
      unit: "bits",
      valueColor: "text-[#06B6D4]"
    },
    {
      name: "Shannon Entropy",
      value: entropy,
      unit: "bits",
      valueColor: "text-[#06B6D4]"
    },
    {
      name: "Coding Efficiency",
      value: `${efficiency}%`,
      unit: "",
      valueColor: "text-[#10B981]"
    },
    {
      name: "Bandwidth Saved",
      value: `${savingsPct}%`,
      unit: "",
      valueColor: "text-[#10B981]"
    }
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, idx) => (
        <div
          key={idx}
          className="bg-[#141922] border border-[#273244] rounded-xl p-4 shadow-sm"
        >
          <div className="text-xs font-medium text-[#94A3B8]">{card.name}</div>
          <div className="mt-2 text-2xl font-bold font-mono tracking-tight flex items-baseline gap-1">
            <span className={card.valueColor}>{card.value}</span>
            {card.unit && (
              <span className="text-xs font-normal font-sans text-[#94A3B8]">{card.unit}</span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};
