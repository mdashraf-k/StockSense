import OperationList from "../../components/OperationList";
import { adjustmentApi } from "../../lib/api";
export default function Adjustments() {
  return <OperationList title="Inventory Adjustments" description="Correct recorded stock to match a physical count." resource="adjustments" api={adjustmentApi} newTo="/operations/adjustments/new" columns={[
    { key: "reference", label: "Reference" }, { key: "product", label: "Product", render: (r) => r.product?.name || r.product_name || "—" }, { key: "location", label: "Location", render: (r) => r.location?.name || r.location_name || "—" }, { key: "counted_quantity", label: "Counted", render: (r) => r.counted_quantity ?? r.quantity ?? "—" }, { key: "reason", label: "Reason", render: (r) => r.reason || "—" }, { key: "status", label: "Status", status: true }
  ]} getCardTitle={(r) => r.reference || `Adjustment #${r.id}`} />;
}