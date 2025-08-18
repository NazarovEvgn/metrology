<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import type { EquipmentRead, ListParams } from "./types";
import { listEquipment, createEquipment, patchEquipment, deleteEquipment } from "./api";

// ====== Данные таблицы ======
const items = ref<EquipmentRead[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

// ====== Фильтры/пагинация ======
const q = ref("");
const type = ref("");
const serial_number = ref("");
const inventory_number = ref("");
const limit = ref(20);
const offset = ref(0);

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

// ====== CRUD: форма ======
type FormState = {
  id?: string | null;
  name: string;
  type: string;
  serial_number: string;
  inventory_number: string;
  state: "в работе" | "на консервации" | "на верификации" | "в ремонте" | "списано";
  verification_date: string | null;   // YYYY-MM-DD
  interval_months: number | null;
};

const emptyForm = (): FormState => ({
  id: null,
  name: "",
  type: "",
  serial_number: "",
  inventory_number: "",
  state: "в работе",
  verification_date: null,
  interval_months: null,
});

const showForm = ref(false);
const saving = ref(false);
const form = ref<FormState>(emptyForm());
const isEdit = computed(() => !!form.value.id);

function openCreate() {
  form.value = emptyForm();
  showForm.value = true;
}
function openEdit(row: EquipmentRead) {
  form.value = {
    id: row.id,
    name: row.name,
    type: row.type,
    serial_number: row.serial_number,
    inventory_number: row.inventory_number,
    state: row.state,
    verification_date: row.verification_date ?? null,
    interval_months: row.interval_months ?? null,
  };
  showForm.value = true;
}
function closeForm() {
  if (saving.value) return;
  showForm.value = false;
}

function validateForm(): string | null {
  if (!form.value.name.trim()) return "Заполните «Название».";
  if (!form.value.type.trim()) return "Заполните «Тип».";
  if (!form.value.serial_number.trim()) return "Заполните «Заводской №».";
  if (!form.value.inventory_number.trim()) return "Заполните «Инвентарный №».";
  if (form.value.interval_months !== null && form.value.interval_months < 0) return "Интервал не может быть отрицательным.";
  return null;
}

async function submitForm() {
  const err = validateForm();
  if (err) {
    alert(err);
    return;
  }
  saving.value = true;
  try {
    if (!isEdit.value) {
      // CREATE
      const created = await createEquipment({
        name: form.value.name.trim(),
        type: form.value.type.trim(),
        serial_number: form.value.serial_number.trim(),
        inventory_number: form.value.inventory_number.trim(),
        state: form.value.state,
        verification_date: form.value.verification_date,
        interval_months: form.value.interval_months,
      });
      items.value.unshift(created);
    } else {
      // PATCH
      const updated = await patchEquipment(form.value.id as string, {
        name: form.value.name.trim(),
        type: form.value.type.trim(),
        serial_number: form.value.serial_number.trim(),
        inventory_number: form.value.inventory_number.trim(),
        state: form.value.state,
        verification_date: form.value.verification_date,
        interval_months: form.value.interval_months,
      });
      const ix = items.value.findIndex(i => i.id === updated.id);
      if (ix >= 0) items.value[ix] = updated;
    }
    showForm.value = false;
  } catch (e: any) {
    alert(e?.message ?? "Не удалось сохранить");
  } finally {
    saving.value = false;
  }
}

async function removeRow(row: EquipmentRead) {
  if (!confirm(`Удалить «${row.name}»?`)) return;
  try {
    await deleteEquipment(row.id);
    items.value = items.value.filter(i => i.id !== row.id);
  } catch (e: any) {
    alert(e?.message ?? "Не удалось удалить");
  }
}

// ====== Утилиты ======
function fmtDate(d?: string | null) {
  if (!d) return "—";
  return d.slice(0, 10);
}
function chipStyle(status: string) {
  const base = {
    padding: "2px 8px",
    borderRadius: "12px",
    display: "inline-block",
    fontWeight: 600 as const,
    border: "1px solid #2b2b2b",
    background: "#2a2a2a",
    color: "#e8e8e8",
  };
  if (status === "срок истек") return { ...base, background: "#4a1f1f" };
  if (status === "срок истекает") return { ...base, background: "#4a3e1f" };
  if (status === "годен") return { ...base, background: "#213f21" };
  if (["на консервации", "на верификации", "в ремонте", "списано"].includes(status))
    return { ...base, background: "#1f2a4a" };
  return base;
}

onMounted(load);
</script>

<template>
  <main class="wrap">
    <h1>Equipment</h1>

    <div class="toolbar">
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
          placeholder="Заводской №…"
          @keyup.enter="applyFilters"
        />
        <input
          v-model="inventory_number"
          type="text"
          placeholder="Инв. №…"
          @keyup.enter="applyFilters"
        />

        <button class="primary" @click="applyFilters">Применить</button>
        <button @click="resetFilters">Сброс</button>
      </div>

      <div class="actions">
        <button class="success" @click="openCreate">+ Добавить</button>
      </div>
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
          <th>Состояние</th>
          <th>Статус</th>
          <th style="width:120px;">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="it in items" :key="it.id">
          <td>{{ it.name }}</td>
          <td>{{ it.type }}</td>
          <td>{{ it.serial_number }}</td>
          <td>{{ it.inventory_number }}</td>
          <td>{{ fmtDate(it.verification_date) }}</td>
          <td>{{ it.interval_months ?? "—" }}</td>
          <td>{{ fmtDate(it.next_verification_date) }}</td>
          <td>{{ it.state }}</td>
          <td>
            <span :style="chipStyle(it.status)" :title="it.status">{{ it.status }}</span>
          </td>
          <td class="row-actions">
            <button class="small" @click="openEdit(it)">Изм.</button>
            <button class="small danger" @click="removeRow(it)">Удалить</button>
          </td>
        </tr>
        <tr v-if="!items.length && !loading && !error">
          <td colspan="10" class="muted">Нет данных</td>
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

    <!-- ====== Модалка формы ====== -->
    <div v-if="showForm" class="modal">
      <div class="modal-backdrop" @click="closeForm"></div>
      <div class="modal-card" @keydown.esc="closeForm">
        <div class="modal-header">
          <h2>{{ isEdit ? "Изменить оборудование" : "Добавить оборудование" }}</h2>
        </div>

        <div class="modal-body">
          <div class="grid">
            <label>
              <span>Название *</span>
              <input v-model="form.name" type="text" maxlength="255" />
            </label>
            <label>
              <span>Тип *</span>
              <input v-model="form.type" type="text" maxlength="100" />
            </label>
            <label>
              <span>Заводской № *</span>
              <input v-model="form.serial_number" type="text" maxlength="100" />
            </label>
            <label>
              <span>Инвентарный № *</span>
              <input v-model="form.inventory_number" type="text" maxlength="100" />
            </label>

            <label>
              <span>Состояние</span>
              <select v-model="form.state">
                <option value="в работе">в работе</option>
                <option value="на консервации">на консервации</option>
                <option value="на верификации">на верификации</option>
                <option value="в ремонте">в ремонте</option>
                <option value="списано">списано</option>
              </select>
            </label>

            <label>
              <span>Дата поверки</span>
              <input v-model="form.verification_date" type="date" />
            </label>
            <label>
              <span>Интервал (мес)</span>
              <input v-model.number="form.interval_months" type="number" min="0" />
            </label>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeForm" :disabled="saving">Отмена</button>
          <button class="primary" @click="submitForm" :disabled="saving">
            {{ saving ? "Сохранение..." : (isEdit ? "Сохранить" : "Добавить") }}
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px 80px;
  color: #e8e8e8;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
}

