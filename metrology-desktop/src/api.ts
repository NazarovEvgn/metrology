// src/api.ts
import type { EquipmentRead, ListParams } from "./types";

// базовый URL API
export const BASE =
  (import.meta.env?.VITE_API_BASE && String(import.meta.env.VITE_API_BASE)) ||
  "http://127.0.0.1:8000";

// сборка query string
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

// универсальный fetch с таймаутом
async function fetchJSON<T>(
  input: RequestInfo | URL,
  init?: RequestInit,
  timeoutMs = 10000
): Promise<T> {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), timeoutMs);
  try {
    const res = await fetch(input, { ...init, signal: ac.signal });
    if (!res.ok) {
      let details = "";
      try {
        details = await res.clone().text();
      } catch {}
      throw new Error(`HTTP ${res.status}${details ? `: ${details}` : ""}`);
    }
    // 204/205 или отсутствует JSON — возвращаем undefined
    const status = res.status;
    if (status === 204 || status === 205) {
      return undefined as unknown as T;
    }
    const ct = res.headers.get("content-type") || "";
    if (!ct.includes("application/json")) {
    // на всякий случай не парсим как JSON
    return undefined as unknown as T;
    }
    // есть JSON — читаем
    return (await res.json()) as T;
  } finally {
    clearTimeout(t);
  }
}

// список оборудования
export async function listEquipment(
  params: ListParams = {}
): Promise<EquipmentRead[]> {
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
  return fetchJSON<EquipmentRead>(url, {
    headers: { Accept: "application/json" },
  });
}

export async function createEquipment(body: {
  name: string;
  type: string;
  serial_number: string;
  inventory_number: string;
  state?: "в работе" | "на консервации" | "на верификации" | "в ремонте" | "списано";
  verification_date?: string | null;
  interval_months?: number | null;
}): Promise<EquipmentRead> {
  const url = new URL("/equipment/", BASE);
  return fetchJSON<EquipmentRead>(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(body),
  });
}

export async function patchEquipment(id: string, body: Partial<{
  name: string;
  type: string;
  serial_number: string;
  inventory_number: string;
  state: "в работе" | "на консервации" | "на верификации" | "в ремонте" | "списано";
  verification_date: string | null;
  interval_months: number | null;
}>): Promise<EquipmentRead> {
  const url = new URL(`/equipment/${encodeURIComponent(id)}`, BASE);
  return fetchJSON<EquipmentRead>(url, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(body),
  });
}

export async function deleteEquipment(id: string): Promise<void> {
  const url = new URL(`/equipment/${encodeURIComponent(id)}`, BASE);
  await fetchJSON<void>(url, { method: "DELETE" });
}
