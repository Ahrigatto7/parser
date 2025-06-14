"""Simple ontology and relation utilities for 명리학.

This module provides helper functions for representing 육친성
relationships as a matrix and fetching concept definitions.
"""

from __future__ import annotations

from typing import Dict, Optional

# 오행 상생 관계 (generating cycle)
GENERATES: Dict[str, str] = {
    "목": "화",
    "화": "토",
    "토": "금",
    "금": "수",
    "수": "목",
}

# 오행 상극 관계 (controlling cycle)
CONTROLS: Dict[str, str] = {
    "목": "토",
    "토": "수",
    "수": "화",
    "화": "금",
    "금": "목",
}

CONCEPT_DEFINITIONS: Dict[str, str] = {
    "비견": "같은 오행으로 서로 돕거나 경쟁하는 관계",
    "식상": "일간이 생하여 나가는 기운",
    "재성": "일간이 극하여 얻는 대상",
    "관성": "일간을 극하는 기운으로 규범이나 통제",
    "인성": "일간을 생하는 기운으로 도움이나 보호",
}

RELATION_MAP = {
    "생": "식상",
    "극": "재성",
    "극당함": "관성",
    "생당함": "인성",
    "동": "비견",
}


def relation_of(day_master: str, other: str) -> Optional[str]:
    """Return simplified 육친성 relation between day_master and other.

    Parameters
    ----------
    day_master: str
        오행 글자 (목/화/토/금/수)
    other: str
        비교할 오행 글자

    Returns
    -------
    Optional[str]
        관계명(식상, 재성, 관성, 인성, 비견) 또는 None
    """
    if day_master == other:
        return "비견"
    if GENERATES.get(day_master) == other:
        return "식상"
    if GENERATES.get(other) == day_master:
        return "인성"
    if CONTROLS.get(day_master) == other:
        return "재성"
    if CONTROLS.get(other) == day_master:
        return "관성"
    return None


def get_definition(concept: str) -> Optional[str]:
    """Fetch concept definition from the dictionary."""
    return CONCEPT_DEFINITIONS.get(concept)


if __name__ == "__main__":  # simple demo
    dm = "목"
    targets = ["화", "토", "목", "금", "수"]
    for t in targets:
        rel = relation_of(dm, t)
        print(f"{dm} vs {t} -> {rel}")

