"use client";
import { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import AgentStatus from "@/components/AgentStatus";
import RiskPanel from "@/components/RiskPanel";

const AGENTS = ["SecuritySentinel", "LogicAuditor", "PerformanceHawk", "BlastRadiusMapper"];
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export default function ReviewPage() {
  const params = useParams();
  const id = params.id as string;
  const [agents, setAgents] = useState<Record<string, any>>({});
  const [report, setReport] = useState<any>(null);
  const [error, setError] = useState<string>("");
  const [done, setDone] = useState(false);
  const retriesRef = useRef(0);

  useEffect(() => {
    if (!id || done) return;

    let ws: WebSocket;
    let timeout: ReturnType<typeof setTimeout>;

    const connect = () => {
      ws = new WebSocket(`${WS_URL}/ws/review/${id}`);

      ws.onopen = () => { retriesRef.current = 0; };

      ws.onmessage = (e) => {
        const evt = JSON.parse(e.data);
        if (evt.event === "agent_started") {
          setAgents((p) => ({ ...p, [evt.agent]: { status: "running", findings: [] } }));
        } else if (evt.event === "agent_completed") {
          setAgents((p) => ({ ...p, [evt.agent]: { status: "done", findings: evt.findings || [] } }));
        } else if (evt.event === "review_complete") {
          setReport(evt.report);
          setDone(true);
        } else if (evt.event === "error") {
          setError(evt.message);
          setDone(true);
        }
      };

      ws.onerror = () => {
        if (retriesRef.current < 5) {
          retriesRef.current += 1;
          timeout = setTimeout(connect, 500 * retriesRef.current);
        } else {
          setError("WebSocket error — could not connect after 5 retries");
        }
      };
    };

    connect();
    return () => {
      clearTimeout(timeout);
      if (ws) ws.close();
    };
  }, [id, done]);

  return (
    <main className="min-h-screen p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Review {id?.slice(0, 8)}</h1>
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