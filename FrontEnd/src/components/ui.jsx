import { Link } from "react-router-dom";
import { AlertCircle, Check, Plus, RefreshCw, Search, X } from "lucide-react";

export function PageHeader({ title, description, actionLabel, actionTo, action, children }) {
  return <div className="page-header"><div><h2>{title}</h2>{description && <p>{description}</p>}</div><div className="page-header-actions">{children}{actionTo && <Link className="btn primary" to={actionTo}><Plus size={17} />{actionLabel}</Link>}{action}</div></div>;
}
export function StatusBadge({ status }) {
  const value = String(status || "Draft");
  return <span className={`status-badge status-${value.toLowerCase().replace(/\s+/g, "-")}`}>{value}</span>;
}
export function EmptyState({ title = "Nothing here yet", description = "Create your first record to get started.", actionTo, actionLabel }) {
  return <div className="empty-state"><div className="empty-icon"><Search size={22} /></div><h3>{title}</h3><p>{description}</p>{actionTo && <Link className="btn primary" to={actionTo}><Plus size={16} />{actionLabel}</Link>}</div>;
}
export function ErrorBox({ message, onRetry }) {
  if (!message) return null;
  return <div className="error-box"><AlertCircle size={17} /><span>{message}</span>{onRetry && <button className="btn ghost small" onClick={onRetry}><RefreshCw size={15} />Retry</button>}</div>;
}
export function Toast({ message, type = "success", onClose }) {
  if (!message) return null;
  return <div className={`toast ${type}`}>{type === "success" ? <Check size={17} /> : <AlertCircle size={17} />}<span>{message}</span><button onClick={onClose}><X size={15} /></button></div>;
}
export function Field({ label, error, children, hint, required }) {
  return <div className="field"><label>{label}{required && <span className="required"> *</span>}</label>{children}{hint && <small>{hint}</small>}{error && <div className="field-error">{error}</div>}</div>;
}
export function Input({ label, error, hint, required, ...props }) {
  return <Field label={label} error={error} hint={hint} required={required}><input className="input" {...props} /></Field>;
}
export function Select({ label, error, hint, required, children, ...props }) {
  return <Field label={label} error={error} hint={hint} required={required}><select className="input" {...props}>{children}</select></Field>;
}
export function Textarea({ label, error, hint, required, ...props }) {
  return <Field label={label} error={error} hint={hint} required={required}><textarea className="input textarea" {...props} /></Field>;
}