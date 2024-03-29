from dataclasses import dataclass
from typing import Any

import psycopg
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ijproblems.internal_functions import get_internal_functions
from ijproblems.internal_functions.github_app import GITHUB_APP_CLIENT_ID
from ijproblems.routers.utils.cookie import get_preference_from_cookie
from ijproblems.routers.utils.database import get_db_conn

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@dataclass
class Page:
    page: int
    selected: bool


USERS_IN_ONE_PAGE = 200


@router.get("/ranking/", response_class=HTMLResponse, name="global_ranking")
def get_global_ranking(
    request: Request,
    conn: psycopg.Connection = Depends(get_db_conn),
) -> Any:
    preference = get_preference_from_cookie(request)
    page = 1
    return get_global_ranking_page(request, preference.contest_type, page, conn)


@router.get(
    "/ranking/{contest_type}/{page}",
    response_class=HTMLResponse,
    name="global_ranking_page",
)
def get_global_ranking_page(
    request: Request,
    contest_type: int,
    page: int,
    conn: psycopg.Connection = Depends(get_db_conn),
) -> Any:
    if contest_type not in [0, 1]:
        raise HTTPException(status_code=400)

    functions = get_internal_functions(conn)
    context: dict[str, Any] = {}

    preference = get_preference_from_cookie(request)
    preference.contest_type = contest_type
    context["preference"] = preference

    context["contest_type"] = contest_type
    context["points"] = functions.get_points(contest_type)
    context["total_row"] = functions.get_problems_total_row(contest_type)
    begin = (page - 1) * USERS_IN_ONE_PAGE + 1
    end = page * USERS_IN_ONE_PAGE
    context["ranking"] = functions.get_global_ranking(contest_type, begin, end)
    context["rank_begin"] = begin
    max_pages = functions.get_user_count(contest_type) // USERS_IN_ONE_PAGE + 1
    context["pages"] = [
        Page(page=p, selected=p == page) for p in range(1, max_pages + 1)
    ]

    github_login_info = functions.get_github_login_info(request)
    context["github_login_info"] = github_login_info
    context["github_app_client_id"] = GITHUB_APP_CLIENT_ID

    response = templates.TemplateResponse(
        request=request,
        name="global_ranking.html",
        context=context,
    )
    return response
