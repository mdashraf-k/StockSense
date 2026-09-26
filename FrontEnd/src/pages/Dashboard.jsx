import { useEffect, useState } from "react";
import { AlertTriangle, ArrowDownToLine, ArrowLeftRight, ArrowUpFromLine, Boxes, PackageSearch, Warehouse } from "lucide-react";
import { Link } from "react-router-dom";
import { dashboardApi, unwrap } from "../lib/api";
import { ErrorBox, PageHeader, StatusBadge } from "../components/ui";

const fallback = { total_products: 0, low_stock: 0, out_of_stock: 0, pending_receipts: 0, pending_deliveries: 0, scheduled_transfers: 0, recent_operations: [] };

export default function Dashboard() {
  const [summary, setSummary] = useState(fallback);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  useEffect(() => {
    dashboardApi.summary()
      .then((response) => setSummary({ ...fallback, ...(unwrap(response) || {}) }))
      .catch((err) => setError(err?.response?.data?.detail || err?.message || "Unable to load dashboard."))
      .finally(() => setLoading(false));
  }, []);
  const kpis = [
    { label: "Total Products", value: summary.total_products, icon: PackageSearch, tone: "blue", to: "/products" },
    { label: "Low Stock", value: summary.low_stock, icon: AlertTriangle, tone: "amber", to: "/inventory" },
    { label: "Out of Stock", value: summary.out_of_stock, icon: Boxes, tone: "red", to: "/inventory" },
    { label: "Pending Receipts", value: summary.pending_receipts, icon: ArrowDownToLine, tone: "green", to: "/operations/receipts" },
    { label: "Pending Deliveries", value: summary.pending_deliveries, icon: ArrowUpFromLine, tone: "purple", to: "/operations/deliveries" },
    { label: "Transfers Scheduled", value: summary.scheduled_transfers, icon: ArrowLeftRight, tone: "cyan", to: "/operations/transfers" },
  ];
  return <>
    <PageHeader title="Dashboard" description="A live snapshot of your inventory operations." />
    {error && <ErrorBox message={error} />}
    <div className="kpi-grid">{kpis.map(({ label, value, icon: Icon, tone, to }) => <Link className="kpi-card" to={to} key={label}><div className={`kpi-icon ${tone}`}><Icon size={19} /></div><div><span>{label}</span><strong>{loading ? "—" : value ?? 0}</strong></div></Link>)}</div>
    <div className="dashboard-grid">
      <section className="panel"><div className="panel-header"><div><h3>Operations</h3><p>Quick access to stock movement workflows.</p></div></div><div className="quick-actions"><QuickAction to="/operations/receipts/new" icon={ArrowDownToLine} title="Receive goods" text="Add incoming vendor stock" /><QuickAction to="/operations/deliveries/new" icon={ArrowUpFromLine} title="Create delivery" text="Prepare an outgoing order" /><QuickAction to="/operations/transfers/new" icon={ArrowLeftRight} title="Move stock" text="Transfer between locations" /><QuickAction to="/operations/adjustments/new" icon={Boxes} title="Adjust stock" text="Fix a physical count" /></div></section>
      <section className="panel"><div className="panel-header"><div><h3>Warehouse</h3><p>Keep locations organized.</p></div><Warehouse size={19} /></div><Link className="warehouse-summary" to="/warehouses"><div className="warehouse-art"><Warehouse size={30} /></div><div><strong>Manage warehouses</strong><span>Warehouses & locations</span></div></Link></section>
    </div>
    <section className="panel recent-panel"><div className="panel-header"><div><h3>Recent operations</h3><p>The latest activity across your inventory.</p></div><Link to="/move-history" className="text-link">View history</Link></div>{summary.recent_operations?.length ? <div className="recent-list">{summary.recent_operations.slice(0, 8).map((item, i) => <div className="recent-row" key={item.id ?? i}><span>{item.reference || item.code || "Operation"}</span><span>{item.type || item.operation_type || "Stock movement"}</span><StatusBadge status={item.status} /><span>{item.created_at ? new Date(item.created_at).toLocaleString() : "—"}</span></div>)}</div> : <div className="empty-inline">No recent operations.</div>}</section>
  </>;
}
function QuickAction({ to, icon: Icon, title, text }) { return <Link to={to} className="quick-action"><div className="quick-icon"><Icon size={18} /></div><div><strong>{title}</strong><span>{text}</span></div></Link>; }