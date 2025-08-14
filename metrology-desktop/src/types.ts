// src/types.ts
export interface EquipmentRead {
  id: string;
  name: string;
  type: string;
  serial_number: string;
  inventory_number: string;
  created_at: string;
  updated_at: string;
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
