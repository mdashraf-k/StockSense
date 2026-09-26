import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import AuthLayout from "./AuthLayout";
import { apiError, authApi } from "../../lib/api";
import { ErrorBox } from "../../components/ui";

export default function ResetPassword() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: params.get("email") || "", otp: "", password: "", confirm_password: "" });
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const submit = async (e) => {
    e.preventDefault(); setError("");
    if (form.password !== form.confirm_password) return setError("Passwords do not match.");
    try { await authApi.resetPassword(form); setMessage("Password updated. You can sign in now."); setTimeout(() => navigate("/login"), 700); }
    catch (err) { setError(apiError(err)); }
  };
  return <AuthLayout title="Choose a new password" subtitle="Use the 6-digit OTP from your email.">
    <form className="auth-form" onSubmit={submit}>
      <input className="input" required type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
      <input className="input" required inputMode="numeric" maxLength={6} placeholder="6-digit OTP" value={form.otp} onChange={(e) => setForm({ ...form, otp: e.target.value.replace(/\D/g, "") })} />
      <input className="input" required minLength={8} type="password" placeholder="New password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
      <input className="input" required minLength={8} type="password" placeholder="Confirm new password" value={form.confirm_password} onChange={(e) => setForm({ ...form, confirm_password: e.target.value })} />
      {message && <div className="success-box">{message}</div>}<ErrorBox message={error} />
      <button className="btn primary full">Reset password</button>
    </form>
    <p className="auth-switch"><Link to="/login">Back to sign in</Link></p>
  </AuthLayout>;
}