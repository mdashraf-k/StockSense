import OperationForm from "../../components/OperationForm";
import { transferApi } from "../../lib/api";
export default function TransferForm() { return <OperationForm title="Internal Transfer" resourceLabel="transfer" api={transferApi} type="transfer" />; }