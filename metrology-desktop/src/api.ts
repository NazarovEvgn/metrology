// src/api.ts
import type { EquipmentRead, ListParams } from "./types";

export const BASE =
  (import.meta.env?.VITE_API_BASE && String(import.meta.env.VITE_API_BASE)) ||
  "http://127.0.0.1:8000";

function buildQuery(params: ListParams): string {
  const sp = new URLSearchParams();
  ([
    ["q", params.q],
    ["name", params.name],
    ["type", params.type],
    ["serial_number", params.serial_number],
    ["inventory_number", params.inventory_number],
    ["limit", params.limit],
    ["offset", params.offset],
  ] as const).forEach(([k, v]) => {
    if (v !== undefined && v !== null && String(v).trim() !== "") sp.set(k, String(v));
  });
  return sp.toString();
}

async function fetchJSON<T>(input: RequestInfo | URL, init?: RequestInit, timeoutMs = 10000): Promise<T> {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), timeoutMs);
  try {
    const res = await fetch(input, { ...init, signal: ac.signal });
    if (!res.ok) {
      let details = "";
      try { details = await res.clone().text(); } catch {}
      throw new Error(`HTTP ${res.status}${details ? `: ${details}` : ""}`);
    }
    return res.json() as Promise<T>;
  } finally {
    clearTimeout(t);
  }
}

export async function listEquipment(params: ListParams = {}): Promise<EquipmentRead[]> {
  const url = new URL("/equipment/", BASE);
  url.search = buildQuery(params);
  return fetchJSON<EquipmentRead[]>(url, {
    headers: { Accept: "application/json" },
    redirect: "follow",
  });
}

// (опционально) детальная запись
export async function getEquipment(id: string): Promise<EquipmentRead> {
  const url = new URL(`/equipment/${encodeURIComponent(id)}`, BASE);
  return fetchJSON<EquipmentRead>(url, { headers: { Accept: "application/json" } });
}
