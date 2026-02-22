import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from app.core.platforms import FormatSpec
from app.models.schemas import CopyVariation


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    # Try system fonts in order of preference
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in font_paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current_line = ""

    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines or [""]


def _draw_gradient(draw: ImageDraw.ImageDraw, width: int, height: int,
                   color_top: tuple, color_bottom: tuple) -> None:
    for y in range(height):
        ratio = y / max(height - 1, 1)
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))


def _draw_accent_shape(draw: ImageDraw.ImageDraw, width: int, height: int,
                       accent_rgb: tuple) -> None:
    """Draw a decorative accent shape on the creative."""
    # Diagonal accent bar in the top-right corner
    accent_with_alpha = accent_rgb + (80,)
    points = [
        (int(width * 0.6), 0),
        (width, 0),
        (width, int(height * 0.35)),
    ]
    draw.polygon(points, fill=accent_with_alpha)


def compose_creative(
    copy: CopyVariation,
    fmt: FormatSpec,
    primary_color: str,
    accent_color: str,
    text_color: str,
    output_path: str,
) -> str:
    w, h = fmt.width, fmt.height
    primary_rgb = _hex_to_rgb(primary_color)
    accent_rgb = _hex_to_rgb(accent_color)
    text_rgb = _hex_to_rgb(text_color)

    # Darken primary for gradient bottom
    darker = tuple(max(0, c - 40) for c in primary_rgb)

    img = Image.new("RGBA", (w, h), primary_rgb + (255,))
    draw = ImageDraw.Draw(img)

    # Background gradient
    _draw_gradient(draw, w, h, primary_rgb, darker)

    # Accent decoration
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    _draw_accent_shape(overlay_draw, w, h, accent_rgb)
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Calculate adaptive font sizes based on image dimensions
    ref = min(w, h)
    hook_size = max(14, int(ref * 0.045))
    headline_size = max(18, int(ref * 0.075))
    body_size = max(12, int(ref * 0.035))
    cta_size = max(14, int(ref * 0.04))

    padding_x = int(w * 0.08)
    max_text_w = w - 2 * padding_x

    font_hook = _get_font(hook_size, bold=False)
    font_headline = _get_font(headline_size, bold=True)
    font_body = _get_font(body_size, bold=False)
    font_cta = _get_font(cta_size, bold=True)

    # Layout: hook at ~20%, headline at ~35%, body at ~55%, CTA at ~75%
    y_hook = int(h * 0.18)
    y_headline = int(h * 0.32)
    y_body = int(h * 0.52)
    y_cta = int(h * 0.72)

    # Draw hook (with accent color)
    accent_muted = tuple(min(255, c + 60) for c in accent_rgb)
    hook_lines = _wrap_text(copy.hook.upper(), font_hook, max_text_w)
    for i, line in enumerate(hook_lines):
        draw.text((padding_x, y_hook + i * (hook_size + 4)),
                  line, fill=accent_muted, font=font_hook)

    # Draw headline
    hl_lines = _wrap_text(copy.headline, font_headline, max_text_w)
    for i, line in enumerate(hl_lines):
        draw.text((padding_x, y_headline + i * (headline_size + 6)),
                  line, fill=text_rgb, font=font_headline)

    # Draw body
    body_lines = _wrap_text(copy.body, font_body, max_text_w)
    for i, line in enumerate(body_lines):
        draw.text((padding_x, y_body + i * (body_size + 4)),
                  line, fill=text_rgb + (200,), font=font_body)

    # Draw CTA button
    cta_lines = _wrap_text(copy.cta, font_cta, max_text_w - 40)
    cta_text = cta_lines[0] if cta_lines else copy.cta
    cta_bbox = font_cta.getbbox(cta_text)
    cta_w = cta_bbox[2] - cta_bbox[0] + 40
    cta_h = cta_bbox[3] - cta_bbox[1] + 20
    cta_x = padding_x
    cta_y = y_cta

    # Button background with rounded rectangle
    btn_rect = [cta_x, cta_y, cta_x + cta_w, cta_y + cta_h]
    radius = min(8, cta_h // 3)
    draw.rounded_rectangle(btn_rect, radius=radius, fill=accent_rgb)
    draw.text((cta_x + 20, cta_y + 8), cta_text, fill=text_rgb, font=font_cta)

    # Save as RGB (no alpha for final output)
    final = img.convert("RGB")
    final.save(output_path, "PNG", quality=95)
    return output_path
