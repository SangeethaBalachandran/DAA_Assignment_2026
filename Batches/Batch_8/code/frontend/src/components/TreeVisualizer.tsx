import React, { useMemo } from 'react';
import {
  ReactFlow,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  MarkerType
} from '@xyflow/react';
import { TreeNode } from '../types';

interface TreeVisualizerProps {
  treeData?: TreeNode;
  title?: string;
  algorithmName?: string;
}

export const TreeVisualizer: React.FC<TreeVisualizerProps> = ({
  treeData,
  title = "Binary Prefix Tree",
  algorithmName = "Huffman"
}) => {
  const { initialNodes, initialEdges } = useMemo(() => {
    if (!treeData) return { initialNodes: [], initialEdges: [] };

    const nodes: Node[] = [];
    const edges: Edge[] = [];

    function getLeafCount(node: TreeNode): number {
      if (!node.children || node.children.length === 0) return 1;
      return node.children.reduce((acc, child) => acc + getLeafCount(child), 0);
    }

    function layout(
      node: TreeNode,
      xMin: number,
      xMax: number,
      depth: number,
      parentId?: string,
      bitLabel?: string
    ) {
      const x = (xMin + xMax) / 2;
      const y = depth * 80 + 30;

      const isLeaf = !!node.symbol;
      const label = (
        <div className={`p-2 rounded-xl border text-center transition-all ${
          isLeaf
            ? node.symbol === 'OK' || node.code?.length === 1
              ? 'bg-[#064E3B] border-[#10B981] text-[#A7F3D0] shadow-xs'
              : node.code && node.code.length > 4
              ? 'bg-[#450A0A] border-[#EF4444] text-[#FECACA] shadow-xs'
              : node.code && node.code.length === 4
              ? 'bg-[#451A03] border-[#F59E0B] text-[#FDE68A] shadow-xs'
              : 'bg-[#0E3A43] border-[#06B6D4] text-[#A5F3FC] shadow-xs'
            : 'bg-[#141922] border-[#273244] text-[#F8FAFC] shadow-xs'
        }`}>
          <div className="text-[11px] font-semibold tracking-tight font-sans">
            {node.symbol ? node.symbol : node.name}
          </div>
          <div className="text-[10px] text-[#94A3B8] font-mono">
            wt: {node.weight}
          </div>
          {node.code && (
            <div className="mt-1 px-1.5 py-0.5 bg-[#090C12]/80 rounded font-mono text-[10px] font-bold text-[#06B6D4] border border-[#06B6D4]/30">
              {node.code}
            </div>
          )}
        </div>
      );

      nodes.push({
        id: node.id,
        position: { x, y },
        data: { label },
        style: { width: 100, padding: 0, border: 'none', background: 'transparent' }
      });

      if (parentId) {
        edges.push({
          id: `e-${parentId}-${node.id}`,
          source: parentId,
          target: node.id,
          label: bitLabel || '',
          labelStyle: { fill: bitLabel === '0' ? '#06B6D4' : '#10B981', fontWeight: 700, fontSize: 11 },
          labelBgStyle: { fill: '#090C12', fillOpacity: 0.9 },
          labelBgPadding: [3, 2],
          labelBgBorderRadius: 4,
          style: { stroke: '#334155', strokeWidth: 1.5 },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 10,
            height: 10,
            color: '#334155'
          }
        });
      }

      if (node.children && node.children.length > 0) {
        const leftCount = getLeafCount(node.children[0]);
        const rightCount = node.children.length > 1 ? getLeafCount(node.children[1]) : 1;
        const total = leftCount + rightCount;
        const splitX = xMin + (xMax - xMin) * (leftCount / total);

        layout(node.children[0], xMin, splitX, depth + 1, node.id, "0");
        if (node.children.length > 1) {
          layout(node.children[1], splitX, xMax, depth + 1, node.id, "1");
        }
      }
    }

    layout(treeData, 0, 780, 0);

    return { initialNodes: nodes, initialEdges: edges };
  }, [treeData]);

  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  if (!treeData) {
    return (
      <div className="h-[420px] flex items-center justify-center bg-[#141922] rounded-2xl border border-[#273244] text-[#64748B] text-sm">
        No tree structure available.
      </div>
    );
  }

  return (
    <div className="bg-[#141922] rounded-2xl border border-[#273244] p-4 shadow-sm">
      <div className="flex items-center justify-between pb-3 border-b border-[#273244] mb-2">
        <div>
          <h3 className="text-sm font-bold text-[#F8FAFC]">{title}</h3>
          <p className="text-xs text-[#94A3B8]">Interactive prefix code structure • Root Σ={treeData.weight}</p>
        </div>
        <span className="px-2.5 py-1 text-xs font-semibold bg-[#0E3A43] text-[#06B6D4] rounded-lg border border-[#06B6D4]/30">
          {algorithmName}
        </span>
      </div>
      <div className="h-[440px] w-full rounded-xl bg-[#090C12]/90 overflow-hidden border border-[#273244]">
        <ReactFlow
          nodes={initialNodes}
          edges={initialEdges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
          minZoom={0.2}
          maxZoom={1.5}
          attributionPosition="bottom-right"
        >
          <Background color="#273244" gap={16} size={1} />
          <Controls showInteractive={false} className="bg-[#141922] border border-[#273244] shadow-sm rounded-lg text-[#F8FAFC]" />
        </ReactFlow>
      </div>
      <div className="mt-3 flex items-center justify-between text-xs text-[#94A3B8] px-1">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#10B981]"></span> Nominal (&le;3b)</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#F59E0B]"></span> 4-bit limit</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#EF4444]"></span> Overflow (&gt;4b)</span>
        </div>
        <span className="font-mono text-[#06B6D4]">Labels: 0 (Left), 1 (Right)</span>
      </div>
    </div>
  );
};
