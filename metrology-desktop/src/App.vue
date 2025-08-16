<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import type { EquipmentRead, ListParams } from "./types";
import { listEquipment } from "./api";

const items = ref<EquipmentRead[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

// фильтры/пагинация
const q = ref("");
const type = ref("");
const serial_number = ref("");
const inventory_number = ref("");
const limit = ref(20);
const offset = ref(0);

// собрать параметры для API
const params = computed<ListParams>(() => {
  const p: Record<string, string | number> = {
    limit: limit.value,
    offset: offset.value,
  };
  if (q.value.trim()) p.q = q.value.trim();
  if (type.value.trim()) p.type = type.value.trim();
  if (serial_number.value.trim()) p.serial_number = serial_number.value.trim();
  if (inventory_number.value.trim()) p.inventory_number = inventory_number.value.trim();
  return p as ListParams;
});

async function load() {
  loading.value = true;
  error.value = null;
  try {
    items.value = await listEquipment(params.value);
  } catch (e: any) {
    error.value = e?.message ?? "Failed to fetch";
    items.value = [];
  } finally {
    loading.value = false;
  }
}

function applyFilters() {
  offset.value = 0;
  load();
}

function resetFilters() {
  q.value = "";
  type.value = "";
  serial_number.value = "";
  inventory_number.value = "";
  offset.value = 0;
  load();
}

function prevPage() {
  if (offset.value > 0) {
    offset.value = Math.max(0, offset.value - limit.value);
    load();
  }
}

function nextPage() {
  offset.value = offset.value + limit.value;
  load();
}

onMounted(load);
</script>

<template>
  <main class="wrap">
    <h1>Equipment (read-only)</h1>

    <div class="filters">
      <input
        v-model="q"
        type="text"
        placeholder="Поиск по всем (q)…"
        @keyup.enter="applyFilters"
      />
      <input
        v-model="type"
        type="text"
        placeholder="Тип (type)…"
        @keyup.enter="applyFilters"
      />
      <input
        v-model="serial_number"
        type="text"
        placeholder="Заводской № (serial_number)…"
        @keyup.enter="applyFilters"
      />
      <input
        v-model="inventory_number"
        type="text"
        placeholder="Инв. № (inventory_number)…"
        @keyup.enter="applyFilters"
      />

      <button class="primary" @click="applyFilters">Применить</button>
      <button @click="resetFilters">Сброс</button>
    </div>

    <p v-if="error" class="error">Ошибка: {{ error }}</p>
    <p v-if="loading" class="muted">Загрузка…</p>

    <table class="table">
      <thead>
        <tr>
          <th>Название</th>
          <th>Тип</th>
          <th>Заводской №</th>
          <th>Инв. №</th>
          <th>Поверка (дата)</th>
          <th>Интервал (мес)</th>
          <th>Следующая поверка</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="it in items" :key="it.id">
          <td>{{ it.name }}</td>
          <td>{{ it.type }}</td>
          <td>{{ it.serial_number }}</td>
          <td>{{ it.inventory_number }}</td>
          <td>{{ it.verification_date ?? "—" }}</td>
          <td>{{ it.interval_months ?? "—" }}</td>
          <td>{{ it.next_verification_date ?? "—" }}</td>
        </tr>
        <tr v-if="!items.length && !loading && !error">
          <td colspan="7" class="muted">Нет данных</td>
        </tr>
      </tbody>
    </table>

    <div class="pager">
      <button :disabled="offset === 0 || loading" @click="prevPage">← Назад</button>
      <button :disabled="loading" @click="nextPage">Вперёд →</button>

      <span class="info">offset: {{ offset }}, limit:</span>
      <select v-model.number="limit" @change="applyFilters">
        <option :value="10">10</option>
        <option :value="20">20</option>
        <option :value="50">50</option>
        <option :value="100">100</option>
      </select>
    </div>
  </main>
</template>

<style scoped>
.wrap {
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 20px 80px;
  color: #e8e8e8;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
}

h1 {
  font-size: 44px;
  margin: 0 0 24px 0;
  font-weight: 800;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 14px;
}

.filters input {
  background: #222;
  border: 1px solid #3a3a3a;
  color: #e8e8e8;
  padding: 8px 10px;
  border-radius: 6px;
  width: 240px;
}

button {
  background: #2b2b2b;
  border: 1px solid #444;
  color: #ddd;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}
button.primary {
  background: #3a3fda;
  border-color: #3a3fda;
  color: #fff;
}
button:disabled {
  opacity: 0.5;
  cursor: default;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  background: #171717;
}
.table th,
.table td {
  border-bottom: 1px solid #2b2b2b;
  padding: 10px 12px;
  text-align: left;
  white-space: nowrap;
}
.table thead th {
  font-weight: 700;
  color: #cfcfcf;
}

.pager {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}
.pager .info {
  color: #aaa;
}
select {
  background: #222;
  border: 1px solid #3a3a3a;
  color: #e8e8e8;
  padding: 6px 8px;
  border-radius: 6px;
}

.muted {
  color: #9aa0a6;
}
.error {
  color: #ff6b6b;
  margin: 6px 0 0;
}
</style>
