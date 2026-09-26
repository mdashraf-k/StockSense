import OperationForm from "../../components/OperationForm";
import { adjustmentApi } from "../../lib/api";
export default function AdjustmentForm() { return <OperationForm title="Inventory Adjustment" resourceLabel="adjustment" api={adjustmentApi} type="adjustment" />; }