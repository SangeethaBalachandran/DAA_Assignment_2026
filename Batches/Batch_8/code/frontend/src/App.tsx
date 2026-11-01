import React, { useState, useEffect } from 'react';
import {
  SymbolFrequency,
  CompressionResponse,
  TwoQueueResponse,
  AlgorithmComparisonResponse,
  NetworkMetrics
} from './types';
import { api } from './services/api';
import { OverviewView } from './views/OverviewView';
import { HuffmanEngineView } from './views/HuffmanEngineView';
import { AlgorithmLabView } from './views/AlgorithmLabView';
import { LiveNetworkView } from './views/LiveNetworkView';
import { HardwareInspectorView } from './views/HardwareInspectorView';
import { CodebookManagementView } from './views/CodebookManagementView';
import { DocumentationView } from './views/DocumentationView';
import {
  LayoutDashboard,
  GitBranch,
  Code2,
  Radio,
  Cpu,
  BookOpen,
  FileText,
  Menu,
  X,
  Share2
} from 'lucide-react';

const DEFAULT_DIST: SymbolFrequency[] = [
  { symbol: "OK", frequency: 52 },
  { symbol: "TEMP_HI", frequency: 14 },
  { symbol: "TEMP_LO", frequency: 11 },
  { symbol: "HUM", frequency: 9 },
  { symbol: "VIB", frequency: 7 },
  { symbol: "DOOR", frequency: 4 },
  { symbol: "FAULT", frequency: 2 },
  { symbol: "RESET", frequency: 1 },
];

