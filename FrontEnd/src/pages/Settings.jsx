import { useState } from "react";
import { Bell, ShieldCheck } from "lucide-react";
import { PageHeader } from "../components/ui";

export default function Settings() {
  const [alerts, setAlerts] = useState(true); const [lowStock, setLowStock] = useState(true);
  return <><PageHeader title="Settings" description="Application preferences and inventory behavior." /><div className="settings-grid"><section className="panel"><div className="panel-header"><div><h3>Notifications</h3><p>Choose which inventory alerts you want to see.</p></div><Bell size={19} /></div><SettingRow title="Operation notifications" description="Show updates when receipts and deliveries change status." checked={alerts} onChange={setAlerts} /><SettingRow title="Low-stock alerts" description="Highlight products below their reorder threshold." checked={lowStock} onChange={setLowStock} /></section><section className="panel"><div className="panel-header"><div><h3>Security</h3><p>Your session is protected by an HttpOnly JWT cookie.</p></div><ShieldCheck size={19} /></div><div className="security-note">Password reset uses the OTP flow configured by the FastAPI backend.</div></section></div></>;
}
function SettingRow({ title, description, checked, onChange }) { return <label className="setting-row"><div><strong>{title}</strong><span>{description}</span></div><input type="checkbox" checked={checked} onChange={(e) => onChange(e.target.checked)} /></label>; }