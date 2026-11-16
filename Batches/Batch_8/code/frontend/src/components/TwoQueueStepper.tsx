import React, { useState } from 'react';
import { TwoQueueStep } from '../types';
import { ChevronLeft, ChevronRight, RotateCcw } from 'lucide-react';

interface TwoQueueStepperProps {
  steps: TwoQueueStep[];
  huffmanOps: number;
  twoQueueOps: number;
}

export const TwoQueueStepper: React.FC<TwoQueueStepperProps> = ({
  steps
}) => {
  const [currentStep, setCurrentStep] = useState<number>(0);

  const totalSteps = steps.length;
  const activeStep = steps[currentStep] || steps[0];

  const handleNext = () => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const handleReset = () => {
    setCurrentStep(0);
  };

  return (
    <div className="bg-[#141922] rounded-2xl border border-[#273244] p-5 shadow-sm space-y-5 text-[#F8FAFC]">
      <div className="flex items-center justify-between pb-3 border-b border-[#273244]">
        <div>
          <h3 className="text-sm font-bold text-[#F8FAFC]">Two-Queue Linear-Time Merge Inspector</h3>
          <p className="text-xs text-[#94A3B8]">
            Step-by-step state of Queue 1 (Leaves) and Queue 2 (Internal Nodes) during O(N) tree construction
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-xs font-mono bg-[#06B6D4]/15 text-[#06B6D4] px-2.5 py-1 rounded-lg border border-[#06B6D4]/30">
            Step {currentStep + 1} of {totalSteps}
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={handlePrev}
              disabled={currentStep === 0}
              className="p-1.5 bg-[#090C12] hover:bg-[#1E293B] disabled:opacity-40 rounded-lg text-[#94A3B8] border border-[#273244] transition-colors cursor-pointer"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={handleNext}
              disabled={currentStep === totalSteps - 1}
              className="p-1.5 bg-[#090C12] hover:bg-[#1E293B] disabled:opacity-40 rounded-lg text-[#94A3B8] border border-[#273244] transition-colors cursor-pointer"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
            <button
              onClick={handleReset}
              className="p-1.5 bg-[#090C12] hover:bg-[#1E293B] rounded-lg text-[#94A3B8] border border-[#273244] transition-colors ml-1 cursor-pointer"
              title="Reset to step 1"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {activeStep && (
        <div className="space-y-4">
          <div className="p-3 bg-[#06B6D4]/10 border border-[#06B6D4]/20 rounded-xl text-xs text-[#06B6D4] leading-relaxed font-medium">
            {activeStep.description}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* QUEUE 1: LEAF NODES */}
            <div className="p-4 bg-[#090C12] border border-[#273244] rounded-xl">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-[#F8FAFC] flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#10B981]"></span>
                  Queue 1: Presorted Leaf Nodes
                </span>
                <span className="text-[11px] font-mono text-[#94A3B8]">{activeStep.q1_before.length} items</span>
              </div>
              <div className="min-h-[70px] flex flex-wrap gap-1.5 items-center p-2.5 bg-[#141922] rounded-lg border border-[#273244]/60">
                {activeStep.q1_before.length > 0 ? (
                  activeStep.q1_before.map((item, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-1 bg-[#10B981]/15 text-[#10B981] border border-[#10B981]/30 text-xs font-mono rounded font-semibold"
                    >
                      {item}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-[#64748B] italic">Queue 1 is empty (all leaves merged)</span>
                )}
              </div>
            </div>

            {/* QUEUE 2: MERGED INTERNAL NODES */}
            <div className="p-4 bg-[#090C12] border border-[#273244] rounded-xl">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold text-[#F8FAFC] flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#06B6D4]"></span>
                  Queue 2: Generated Internal Nodes
                </span>
                <span className="text-[11px] font-mono text-[#94A3B8]">{activeStep.q2_before.length} items</span>
              </div>
              <div className="min-h-[70px] flex flex-wrap gap-1.5 items-center p-2.5 bg-[#141922] rounded-lg border border-[#273244]/60">
                {activeStep.q2_before.length > 0 ? (
                  activeStep.q2_before.map((item, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-1 bg-[#06B6D4]/15 text-[#06B6D4] border border-[#06B6D4]/30 text-xs font-mono rounded font-semibold"
                    >
                      {item}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-[#64748B] italic">Queue 2 initialized empty</span>
                )}
              </div>
            </div>
          </div>

          {/* MERGE ACTION CALLOUT */}
          <div className="p-3.5 bg-[#090C12] border border-[#273244] rounded-xl flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-[#94A3B8]">Popped Min Candidates:</span>
              <span className="px-2 py-0.5 bg-[#141922] border border-[#273244] rounded font-mono font-bold text-[#F8FAFC]">{activeStep.popped[0]}</span>
              <span className="text-[#64748B] font-bold">+</span>
              <span className="px-2 py-0.5 bg-[#141922] border border-[#273244] rounded font-mono font-bold text-[#F8FAFC]">{activeStep.popped[1]}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-[#94A3B8]">Enqueued to Q2:</span>
              <span className="px-2.5 py-0.5 bg-[#06B6D4] text-[#090C12] rounded font-mono font-bold">{activeStep.result_node}</span>
            </div>
          </div>
        </div>
      )}

      {/* COMPLEXITY COMPARISON FOOTER */}
      <div className="pt-3 border-t border-[#273244] grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
        <div className="p-2.5 bg-[#090C12] border border-[#273244] rounded-lg">
          <div className="text-[#64748B]">Two-Queue Complexity</div>
          <div className="font-mono font-bold text-[#06B6D4]">O(N) Linear Time</div>
        </div>
        <div className="p-2.5 bg-[#090C12] border border-[#273244] rounded-lg">
          <div className="text-[#64748B]">Min-Heap Complexity</div>
          <div className="font-mono font-bold text-[#F8FAFC]">O(N log N)</div>
        </div>
        <div className="p-2.5 bg-[#090C12] border border-[#273244] rounded-lg">
          <div className="text-[#64748B]">Merge Operations</div>
          <div className="font-mono font-bold text-[#06B6D4]">{totalSteps} merges (N-1)</div>
        </div>
        <div className="p-2.5 bg-[#090C12] border border-[#273244] rounded-lg">
          <div className="text-[#64748B]">Monotonicity Invariant</div>
          <div className="font-mono font-bold text-[#10B981]">Guaranteed by Induction</div>
        </div>
      </div>
    </div>
  );
};
