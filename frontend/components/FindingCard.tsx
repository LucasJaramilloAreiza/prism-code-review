export default function FindingCard({ finding }: { finding: any }) {
  const colors: Record<string, string> = {
    critical: "border-l-red-500 bg-red-950",
    medium: "border-l-yellow-500 bg-yellow-950",
    low: "border-l-green-500 bg-green-950",
  };
  return (
    <div className={`border-l-4 p-4 rounded mb-3 ${colors[finding.severity] || "border-l-gray-500"}`}>
      <div className="flex justify-between items-start mb-2">
        <h4 className="font-bold">{finding.title}</h4>
        <span className="text-xs uppercase text-gray-400">{finding.severity}</span>
      </div>
      <p className="text-sm text-gray-300 mb-2">{finding.description}</p>
      <div className="text-xs text-gray-500 font-mono">
        {finding.agent}{finding.file ? ` · ${finding.file}${finding.line ? `:${finding.line}` : ""}` : ""}
      </div>
    </div>
  );
}
