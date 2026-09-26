import OperationList from "../../components/OperationList";
import { transferApi } from "../../lib/api";
export default function Transfers() {
  return <OperationList title="Internal Transfers" description="Move stock between warehouses or locations." resource="transfers" api={transferApi} newTo="/operations/transfers/new" columns={[
    { key: "reference", label: "Reference" }, { key: "from", label: "From", render: (r) => r.from || r.source_location || "—" }, { key: "to", label: "To", render: (r) => r.to || r.destination_location || "—" }, { key: "contact", label: "Contact", render: (r) => r.contact || "—" }, { key: "scheduled_date", label: "Schedule date", render: (r) => r.scheduled_date || "—" }, { key: "status", label: "Status", status: true }
  ]} getCardTitle={(r) => r.reference || `Transfer #${r.id}`} />;
}