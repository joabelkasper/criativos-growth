import uuid
from pathlib import Path

from app.core.config import settings
from app.core.platforms import ALL_FORMATS, PLATFORM_FORMATS, FormatSpec
from app.models.schemas import (
    CampaignBrief,
    CopyVariation,
    GeneratedCreative,
    GenerationResult,
)
from app.services.copy_generator import generate_copy
from app.services.image_composer import compose_creative


def _resolve_formats(brief: CampaignBrief) -> list[FormatSpec]:
    """Resolve which image formats to generate based on the brief."""
    # If specific formats were requested, use those
    if brief.formats:
        formats = []
        for name in brief.formats:
            if name in ALL_FORMATS:
                formats.append(ALL_FORMATS[name])
        if formats:
            return formats

    # Otherwise, use defaults for selected platforms
    formats = []
    for platform in brief.platforms:
        key = platform.lower()
        if key in PLATFORM_FORMATS:
            formats.extend(PLATFORM_FORMATS[key])

    return formats or list(PLATFORM_FORMATS["meta"])


def generate_creatives(brief: CampaignBrief) -> GenerationResult:
    campaign_id = uuid.uuid4().hex[:12]
    campaign_dir = Path(settings.output_dir) / campaign_id
    campaign_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate copy variations via Claude
    copy_variations = generate_copy(brief)

    # 2. Resolve target formats
    formats = _resolve_formats(brief)

    # 3. Compose image for each copy x format combination
    creatives: list[GeneratedCreative] = []
    for vi, copy in enumerate(copy_variations, 1):
        for fmt in formats:
            safe_name = fmt.name.replace(" ", "_").replace("/", "-").lower()
            filename = f"v{vi}_{safe_name}_{fmt.width}x{fmt.height}.png"
            output_path = str(campaign_dir / filename)

            compose_creative(
                copy=copy,
                fmt=fmt,
                primary_color=brief.primary_color,
                accent_color=brief.accent_color,
                text_color=brief.text_color,
                output_path=output_path,
            )

            creatives.append(
                GeneratedCreative(
                    ad_copy=copy,
                    format_name=fmt.name,
                    platform=fmt.platform,
                    placement=fmt.placement,
                    width=fmt.width,
                    height=fmt.height,
                    image_path=output_path,
                )
            )

    return GenerationResult(
        campaign_id=campaign_id,
        brief=brief,
        creatives=creatives,
    )
