---
name: website-research
description: Use when researching a website for 投放/placement decisions.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, traffic, user-profile, placement, report, chinese]
    related_skills: [competitor-news-monitor]
---

# Website Research & Placement Assessment (网站/平台调研与投放评估)

## When to Use

Use when the user wants to evaluate an unfamiliar website or platform before a business decision — typically 投放 (advertising or content placement), partnership, or collaboration. Trigger phrases: "调研/调查这个网站", "它的访问量、用户画像", "领导想在上面投作品/投放/合作", "整理一份报告，尽量以图表形式展现".

## Workflow

1. **Clarify the decision first.** 投放(品牌广告曝光) vs 作品上架试水 vs 合作/接单 changes the entire recommendation. The user may not know the marketing vocabulary ("我不是互联网从业者不知道该怎么描述需求") — translate their intent yourself: e.g. "领导想在这个网站上投作品" = placing content/works on the platform, not buying ads. If ambiguous, ask one targeted question.
2. **Third-party traffic check — do this EARLY, because absence is evidence.**
   - SimilarWeb public endpoint: `curl https://data.similarweb.com/api/v1/data?domain=<d>` (frequently CloudFront-403 from datacenter IPs — note the block, but don't conclude anything from it alone).
   - `https://hypestat.com/info/<d>`, `https://website.informer.com/<d>`, `https://www.siteprice.org/website-worth/<d>`. If the site is NOT in these databases, it is below their indexing threshold (typically under ~tens of thousands of monthly visits). **Write this explicitly in the report: absence from third-party traffic databases is itself a traffic-size signal.**
3. **Domain age / WHOIS**: `whois <d>` → `Creation Date` = launch age; registrar (NameCheap = likely indie/cheap setup); nameservers (Cloudflare common).
4. **App Store presence**: `curl "https://itunes.apple.com/search?term=<name>&entity=software&limit=10"` → `releaseDate` (app age), `averageUserRating` + `userRatingCount` (user-base scale), `sellerName` (often reveals the operating entity), `bundleId`, `genres`. iTunes returns loose name matches — filter by exact `trackName`.
5. **YouTube channel**: `curl "https://www.youtube.com/results?search_query=<name>"` and regex `var ytInitialData = ({...});</script>` for `channelRenderer` (title, subscriberCountText, videoCountText); or browse `https://www.youtube.com/@<handle>/about` (subs, joined date, total views). Single-digit video views + tiny subs = no organic reach.
6. **Browse the site itself** — marketing sites are JS-rendered; `curl` yields only meta tags. Use the browser: home, /about, /faq, /pricing, /market (marketplace), player/viewer pages. Extract compact text via browser_console `document.body.innerText` when full snapshots get huge. Harvest:
   - Pricing tiers → business model & per-seat cost
   - Creator payouts ("$0.70 per 10K views") → compute effective CPM; compare vs industry (~$10-35 CPM YouTube long-form) to expose weak monetization
   - Marketplace/demand-wall posts → who pays, for what, in which language, price ranges (gold for user profile)
   - Content categories, language switch options, 18+/R-rated add-ons (compliance risk), app links (App Store / Google Play / APK-only)
   - **APK-only Android distribution (no Google Play) is a maturity red flag.**
7. **Competitor comparison**: iTunes search results give rating counts for competitors in the same query (e.g. ReelShort 467k ratings vs target 1) — a log-scale bar chart makes the gap vivid for leadership.
8. **User profile inference**: platforms almost never publish user data — infer from demand-post language mix, genres, RMB vs USD pricing, creator nicknames, content categories, target-market statements (出海/TikTok/YouTube Shorts). **Label every inference as 推断 in the report; never present it as fact.**
9. **Generate the charted report** (structure below).

## Report format (what this user's leadership expects)

Deliver: self-contained HTML with base64-embedded charts (single file, opens in any browser, printable to PDF) + the key chart PNGs as chat attachments + a short Chinese chat summary with the headline conclusion first.

Structure:
1. **执行摘要** — decision-maker table (结论/依据), first page only
2. **平台基本信息** — facts table + launch-timeline chart
3. **流量规模** — third-party-absence statement + traffic-signal charts + competitor comparison
4. **用户画像** — creator side vs viewer side, all inferences labeled
5. **商业模式与变现** — pricing chart + payout-math chart
6. **投放建议** — SWOT (优势/劣势/机会/威胁) + tiered recommendation table (品牌曝光/作品试水/接单, each with budget) + "投放前必核实" question list (DAU/MAU, payout terms, IP rights, compliance, funding)
7. **数据来源与局限性** — every data item sourced; estimates explicitly flagged

Pitfalls:
- `web_extract` fails when the search backend is Brave (search-only, no extraction backend configured) — use browser or curl instead.
- SimilarWeb blocks datacenter IPs (CloudFront 403) — don't burn time on it; absence from the OTHER tools is the evidence.
- Never mix estimates and verified facts without labels — decision-maker reports lose credibility.
- For sites <6 months old with tiny traffic: recommend 低成本试水 (cheapest subscription tier, 1-3 months) over 广告投放; lead with this in the exec summary.

## Support files
- `references/chinese-matplotlib-charts.md` — Chinese font setup for matplotlib + base64 HTML embedding (required for charted reports in Chinese).
- `scripts/site_signals.sh` — one-shot probe: WHOIS + traffic-tool absence + iTunes search + YouTube channel for any domain.
- `templates/charts_template.py` — ready-to-run chart generator (8 chart types: timeline / traffic signals / top works / pricing / demand-wall / payout math / competitor / requester profile). Edit the `DATA` dict, run, get `charts/*.png`.
- `templates/report_template.py` — ready-to-run self-contained HTML report builder (hero + KPI cards + 7 sections incl. exec-summary table, SWOT, tiered recommendation, sources). Edit the `DATA` section, run after charts, get a single portable HTML file.

## Fast path (proven workflow from ReelFork project)
1. `scripts/site_signals.sh <domain> <term>` → WHOIS age, App Store listing, traffic-DB absence, YouTube channel.
2. Browse the site (browser_navigate + browser_console `document.body.innerText` for compact text): pricing, creator payouts, marketplace/demand-wall, categories, app-store links, language options, 18+ flags.
3. Sample recommendation slots / marketplace for real numbers (播放量、需求条数、单价) — time-stamped snapshot.
4. Copy the two templates into a new project dir, replace the `DATA` blocks with real findings, run charts then report.
5. Verify in browser (browser_vision: 中文无乱码、布局正常), then deliver HTML + 2-4 key PNGs via MEDIA + a short Chinese chat summary (headline conclusion first).
