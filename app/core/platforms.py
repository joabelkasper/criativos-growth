from dataclasses import dataclass


@dataclass(frozen=True)
class FormatSpec:
    name: str
    width: int
    height: int
    platform: str
    placement: str


PLATFORM_FORMATS: dict[str, list[FormatSpec]] = {
    "meta": [
        FormatSpec("Feed Quadrado", 1080, 1080, "Meta", "Feed"),
        FormatSpec("Feed Retrato", 1080, 1350, "Meta", "Feed"),
        FormatSpec("Stories / Reels", 1080, 1920, "Meta", "Stories/Reels"),
    ],
    "google": [
        FormatSpec("Leaderboard", 728, 90, "Google Ads", "Display"),
        FormatSpec("Retângulo Médio", 300, 250, "Google Ads", "Display"),
        FormatSpec("Retângulo Grande", 336, 280, "Google Ads", "Display"),
        FormatSpec("Skyscraper", 160, 600, "Google Ads", "Display"),
    ],
    "tiktok": [
        FormatSpec("TikTok Feed", 1080, 1920, "TikTok", "Feed"),
    ],
}

ALL_FORMATS = {
    fmt.name: fmt
    for fmts in PLATFORM_FORMATS.values()
    for fmt in fmts
}
