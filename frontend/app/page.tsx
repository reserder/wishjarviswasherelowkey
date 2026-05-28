"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Mic, Activity, Zap, Cpu, Search, Fingerprint, Layers } from "lucide-react";

export default function AegisDashboard() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ role: string; content: string; agent?: string; trace?: string[] }[]>([
    { role: "system", content: "AEGIS ORBIT ACTIVE. NEURAL LINK ESTABLISHED." },
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleExecute = async () => {
    if (!input.trim()) return;
    const userGoal = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userGoal }]);
    setIsProcessing(true);

    try {
      const res = await fetch("http://127.0.0.1:8001/orbit/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal: userGoal }),
      });
      const data = await res.json();
      
      setMessages((prev) => [
        ...prev,
        { 
          role: "aegis", 
          content: data.response, 
          agent: data.agent,
          trace: ["Context compressed", "DeepSeek Reasoner Engaged", "Fact-check verified"] // Mocking trace for UI
        },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "system", content: "CRITICAL FAULT: Connection to Core Backend Lost. Verify ./start-native.sh is running." },
      ]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-slate-200 font-sans selection:bg-cyan-900 overflow-hidden flex selection:text-cyan-50">
      {/* Background Ambience */}
      <div className="fixed inset-0 z-0 opacity-20 pointer-events-none bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-cyan-900/40 via-black to-black"></div>

      {/* Sidebar: Features & Connectors */}
      <aside className="w-80 border-r border-white/5 bg-white/[0.02] backdrop-blur-3xl z-10 flex flex-col p-6 space-y-8">
        <div className="flex items-center space-x-3 text-cyan-400 font-medium tracking-widest text-sm uppercase">
          <Fingerprint className="w-5 h-5" />
          <span>Aegis Modules</span>
        </div>

        <div className="space-y-4 flex-1">
          <ModuleCard icon={<Cpu />} name="Orbit Core" status="ONLINE" />
          <ModuleCard icon={<Layers />} name="Forge Architect" status="ACTIVE" desc="Recursive Agency" />
          <ModuleCard icon={<Zap />} name="Evolver" status="HARVESTING" desc="GitHub Open Design" />
          <ModuleCard icon={<Mic />} name="Voice Gateway" status="READY" desc="Alexa / Twilio" />
        </div>

        <div className="pt-6 border-t border-white/5 space-y-4">
          <div className="text-xs text-slate-500 uppercase tracking-widest font-semibold flex items-center justify-between">
            <span>Connectors</span>
            <span className="text-[10px] bg-cyan-500/10 text-cyan-400 px-2 rounded cursor-pointer hover:bg-cyan-500/20">Marketplace</span>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <ConnectorButton name="Drive" status="Add" color="amber" />
            <ConnectorButton name="GitHub" status="Active" color="emerald" />
            <ConnectorButton name="Search" status="Add" color="blue" />
            <ConnectorButton name="Gmail" status="Add" color="red" />
          </div>
        </div>

        <div className="pt-6 border-t border-white/5 space-y-4">
          <div className="text-xs text-slate-500 uppercase tracking-widest font-semibold">Intelligence Hub</div>
          <div className="flex justify-between items-center text-sm">
            <span className="text-slate-400">Memory (Qdrant)</span>
            <span className="text-emerald-400 flex items-center"><div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-2 animate-pulse"></div> SYNCED</span>
          </div>
          <div className="flex justify-between items-center text-sm">
            <span className="text-slate-400">Models</span>
            <span className="text-cyan-400 font-mono text-xs">deepseek, gemma</span>
          </div>
        </div>
      </aside>

      {/* Main Interface */}
      <main className="flex-1 flex flex-col z-10 relative">
        {/* Header */}
        <header className="h-20 flex items-center px-8 border-b border-white/5 justify-between">
          <h1 className="text-xl font-light tracking-[0.2em] text-white">ORBIT <span className="text-cyan-500 font-semibold">OS</span></h1>
          <div className="flex items-center space-x-4 text-xs font-mono text-slate-500">
            <span>RAM: 11.2/16GB</span>
            <span>LATENCY: &lt;2ms</span>
          </div>
        </header>

        {/* Neural Canvas (Terminal Area) */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8 custom-scrollbar">
          <AnimatePresence>
            {messages.map((msg, i) => (
              <motion.div 
                initial={{ opacity: 0, y: 10 }} 
                animate={{ opacity: 1, y: 0 }} 
                key={i}
                className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
              >
                {msg.role === 'aegis' && (
                  <div className="flex items-center space-x-2 text-cyan-500 text-xs font-mono mb-2 tracking-widest uppercase">
                    <Activity className="w-3 h-3" />
                    <span>AGENT: {msg.agent || 'ORBIT'}</span>
                  </div>
                )}
                
                <div className={`max-w-3xl p-5 rounded-2xl text-sm leading-relaxed backdrop-blur-md ${
                  msg.role === 'user' ? 'bg-cyan-900/20 text-cyan-50 border border-cyan-500/20 rounded-tr-sm' : 
                  msg.role === 'system' ? 'bg-red-900/10 text-red-400 border border-red-500/20 font-mono text-xs w-full' :
                  'bg-white/5 text-slate-300 border border-white/10 rounded-tl-sm shadow-2xl shadow-cyan-900/10'
                }`}>
                  {msg.content}
                </div>

                {msg.trace && (
                  <div className="mt-3 flex space-x-2">
                    {msg.trace.map((t, idx) => (
                      <span key={idx} className="px-2 py-1 bg-white/5 border border-white/5 rounded text-[10px] text-slate-500 font-mono">
                        {t}
                      </span>
                    ))}
                  </div>
                )}
              </motion.div>
            ))}
            
            {isProcessing && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-center space-x-3 text-cyan-500/50 font-mono text-xs">
                <div className="w-4 h-4 border-2 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin"></div>
                <span>Synthesizing intent...</span>
              </motion.div>
            )}
          </AnimatePresence>
          <div ref={endOfMessagesRef} />
        </div>

        {/* Input Dock */}
        <div className="p-8">
          <div className="relative max-w-4xl mx-auto flex items-center group">
            <Search className="absolute left-6 text-slate-500 w-5 h-5 group-focus-within:text-cyan-400 transition-colors" />
            <input 
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleExecute()}
              placeholder="Command Orbit, request an evolution, or query memory..."
              className="w-full bg-white/[0.03] border border-white/10 rounded-full py-5 pl-16 pr-8 text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500/50 focus:bg-cyan-950/10 transition-all shadow-inner"
            />
          </div>
        </div>
      </main>
    </div>
  );
}

