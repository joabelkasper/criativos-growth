from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.core.platforms import PLATFORM_FORMATS
from app.models.schemas import CampaignBrief
from app.services.creative_engine import generate_creatives

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "platforms": PLATFORM_FORMATS,
    })


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    product_name: str = Form(...),
    product_description: str = Form(...),
    target_audience: str = Form(...),
    tone: str = Form("profissional"),
    language: str = Form("pt-BR"),
    platforms: list[str] = Form(["meta"]),
    num_variations: int = Form(3),
    primary_color: str = Form("#1a1a2e"),
    accent_color: str = Form("#e94560"),
    text_color: str = Form("#ffffff"),
    cta_text: str = Form(""),
):
    brief = CampaignBrief(
        product_name=product_name,
        product_description=product_description,
        target_audience=target_audience,
        tone=tone,
        language=language,
        platforms=platforms,
        num_variations=num_variations,
        primary_color=primary_color,
        accent_color=accent_color,
        text_color=text_color,
        include_cta=True,
        cta_text=cta_text,
    )

    result = generate_creatives(brief)

    return templates.TemplateResponse("results.html", {
        "request": request,
        "result": result,
    })


@router.get("/creative/{campaign_id}/{filename}")
async def serve_creative(campaign_id: str, filename: str):
    path = Path("output") / campaign_id / filename
    if not path.exists():
        return HTMLResponse("Arquivo não encontrado", status_code=404)
    return FileResponse(path, media_type="image/png")
