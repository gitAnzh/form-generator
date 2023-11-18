from typing import Union

from fastapi import APIRouter
from fastapi import Query

from routers.main_page.models.main_page import main_page_detail
from routers.users.models.auth import AuthHandler

main_router = APIRouter()
auth_handler = AuthHandler()


@main_router.get("/main_page", tags=["Main Page"])
def main_page(search: Union[str, None] = Query(default=None, alias="searchByCompanyName")):
    return main_page_detail(search)

