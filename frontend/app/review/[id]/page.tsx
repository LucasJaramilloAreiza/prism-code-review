"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import AgentStatus from "@/components/AgentStatus";
import RiskPanel from "@/components/RiskPanel";

const AGENTS = ["SecuritySentinel", "LogicAuditor", "PerformanceHawk", "BlastRadiusMapper"];

export default function ReviewPage() {
  const params = useParams();
  const id = params.id as string;
  const [agents, setAgents] = useState<Record<string, any>>({});
  const [report, setReport] = useState<any>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    if (!id) return;
    const ws = new WebSocket(`ws://localhost:8000/ws/review/${id}`);
    ws.onmessage = (e) => {
      const evt = JSON.parse(e.data);
      if (evt.event === "agent_started") {
        setAgents((p) => ({ ...p, [evt.agent]: { status: "running", findings: [] } }));
      } else if (evt.event === "agent_completed") {
        setAgents((p) => ({ ...p, [evt.agent]: { status: "done", findings: evt.findings || [] } }));
      } else if (evt.event === "review_complete") {
        setReport(evt.report);
      } else if (evt.event === "error") {
        setError(evt.message);
      }
    };
    ws.onerror = () => setError("WebSocket error");
    return () => ws.close();
  }, [id]);

  return (
    <main className="min-h-screen p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Review {id.slice(0, 8)}</h1>
      {error && <div className="bg-red-900 p-4 mb-6 rounded">{error}</div>}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1">
          <h2 className="text-xl mb-4">Agents</h2>
          {AGENTS.map((a) => (
            <AgentStatus key={a} name={a} status={agents[a]?.status || "pending"} count={agents[a]?.findings?.length || 0} />
          ))}
        </div>
        <div className="md:col-span-2">
          <RiskPanel report={report} agents={agents} />
        </div>
      </div>
    </main>
  );
}