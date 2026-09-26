import { useState } from "react";
import { Link } from "react-router-dom";
import AuthLayout from "./AuthLayout";
import { apiError, authApi } from "../../lib/api";
import { ErrorBox } from "../../components/ui";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");
    try {
      await authApi.forgotPassword({ email });
      setMessage("If the account exists, a reset OTP has been sent.");
    } catch (err) {
      setError(apiError(err));
    }
  };

  return (
    <AuthLayout title="Reset your password" subtitle="Enter your account email to receive the OTP.">
      <form className="auth-form" onSubmit={submit}>
        <input
          className="input"
          type="email"
          required
          placeholder="Email address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button className="btn primary full" type="submit">Send OTP</button>
        {message && <div className="success-box">{message}</div>}
        <ErrorBox message={error} />
      </form>
      <p className="auth-switch">
        <Link to="/reset-password">I already have an OTP</Link> · <Link to="/login">Back to sign in</Link>
      </p>
    </AuthLayout>
  );
}
