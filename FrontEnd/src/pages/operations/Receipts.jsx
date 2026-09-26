import OperationList from "../../components/OperationList";
import { receiptApi } from "../../lib/api";
export default function Receipts() {
  return <OperationList title="Receipts" description="Incoming goods from vendors. Validate to increase stock." resource="receipts" api={receiptApi} newTo="/operations/receipts/new" columns={[
    { key: "reference", label: "Reference" }, { key: "from", label: "From", render: (r) => r.from || r.supplier || r.vendor || "Vendor" }, { key: "to", label: "To", render: (r) => r.to || r.location?.name || r.destination || "—" }, { key: "contact", label: "Contact", render: (r) => r.contact || r.supplier || "—" }, { key: "scheduled_date", label: "Schedule date", render: (r) => r.scheduled_date || r.schedule_date || "—" }, { key: "status", label: "Status", status: true }
  ]} getCardTitle={(r) => r.reference || `Receipt #${r.id}`} />;
}