import { MoreHorizontal } from "lucide-react";
import { EmptyState, StatusBadge } from "./ui";

export function DataTable({ columns, rows, loading, emptyTitle, emptyDescription, onRowClick, rowKey }) {
  if (loading) return <div className="table-loading"><div className="spinner" />Loading...</div>;
  if (!rows.length) return <EmptyState title={emptyTitle} description={emptyDescription} />;
  return <div className="table-wrap"><table className="data-table"><thead><tr>{columns.map((column) => <th key={column.key}>{column.label}</th>)}</tr></thead><tbody>{rows.map((row, index) => <tr key={rowKey ? rowKey(row) : row.id ?? index} onClick={() => onRowClick?.(row)}>{columns.map((column) => <td key={column.key}>{column.status ? <StatusBadge status={row[column.key]} /> : column.render ? column.render(row) : (row[column.key] ?? "—")}</td>)}</tr>)}</tbody></table></div>;
}
export function TableActions({ children }) {
  return <div className="table-actions"><button className="icon-button small"><MoreHorizontal size={16} /></button>{children}</div>;
}