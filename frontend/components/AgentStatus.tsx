export default function AgentStatus({ name, status, count }: { name: string; status: string; count: number }) {
  const icon = status === "done" ? "✓" : status === "running" ? "⟳" : status === "error" ? "✗" : "○";
  const color = status === "done" ? "text-green-400" : status === "running" ? "text-blue-400" : status === "error" ? "text-red-400" : "text-gray-500";
  return (
    <div className="flex items-center justify-between bg-gray-900 rounded p-3 mb-2">
      <span className="text-sm">{name}</span>
      <span className={`${color} font-bold`}>{icon} {count > 0 && <span className="text-xs ml-2">{count}</span>}</span>
    </div>
  );
}
