# Chinese Charts with matplotlib + Self-Contained HTML Reports

Verified working on this machine (Debian, matplotlib 3.6.3, WenQuanYi Zen Hei present).

## Install (if missing)

```bash
apt-get install -y python3-matplotlib   # no pip on this box (PEP 668); apt is the path
```

## Chinese font setup

WenQuanYi Zen Hei ships at `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc`. matplotlib's
`addfont` accepts `.ttc` since 3.x. Verify availability first with `fc-list :lang=zh`.

```python
from matplotlib import font_manager
import matplotlib.pyplot as plt

font_manager.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False   # minus signs render as boxes otherwise
```

Pitfalls:
- Glyphs like ✓/✗ may be missing from WenQuanYi (UserWarning "Glyph missing from current font") — avoid decorative glyphs inside charts; they render as boxes.
- Set `figure.dpi = 140`+ and `bbox_inches='tight'` for crisp embedding.
- `ax.spines[['top','right']].set_visible(False)` + light `grid(axis=..., ls='--', alpha=0.3)` gives the clean look leadership reports need.

## Self-contained HTML report (single file, opens anywhere, printable to PDF)

Embed every chart as base64 so the report is ONE file with no external assets:

```python
import base64
def b64(name):
    with open(f'charts/{name}', 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()
# <img src="{b64('chart_x.png')}">
```

Design conventions that worked (Chinese business report):
- Hero header: dark navy → indigo gradient, title + 调研日期/用途/数据来源 meta line
- 4 KPI cards grid under the hero (big number + label) so leadership gets the scale instantly
- Card sections with `border-left: 4px solid` colored headings
- Colored callout boxes: `.warn` (amber) / `.ok` (teal) / `.risk` (red) for 提示/积极信号/风险
- Two-column grids for SWOT and side-by-side tables; collapse to 1 col under 760px
- Final card: 数据来源与局限性 table + honest limitations box — every figure sourced
- Footer: "由 Hermes Agent 自动生成 · 调研时间 … · 估算部分已明确标注"

## Chart ideas that land well for placement decisions

- Launch timeline (WHOIS date → app store date → socials → today)
- Traffic-signal bars (YouTube subs/videos/views, App Store rating count, directory page views)
- Top-content plays bar chart (sample from the platform's own recommendation slots)
- Pricing tier bars, payout-math bars (播放量→收入 at official rate, log scale)
- Competitor comparison via App Store rating counts (log scale: 1 vs 467,643 makes the gap obvious)
- Marketplace/demand-wall category pie; requester-profile horizontal bars
