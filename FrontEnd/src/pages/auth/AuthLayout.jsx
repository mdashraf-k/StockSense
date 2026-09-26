import { Boxes, CheckCircle2, Package, ShieldCheck, Warehouse } from "lucide-react";
import { Link } from "react-router-dom";

export default function AuthLayout({ children, title, subtitle }) {
  return <div className="auth-page">
    <section className="auth-visual">
      <div className="auth-brand"><div className="brand-mark large">S</div><div><strong>StockSense</strong><span>Inventory Management System</span></div></div>
      <div className="auth-hero"><div className="eyebrow">CENTRALIZED INVENTORY</div><h1>Know what you have.<br /><em>Know where it is.</em></h1><p>Manage products, warehouses, receipts, deliveries and every stock movement from one clean workspace.</p><div className="feature-stack"><Feature icon={Package} text="Real-time product availability" /><Feature icon={Warehouse} text="Multi-warehouse locations" /><Feature icon={CheckCircle2} text="Validated stock operations" /><Feature icon={ShieldCheck} text="Role-based access" /></div></div>
      <div className="auth-grid-decoration"><Boxes size={180} strokeWidth={0.6} /></div>
    </section>
    <section className="auth-form-area"><div className="auth-form-card"><div className="mobile-brand"><Link to="/login">StockSense</Link></div><h2>{title}</h2><p className="auth-subtitle">{subtitle}</p>{children}</div></section>
  </div>;
}
function Feature({ icon: Icon, text }) { return <div className="auth-feature"><Icon size={18} /><span>{text}</span></div>; }