function ConnectorButton({ name, status, color }: { name: string, status: string, color: string }) {
  const colors: Record<string, string> = {
    amber: "bg-amber-500/10 text-amber-400 border-amber-500/20 hover:bg-amber-500/20",
    emerald: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/20",
    blue: "bg-blue-500/10 text-blue-400 border-blue-500/20 hover:bg-blue-500/20",
    red: "bg-red-500/10 text-red-400 border-red-500/20 hover:bg-red-500/20",
  };
  return (
    <div className={`p-2 rounded-lg border text-center cursor-pointer transition-all ${colors[color]}`}>
      <div className="text-[10px] font-bold uppercase">{name}</div>
      <div className="text-[8px] opacity-70 tracking-widest">{status}</div>
    </div>
  );
}

function ModuleCard({ icon, name, status, desc }: { icon: React.ReactNode, name: string, status: string, desc?: string }) {
  return (
    <div className="group p-4 bg-white/[0.01] border border-white/5 rounded-xl hover:bg-white/[0.03] hover:border-cyan-500/30 transition-all cursor-pointer">
      <div className="flex items-center justify-between mb-1">
        <div className="flex items-center space-x-3 text-slate-300 group-hover:text-white transition-colors">
          <div className="text-cyan-500/70 group-hover:text-cyan-400 [&>svg]:w-4 [&>svg]:h-4">
            {icon}
          </div>
          <span className="font-medium text-sm">{name}</span>
        </div>
        <span className="text-[10px] font-mono text-cyan-500 tracking-wider bg-cyan-500/10 px-2 py-0.5 rounded">{status}</span>
      </div>
      {desc && <div className="text-xs text-slate-600 pl-7">{desc}</div>}
    </div>
  );
}
