import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Edit3, MapPin, Trash2, Warehouse } from "lucide-react";
import { warehouseApi, unwrapList } from "../../lib/api";
import { DataTable } from "../../components/DataTable";
import { ErrorBox, PageHeader } from "../../components/ui";

export default function Warehouses() {
  const [rows, setRows] = useState([]); const [loading, setLoading] = useState(true); const [error, setError] = useState("");
  const load = async () => { setLoading(true); try { setRows(unwrapList(await warehouseApi.list())); } catch (e) { setError(e?.response?.data?.detail || e?.message || "Unable to load warehouses."); } finally { setLoading(false); } };
  useEffect(() => { load(); }, []);
  const remove = async (id) => { if (!window.confirm("Delete this warehouse?")) return; try { await warehouseApi.remove(id); setRows((x) => x.filter((r) => r.id !== id)); } catch (e) { setError(e?.response?.data?.detail || e?.message || "Unable to delete."); } };
  const columns = [
    { key: "name", label: "Warehouse", render: (r) => <div className="product-cell"><div className="product-icon"><Warehouse size={17} /></div><div><strong>{r.name}</strong><span>{r.short_code || r.code || "—"}</span></div></div> },
    { key: "address", label: "Address", render: (r) => r.address || "—" },
    { key: "locations_count", label: "Locations", render: (r) => r.locations_count ?? r.location_count ?? "—" },
    { key: "actions", label: "", render: (r) => <div className="row-actions"><Link className="icon-button small" to={`/warehouses/${r.id}/edit`}><Edit3 size={15} /></Link><button className="icon-button small" onClick={() => remove(r.id)}><Trash2 size={15} /></button></div> },
  ];
  return <><PageHeader title="Warehouses" description="Warehouse details, addresses and storage locations." actionLabel="New Warehouse" actionTo="/warehouses/new"><Link className="btn ghost" to="/locations"><MapPin size={16} />Locations</Link></PageHeader><ErrorBox message={error} onRetry={load} /><DataTable columns={columns} rows={rows} loading={loading} emptyTitle="No warehouses" emptyDescription="Create your first warehouse to organize stock." /></>;
}