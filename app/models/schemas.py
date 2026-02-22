from pydantic import BaseModel, ConfigDict


class CampaignBrief(BaseModel):
    product_name: str
    product_description: str
    target_audience: str
    tone: str = "profissional"
    language: str = "pt-BR"
    platforms: list[str] = ["meta"]
    formats: list[str] = []
    num_variations: int = 3
    primary_color: str = "#1a1a2e"
    accent_color: str = "#e94560"
    text_color: str = "#ffffff"
    include_cta: bool = True
    cta_text: str = ""


class CopyVariation(BaseModel):
    hook: str
    headline: str
    body: str
    cta: str


class GeneratedCreative(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    ad_copy: CopyVariation
    format_name: str
    platform: str
    placement: str
    width: int
    height: int
    image_path: str


class GenerationResult(BaseModel):
    campaign_id: str
    brief: CampaignBrief
    creatives: list[GeneratedCreative]
