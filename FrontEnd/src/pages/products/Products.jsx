import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Edit3, Package, Trash2 } from "lucide-react";
import { productApi, unwrapList } from "../../lib/api";
import { DataTable } from "../../components/DataTable";
import { ErrorBox, PageHeader } from "../../components/ui";

export default function Products() {
  const [rows, setRows] = useState([]); const [search, setSearch] = useState(""); const [category, setCategory] = useState(""); const [loading, setLoading] = useState(true); const [error, setError] = useState("");
  const load = async () => { setLoading(true); try { setRows(unwrapList(await productApi.list({ search: search || undefined, category_id: category || undefined }))); } catch (err) { setError(err?.response?.data?.detail || err?.message || "Unable to load products."); } finally { setLoading(false); } };
  useEffect(() => { load(); }, [category]);
  const remove = async (id) => { if (!window.confirm("Delete this product?")) return; try { await productApi.remove(id); setRows((items) => items.filter((x) => x.id !== id)); } catch (err) { setError(err?.response?.data?.detail || err?.message || "Unable to delete product."); } };
  const filtered = rows.filter((row) => JSON.stringify(row).toLowerCase().includes(search.toLowerCase()));
  const columns = [
    { key: "name", label: "Product", render: (r) => <div className="product-cell"><div className="product-icon"><Package size={17} /></div><div><strong>{r.name}</strong><span>{r.sku || r.code || "No SKU"}</span></div></div> },
    { key: "category", label: "Category", render: (r) => r.category?.name || r.category_name || "—" },
    { key: "unit", label: "Unit", render: (r) => r.unit || r.unit_of_measure || "—" },
    { key: "stock", label: "Initial stock", render: (r) => r.initial_stock ?? r.stock ?? "—" },
    { key: "actions", label: "", render: (r) => <div className="row-actions"><Link className="icon-button small" to={`/products/${r.id}/edit`} onClick={(e) => e.stopPropagation()}><Edit3 size={15} /></Link><button className="icon-button small danger" onClick={(e) => { e.stopPropagation(); remove(r.id); }}><Trash2 size={15} /></button></div> },
  ];
  return <><PageHeader title="Products" description="Create and maintain your product catalog." actionLabel="New Product" actionTo="/products/new" /><div className="toolbar"><input className="input compact search-input-wide" placeholder="Search name, SKU or category..." value={search} onChange={(e) => setSearch(e.target.value)} /><select className="input compact" value={category} onChange={(e) => setCategory(e.target.value)}><option value="">All categories</option></select></div><ErrorBox message={error} onRetry={load} /><DataTable columns={columns} rows={filtered} loading={loading} emptyTitle="No products yet" emptyDescription="Create a product with a name, SKU, category and unit." /></>;
}