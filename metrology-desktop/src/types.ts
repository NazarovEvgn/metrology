// src/types.ts

export type EquipmentState =
  | "в работе"
  | "на консервации"
  | "на верификации"
  | "в ремонте"
  | "списано";

export interface EquipmentRead {
  id: string;
  name: string;
  type: string;
  serial_number: string;
  inventory_number: string;
  created_at: string;             // ISO
  updated_at: string;             // ISO

  // verification (плоскими полями из API)
  verification_date?: string | null;
  interval_months?: number | null;
  next_verification_date?: string | null;

  // Status-модуль
  state: EquipmentState;          // ручное поле
  status: string;                 // вычисляется на бэкенде
}

export interface ListParams {
  q?: string;
  name?: string;
  type?: string;
  serial_number?: string;
  inventory_number?: string;
  limit?: number;
  offset?: number;
}
