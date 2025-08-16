// src/types.ts
export interface EquipmentRead {
  id: string;
  name: string;
  type: string;
  serial_number: string;
  inventory_number: string;
  created_at: string;
  updated_at: string;
  verification_date?: string | null;
  interval_months?: number | null;
  next_verification_date?: string | null;
}

export type ListParams = Partial<{
  q: string;
  name: string;
  type: string;
  serial_number: string;
  inventory_number: string;
  limit: number;
  offset: number;
}>;

export interface Verification {
  verification_date: string
  interval_months: number
  next_verification_date: string
}

export interface Equipment {
  id: string
  name: string
  type: string
  serial_number: string
  inventory_number: string
  created_at: string
  updated_at: string
  verification?: Verification
}
