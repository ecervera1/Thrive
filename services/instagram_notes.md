**# Instagram Intake Options for @thrivewfrida

This app supports three practical paths to get images/bio content in:

## 1) Manual (Recommended to start)
- Export a curated set of images from Instagram.
- Drop them into: `assets/images/` (JPEG/PNG/WebP).
- Update any captions or alt text directly in the UI or by renaming files.

**Pros**: Zero tokens/keys, very reliable.  
**Cons**: Manual refresh when you want new images.

## 2) URL List
- In `.streamlit/secrets.toml`, add:
  ```toml
  INSTAGRAM_POST_URLS=["https://www.instagram.com/p/XXXXXXXX/", "https://www.instagram.com/reel/YYYYYYYY/"]
**
