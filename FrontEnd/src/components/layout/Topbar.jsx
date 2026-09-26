import { Bell, Search, UserCircle2 } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const titles = {
  "/dashboard": ["Dashboard", "Your inventory at a glance"],
  "/products": ["Products", "Manage your product catalog"],
  "/inventory": ["Inventory", "Stock availability by location"],
  "/warehouses": ["Warehouses", "Manage warehouse details"],
  "/locations": ["Locations", "Organize warehouse locations"],
  "/operations/receipts": ["Receipts", "Incoming goods from vendors"],
  "/operations/deliveries": ["Deliveries", "Outgoing customer shipments"],
  "/operations/transfers": ["Internal Transfers", "Move stock between locations"],
  "/operations/adjustments": ["Adjustments", "Correct physical stock mismatches"],
  "/move-history": ["Move History", "Every inventory movement in one ledger"],
  "/profile": ["My Profile", "Account information"],
  "/settings": ["Settings", "Warehouse and application settings"],
};

export default function Topbar() {
  const location = useLocation();
  const { user } = useAuth();
  const current = titles[location.pathname] || titles[`/${location.pathname.split("/")[1]}`] || ["StockSense", "Inventory management"];
  return (
    <header className="topbar">
      <div className="topbar-title"><h1>{current[0]}</h1><span>{current[1]}</span></div>
      <div className="topbar-actions">
        <label className="global-search"><Search size={16} /><input placeholder="Search products, SKU, reference..." /><kbd>⌘ K</kbd></label>
        <button className="icon-button"><Bell size={18} /></button>
        <Link className="topbar-user" to="/profile">
          <div className="avatar small">{(user?.name || user?.username || "U").slice(0, 1).toUpperCase()}</div>
          <div className="topbar-user-text"><strong>{user?.name || user?.username || "User"}</strong><span>{user?.role || "User"}</span></div>
          <UserCircle2 size={17} />
        </Link>
      </div>
    </header>
  );
}