import { Navigate, Route, Routes } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import AppShell from "./components/layout/AppShell";
import Login from "./pages/auth/Login";
import Signup from "./pages/auth/Signup";
import ForgotPassword from "./pages/auth/ForgotPassword";
import ResetPassword from "./pages/auth/ResetPassword";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/products/Products";
import ProductForm from "./pages/products/ProductForm";
import Inventory from "./pages/inventory/Inventory";
import Warehouses from "./pages/warehouses/Warehouses";
import WarehouseForm from "./pages/warehouses/WarehouseForm";
import Locations from "./pages/warehouses/Locations";
import Receipts from "./pages/operations/Receipts";
import ReceiptForm from "./pages/operations/ReceiptForm";
import Deliveries from "./pages/operations/Deliveries";
import DeliveryForm from "./pages/operations/DeliveryForm";
import Transfers from "./pages/operations/Transfers";
import TransferForm from "./pages/operations/TransferForm";
import Adjustments from "./pages/operations/Adjustments";
import AdjustmentForm from "./pages/operations/AdjustmentForm";
import MoveHistory from "./pages/history/MoveHistory";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";

function ProtectedLayout() {
  return <ProtectedRoute><AppShell /></ProtectedRoute>;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route element={<ProtectedLayout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/new" element={<ProductForm />} />
        <Route path="/products/:id/edit" element={<ProductForm />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/warehouses" element={<Warehouses />} />
        <Route path="/warehouses/new" element={<WarehouseForm />} />
        <Route path="/warehouses/:id/edit" element={<WarehouseForm />} />
        <Route path="/locations" element={<Locations />} />
        <Route path="/operations/receipts" element={<Receipts />} />
        <Route path="/operations/receipts/new" element={<ReceiptForm />} />
        <Route path="/operations/receipts/:id/edit" element={<ReceiptForm />} />
        <Route path="/operations/deliveries" element={<Deliveries />} />
        <Route path="/operations/deliveries/new" element={<DeliveryForm />} />
        <Route path="/operations/deliveries/:id/edit" element={<DeliveryForm />} />
        <Route path="/operations/transfers" element={<Transfers />} />
        <Route path="/operations/transfers/new" element={<TransferForm />} />
        <Route path="/operations/transfers/:id/edit" element={<TransferForm />} />
        <Route path="/operations/adjustments" element={<Adjustments />} />
        <Route path="/operations/adjustments/new" element={<AdjustmentForm />} />
        <Route path="/operations/adjustments/:id/edit" element={<AdjustmentForm />} />
        <Route path="/move-history" element={<MoveHistory />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}