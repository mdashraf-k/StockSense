import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Plus, Trash2 } from "lucide-react";
import { productApi, warehouseApi, locationApi, unwrap, unwrapList } from "../lib/api";
import { ErrorBox, Input, PageHeader, Select, StatusBadge, Textarea } from "./ui";

const defaultHeader = { reference: "", contact: "", scheduled_date: "", responsible: "", delivery_address: "", operation_type: "", source_location_id: "", destination_location_id: "", warehouse_id: "", location_id: "", reason: "", notes: "" };

export default function OperationForm({ title, resourceLabel, api, type }) {
  const { id } = useParams(); const editing = Boolean(id); const navigate = useNavigate();
  const [form, setForm] = useState(defaultHeader); const [items, setItems] = useState([{ product_id: "", quantity: 1 }]); const [products, setProducts] = useState([]); const [warehouses, setWarehouses] = useState([]); const [locations, setLocations] = useState([]); const [error, setError] = useState(""); const [saving, setSaving] = useState(false); const [busyAction, setBusyAction] = useState("");
  const listPath = resourceLabel === "receipt" ? "receipts" : resourceLabel === "delivery" ? "deliveries" : resourceLabel === "transfer" ? "transfers" : "adjustments";

  useEffect(() => {
    Promise.all([productApi.list(), warehouseApi.list(), locationApi.list()]).then(([p, w, l]) => { setProducts(unwrapList(p)); setWarehouses(unwrapList(w)); setLocations(unwrapList(l)); }).catch(() => {});
    if (editing) api.get(id).then((r) => {
      const data = unwrap(r) || {}; setForm((x) => ({ ...x, ...data }));
      const serverItems = data.items || data.products || data.lines || [];
      if (serverItems.length) setItems(serverItems.map((x) => ({ product_id: x.product_id ?? x.product?.id ?? "", quantity: x.quantity ?? 1 })));
    }).catch((e) => setError(e?.response?.data?.detail || e?.message || `Unable to load ${resourceLabel}.`));
  }, [id, editing, api, resourceLabel]);

  const setItem = (index, key, value) => setItems((old) => old.map((x, i) => i === index ? { ...x, [key]: value } : x));
  const addItem = () => setItems((x) => [...x, { product_id: "", quantity: 1 }]);
  const removeItem = (index) => setItems((x) => x.length === 1 ? x : x.filter((_, i) => i !== index));
  const payload = useMemo(() => {
    const base = { ...form, items: items.map((x) => ({ product_id: x.product_id, quantity: Number(x.quantity) })) };
    if (!base.reference) delete base.reference;
    if (type === "receipt") { delete base.source_location_id; delete base.destination_location_id; }
    if (type === "delivery") { delete base.destination_location_id; }
    return base;
  }, [form, items, type]);

  const submit = async (e) => {
    e.preventDefault(); setSaving(true); setError("");
    try { if (editing) await api.update(id, payload); else await api.create(payload); navigate(`/operations/${listPath}`); }
    catch (e) { setError(e?.response?.data?.detail || e?.message || `Unable to save ${resourceLabel}.`); }
    finally { setSaving(false); }
  };
  const runAction = async (action) => {
    if (!id) return; setBusyAction(action);
    try { await api[action](id); navigate(`/operations/${listPath}`); }
    catch (e) { setError(e?.response?.data?.detail || e?.message || `Unable to ${action} this operation.`); }
    finally { setBusyAction(""); }
  };

  return <><PageHeader title={editing ? `Edit ${title}` : `New ${title}`} description={`Manage this ${resourceLabel} from draft through validation.`} /><form className="form-panel" onSubmit={submit}>
    {editing && form.status && <div className="detail-status"><span>Current status</span><StatusBadge status={form.status} /></div>}
    <div className="form-grid">
      <Input label="Reference" placeholder="Auto-generated if blank" value={form.reference || ""} onChange={(e) => setForm({ ...form, reference: e.target.value })} />
      {type === "receipt" && <Input label="Supplier / Contact" value={form.contact || ""} onChange={(e) => setForm({ ...form, contact: e.target.value })} />}
      {type === "delivery" && <Input label="Delivery address" required value={form.delivery_address || ""} onChange={(e) => setForm({ ...form, delivery_address: e.target.value })} />}
      <Input label="Schedule date" type="date" value={form.scheduled_date || ""} onChange={(e) => setForm({ ...form, scheduled_date: e.target.value })} />
      <Input label="Responsible" value={form.responsible || ""} onChange={(e) => setForm({ ...form, responsible: e.target.value })} />
      {(type === "receipt" || type === "delivery" || type === "transfer") && <Select label="Warehouse" value={form.warehouse_id || ""} onChange={(e) => setForm({ ...form, warehouse_id: e.target.value })}><option value="">Select warehouse</option>{warehouses.map((w) => <option key={w.id} value={w.id}>{w.name}</option>)}</Select>}
      {type === "transfer" && <><Select label="From location" required value={form.source_location_id || ""} onChange={(e) => setForm({ ...form, source_location_id: e.target.value })}><option value="">Select source</option>{locations.map((l) => <option key={l.id} value={l.id}>{l.name}</option>)}</Select><Select label="To location" required value={form.destination_location_id || ""} onChange={(e) => setForm({ ...form, destination_location_id: e.target.value })}><option value="">Select destination</option>{locations.map((l) => <option key={l.id} value={l.id}>{l.name}</option>)}</Select></>}
      {type === "adjustment" && <><Select label="Location" value={form.location_id || ""} onChange={(e) => setForm({ ...form, location_id: e.target.value })}><option value="">Select location</option>{locations.map((l) => <option key={l.id} value={l.id}>{l.name}</option>)}</Select><Input label="Reason" value={form.reason || ""} onChange={(e) => setForm({ ...form, reason: e.target.value })} /></>}
    </div>
    <div className="section-divider"><h3>Products</h3><button type="button" className="btn ghost small" onClick={addItem}><Plus size={15} />Add product</button></div>
    <div className="line-items"><div className="line-item header"><span>Product</span><span>Quantity</span><span /></div>{items.map((item, index) => <div className="line-item" key={index}><select className="input" required value={item.product_id} onChange={(e) => setItem(index, "product_id", e.target.value)}><option value="">Select product</option>{products.map((p) => <option key={p.id} value={p.id}>{p.name}{p.sku ? ` · ${p.sku}` : ""}</option>)}</select><input className="input" required min="1" type="number" value={item.quantity} onChange={(e) => setItem(index, "quantity", e.target.value)} /><button type="button" className="icon-button danger" onClick={() => removeItem(index)}><Trash2 size={16} /></button></div>)}</div>
    <Textarea label="Notes" rows={4} value={form.notes || ""} onChange={(e) => setForm({ ...form, notes: e.target.value })} /><ErrorBox message={error} />
    <div className="form-actions"><button type="button" className="btn ghost" onClick={() => navigate(-1)}>Cancel</button>{editing && <>{form.status !== "Canceled" && <button type="button" className="btn danger-outline" disabled={busyAction} onClick={() => runAction("cancel")}>Cancel operation</button>}{form.status !== "Done" && form.status !== "Canceled" && <button type="button" className="btn secondary" disabled={busyAction} onClick={() => runAction("validate")}>{busyAction === "validate" ? "Validating..." : "Validate"}</button>}</>}<button className="btn primary" disabled={saving}>{saving ? "Saving..." : editing ? "Save changes" : `Create ${resourceLabel}`}</button></div>
  </form></>;
}