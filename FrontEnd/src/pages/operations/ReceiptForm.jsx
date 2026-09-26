import OperationForm from "../../components/OperationForm";
import { receiptApi } from "../../lib/api";
export default function ReceiptForm() { return <OperationForm title="Receipt" resourceLabel="receipt" api={receiptApi} type="receipt" />; }