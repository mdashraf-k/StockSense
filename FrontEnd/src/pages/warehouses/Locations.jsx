import { useEffect, useState } from "react";
import { MapPin, Trash2 } from "lucide-react";
import { locationApi, warehouseApi, unwrapList } from "../../lib/api";
import { DataTable } from "../../components/DataTable";
import { ErrorBox, Input, PageHeader, Select } from "../../components/ui";

export default function Locations() {
  const [rows, setRows] = useState([]); const [warehouses, setWarehouses] = useState([]); const [form, setForm] = useState({ name: "", short_code: "", warehouse_id: "" }); const [loading, setLoading] = useState(true); const [error, setError] = useState("");
  const load = async () => { setLoading(true); try { setRows(unwrapList(await locationApi.list())); } catch (e) { setError(e?.response?.data?.detail || e?.message || "Unable to load locations."); } finally { setLoading(false); } };
  useEffect(() => { load(); warehouseApi.list().then((r) => setWarehouses(unwrapList(r))).catch(() => {}); }, []);
  const create = async (e) => { e.preventDefault(); setError(""); try { await locationApi.create(form); setForm({ name: "", short_code: "", warehouse_id: "" }); load(); } catch (e) { setError(e?.response?.data?.detail || e?.message || "Unable to create location."); } };
  const remove = async (id) => { if (!window.confirm("Delete this location?")) return; try { await locationApi.remove(id); setRows((x) => x.filter((r) => r.id !== id)); } catch (e) { setError(e?.response?.data?.detail || e?.message || "Unable to delete."); } };
  const columns = [
    { key: "name", label: "Location", render: (r) => <div className="product-cell"><div className="product-icon"><MapPin size={17} /></div><div><strong>{r.name}</strong><span>{r.short_code || r.code || "—"}</span></div></div> },
    { key: "warehouse", label: "Warehouse", render: (r) => r.warehouse?.name || r.warehouse_name || "—" },
    { key: "actions", label: "", render: (r) => <button className="icon-button small danger" onClick={() => remove(r.id)}><Trash2 size={15} /></button> },
  ];
  return <><PageHeader title="Locations" description="Multiple locations can live inside each warehouse." /><div className="split-grid"><form className="form-panel compact-panel" onSubmit={create}><h3>Create location</h3><Input label="Name" required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /><Input label="Short code" required value={form.short_code} onChange={(e) => setForm({ ...form, short_code: e.target.value.toUpperCase() })} /><Select label="Warehouse" required value={form.warehouse_id} onChange={(e) => setForm({ ...form, warehouse_id: e.target.value })}><option value="">Select warehouse</option>{warehouses.map((w) => <option key={w.id} value={w.id}>{w.name}</option>)}</Select><button className="btn primary full">Create location</button></form><div><ErrorBox message={error} onRetry={load} /><DataTable columns={columns} rows={rows} loading={loading} emptyTitle="No locations" emptyDescription="Create locations such as WH/Stock, Production Rack or Rack A." /></div></div></>;
}