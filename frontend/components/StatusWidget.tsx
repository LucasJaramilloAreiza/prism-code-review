"use client";
import { useEffect, useState } from "react";

type StatusData = {
  database: string;
  bob_api_key: string;
  github_token: string;
  bob_cli: string;
  overall: string;
};

function Dot({ value }: { value: string }) {
  const ok = value === "ok" || (!value.startsWith("error") && value !== "missing or invalid");
  return (
    <span className={`inline-block w-2 h-2 rounded-full mr-2 ${ok ? "bg-green-400" : "bg-red-400"}`} />
  );
}

export default function StatusWidget() {
  const [status, setStatus] = useState<StatusData | null>(null);
  const [loading, setLoading] = useState(true);

  const check = () => {
    setLoading(true);
    fetch("/api/status")
      .then((r) => r.json())
      .then((d) => { setStatus(d); setLoading(false); })
      .catch(() => { setLoading(false); });
  };

  useEffect(() => { check(); }, []);

  if (loading) return <div className="text-xs text-gray-600 mb-6">Checking system status...</div>;
  if (!status) return null;

  const rows: [string, string][] = [
    ["Database", status.database],
    ["Bob API Key", status.bob_api_key],
    ["GitHub Token", status.github_token],
    ["Bob CLI", status.bob_cli],
  ];

  return (
    <div className="bg-gray-900 border border-gray-800 rounded p-4 mb-6 text-xs">
      <div className="flex items-center justify-between mb-3">
        <span className="text-gray-400 font-semibold uppercase tracking-wider">System Status</span>
        <span className={`text-xs px-2 py-0.5 rounded ${status.overall === "ok" ? "bg-green-900 text-green-300" : "bg-red-900 text-red-300"}`}>
          {status.overall === "ok" ? "All systems go" : "Degraded"}
        </span>
        <button onClick={check} className="text-gray-600 hover:text-gray-400 ml-2">↻</button>
      </div>
      {rows.map(([label, val]) => (
        <div key={label} className="flex items-center justify-between py-1 border-t border-gray-800">
          <span className="text-gray-500">{label}</span>
          <span className="flex items-center text-gray-300">
            <Dot value={val} />
            {val === "ok" ? <span className="text-green-400">ok</span> : <span className="text-red-400 truncate max-w-xs">{val}</span>}
          </span>
        </div>
      ))}
    </div>
  );
}