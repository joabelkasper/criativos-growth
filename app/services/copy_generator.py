import json

import anthropic

from app.core.config import settings
from app.models.schemas import CampaignBrief, CopyVariation

SYSTEM_PROMPT = """\
Você é um copywriter especialista em tráfego pago e social media.
Sua tarefa é gerar variações de criativos publicitários de alta conversão.

Regras:
- Cada variação deve ter: hook, headline, body e cta
- Os hooks devem ser emocionalmente impactantes e diferentes entre si
- As headlines devem ser curtas e diretas (máximo 8 palavras)
- O body deve ter no máximo 2 frases curtas
- O CTA deve ser um comando de ação claro
- Adapte o tom conforme solicitado
- SEMPRE responda em JSON válido, sem markdown ou texto extra
"""


def _build_user_prompt(brief: CampaignBrief) -> str:
    platform_names = ", ".join(brief.platforms)
    cta_instruction = (
        f'Use este CTA em todas as variações: "{brief.cta_text}"'
        if brief.cta_text
        else "Crie CTAs variados e persuasivos"
    )

    return f"""\
Gere {brief.num_variations} variações de copy para o seguinte produto/serviço:

Produto: {brief.product_name}
Descrição: {brief.product_description}
Público-alvo: {brief.target_audience}
Tom de voz: {brief.tone}
Idioma: {brief.language}
Plataformas: {platform_names}
CTA: {cta_instruction}

Responda APENAS com um JSON no formato:
{{
  "variations": [
    {{
      "hook": "texto do hook",
      "headline": "texto da headline",
      "body": "texto do body",
      "cta": "texto do CTA"
    }}
  ]
}}
"""


def generate_copy(brief: CampaignBrief) -> list[CopyVariation]:
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    message = client.messages.create(
        model=settings.model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_user_prompt(brief)}],
    )

    raw = message.content[0].text.strip()
    # Handle potential markdown fencing
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    data = json.loads(raw)
    return [CopyVariation(**v) for v in data["variations"]]
