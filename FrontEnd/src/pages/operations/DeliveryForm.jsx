import OperationForm from "../../components/OperationForm";
import { deliveryApi } from "../../lib/api";
export default function DeliveryForm() { return <OperationForm title="Delivery" resourceLabel="delivery" api={deliveryApi} type="delivery" />; }