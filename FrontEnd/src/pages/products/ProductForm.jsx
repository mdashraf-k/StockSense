import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { productApi, unwrap } from "../../lib/api";
import { ErrorBox, PageHeader, Input, Select, Textarea } from "../../components/ui";

const empty = { name: "", sku: "", category_id: "", unit: "", description: "", initial_stock: 0 };

export default function ProductForm() {
  const { id } = useParams(); const editing = Boolean(id); const navigate = useNavigate();
  const [form, setForm] = useState(empty); const [categories, setCategories] = useState([]); const [error, setError] = useState(""); const [saving, setSaving] = useState(false);
  useEffect(() => {
    productApi.categories().then((r) => { const raw = unwrap(r); setCategories(Array.isArray(raw) ? raw : raw?.items ?? raw?.results ?? []); }).catch(() => {});
    if (editing) productApi.get(id).then((r) => { const p = unwrap(r); setForm({ ...empty, ...p, category_id: p.category_id ?? p.category?.id ?? "" }); }).catch((e) => setError(e?.response?.data?.detail || e?.message || "Unable to load product."));
  }, [id, editing]);
  const submit = async (e) => { e.preventDefault(); setSaving(true); setError(""); try { const payload = { ...form, initial_stock: Number(form.initial_stock || 0), category_id: form.category_id || null }; if (editing) await productApi.update(id, payload); else await productApi.create(payload); navigate("/products"); } catch (e) { setError(e?.response?.data?.detail || e?.message || "Unable to save product."); } finally { setSaving(false); } };
  return <><PageHeader title={editing ? "Edit Product" : "New Product"} description="Product information used throughout inventory operations." /><form className="form-panel" onSubmit={submit}><div className="form-grid"><Input label="Product name" required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /><Input label="SKU / Code" required value={form.sku} onChange={(e) => setForm({ ...form, sku: e.target.value })} /><Select label="Category" value={form.category_id} onChange={(e) => setForm({ ...form, category_id: e.target.value })}><option value="">Select category</option>{categories.map((c) => <option value={c.id} key={c.id}>{c.name}</option>)}</Select><Input label="Unit of measure" placeholder="pcs, kg, box..." required value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })} />{!editing && <Input label="Initial stock" type="number" min="0" value={form.initial_stock} onChange={(e) => setForm({ ...form, initial_stock: e.target.value })} />}</div><Textarea label="Description" rows={5} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /><ErrorBox message={error} /><div className="form-actions"><button type="button" className="btn ghost" onClick={() => navigate("/products")}>Cancel</button><button className="btn primary" disabled={saving}>{saving ? "Saving..." : editing ? "Save changes" : "Create product"}</button></div></form></>;
}