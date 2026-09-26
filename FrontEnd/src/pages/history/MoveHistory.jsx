import { useEffect, useMemo, useState } from "react";
import { Search } from "lucide-react";
import { ledgerApi, unwrapList } from "../../lib/api";
import { DataTable } from "../../components/DataTable";
import { ErrorBox, PageHeader } from "../../components/ui";

export default function MoveHistory() {
  const [rows, setRows] = useState([]); const [search, setSearch] = useState(""); const [type, setType] = useState(""); const [loading, setLoading] = useState(true); const [error, setError] = useState("");
  const load = async () => { setLoading(true); try { setRows(unwrapList(await ledgerApi.list({ type: type || undefined }))); } catch (e) { setError(e?.response?.data?.detail || e?.message || "Unable to load move history."); } finally { setLoading(false); } };
  useEffect(() => { load(); }, [type]);
  const filtered = useMemo(() => rows.filter((r) => JSON.stringify(r).toLowerCase().includes(search.toLowerCase())), [rows, search]);
  const columns = [
    { key: "reference", label: "Reference", render: (r) => <strong>{r.reference || r.document_reference || `#${r.id}`}</strong> },
    { key: "date", label: "Date", render: (r) => r.date ? new Date(r.date).toLocaleDateString() : r.created_at ? new Date(r.created_at).toLocaleDateString() : "—" },
    { key: "contact", label: "Contact", render: (r) => r.contact || r.partner || "—" },
    { key: "from", label: "From", render: (r) => r.from || r.from_location || "—" },
    { key: "to", label: "To", render: (r) => r.to || r.to_location || "—" },
    { key: "quantity", label: "Quantity", render: (r) => r.quantity ?? "—" },
    { key: "status", label: "Status", status: true },
  ];
  return <><PageHeader title="Move History" description="A complete ledger of stock movements between locations." /><div className="toolbar"><label className="search-box"><Search size={16} /><input placeholder="Search reference or contact..." value={search} onChange={(e) => setSearch(e.target.value)} /></label><select className="input compact" value={type} onChange={(e) => setType(e.target.value)}><option value="">All moves</option><option value="receipt">Receipts</option><option value="delivery">Deliveries</option><option value="transfer">Transfers</option><option value="adjustment">Adjustments</option></select></div><ErrorBox message={error} onRetry={load} /><DataTable columns={columns} rows={filtered} loading={loading} emptyTitle="No movements yet" emptyDescription="Validated receipts, deliveries, transfers and adjustments will appear here." /></>;
}