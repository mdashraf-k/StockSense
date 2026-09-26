import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { ErrorBox, Input, PageHeader } from "../components/ui";

export default function Profile() {
  const { user, updateProfile } = useAuth();
  const [form, setForm] = useState({ name: user?.name || "", username: user?.username || "", email: user?.email || "" });
  const [message, setMessage] = useState(""); const [error, setError] = useState(""); const [saving, setSaving] = useState(false);
  const submit = async (e) => { e.preventDefault(); setSaving(true); setMessage(""); setError(""); try { await updateProfile(form); setMessage("Profile updated successfully."); } catch (e) { setError(e?.response?.data?.detail || e?.message || "Unable to update profile."); } finally { setSaving(false); } };
  return <><PageHeader title="My Profile" description="Update the information associated with your account." /><form className="form-panel profile-panel" onSubmit={submit}><div className="profile-hero"><div className="avatar huge">{(user?.name || user?.username || "U").slice(0, 1).toUpperCase()}</div><div><h3>{user?.name || "User"}</h3><p>{user?.role || "Inventory user"}</p></div></div><div className="form-grid"><Input label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /><Input label="Username" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /><Input label="Email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></div>{message && <div className="success-box">{message}</div>}<ErrorBox message={error} /><div className="form-actions"><button className="btn primary" disabled={saving}>{saving ? "Saving..." : "Save profile"}</button></div></form></>;
}