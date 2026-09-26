import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { warehouseApi, unwrap } from "../../lib/api";
import { ErrorBox, Input, PageHeader, Textarea } from "../../components/ui";

export default function WarehouseForm() {
  const { id } = useParams(); const editing = Boolean(id); const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", short_code: "", address: "" }); const [error, setError] = useState(""); const [saving, setSaving] = useState(false);
  useEffect(() => { if (editing) warehouseApi.get(id).then((r) => setForm((x) => ({ ...x, ...(unwrap(r) || {}) }))).catch((e) => setError(e?.response?.data?.detail || e?.message || "Unable to load warehouse.")); }, [id, editing]);
  const submit = async (e) => { e.preventDefault(); setSaving(true); setError(""); try { if (editing) await warehouseApi.update(id, form); else await warehouseApi.create(form); navigate("/warehouses"); } catch (e) { setError(e?.response?.data?.detail || e?.message || "Unable to save warehouse."); } finally { setSaving(false); } };
  return <><PageHeader title={editing ? "Edit Warehouse" : "New Warehouse"} description="Keep the warehouse name, code and address accurate." /><form className="form-panel" onSubmit={submit}><div className="form-grid"><Input label="Name" required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /><Input label="Short code" required value={form.short_code} onChange={(e) => setForm({ ...form, short_code: e.target.value.toUpperCase() })} /></div><Textarea label="Address" rows={4} value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} /><ErrorBox message={error} /><div className="form-actions"><button type="button" className="btn ghost" onClick={() => navigate("/warehouses")}>Cancel</button><button className="btn primary" disabled={saving}>{saving ? "Saving..." : "Save warehouse"}</button></div></form></>;
}