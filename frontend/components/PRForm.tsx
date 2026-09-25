"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import ModeToggle from "./ModeToggle";

export default function PRForm() {
  const [url, setUrl] = useState("");
  const [mode, setMode] = useState<"eco" | "full">("eco");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!/^https?:\/\/github\.com\/[^/]+\/[^/]+\/pull\/\d+/.test(url)) {
      setError("Invalid GitHub PR URL");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("/api/review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pr_url: url, mode }),
      });
      if (!res.ok) throw new Error("Request failed");
      const data = await res.json();
      router.push(`/review/${data.id}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={submit} className="bg-gray-900 p-6 rounded mb-8">
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://github.com/owner/repo/pull/123"
          className="flex-1 bg-gray-800 border border-gray-700 rounded px-4 py-2 text-white"
        />
        <button type="submit" disabled={loading} className="bg-blue-700 px-6 py-2 rounded disabled:opacity-50">
          {loading ? "Analyzing..." : "Analyze PR"}
        </button>
      </div>
      <ModeToggle mode={mode} onChange={setMode} />
      {error && <p className="text-red-400 mt-3">{error}</p>}
    </form>
  );
}
