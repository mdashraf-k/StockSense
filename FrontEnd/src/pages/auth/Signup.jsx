import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { LockKeyhole, Mail, UserRound } from "lucide-react";
import AuthLayout from "./AuthLayout";
import { useAuth } from "../../context/AuthContext";
import { ErrorBox } from "../../components/ui";

export default function Signup() {
  const { signup, error, setError } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", username: "", email: "", password: "", confirm_password: "" });
  const [submitting, setSubmitting] = useState(false);
  const submit = async (e) => {
    e.preventDefault();
    if (form.password !== form.confirm_password) return setError("Passwords do not match.");
    setSubmitting(true); setError("");
    try { await signup(form); navigate("/login", { replace: true }); }
    catch { /* context exposes the message */ }
    finally { setSubmitting(false); }
  };
  return <AuthLayout title="Create your account" subtitle="Set up your StockSense inventory workspace.">
    <form className="auth-form" onSubmit={submit}>
      <label className="auth-input"><UserRound size={17} /><input required placeholder="Full name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label>
      <label className="auth-input"><UserRound size={17} /><input required placeholder="Username" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /></label>
      <label className="auth-input"><Mail size={17} /><input required type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
      <label className="auth-input"><LockKeyhole size={17} /><input required type="password" minLength={8} placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
      <label className="auth-input"><LockKeyhole size={17} /><input required type="password" minLength={8} placeholder="Confirm password" value={form.confirm_password} onChange={(e) => setForm({ ...form, confirm_password: e.target.value })} /></label>
      {error && <ErrorBox message={error} />}
      <button className="btn primary full" disabled={submitting}>{submitting ? "Creating..." : "Create account"}</button>
    </form>
    <p className="auth-switch">Already have an account? <Link to="/login">Sign in</Link></p>
  </AuthLayout>;
}