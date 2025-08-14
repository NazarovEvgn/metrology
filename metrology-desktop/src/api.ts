// src/api.ts
import type { EquipmentRead, ListParams } from "./types";

const BASE = (import.meta.env.VITE_API_BASE as string) || "http://127.0.0.1:8000";

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
    if (v !== undefined && v !== null && String(v) !== "") sp.set(k, String(v));
  });
  return sp.toString();
}

export async function listEquipment(params: ListParams = {}): Promise<EquipmentRead[]> {
  const url = new URL("/equipment/", BASE); // <-- со слэшем
  url.search = buildQuery(params);
  const res = await fetch(url.toString(), {
    headers: { Accept: "application/json" },
    redirect: "follow",
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json() as Promise<EquipmentRead[]>;
}
