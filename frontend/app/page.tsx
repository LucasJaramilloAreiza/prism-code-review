"use client";
import { useState } from "react";
import PRForm from "@/components/PRForm";
import HistoryList from "@/components/HistoryList";

export default function Home() {
  return (
    <main className="min-h-screen p-8 max-w-5xl mx-auto">
<h1 className="text-4xl font-bold mb-2">PRism</h1>
<p className="text-gray-400 mb-8">Multi-agent code review orchestrator</p>
<PRForm />
<HistoryList />
</main>
  );
}
