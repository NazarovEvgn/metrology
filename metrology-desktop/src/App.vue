<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import type { EquipmentRead, ListParams } from "./types";
import { listEquipment } from "./api";

// состояние
const items = ref<EquipmentRead[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

// фильтры
const q = ref("");
const type = ref("");
const serial = ref("");
const inventory = ref("");

// пагинация
const limit = ref(20);
const offset = ref(0);

async function fetchData() {
  loading.value = true;
  error.value = null;
  try {
    const params: ListParams = {
      q: q.value || undefined,
      type: type.value || undefined,
      serial_number: serial.value || undefined,
      inventory_number: inventory.value || undefined,
      limit: limit.value,
      offset: offset.value,
    };
    items.value = await listEquipment(params);
  } catch (e: any) {
    error.value = e?.message ?? String(e);
  } finally {
    loading.value = false;
  }
}

function applyFilters() {
  offset.value = 0;
  fetchData();
}
function resetFilters() {
  q.value = "";
  type.value = "";
  serial.value = "";
  inventory.value = "";
  applyFilters();
}

function nextPage() {
  offset.value += limit.value;
  fetchData();
}
function prevPage() {
  offset.value = Math.max(0, offset.value - limit.value);
  fetchData();
}

// дебаунс для q
let t: number | undefined;
watch(q, () => {
  window.clearTimeout(t);
  t = window.setTimeout(() => applyFilters(), 300);
});

onMounted(fetchData);
</script>

<template>
  <main class="wrap">
    <h1>Equipment (read-only)</h1>

    <section class="filters">
      <input v-model="q" placeholder="Поиск по всем (q)..." />
      <input v-model="type" placeholder="Тип (type)..." />
      <input v-model="serial" placeholder="Заводской № (serial_number)..." />
      <input v-model="inventory" placeholder="Инв. № (inventory_number)..." />
      <button @click="applyFilters">Применить</button>
      <button @click="resetFilters">Сброс</button>
    </section>

    <section v-if="loading" class="muted">Загрузка…</section>
    <section v-else-if="error" class="error">Ошибка: {{ error }}</section>

    <table v-else class="tbl">
      <thead>
        <tr>
          <th>Название</th>
          <th>Тип</th>
          <th>Заводской №</th>
          <th>Инв. №</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="it in items" :key="it.id">
          <td>{{ it.name }}</td>
          <td>{{ it.type }}</td>
          <td>{{ it.serial_number }}</td>
          <td>{{ it.inventory_number }}</td>
        </tr>
        <tr v-if="!items.length">
          <td colspan="4" class="muted">Нет данных</td>
        </tr>
      </tbody>
    </table>

    <section class="pager">
      <button :disabled="offset===0" @click="prevPage">← Назад</button>
      <button :disabled="items.length < limit" @click="nextPage">Вперёд →</button>
      <span class="muted">offset: {{ offset }}, limit:
        <select v-model.number="limit" @change="applyFilters">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select>
      </span>
    </section>
  </main>
</template>

<style>
.wrap { max-width: 1000px; margin: 24px auto; font-family: system-ui, sans-serif; }
.filters { display: grid; grid-template-columns: repeat(4, 1fr) auto auto; gap: 8px; margin: 12px 0; }
.tbl { width: 100%; border-collapse: collapse; }
.tbl th, .tbl td { padding: 8px; border-bottom: 1px solid #eee; text-align: left; }
.muted { color: #666; }
.error { color: #b00020; }
.pager { display: flex; gap: 8px; align-items: center; margin-top: 12px; }
input, button, select { padding: 6px 10px; }
button:disabled { opacity: .5; cursor: not-allowed; }
</style>
