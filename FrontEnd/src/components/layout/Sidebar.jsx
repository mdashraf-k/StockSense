import { NavLink } from "react-router-dom";
import {
  BarChart3, Boxes, ClipboardList, History, LayoutDashboard, LogOut,
  MapPin, Package, Settings, Truck, Warehouse, ArrowLeftRight,
  SlidersHorizontal, UserRound, ChevronDown
} from "lucide-react";
import { useState } from "react";
import { useAuth } from "../../context/AuthContext";

const nav = [
  { label: "Dashboard", to: "/dashboard", icon: LayoutDashboard },
  { label: "Products", to: "/products", icon: Package },
  { label: "Inventory", to: "/inventory", icon: Boxes },
];
const operations = [
  { label: "Receipts", to: "/operations/receipts", icon: ClipboardList },
  { label: "Deliveries", to: "/operations/deliveries", icon: Truck },
  { label: "Internal Transfers", to: "/operations/transfers", icon: ArrowLeftRight },
  { label: "Adjustments", to: "/operations/adjustments", icon: SlidersHorizontal },
];

export default function Sidebar() {
  const [opsOpen, setOpsOpen] = useState(true);
  const { user, logout } = useAuth();

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">S</div>
        <div><div className="brand-name">StockSense</div><div className="brand-subtitle">Inventory OS</div></div>
      </div>
      <div className="sidebar-scroll">
        <div className="nav-section">
          <div className="nav-label">Workspace</div>
          {nav.map((item) => <NavItem key={item.to} {...item} />)}
        </div>
        <div className="nav-section">
          <button className="nav-group-button" onClick={() => setOpsOpen((v) => !v)}>
            <span><BarChart3 size={17} /> Operations</span>
            <ChevronDown size={15} className={opsOpen ? "" : "rotate-180"} />
          </button>
          {opsOpen && operations.map((item) => <NavItem key={item.to} {...item} />)}
        </div>
        <div className="nav-section">
          <div className="nav-label">Stock Control</div>
          <NavItem label="Move History" to="/move-history" icon={History} />
          <NavItem label="Warehouses" to="/warehouses" icon={Warehouse} />
          <NavItem label="Locations" to="/locations" icon={MapPin} />
        </div>
        <div className="nav-section">
          <div className="nav-label">Account</div>
          <NavItem label="My Profile" to="/profile" icon={UserRound} />
          <NavItem label="Settings" to="/settings" icon={Settings} />
        </div>
      </div>
      <div className="sidebar-footer">
        <div className="mini-user">
          <div className="avatar">{(user?.name || user?.username || "U").slice(0, 1).toUpperCase()}</div>
          <div className="mini-user-copy"><strong>{user?.name || user?.username || "User"}</strong><span>{user?.role || "Inventory user"}</span></div>
        </div>
        <button className="icon-button subtle" title="Logout" onClick={logout}><LogOut size={17} /></button>
      </div>
    </aside>
  );
}
function NavItem({ label, to, icon: Icon }) {
  return <NavLink to={to} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}><Icon size={17} /><span>{label}</span></NavLink>;
}