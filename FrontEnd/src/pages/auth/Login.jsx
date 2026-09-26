import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { LockKeyhole, Mail } from "lucide-react";
import AuthLayout from "./AuthLayout";
import { useAuth } from "../../context/AuthContext";
import { ErrorBox } from "../../components/ui";

export default function Login() {
  const { login, error, setError } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: "", password: "" });
  const [submitting, setSubmitting] = useState(false);

  const submit = async (e) => {
    e.preventDefault(); setSubmitting(true); setError("");
    try { await login(form); navigate(location.state?.from || "/dashboard", { replace: true }); }
    catch { /* context exposes the message */ }
    finally { setSubmitting(false); }
  };

  return <AuthLayout title="Welcome back" subtitle="Sign in to your StockSense workspace.">
    <form className="auth-form" onSubmit={submit}>
      <label className="auth-input"><Mail size={17} /><input required type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
      <label className="auth-input"><LockKeyhole size={17} /><input required type="password" placeholder="Password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
      <div className="auth-row"><span>Secure JWT session</span><Link to="/forgot-password">Forgot password?</Link></div>
      {error && <ErrorBox message={error} />}
      <button className="btn primary full" disabled={submitting}>{submitting ? "Signing in..." : "Sign in"}</button>
    </form>
    <p className="auth-switch">Don't have an account? <Link to="/signup">Create one</Link></p>
  </AuthLayout>;
}