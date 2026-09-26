import OperationList from "../../components/OperationList";
import { deliveryApi } from "../../lib/api";
export default function Deliveries() {
  return <OperationList title="Delivery" description="Outgoing customer shipments. Validate to decrease stock." resource="deliveries" api={deliveryApi} newTo="/operations/deliveries/new" columns={[
    { key: "reference", label: "Reference" }, { key: "from", label: "From", render: (r) => r.from || r.location?.name || "—" }, { key: "to", label: "To", render: (r) => r.to || r.delivery_address || r.customer || "Customer" }, { key: "contact", label: "Contact", render: (r) => r.contact || r.customer || "—" }, { key: "scheduled_date", label: "Schedule date", render: (r) => r.scheduled_date || r.schedule_date || "—" }, { key: "status", label: "Status", status: true }
  ]} getCardTitle={(r) => r.reference || `Delivery #${r.id}`} />;
}