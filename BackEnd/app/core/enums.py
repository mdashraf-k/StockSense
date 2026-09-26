from enum import Enum


class UserRole(str, Enum):

    INVENTORY_MANAGER = "inventory_manager"

    WAREHOUSE_STAFF = "warehouse_staff"

class DocumentStatus(str, Enum):
    DRAFT = "draft"
    WAITING = "waiting"
    READY = "ready"
    DONE = "done"
    CANCELED = "canceled"


class MovementType(str, Enum):
    RECEIPT = "receipt"
    DELIVERY = "delivery"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    ADJUSTMENT = "adjustment"