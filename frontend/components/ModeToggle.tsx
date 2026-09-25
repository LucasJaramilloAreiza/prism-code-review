"use client";
import { Coins, Zap } from "lucide-react";

export default function ModeToggle({ mode, onChange }: { mode: "eco" | "full"; onChange: (m: "eco" | "full") => void }) {
  return (
    <div className="flex gap-2">
      <button
        type="button"
        onClick={() => onChange("eco")}
        className={`flex items-center gap-2 px-4 py-2 rounded ${mode === "eco" ? "bg-green-700" : "bg-gray-800"}`}
      >
        <Coins size={16} /> ECO
      </button>
      <button
        type="button"
        onClick={() => onChange("full")}
        className={`flex items-center gap-2 px-4 py-2 rounded ${mode === "full" ? "bg-blue-700" : "bg-gray-800"}`}
      >
        <Zap size={16} /> FULL
      </button>
    </div>
  );
}