export function App() {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [frequencies, setFrequencies] = useState<SymbolFrequency[]>(DEFAULT_DIST);
  const [packageMergeLimit, setPackageMergeLimit] = useState<number>(4);
  const [mobileMenuOpen, setMobileMenuOpen] = useState<boolean>(false);

  const [huffmanData, setHuffmanData] = useState<CompressionResponse | undefined>();
  const [packageMergeData, setPackageMergeData] = useState<CompressionResponse | undefined>();
  const [comparisonData, setComparisonData] = useState<AlgorithmComparisonResponse | undefined>();
  const [twoQueueData, setTwoQueueData] = useState<TwoQueueResponse | undefined>();
  const [networkMetrics, setNetworkMetrics] = useState<NetworkMetrics | undefined>();
  const [loading, setLoading] = useState<boolean>(true);

  // Re-fetch all dependent algorithms whenever frequencies change
  useEffect(() => {
    refreshAllData(frequencies, packageMergeLimit);
  }, [frequencies, packageMergeLimit]);

  const refreshAllData = async (freqs: SymbolFrequency[], pmLimit: number) => {
    try {
      setLoading(true);
      const [huff, pm, comp, tq, net] = await Promise.all([
        api.generateHuffman(freqs),
        api.generatePackageMerge(freqs, pmLimit),
        api.compareAlgorithms(freqs),
        api.generateTwoQueue(freqs),
        api.getNetworkMetrics()
      ]);
      setHuffmanData(huff);
      setPackageMergeData(pm);
      setComparisonData(comp);
      setTwoQueueData(tq);
      setNetworkMetrics(net);
    } catch (err) {
      console.error("Error refreshing backend algorithm data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleResetFrequencies = () => {
    setFrequencies(DEFAULT_DIST);
  };

  const handleLoadPreset = async (presetName: string) => {
    if (presetName === 'counterexample') {
      const res = await api.getCounterexample('8-symbol');
      setFrequencies(res.distribution);
    }
  };

  const navItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'huffman', label: 'Huffman Engine', icon: GitBranch },
    { id: 'lab', label: 'Algorithm Lab', icon: Code2 },
    { id: 'live', label: 'Live Network', icon: Radio },
    { id: 'hardware', label: 'Hardware Inspector', icon: Cpu },
    { id: 'codebook', label: 'Codebook Manager', icon: BookOpen },
    { id: 'docs', label: 'Docs', icon: FileText },
  ];

  return (
    <div className="min-h-screen bg-[#0F1117] text-[#F8FAFC] flex font-sans">
      {/* ============================================================ */}
      {/* FIXED LEFT SIDEBAR (DESKTOP)                                 */}
      {/* ============================================================ */}
      <aside className="hidden md:flex flex-col w-56 bg-[#090C12] border-r border-[#273244] fixed top-0 bottom-0 left-0 z-40">
        {/* Brand Header */}
        <div className="h-16 flex items-center gap-2.5 px-5 border-b border-[#273244]/60">
          <div className="w-7 h-7 rounded-lg bg-[#06B6D4]/15 border border-[#06B6D4]/30 flex items-center justify-center text-[#06B6D4]">
            <Share2 className="w-4 h-4" />
          </div>
          <span className="font-bold text-[#F8FAFC] text-base tracking-tight">
            IoTCompress
          </span>
        </div>

        {/* Navigation Item List */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-[#0E3A43] text-[#06B6D4] shadow-xs'
                    : 'text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#141922]'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-[#06B6D4]' : 'text-[#64748B]'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Sidebar Footer Info */}
        <div className="p-4 border-t border-[#273244]/60 text-[11px] text-[#64748B] space-y-1">
          <div className="text-[#94A3B8] font-medium">IoT-Gateway-01</div>
          <div className="font-mono text-[10px]">9.6 kbps · 5k Sensors</div>
        </div>
      </aside>

      {/* ============================================================ */}
      {/* MOBILE DRAWER / HEADER                                       */}
      {/* ============================================================ */}
      <div className="md:hidden fixed top-0 left-0 right-0 h-14 bg-[#090C12] border-b border-[#273244] z-50 flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded bg-[#06B6D4]/15 border border-[#06B6D4]/30 flex items-center justify-center text-[#06B6D4]">
            <Share2 className="w-3.5 h-3.5" />
          </div>
          <span className="font-bold text-sm text-[#F8FAFC]">IoTCompress</span>
        </div>
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="p-1.5 rounded-lg bg-[#141922] text-[#94A3B8] border border-[#273244]"
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {mobileMenuOpen && (
        <div className="md:hidden fixed inset-0 z-40 bg-[#090C12] pt-16 px-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id);
                  setMobileMenuOpen(false);
                }}
                className={`w-full flex items-center gap-3 px-3 py-3 rounded-xl text-xs font-semibold ${
                  isActive ? 'bg-[#0E3A43] text-[#06B6D4]' : 'text-[#94A3B8]'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      )}

      {/* ============================================================ */}
      {/* MAIN CONTENT AREA (SINGLE COLUMN VERTICALLY STACKED)         */}
      {/* ============================================================ */}
      <main className="flex-1 md:ml-56 min-h-screen p-4 sm:p-6 lg:p-7 pt-18 md:pt-6 overflow-y-auto">
        <div className="max-w-[1400px] mx-auto w-full">
          {loading && !huffmanData && (
            <div className="py-24 flex flex-col items-center justify-center gap-3 text-[#94A3B8] text-xs">
              <div className="w-6 h-6 border-2 border-[#06B6D4] border-t-transparent rounded-full animate-spin"></div>
              <span>Evaluating optimal prefix codes on FastAPI backend...</span>
            </div>
          )}

          {activeTab === 'overview' && (
            <OverviewView
              frequencies={frequencies}
              huffmanData={huffmanData}
              packageMergeData={packageMergeData}
              networkMetrics={networkMetrics}
              onNavigate={setActiveTab}
            />
          )}

          {activeTab === 'huffman' && (
            <HuffmanEngineView
              frequencies={frequencies}
              huffmanData={huffmanData}
              onFrequencyChange={setFrequencies}
              onResetFrequencies={handleResetFrequencies}
              onLoadPreset={handleLoadPreset}
            />
          )}

          {activeTab === 'lab' && (
            <AlgorithmLabView
              frequencies={frequencies}
              comparisonData={comparisonData}
              twoQueueData={twoQueueData}
              onLoadFrequencies={setFrequencies}
            />
          )}

          {activeTab === 'live' && (
            <LiveNetworkView
              initialMetrics={networkMetrics}
            />
          )}

          {activeTab === 'hardware' && (
            <HardwareInspectorView
              frequencies={frequencies}
              huffmanData={huffmanData}
              packageMergeData={packageMergeData}
              onRefreshPackageMerge={setPackageMergeLimit}
            />
          )}

          {activeTab === 'codebook' && (
            <CodebookManagementView />
          )}

          {activeTab === 'docs' && (
            <DocumentationView />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
