import { useEffect, useMemo, useState } from "react";
import { Grid2X2, List, Search } from "lucide-react";
import { Link } from "react-router-dom";
import { DataTable } from "./DataTable";
import { PageHeader, StatusBadge } from "./ui";

export default function OperationList({ title, description, resource, api, columns, newTo, newLabel = "New", statuses = ["Draft", "Waiting", "Ready", "Done", "Canceled"], filters = [], getCardTitle }) {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [view, setView] = useState("list");

  const load = async () => {
    setLoading(true); setError("");
    try {
      const response = await api.list({ status: status || undefined, search: search || undefined });
      const data = response?.data?.data ?? response?.data;
      setRows(Array.isArray(data) ? data : data?.items ?? data?.results ?? []);
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || `Could not load ${resource}.`);
    } finally { setLoading(false); }
  };
  useEffect(() => { load(); }, [status]);

  const filtered = useMemo(() => !search ? rows : rows.filter((row) => JSON.stringify(row).toLowerCase().includes(search.toLowerCase())), [rows, search]);

  return <>
    <PageHeader title={title} description={description} actionLabel={newLabel} actionTo={newTo} />
    <div className="toolbar">
      <label className="search-box"><Search size={16} /><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder={`Search ${resource}...`} /></label>
      <select className="input compact" value={status} onChange={(e) => setStatus(e.target.value)}><option value="">All statuses</option>{statuses.map((item) => <option key={item}>{item}</option>)}</select>
      {filters.map((filter) => <div key={filter.key}>{filter.element}</div>)}
      <div className="view-toggle"><button className={view === "list" ? "active" : ""} onClick={() => setView("list")}><List size={16} /></button><button className={view === "kanban" ? "active" : ""} onClick={() => setView("kanban")}><Grid2X2 size={16} /></button></div>
    </div>
    {error && <div className="error-box">{error}</div>}
    {view === "list" ? <DataTable columns={columns} rows={filtered} loading={loading} emptyTitle={`No ${resource} found`} emptyDescription={`Create a ${resource.slice(0, -1) || "record"} to see it here.`} /> : <Kanban rows={filtered} statuses={statuses} getCardTitle={getCardTitle} />}
  </>;
}
function Kanban({ rows, statuses, getCardTitle }) {
  return <div className="kanban">{statuses.map((status) => { const cards = rows.filter((row) => String(row.status || "").toLowerCase() === status.toLowerCase()); return <div className="kanban-column" key={status}><div className="kanban-heading"><span>{status}</span><b>{cards.length}</b></div>{cards.map((row) => <Link className="kanban-card" to={`./${row.id}/edit`} key={row.id}><div className="kanban-card-top"><strong>{getCardTitle(row)}</strong><StatusBadge status={row.status} /></div><small>{row.reference || row.code || `#${row.id}`}</small><div className="kanban-meta">{row.contact || row.supplier || row.customer || "—"}</div></Link>)}</div>; })}</div>;
}