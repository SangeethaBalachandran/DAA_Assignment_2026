import React, { useState } from 'react';
import { api } from '../services/api';
import { Play, RotateCw, Copy, Check, AlertCircle } from 'lucide-react';

interface MessageCodecProps {
  codebookMap: Record<string, string>;
  algorithmName?: string;
}

export const MessageCodec: React.FC<MessageCodecProps> = ({
  codebookMap,
  algorithmName = "Huffman"
}) => {
  const [inputMessages, setInputMessages] = useState<string>("OK OK TEMP_HI OK OK VIB HUM OK FAULT RESET OK");
  const [encodedStream, setEncodedStream] = useState<string>("");
  const [encodingStats, setEncodingStats] = useState<any>(null);
  const [encodeError, setEncodeError] = useState<string>("");

  const [decodeStream, setDecodeStream] = useState<string>("");
  const [decodedSymbols, setDecodedSymbols] = useState<string[]>([]);
  const [decodeError, setDecodeError] = useState<string>("");
  const [decodeVersion, setDecodeVersion] = useState<string>("v1.0.0");
  const [copied, setCopied] = useState(false);

  const presets = [
    { label: "Nominal Baseline", text: "OK OK OK OK OK OK OK OK" },
    { label: "Thermal Warning", text: "OK TEMP_HI TEMP_HI OK OK TEMP_LO OK OK" },
    { label: "Inverter Fault", text: "OK VIB DOOR FAULT RESET OK OK" },
    { label: "Mixed Stream", text: "OK OK TEMP_HI HUM OK VIB DOOR OK FAULT" }
  ];

  const handleEncode = async () => {
    try {
      setEncodeError("");
      const tokens = inputMessages.trim().split(/\s+/).filter(Boolean);
      if (tokens.length === 0) return;

      const res = await api.encode(tokens, codebookMap, algorithmName.toLowerCase().includes('package') ? 'package_merge' : 'huffman');
      setEncodedStream(res.encoded_bitstream);
      setEncodingStats(res);
      setDecodeStream(res.encoded_bitstream);
    } catch (err: any) {
      setEncodeError(err.message || "Failed to encode telemetry message.");
    }
  };

  const handleDecode = async () => {
    try {
      setDecodeError("");
      if (!decodeStream.trim()) return;

      const res = await api.decode(decodeStream.trim(), codebookMap, decodeVersion || undefined);
      if (res.success) {
        setDecodedSymbols(res.decoded_symbols);
      } else {
        setDecodeError(res.error || "Decoding failed.");
      }
    } catch (err: any) {
      setDecodeError(err.message || "Decoding error.");
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(encodedStream);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-[#141922] rounded-2xl border border-[#273244] p-5 shadow-sm space-y-6">
      <div className="pb-3 border-b border-[#273244] flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-[#F8FAFC]">Telemetry Message Encoder & Decoder</h3>
          <p className="text-xs text-[#94A3B8]">
            Real-time prefix encoding and instantaneous symbol-by-symbol reconstruction
          </p>
        </div>
        <span className="px-2.5 py-1 text-xs font-semibold bg-[#090C12] text-[#06B6D4] border border-[#273244] rounded-lg">
          Codec: {algorithmName}
        </span>
      </div>

      {/* ENCODER */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-xs font-bold text-[#F8FAFC]">1. Transmit Telemetry Sequence</label>
          <div className="flex items-center gap-1.5">
            {presets.map(p => (
              <button
                key={p.label}
                onClick={() => { setInputMessages(p.text); }}
                className="px-2 py-0.5 text-[11px] font-medium bg-[#090C12] hover:bg-[#1E293B] text-[#94A3B8] hover:text-[#F8FAFC] border border-[#273244] rounded transition-colors cursor-pointer"
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={inputMessages}
            onChange={(e) => setInputMessages(e.target.value)}
            placeholder="Space-separated status symbols (e.g. OK TEMP_HI VIB FAULT)"
            className="flex-1 px-3 py-2 bg-[#090C12] border border-[#273244] rounded-xl text-xs font-mono text-[#F8FAFC] focus:outline-none focus:ring-1 focus:ring-[#06B6D4]"
          />
          <button
            onClick={handleEncode}
            className="px-4 py-2 bg-[#06B6D4] hover:bg-[#0891B2] text-[#090C12] font-bold text-xs rounded-xl transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer"
          >
            <Play className="w-3.5 h-3.5 fill-current" /> Encode
          </button>
        </div>

        {encodeError && (
          <div className="p-3 bg-[#450A0A] border border-[#EF4444] text-[#FECACA] rounded-xl text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-[#EF4444]" />
            <span>{encodeError}</span>
          </div>
        )}

        {encodingStats && (
          <div className="p-4 bg-[#090C12] border border-[#273244] rounded-xl space-y-3">
            <div className="flex flex-wrap items-center justify-between text-xs text-[#94A3B8] gap-2">
              <span>Messages: <strong className="text-[#F8FAFC]">{encodingStats.message_count}</strong></span>
              <span>Original: <strong className="text-[#F8FAFC] font-mono">{encodingStats.original_bits} bits</strong> (3b fixed)</span>
              <span>Compressed: <strong className="text-[#10B981] font-mono">{encodingStats.compressed_bits} bits</strong></span>
              <span>Savings: <strong className="text-[#10B981]">{encodingStats.bandwidth_saved_pct}%</strong></span>
              <span>Ratio: <strong className="text-[#06B6D4]">{encodingStats.compression_ratio}:1</strong></span>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1 text-[11px] font-medium text-[#94A3B8]">
                <span>Output Bitstream:</span>
                <button
                  onClick={copyToClipboard}
                  className="flex items-center gap-1 text-[#06B6D4] hover:text-[#38BDF8] font-medium cursor-pointer"
                >
                  {copied ? <Check className="w-3 h-3 text-[#10B981]" /> : <Copy className="w-3 h-3" />}
                  {copied ? "Copied" : "Copy Bitstream"}
                </button>
              </div>
              <div className="p-2.5 bg-[#141922] border border-[#273244] rounded-lg font-mono text-xs text-[#06B6D4] break-all select-all leading-relaxed tracking-wider">
                {encodedStream}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* DECODER */}
      <div className="pt-4 border-t border-[#273244] space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-xs font-bold text-[#F8FAFC]">2. Receiver Bitstream Decoder</label>
          <div className="flex items-center gap-2 text-xs">
            <span className="text-[#94A3B8]">Receiver Codebook Version:</span>
            <input
              type="text"
              value={decodeVersion}
              onChange={(e) => setDecodeVersion(e.target.value)}
              placeholder="e.g. v1.0.0"
              className="w-20 px-2 py-0.5 bg-[#090C12] border border-[#273244] rounded font-mono text-xs text-center text-[#F8FAFC]"
            />
          </div>
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={decodeStream}
            onChange={(e) => setDecodeStream(e.target.value)}
            placeholder="Binary bitstream (e.g. 101011100010)"
            className="flex-1 px-3 py-2 bg-[#090C12] border border-[#273244] rounded-xl text-xs font-mono text-[#F8FAFC] focus:outline-none focus:ring-1 focus:ring-[#06B6D4]"
          />
          <button
            onClick={handleDecode}
            className="px-4 py-2 bg-[#1E293B] hover:bg-[#334155] text-[#F8FAFC] font-medium text-xs rounded-xl transition-colors flex items-center gap-1.5 shadow-xs cursor-pointer border border-[#273244]"
          >
            <RotateCw className="w-3.5 h-3.5" /> Decode Stream
          </button>
        </div>

        {decodeError && (
          <div className="p-3 bg-[#451A03] border border-[#F59E0B] text-[#FDE68A] rounded-xl text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-[#F59E0B]" />
            <span>{decodeError}</span>
          </div>
        )}

        {decodedSymbols.length > 0 && !decodeError && (
          <div className="p-3 bg-[#064E3B]/40 border border-[#10B981]/60 rounded-xl">
            <div className="text-[11px] font-semibold text-[#10B981] mb-1.5 flex items-center gap-1.5">
              <Check className="w-3.5 h-3.5 text-[#10B981]" /> Losslessly Decoded {decodedSymbols.length} Telemetry Messages:
            </div>
            <div className="flex flex-wrap gap-1.5">
              {decodedSymbols.map((s, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 bg-[#090C12] border border-[#10B981]/40 rounded text-xs font-mono font-semibold text-[#A7F3D0]"
                >
                  {s}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
