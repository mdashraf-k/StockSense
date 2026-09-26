# StockSense

StockSense is a modular **Inventory Management System (IMS)** designed to digitize and streamline stock-related operations within a business.

The system replaces manual registers, Excel sheets, and scattered inventory-tracking methods with a centralized, real-time, easy-to-use application.

## Table of Contents

- [Overview](#overview)
- [Target Users](#target-users)
- [Authentication](#authentication)
- [Dashboard](#dashboard)
- [Navigation](#navigation)
- [Core Features](#core-features)
  - [Product Management](#1-product-management)
  - [Receipts](#2-receipts-incoming-goods)
  - [Delivery Orders](#3-delivery-orders-outgoing-goods)
  - [Internal Transfers](#4-internal-transfers)
  - [Stock Adjustments](#5-stock-adjustments)
- [Additional Features](#additional-features)
- [Inventory Flow](#inventory-flow)
- [Stock Ledger](#stock-ledger)
- [Project Scope](#project-scope)
- [Mockup](#mockup)

---

## Overview

Inventory operations can become difficult to manage when stock is tracked through manual registers, spreadsheets, or disconnected systems.

StockSense provides a centralized inventory workflow for managing:

- Products
- Stock availability
- Warehouses and locations
- Incoming goods
- Outgoing goods
- Internal stock movements
- Inventory adjustments
- Stock history
- Reordering rules
- Low-stock alerts

The goal is to keep inventory information organized and make stock movement traceable from one location.

---

## Target Users

StockSense is designed primarily for:

### Inventory Managers

Inventory managers can manage:

- Incoming stock
- Outgoing stock
- Product information
- Inventory adjustments
- Stock availability
- Warehouse-related operations

### Warehouse Staff

Warehouse staff can perform operational activities such as:

- Stock transfers
- Picking
- Shelving
- Stock counting

---

## Authentication

StockSense includes user authentication with:

- Sign up
- Log in
- OTP-based password reset
- Redirect to the Inventory Dashboard after authentication

---

## Dashboard

The dashboard provides a snapshot of current inventory operations.

### Dashboard KPIs

The dashboard can display:

- **Total Products in Stock**
- **Low Stock / Out of Stock Items**
- **Pending Receipts**
- **Pending Deliveries**
- **Internal Transfers Scheduled**

### Dynamic Filters

Inventory information can be filtered by:

- Document type
  - Receipts
  - Delivery
  - Internal
  - Adjustments
- Status
  - Draft
  - Waiting
  - Ready
  - Done
  - Canceled
- Warehouse or location
- Product category

---

## Navigation

The main navigation is organized around inventory management workflows.

### Products

- Create products
- Update products
- View stock availability by location
- Manage product categories
- Configure reordering rules

### Operations

- Receipts
- Delivery Orders
- Inventory Adjustments
- Move History

### Dashboard

Provides an overview of inventory operations and important stock KPIs.

### Settings

Contains warehouse-related settings.

### Profile Menu

Includes:

- My Profile
- Logout

---

# Core Features

## 1. Product Management

StockSense allows products to be created and managed with information such as:

- Product Name
- SKU / Code
- Category
- Unit of Measure
- Initial Stock (optional)

Products also support stock availability tracking per location.

---

## 2. Receipts (Incoming Goods)

Receipts are used when goods arrive from vendors.

### Workflow

1. Create a new receipt.
2. Add the supplier and products.
3. Enter the quantities received.
4. Validate the receipt.
5. Stock increases automatically.

### Example

If the business receives **50 units of Steel Rods**:

```text
Steel Rods Stock
Before: X
Received: +50
After:  X + 50
```

---

## 3. Delivery Orders (Outgoing Goods)

Delivery Orders are used when inventory leaves the warehouse for customer shipment.

### Workflow

1. Pick the required items.
2. Pack the items.
3. Validate the delivery.
4. Stock decreases automatically.

### Example

If a sales order requires **10 chairs**:

```text
Chair Stock
Before: X
Delivered: -10
After:  X - 10
```

---

## 4. Internal Transfers

Internal transfers move stock between locations within the company.

Examples include:

```text
Main Warehouse → Production Floor
Rack A          → Rack B
Warehouse 1     → Warehouse 2
```

An internal transfer does not change the company's total quantity of stock. Instead, it changes the location where that stock is held.

Every movement is logged in the stock ledger.

---

## 5. Stock Adjustments

Stock adjustments are used when the recorded stock does not match the physical stock count.

### Workflow

1. Select the product and location.
2. Enter the physically counted quantity.
3. The system updates the stock.
4. The adjustment is recorded in the stock ledger.

This helps keep system inventory aligned with actual physical inventory.

---

# Additional Features

StockSense also includes the following inventory-management capabilities:

### Low-Stock Alerts

The system can alert users when products reach a low-stock condition.

### Multi-Warehouse Support

Inventory can be managed across multiple warehouses and locations.

### SKU Search

Products can be searched using their SKU or code.

### Smart Filters

Users can narrow inventory information using filters such as:

- Document type
- Status
- Warehouse
- Location
- Product category

---

# Inventory Flow

A typical StockSense inventory flow can be represented as:

```text
             ┌─────────────────────┐
             │   Vendor / Supplier │
             └──────────┬──────────┘
                        │
                        ▼
                ┌───────────────┐
                │    Receipt    │
                └───────┬───────┘
                        │
                        │ Stock +
                        ▼
              ┌───────────────────┐
              │ Warehouse / Stock │
              └─────────┬─────────┘
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
   ┌──────────────────┐   ┌──────────────────┐
   │ Internal Transfer│   │ Delivery Order   │
   └────────┬─────────┘   └────────┬─────────┘
            │                      │
            │ Location change      │ Stock -
            ▼                      ▼
   ┌──────────────────┐   ┌──────────────────┐
   │ Another Location │   │ Customer Shipment│
   └──────────────────┘   └──────────────────┘

                        +
                        │
                        ▼
              ┌──────────────────┐
              │ Stock Adjustment │
              └──────────────────┘
```

---

# Stock Ledger

StockSense keeps inventory movements traceable through a stock ledger.

The ledger records stock-related operations such as:

- Receipts
- Deliveries
- Internal transfers
- Stock adjustments

For example:

```text
1. Receive 100 kg Steel
   Stock: +100

2. Move Steel
   Main Store → Production Rack
   Total stock: unchanged
   Location: updated

3. Deliver 20 kg Steel
   Stock: -20

4. Adjust damaged stock by 3 kg
   Stock: -3
```

This provides a complete history of how stock changes over time.

---

# Project Scope

StockSense focuses on the core inventory lifecycle:

```text
Product Management
       ↓
Receiving Stock
       ↓
Storing / Locating Stock
       ↓
Internal Transfers
       ↓
Outgoing Deliveries
       ↓
Physical Stock Counting
       ↓
Stock Adjustments
       ↓
Stock Ledger / History
```

The system is intended to provide a centralized view of inventory operations while supporting multiple warehouses and locations.

---

# Statuses

Inventory documents can use the following statuses:

| Status | Description |
|---|---|
| `Draft` | Document is being prepared |
| `Waiting` | Operation is waiting for the next action |
| `Ready` | Operation is ready to be processed |
| `Done` | Operation has been completed |
| `Canceled` | Operation has been canceled |

---

# Example Inventory Scenario

Consider a business managing steel inventory.

### Step 1 — Receive Goods

The business receives:

```text
100 kg Steel
```

Stock increases by:

```text
+100 kg
```

### Step 2 — Internal Transfer

The steel is moved:

```text
Main Store → Production Rack
```

The total stock remains unchanged, but its location is updated.

### Step 3 — Deliver Goods

The business delivers:

```text
20 kg Steel
```

Stock changes by:

```text
-20 kg
```

### Step 4 — Adjust Damaged Stock

Suppose:

```text
3 kg Steel
```

is damaged.

The stock is adjusted by:

```text
-3 kg
```

All of these operations are recorded in the Stock Ledger.

---

# Mockup

The project specification includes a UI mockup for StockSense:

[Open StockSense Mockup](https://link.excalidraw.com/l/65VNwvy7c4X/3ENvQFu9o8R)

---

## Summary

StockSense is an inventory management system centered around a simple principle:

> **Every stock movement should be organized, traceable, and reflected in the current inventory.**

The system brings together product management, receiving, delivery, internal transfers, stock adjustments, warehouse/location tracking, filtering, alerts, and inventory history into one centralized workflow.
