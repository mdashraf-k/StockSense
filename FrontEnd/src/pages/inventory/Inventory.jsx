import { useEffect, useState } from "react";
import { Boxes, Search } from "lucide-react";
import { inventoryApi, unwrapList } from "../../lib/api";
import { DataTable } from "../../components/DataTable";
import { ErrorBox, PageHeader } from "../../components/ui";

export default function Inventory() {
  const [rows, setRows] = useState([]); const [search, setSearch] = useState(""); const [warehouse, setWarehouse] = useState(""); const [loading, setLoading] = useState(true); const [error, setError] = useState("");
  const load = async () => { setLoading(true); try { setRows(unwrapList(await inventoryApi.list({ warehouse_id: warehouse || undefined }))); } catch (e) { setError(e?.response?.data?.detail || e?.message || "Unable to load inventory."); } finally { setLoading(false); } };
  useEffect(() => { load(); }, [warehouse]);
  const filtered = rows.filter((r) => JSON.stringify(r).toLowerCase().includes(search.toLowerCase()));
  const columns = [
    { key: "product", label: "Product", render: (r) => <div className="product-cell"><div className="product-icon"><Boxes size={17} /></div><div><strong>{r.product?.name || r.product_name || "—"}</strong><span>{r.product?.sku || r.sku || r.product_code || "—"}</span></div></div> },
    { key: "warehouse", label: "Warehouse", render: (r) => r.warehouse?.name || r.warehouse_name || "—" },
    { key: "location", label: "Location", render: (r) => r.location?.name || r.location_name || "—" },
    { key: "quantity", label: "On hand", render: (r) => r.quantity ?? r.on_hand ?? 0 },
    { key: "reserved", label: "Reserved", render: (r) => r.reserved ?? 0 },
    { key: "available", label: "Free to use", render: (r) => r.available ?? r.free_to_use ?? ((r.quantity ?? 0) - (r.reserved ?? 0)) },
  ];
  return <><PageHeader title="Inventory" description="Stock availability per product, warehouse and location." /><div className="toolbar"><label className="search-box"><Search size={16} /><input placeholder="Search product, SKU, location..." value={search} onChange={(e) => setSearch(e.target.value)} /></label><input className="input compact" placeholder="Warehouse ID" value={warehouse} onChange={(e) => setWarehouse(e.target.value)} /></div><ErrorBox message={error} onRetry={load} /><DataTable columns={columns} rows={filtered} loading={loading} emptyTitle="No stock records" emptyDescription="Inventory will appear here after products or operations are created." /></>;
}