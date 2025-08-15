from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

import streamlit as st
from streamlit.components.v1 import html


def _local_images(images_dir: Path) -> List[Path]:
    if not images_dir.exists():
        return []
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    return sorted([p for p in images_dir.iterdir() if p.suffix.lower() in exts])


def render_gallery(images_dir: Path, instagram_post_urls: Iterable[str], max_images: int = 8) -> None:
    st.markdown("### Gallery")
    local = _local_images(images_dir)
    if local:
        cols = st.columns(4, gap="small")
        for i, img_path in enumerate(local[:max_images]):
            with cols[i % 4]:
                st.image(str(img_path), use_container_width=True, caption=img_path.name)
    else:
        st.caption("Add images to `assets/images/` to populate the gallery.")

    # Optional: show embeds if provided
    urls = list(instagram_post_urls or [])
    if urls:
        st.divider()
        st.caption("Instagram highlights")
        for u in urls[:2]:  # keep it light
            html(
                f"""
                <blockquote class="instagram-media" data-instgrm-permalink="{u}" data-instgrm-version="14"></blockquote>
                <script async src="//www.instagram.com/embed.js"></script>
                """,
                height=600,
            )
