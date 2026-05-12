# Context
User has 3 Korean promotional banners (yellow background, black bold text) and wants specific text changes in each. Since these are image files, they must be recreated programmatically using Python + Pillow. The originals were created with Genspark.

## Text Changes

### Banner 1 (portrait, ~810×1440px)
- Keep: `'뭐 사실 필요 없어요.'` (top, small)
- **Change**: Large center `그냥 들어오세요!` → `액상만 리필하고 가세요!`
- **Delete**: Bottom line `본인 기기만 들고 오면`

### Banner 2 (landscape, ~1440×540px)
- Keep: `본인 기기만 들고 오면` (top)
- **Change**: Large center `액상은 꽁짜!` → `액상 충전 = 꽁짜!`
- Keep: `구매 강요 없음 · 눈치 없음` (bottom)

### Banner 3 (landscape, ~1440×540px)
- Keep: `이건 진심입니다.` (top)
- **Change**: Large center `액상만 채우고 나가도` → `액상만 리필하고 가셔도`
- **Change**: Bottom `액상 충전 무료 · 구매 강요 없음` → `알바생은 섭섭하지 않습니다!`

## Implementation Plan

### Step 1 — Install Pillow
```
/c/Python314/python -m pip install Pillow
```

### Step 2 — Write Python script to recreate banners
File: `C:\Users\minho\Documents\Claude\make_banners.py`

**Approach:**
- Background: yellow `#FFD400` (approximated from originals)
- Font: `C:/Windows/Fonts/malgunbd.ttf` (Malgun Gothic Bold) — best available bold Korean system font
- Stroke/outline: simulate heavy weight by drawing text with a thick black stroke (or use font size scaling)
- Text alignment: centered horizontally
- Reproduce layout tiers: top small text / large center text / bottom small text

**Output files:**
- `banner1_updated.png` (portrait ~810×1440)
- `banner2_updated.png` (landscape ~1440×540)  
- `banner3_updated.png` (landscape ~1440×540)

All saved to `C:\Users\minho\Documents\Claude\`

### Step 3 — Run script and verify output

## Notes
- `malgunbd.ttf` is the boldest available sans-serif Korean font on this system; the originals used a heavier display font, so the result will be visually similar but not pixel-identical
- If the user wants an exact font match, NanumSquareExtraBold or GmarketSansBold can be downloaded separately