h1 {
  font-size: 44px;
  margin: 0 0 16px 0;
  font-weight: 800;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 14px;
}
.filters input, .filters select {
  background: #222;
  border: 1px solid #3a3a3a;
  color: #e8e8e8;
  padding: 8px 10px;
  border-radius: 6px;
  width: 240px;
}

.actions { display: flex; gap: 8px; }

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
button.success {
  background: #2d7a46;
  border-color: #2d7a46;
  color: #fff;
}
button.danger {
  background: #7a2d2d;
  border-color: #7a2d2d;
  color: #fff;
}
button.small {
  padding: 6px 8px;
  font-size: 12px;
}
button:disabled { opacity: 0.5; cursor: default; }

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  background: #171717;
}
.table th, .table td {
  border-bottom: 1px solid #2b2b2b;
  padding: 10px 12px;
  text-align: left;
  white-space: nowrap;
}
.table thead th {
  font-weight: 700;
  color: #cfcfcf;
}
.row-actions { display: flex; gap: 6px; }

.pager {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}
.pager .info { color: #aaa; }
select {
  background: #222;
  border: 1px solid #3a3a3a;
  color: #e8e8e8;
  padding: 6px 8px;
  border-radius: 6px;
}

.muted { color: #9aa0a6; }
.error { color: #ff6b6b; margin: 6px 0 0; }

/* ====== Modal ====== */
.modal { position: fixed; inset: 0; display: grid; place-items: center; z-index: 50; }
.modal-backdrop { position: absolute; inset: 0; background: rgba(0,0,0,.6); backdrop-filter: blur(2px); }
.modal-card {
  position: relative;
  width: min(820px, 92vw);
  background: #121212;
  border: 1px solid #2b2b2b;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,.5);
  overflow: hidden;
}
.modal-header, .modal-footer { padding: 14px 16px; border-bottom: 1px solid #2b2b2b; }
.modal-footer { border-top: 1px solid #2b2b2b; border-bottom: 0; display: flex; justify-content: flex-end; gap: 10px; }
.modal-body { padding: 16px; }

.grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(260px, 1fr));
  gap: 12px 16px;
}
label { display: grid; gap: 6px; }
label span { color: #cfcfcf; font-size: 13px; }
label input, label select {
  background: #1e1e1e;
  border: 1px solid #3a3a3a;
  color: #e8e8e8;
  padding: 8px 10px;
  border-radius: 6px;
}
</style>
