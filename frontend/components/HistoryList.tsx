"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

export default function HistoryList() {
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    fetch("/api/history").then((r) => r.json()).then(setItems).catch(() => {});
  }, []);

  if (items.length === 0) return null;

  return (
    <div className="mt-12">
      <h2 className="text-xl mb-4">Recent Reviews</h2>
      <div className="bg-gray-900 rounded">
        {items.map((it) => (
          <Link key={it.id} href={`/review/${it.id}`} className="block p-4 border-b border-gray-800 hover:bg-gray-800">
            <div className="flex justify-between">
              <span className="text-sm truncate">{it.pr_url}</span>
              <span className="text-xs text-gray-500">
                <span className="text-red-400">{it.critical_count}</span> · <span className="text-yellow-400">{it.medium_count}</span> · <span className="text-green-400">{it.low_count}</span>
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
