from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import DB

from .repository import ProductRepository
from .schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate
)
from .service import ProductService


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


def get_product_service(
    db: DB
):
    return ProductService(
        ProductRepository(db),
        db
    )


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201
)
def create_product(
    data: ProductCreate,
    service: ProductService = Depends(
        get_product_service
    )
):
    return service.create(data)


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_products(
    service: ProductService = Depends(
        get_product_service
    )
):
    return service.get_all()


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    service: ProductService = Depends(
        get_product_service
    )
):
    return service.get_by_id(product_id)


@router.patch(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductService = Depends(
        get_product_service
    )
):
    return service.update(
        product_id,
        data
    )


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    service: ProductService = Depends(
        get_product_service
    )
):
    service.delete(product_id)

    return {
        "message": "Product deleted successfully"
    }