#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report_template.py — 网站投放调研报告自包含 HTML 生成模板(泛化自 ReelFork 项目,已验证)
用法:
  1. 先运行 charts_template.py 生成 ./charts/*.png
  2. 编辑下方 DATA(章节标题、KPI、表格内容、SWOT、结论)
  3. 运行: python3 report_template.py
  4. 输出: 单文件自包含 HTML(图表 base64 内嵌,浏览器直接打开,可打印为 PDF)
注意: 内容区大量使用 f-string,正文中的 { } 需转义为 {{ }}
"""
import base64, os, datetime

CH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
OUT_HTML = '网站投放调研报告.html'  # 建议改为 <目标网站名>投放调研报告.html

def b64(name):
    with open(os.path.join(CH, name), 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

imgs = {n: b64(n) for n in os.listdir(CH)}
TODAY = datetime.date.today().isoformat()

# ============ 数据区:每次调研替换这里 ============
SITE = '目标平台'
DOMAIN = 'example.com'
REPORT_TITLE = f'{SITE}({DOMAIN})投放调研报告'
SUB = '平台定位一句话 · 网站基本信息 / 流量规模 / 用户画像 / 投放评估'
KPIS = [  # (数值, 小注, 标签)
    ('~5', '个月', '上线时间(域名注册日推算)'),
    ('22', '订阅', '官方 YouTube 频道'),
    ('1', '条', 'App Store 评分'),
    ('1.4', '万次', '平台头部作品最高播放量'),
]
EXEC_ROWS = [  # 执行摘要表: (结论tag, 结论, 依据)
    ('t-red', '极早期', '平台上线约5个月,处于冷启动阶段', '域名 2026-03-19 注册;iOS App 2026-05-10 上架(仅1条评分);未进入第三方流量库'),
    ('t-amber', '流量极小', '全站头部作品播放量仅 2,000~14,000 次', '对推荐位12部热门作品采样,多数在 2k~9k'),
    ('t-teal', '生态初具', '创作者生态以中文网文IP改编为特色,变现闭环已跑通', '创意市场需求墙约9成为中文需求,平台提供创作→上架→付费解锁闭环'),
]
EXEC_WARN = '投放决策提示:若"投作品"指品牌广告投放——当前流量规模不足以支撑有效曝光;若指内容/作品上架试水或抢占早期生态位——成本低、竞争小,可作低成本试验。'
BASIC_TABLE = [  # 平台基本信息表: (项目, 信息, 项目, 信息) 每行4列
    ('平台定位', '一句话定位(可引用官网)', '官方表述', '"无需编程、无需拍摄"的交互式创作'),
    ('域名注册', '2026-03-19(注册商,DNS)', 'iOS App', '上架日期,发行方,包名'),
    ('Android', '仅官网 APK 直装(未上架 Google Play)', '语言', '支持语言,中英双语,运营账号迹象'),
    ('开放格式', 'RFD 等', '内容分级', 'G 级为主,Pro 含 R-rated 18+ 模型'),
    ('创作者激励', '$X / 万次播放,月度结算,无排他性', '付费模式', '整剧/单集/DLC 付费解锁'),
]
BASIC_OK = '积极信号:产品完成度高于同类早期项目——(列举已上线的功能闭环)。'
TRAFFIC_NOTE = 'SimilarWeb、HypeStat、Website Informer、SitePrice 均未收录该域名(低于收录门槛,通常对应月访问量低于数万级),以下为可获取的公开信号:'
TRAFFIC_OFFICIAL = [  # 官方渠道数据表
    ('渠道', '数据'),
    ('YouTube 官方频道', '22 订阅 · 33 视频 · 总播放 8,871'),
    ('YouTube 视频表现', '单条播放多在 2~14 次,最高一条 431 次'),
    ('App Store', '评分 5.0 但仅 1 条评分;无下载量公开数据'),
    ('AI 工具导航收录页', '累计浏览 792 次'),
]
TRAFFIC_SITE = [  # 平台内容数据表
    ('指标', '数值'),
    ('全站头部作品播放', '最高 1.4 万次;推荐位 12 部热门均 1.7k~14k'),
    ('内容分类', '12 类:Romance / Mystery / Comedy / ...'),
    ('创作者身份', '中英文混合(中文昵称占比高)'),
]
TRAFFIC_EST = '规模估算(粗略,非精确):按头部作品播放与长尾水平推算,全站日活估计数百至数千级、月访问量数千至3万以内,与第三方流量库未收录相互印证。'
COMPETITOR_NOTE = '对比同类平台/App(ReelShort 46.7万评分、Shorts 2.5万评分),目标平台用户规模相差数万倍,属于绝对早期玩家。'
PROFILE_CREATOR = [  # 创作者侧画像
    ('核心人群', '中文区短剧团队、网文IP改编方、跨境MCN、独立创作者'),
    ('创作偏好', '宫斗/权谋/仙侠/志怪/都市异能/国风东方美学/乙女向'),
    ('变现诉求', '承制费($900~$20,000/部)+ 播放分成 + App 内付费解锁'),
    ('特征', '低门槛工具型用户——"输入网文设定→AI 批量产出",不需要拍摄剪辑能力'),
]
PROFILE_VIEWER = [  # 观看者侧画像
    ('移动端优先', '官方主推 iOS App 与 Android APK 直装'),
    ('内容口味', '互动/多结局剧情、乙女向、国风奇幻、悬疑惊悚'),
    ('地域推测', '中英双语+多语言+出海分发 → 中文区+海外华语圈为主,少量欧美东南亚尝鲜用户'),
    ('年龄画像', '参照短剧/互动内容受众,推测集中在 18~34 岁,女性向内容占比高'),
    ('注意', 'Pro 以上含 R-rated 18+ 模型,存在成人内容受众属性'),
]
BUSINESS_TABLE = [  # 创作者收入构成表
    ('渠道', '说明'),
    ('播放分成', '$0.70/万次播放,月度结算,无排他性(可多平台分发)'),
    ('承制订单', '需求墙公开订单,单价 $0~$20,000'),
    ('付费解锁', '整剧/单集/DLC 解锁收入'),
    ('邀请奖励', '邀请注册送积分;官方 Affiliate 计划'),
]
BUSINESS_WARN = '收益现实性提示:$0.70/万次播放的单价显著低于主流平台(YouTube 长视频分成约为其 5~20 倍量级)。平台现阶段更接近"作品展示+订单获客"场所,而非流量变现渠道。'
SWOT = dict(
    s=[('细分赛道差异化明确', 'AI 互动短剧(分支剧情/多结局),传统平台无此形态'),
       ('内容生态契合', '与国内网文 IP 供给高度契合(宫斗/仙侠/志怪题材需求旺盛)'),
       ('创作成本极低', 'AI 批量生成,试错成本小'),
       ('无排他性', '作品可同步分发到其他平台')],
    w=[('流量规模极小', '头部作品仅 1.4 万播放,曝光天花板低'),
       ('数据不透明', '第三方流量数据不可得,运营数据不公开'),
       ('分成单价低', '$0.7/万次,流量变现效率差'),
       ('分发受限', '无 Google Play 发行,Android 分发受限')],
    o=[('早期红利', '冷启动期,早期内容易获推荐位与官方扶持'),
       ('赛道叙事', '互动短剧出海是增长叙事,若平台起量则早期布局受益'),
       ('B端机会', '品牌互动广告模板(电商/文旅/游戏)已有需求单')],
    t=[('存活风险', '初创平台(运营不满6个月,无融资公开信息)'),
       ('合规风险', 'R-rated 18+ 模型带来内容合规与品牌形象风险'),
       ('竞争激烈', '同类巨头与AI短剧工具竞争'),
       ('版权条款', 'AI 生成内容版权与平台条款需逐条核实')],
)
TIER_TABLE = [  # 落地建议分档表
    ('投放目标', '建议方案', '预算参考'),
    ('A. 品牌曝光投放', '不建议。全站流量不足以支撑品牌广告回报;若坚持,仅作"新兴渠道占位"象征性投放', '—'),
    ('B. 作品/内容上架试水', '推荐作为低成本试验。以单部作品/模板入驻,观察流量扶持与用户反馈', '最低订阅档 $9~29/月,试水期 1~3 个月'),
    ('C. B 端接单/合作', '可注册创作者账号承接需求墙订单,以订单收入覆盖成本', '视订单体量'),
]
VERIFY_LIST = '① 真实 DAU/MAU 与留存数据;② 结算周期与到账机制;③ 官方流量扶持/推荐位规则;④ 内容版权归属与抽成条款;⑤ 成人内容政策与合规边界;⑥ 平台运营主体与融资情况。'
SOURCES = [  # 数据来源表
    ('数据项', '来源', '说明'),
    ('平台功能/定位/定价/激励', '官网各页面(首页、About、Pricing、FAQ 等)', '平台官方口径'),
    ('上线时间', 'WHOIS / App Store API / 社媒频道页', '可验证'),
    ('播放量/需求墙数据', '官网推荐位与创意市场页面实时采样', '时点快照,随时间变化'),
    ('第三方流量', 'SimilarWeb / HypeStat / Website Informer / SitePrice', '均无收录——这本身即为流量极小的证据'),
    ('竞品对比', 'Apple iTunes Search API', '公开榜单数据'),
]
LIMIT_NOTE = '局限性:① 平台不公开运营数据(DAU/MAU/收入),所有规模估算均为间接推断;② 用户画像无一手数据,系由内容与需求侧信号推断;③ 未发现融资、团队规模等公开信息;④ 数据采集于单一时点,早期平台变化快,建议投放前复核。'

# ============ 以下为渲染逻辑,一般无需修改 ============
CSS = """
:root{--navy:#1B2A4A;--indigo:#4C6EF5;--teal:#12B886;--amber:#FAB005;--red:#FA5252;--gray:#868E96;--bg:#F4F6FB;--card:#fff;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:"PingFang SC","Microsoft YaHei","WenQuanYi Zen Hei",sans-serif;background:var(--bg);color:#2b2f36;line-height:1.7;padding:24px;}
.wrap{max-width:980px;margin:0 auto;}
.hero{background:linear-gradient(135deg,#1B2A4A 0%,#3B5BDB 100%);color:#fff;border-radius:16px;padding:34px 38px;margin-bottom:22px;}
.hero h1{font-size:26px;margin-bottom:6px;}
.hero .sub{opacity:.85;font-size:14px;}
.hero .meta{margin-top:14px;font-size:12.5px;opacity:.9;border-top:1px solid rgba(255,255,255,.25);padding-top:12px;}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:22px;}
.kpi{background:var(--card);border-radius:12px;padding:16px;border:1px solid #E5EAF3;box-shadow:0 1px 3px rgba(27,42,74,.06);}
.kpi .v{font-size:21px;font-weight:700;color:var(--navy);}
.kpi .v small{font-size:12px;color:var(--gray);font-weight:400;}
.kpi .l{font-size:12px;color:var(--gray);margin-top:2px;}
.card{background:var(--card);border-radius:14px;padding:24px 26px;margin-bottom:20px;border:1px solid #E5EAF3;box-shadow:0 1px 3px rgba(27,42,74,.06);}
.card h2{font-size:18px;color:var(--navy);margin-bottom:4px;border-left:4px solid var(--indigo);padding-left:10px;}
.card .lead{font-size:13px;color:var(--gray);margin-bottom:14px;}
.card img{width:100%;border-radius:10px;border:1px solid #EDF0F7;margin:6px 0;}
table{width:100%;border-collapse:collapse;font-size:13px;margin:10px 0;}
th{background:var(--navy);color:#fff;padding:8px 10px;text-align:left;font-weight:600;}
td{padding:7px 10px;border-bottom:1px solid #EDF0F7;vertical-align:top;}
tr:nth-child(even) td{background:#F8FAFE;}
.tag{display:inline-block;padding:1px 8px;border-radius:20px;font-size:11.5px;margin-right:6px;}
.t-red{background:#FFE3E3;color:#C92A2A;}.t-amber{background:#FFF3BF;color:#A06100;}.t-teal{background:#C3FAE8;color:#087F5B;}.t-indigo{background:#DBE4FF;color:#364FC7;}.t-gray{background:#F1F3F5;color:#495057;}
.warn{background:#FFF9E6;border:1px solid #FFD43B;border-left:5px solid var(--amber);border-radius:8px;padding:12px 14px;font-size:13px;margin:10px 0;}
.ok{background:#E6FCF5;border:1px solid #38D9A9;border-left:5px solid var(--teal);border-radius:8px;padding:12px 14px;font-size:13px;margin:10px 0;}
.risk{background:#FFF5F5;border:1px solid #FFA8A8;border-left:5px solid var(--red);border-radius:8px;padding:12px 14px;font-size:13px;margin:10px 0;}
.foot{text-align:center;color:var(--gray);font-size:12px;margin:26px 0 10px;}
ul,ol{padding-left:20px;font-size:13.5px;}
li{margin:3px 0;}
.col2{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
@media(max-width:760px){.kpis{grid-template-columns:1fr 1fr}.col2{grid-template-columns:1fr}}
"""

def tbl(rows):
    out = ['<table>']
    for i, r in enumerate(rows):
        tag = 'th' if i == 0 else 'td'
        out.append('<tr>' + ''.join(f'<{tag}>' + str(c) + f'</{tag}>' for c in r) + '</tr>')
    out.append('</table>')
    return ''.join(out)

H = []
H.append(f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
          f'<meta name="viewport" content="width=device-width,initial-scale=1">'
          f'<title>{REPORT_TITLE}</title><style>{CSS}</style></head><body><div class="wrap">')

# Hero + KPI
kpi_html = ''.join(f'<div class="kpi"><div class="v">{v}<small> {u}</small></div>'
                   f'<div class="l">{l}</div></div>' for v, u, l in KPIS)
H.append(f'''<div class="hero"><h1>{REPORT_TITLE}</h1><div class="sub">{SUB}</div>
<div class="meta">调研日期:{TODAY} ｜ 用途:投放决策评估 ｜ 数据来源:官网各页面、App Store、YouTube、WHOIS、公开流量查询工具(详见文末)</div></div>
<div class="kpis">{kpi_html}</div>''')

# 一、执行摘要
rows = ''.join(f'<tr><td><span class="tag {t}">{tag}</span>{concl}</td><td>{basis}</td></tr>'
               for t, tag, concl, basis in EXEC_ROWS)
H.append(f'''<div class="card"><h2>执行摘要(领导一页速览)</h2><div class="lead">三句话结论</div>
<table><tr><th style="width:26%">结论</th><th>依据</th></tr>{rows}</table>
<div class="warn"><b>{EXEC_WARN}</b></div></div>''')

# 二、平台基本信息
H.append(f'''<div class="card"><h2>一、平台基本信息</h2><div class="lead">{SUB}</div>
<img src="{imgs.get('chart_timeline.png','')}" alt="时间线">
{tbl(BASIC_TABLE)}
<div class="ok"><b>积极信号:</b>{BASIC_OK}</div></div>''')

# 三、流量规模
H.append(f'''<div class="card"><h2>二、流量规模:第三方数据缺失,仅能基于平台自身信号估算</h2>
<div class="lead">{TRAFFIC_NOTE}</div>
<img src="{imgs.get('chart_traffic_signals.png','')}" alt="流量信号">
<img src="{imgs.get('chart_top_works.png','')}" alt="头部作品播放量">
<div class="col2"><div><h3 style="font-size:15px;color:var(--navy);margin:10px 0 4px">官方渠道数据</h3>
{tbl(TRAFFIC_OFFICIAL)}</div><div><h3 style="font-size:15px;color:var(--navy);margin:10px 0 4px">平台内容数据</h3>
{tbl(TRAFFIC_SITE)}</div></div>
<div class="warn"><b>规模估算(粗略,非精确):</b>{TRAFFIC_EST}</div>
<img src="{imgs.get('chart_competitor.png','')}" alt="竞品对比">
<div class="lead" style="margin-top:8px">{COMPETITOR_NOTE}</div></div>''')

# 四、用户画像
pc = ''.join(f'<li><b>{k}:</b>{v}</li>' for k, v in PROFILE_CREATOR)
pv = ''.join(f'<li><b>{k}:</b>{v}</li>' for k, v in PROFILE_VIEWER)
H.append(f'''<div class="card"><h2>三、用户画像(基于平台内容、需求墙与官方定位推断)</h2>
<div class="lead">注意:平台不公开用户数据,以下画像由可观察信号推断得出,供决策参考。</div>
<div class="col2"><div><h3 style="font-size:15px;color:var(--navy);margin-bottom:6px">创作者侧(供给侧)</h3><ul>{pc}</ul></div>
<div><h3 style="font-size:15px;color:var(--navy);margin-bottom:6px">观看者侧(需求侧)</h3><ul>{pv}</ul></div></div>
<img src="{imgs.get('chart_profile.png','')}" alt="需求方画像">
<img src="{imgs.get('chart_demand_wall.png','')}" alt="需求墙类型"></div>''')

# 五、商业模式
H.append(f'''<div class="card"><h2>四、商业模式与创作者变现</h2><div class="lead">平台收入来自创作者订阅(AI 生成额度),创作者收入来自播放分成+承制订单+内容付费解锁。</div>
<img src="{imgs.get('chart_pricing.png','')}" alt="定价">
<div class="col2"><div><h3 style="font-size:15px;color:var(--navy);margin:10px 0 4px">创作者收入构成</h3>
{tbl(BUSINESS_TABLE)}</div><div><h3 style="font-size:15px;color:var(--navy);margin:10px 0 4px">播放分成收入测算</h3>
<img src="{imgs.get('chart_payout_math.png','')}" alt="收入测算"></div></div>
<div class="warn"><b>{BUSINESS_WARN}</b></div></div>''')

# 六、投放建议 SWOT
def swot_list(title, color, items):
    lis = ''.join(f'<li><b>{k}:</b>{v}</li>' for k, v in items)
    return f'<h3 style="font-size:15px;color:{color};margin-bottom:6px">{title}</h3><ul>{lis}</ul>'
H.append(f'''<div class="card"><h2>五、投放决策建议(SWOT)</h2><div class="lead">围绕领导"在该平台投放作品"的目标,给出结构化评估</div>
<div class="col2"><div>{swot_list('优势 Strengths','#C92A2A',SWOT['s'])}
{swot_list('劣势 Weaknesses','#A06100',SWOT['w'])}</div>
<div>{swot_list('机会 Opportunities','#087F5B',SWOT['o'])}
{swot_list('威胁 Threats','#364FC7',SWOT['t'])}</div></div>
<h3 style="font-size:15px;color:var(--navy);margin:12px 0 6px">落地建议(按投放目标分档)</h3>
{tbl(TIER_TABLE)}
<div class="risk"><b>投放前必核实(建议直接联系平台方):</b>{VERIFY_LIST}</div></div>''')

# 七、数据来源
H.append(f'''<div class="card"><h2>六、数据来源与局限性说明</h2>
{tbl(SOURCES)}
<div class="warn"><b>局限性:</b>{LIMIT_NOTE}</div>
<div class="foot">本报告由 Hermes Agent 自动生成 · 调研时间 {TODAY} · 数据均附来源,估算部分已明确标注</div></div>''')

H.append('</div></body></html>')
with open(OUT_HTML, 'w', encoding='utf-8') as f:
    f.write('\n'.join(H))
print('written:', OUT_HTML, os.path.getsize(OUT_HTML), 'bytes')
