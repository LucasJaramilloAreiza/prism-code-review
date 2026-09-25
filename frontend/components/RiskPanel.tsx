import FindingCard from "./FindingCard";

export default function RiskPanel({ report, agents }: { report: any; agents: any }) {
  const all = report
    ? report.agents.flatMap((a: any) => a.findings)
    : Object.values(agents).flatMap((a: any) => a.findings || []);

  const grouped = {
    critical: all.filter((f: any) => f.severity === "critical"),
    medium: all.filter((f: any) => f.severity === "medium"),
    low: all.filter((f: any) => f.severity === "low"),
  };

  return (
    <div>
      <h2 className="text-xl mb-4">
        Findings {report && <span className="text-sm text-gray-500">({all.length} total)</span>}
      </h2>
      {(["critical", "medium", "low"] as const).map((sev) => (
        <div key={sev} className="mb-6">
          <h3 className="text-sm uppercase mb-2 text-gray-400">
            {sev === "critical" ? "🔴" : sev === "medium" ? "🟡" : "🟢"} {sev} ({grouped[sev].length})
          </h3>
          {grouped[sev].map((f: any, i: number) => <FindingCard key={i} finding={f} />)}
        </div>
      ))}
      {all.length === 0 && <p className="text-gray-500">Waiting for findings...</p>}
    </div>
  );
}
