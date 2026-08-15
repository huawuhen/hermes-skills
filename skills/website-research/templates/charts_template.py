#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
charts_template.py — 网站调研报告图表生成模板(泛化自 ReelFork 项目,已验证)
用法:
  1. 把下面各图函数中的 DATA 换成新目标网站的实际调研数据
  2. 运行: python3 charts_template.py  (输出到 ./charts/)
  3. 所有图表为 PNG,供 report_template.py 以 base64 内嵌进自包含 HTML
依赖: python3-matplotlib(apt 安装), 中文字体 WenQuanYi Zen Hei
"""
import os
from matplotlib import font_manager
import matplotlib.pyplot as plt
import numpy as np

# ---- 中文字体(本机已验证,若缺先 apt-get install fonts-wqy-zenhei) ----
font_manager.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 140

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
os.makedirs(OUT, exist_ok=True)

# 统一商务配色(与报告 CSS 的 --navy/--indigo/--teal/--amber/--red 呼应)
C = dict(indigo='#4C6EF5', teal='#12B886', amber='#FAB005', red='#FA5252',
         gray='#868E96', navy='#1B2A4A', light='#E9ECEF')


def save(fig, name):
    fig.savefig(f'{OUT}/{name}', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('saved', name)


# ---------- 0. 数据区:每次调研替换这里 ----------
SITE = 'Example.com'
DATA = dict(
    timeline=[  # (日期, 事件), 至少含: 域名注册 / App上架 / 社媒开通 / 调研时点
        ('2026-01-01', '域名注册\nexample.com'),
        ('2026-03-01', 'iOS App 上架'),
        ('2026-08-01', '调研时点\n(上线约7个月)'),
    ],
    traffic_signals=[  # (标签, 数值): YouTube订阅/视频数/播放、AppStore评分数、目录页浏览
        ('YouTube\n订阅数', 22), ('YouTube\n视频数', 33),
        ('App Store\n评分数', 1), ('AI目录页\n浏览数', 792),
    ],
    top_works=[  # (作品名, 播放量) — 从平台推荐位/榜单实时采样
        ('Work A', 14000), ('Work B', 12000), ('Work C', 7900), ('Work D', 2000),
    ],
    pricing=[  # (档位, 月费USD)
        ('Lite', 9), ('Pro\n(热门)', 29), ('Max', 99), ('Studio', 199),
    ],
    demand_wall=[  # (需求类别标签, 条数) — 需求墙/创意市场采样, 共N条
        ('智能工作流/模板\n12条 (40%)', 12), ('短剧承制\n7条 (23%)', 7),
        ('互动剧承制\n6条 (20%)', 6), ('品牌广告\n5条 (17%)', 5),
    ],
    payout_rate=0.70,  # 官方激励 USD/万次播放
    competitor_ratings=[  # (应用名, AppStore评分数量)
        ('目标平台', 1), ('竞品A', 25610), ('竞品B\n(行业龙头)', 467643),
    ],
    requester_profile=[  # (需求方画像标签, 条数)
        ('短剧/IP团队 & MCN\n(承制单)', 13), ('平台增长/泛娱乐\n(裂变模板)', 9),
        ('品牌/商家营销\n(电商·文旅·游戏)', 6), ('工具型用户', 2),
    ],
)


# ---------- 1. 发展时间线 ----------
def chart_timeline():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    events = DATA['timeline']
    x = np.arange(len(events))
    for i, (d, t) in enumerate(events):
        is_now = '调研' in t
        ax.plot(i, 0, 'o', ms=10, color=C['red'] if is_now else C['indigo'], zorder=3)
        ax.annotate(d, (i, 0.12), ha='center', fontsize=10, fontweight='bold', color=C['navy'])
        ax.annotate(t, (i, 0.42), ha='center', fontsize=9.5, color='#333',
                    bbox=dict(boxstyle='round,pad=0.35', fc=C['light'], ec='none'))
    ax.plot(x, [0]*len(x), color=C['gray'], lw=2, zorder=1)
    ax.set_ylim(-0.4, 1.1)
    ax.axis('off')
    ax.set_title(f'{SITE} 发展时间线', fontsize=14, fontweight='bold', color=C['navy'], pad=14)
    save(fig, 'chart_timeline.png')


# ---------- 2. 流量信号(对数刻度) ----------
def chart_traffic_signals():
    fig, ax = plt.subplots(figsize=(9, 4.2))
    items = [i[0] for i in DATA['traffic_signals']]
    vals = [i[1] for i in DATA['traffic_signals']]
    cols = [C['indigo'], C['teal'], C['amber'], C['gray']][:len(vals)]
    bars = ax.bar(items, vals, color=cols, width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, v*1.03, f'{v:,}', ha='center',
                fontsize=12, fontweight='bold', color=C['navy'])
    ax.set_yscale('log'); ax.set_ylim(0.8, max(vals)*3)
    ax.set_ylabel('数量(对数刻度)', fontsize=10)
    ax.set_title('平台自有渠道的流量信号(均为个位数到百级)', fontsize=13,
                 fontweight='bold', color=C['navy'])
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', ls='--', alpha=0.3)
    save(fig, 'chart_traffic_signals.png')


# ---------- 3. 头部作品播放量(横向条形) ----------
def chart_top_works():
    fig, ax = plt.subplots(figsize=(10, 5.2))
    works = sorted(DATA['top_works'], key=lambda w: w[1])
    names = [w[0] for w in works]
    vals = [w[1] for w in works]
    colors = [C['red'] if v == max(vals) else C['indigo'] for v in vals]
    bars = ax.barh(names, vals, color=colors, height=0.6)
    for b, v in zip(bars, vals):
        ax.text(v + max(vals)*0.02, b.get_y()+b.get_height()/2, f'{v/1000:.1f}k',
                va='center', fontsize=9.5, color=C['navy'])
    ax.set_xlim(0, max(vals)*1.18)
    ax.set_xlabel('播放量(次)', fontsize=10)
    ax.set_title(f'{SITE} 推荐位热门作品播放量(调研日采样)', fontsize=13,
                 fontweight='bold', color=C['navy'])
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='x', ls='--', alpha=0.3)
    save(fig, 'chart_top_works.png')


# ---------- 4. 定价阶梯 ----------
def chart_pricing():
    fig, ax = plt.subplots(figsize=(9, 4.4))
    tiers = [p[0] for p in DATA['pricing']]
    prices = [p[1] for p in DATA['pricing']]
    cols = [C['gray'], C['indigo'], C['teal'], C['amber']][:len(prices)]
    bars = ax.bar(tiers, prices, color=cols, width=0.55)
    for b, v in zip(bars, prices):
        ax.text(b.get_x()+b.get_width()/2, v+max(prices)*0.03, f'${v}/月',
                ha='center', fontsize=12, fontweight='bold', color=C['navy'])
    ax.set_ylim(0, max(prices)*1.15)
    ax.set_ylabel('月费(美元)', fontsize=10)
    ax.set_title('创作者端订阅价格阶梯', fontsize=13, fontweight='bold', color=C['navy'])
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', ls='--', alpha=0.3)
    save(fig, 'chart_pricing.png')


# ---------- 5. 需求墙类型分布(环形图) ----------
def chart_demand_wall():
    fig, ax = plt.subplots(figsize=(7.2, 5))
    labels = [d[0] for d in DATA['demand_wall']]
    sizes = [d[1] for d in DATA['demand_wall']]
    cols = [C['indigo'], C['teal'], C['amber'], C['red']][:len(sizes)]
    ax.pie(sizes, labels=labels, colors=cols, autopct='', startangle=90,
           counterclock=False, wedgeprops=dict(width=0.42, edgecolor='white'))
    ax.set_title(f'创意市场(Demand Wall)需求类型分布\n(调研日采集,共{sum(sizes)}条公开需求)',
                 fontsize=12.5, fontweight='bold', color=C['navy'])
    save(fig, 'chart_demand_wall.png')


# ---------- 6. 播放→收入测算(对数刻度) ----------
def chart_payout_math():
    fig, ax = plt.subplots(figsize=(9, 4.4))
    views = [1, 10, 100, 1000]
    rate = DATA['payout_rate']
    earn = [rate*v for v in views]
    bars = ax.bar([f'{v}万' for v in views], earn, color=C['teal'], width=0.5)
    for b, v in zip(bars, earn):
        ax.text(b.get_x()+b.get_width()/2, v*1.04, f'${v:,.0f}',
                ha='center', fontsize=12, fontweight='bold', color=C['navy'])
    ax.set_yscale('log'); ax.set_ylim(rate*0.6, max(earn)*3)
    ax.set_ylabel('创作者收入(美元,对数刻度)', fontsize=10)
    ax.set_title(f'按官方激励 ${rate}/万次播放 测算:播放量→收入', fontsize=13,
                 fontweight='bold', color=C['navy'])
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', ls='--', alpha=0.3)
    save(fig, 'chart_payout_math.png')


# ---------- 7. 竞品对比(App Store 评分规模,对数) ----------
def chart_competitor():
    fig, ax = plt.subplots(figsize=(9, 4.4))
    apps = [c[0] for c in DATA['competitor_ratings']]
    ratings = [c[1] for c in DATA['competitor_ratings']]
    cols = [C['red'] if i == 0 else C['amber'] if i < len(ratings)-1 else C['indigo']
            for i in range(len(ratings))]
    bars = ax.bar(apps, ratings, color=cols, width=0.5)
    for b, v in zip(bars, ratings):
        ax.text(b.get_x()+b.get_width()/2, v*1.05, f'{v:,}',
                ha='center', fontsize=11.5, fontweight='bold', color=C['navy'])
    ax.set_yscale('log'); ax.set_ylim(0.7, max(ratings)*6)
    ax.set_ylabel('App Store 评分数量(对数刻度)', fontsize=10)
    ax.set_title(f'App Store 用户规模对比:{SITE} vs 同类竞品', fontsize=13,
                 fontweight='bold', color=C['navy'])
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', ls='--', alpha=0.3)
    save(fig, 'chart_competitor.png')


# ---------- 8. 需求方画像(横向条形) ----------
def chart_profile():
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    seg = sorted(DATA['requester_profile'], key=lambda s: s[1])
    names = [s[0] for s in seg]
    vals = [s[1] for s in seg]
    bars = ax.barh(names, vals, color=[C['indigo'], C['teal'], C['amber'], C['gray']][:len(vals)],
                   height=0.55)
    for b, v in zip(bars, vals):
        ax.text(v+0.15, b.get_y()+b.get_height()/2, str(v), va='center',
                fontsize=11, fontweight='bold', color=C['navy'])
    ax.set_xlim(0, max(vals)*1.15)
    ax.set_xlabel('需求条数', fontsize=10)
    ax.set_title('需求方画像:谁在平台上花钱找创作者?(按需求墙归类)', fontsize=13,
                 fontweight='bold', color=C['navy'])
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='x', ls='--', alpha=0.3)
    save(fig, 'chart_profile.png')


if __name__ == '__main__':
    chart_timeline()
    chart_traffic_signals()
    chart_top_works()
    chart_pricing()
    chart_demand_wall()
    chart_payout_math()
    chart_competitor()
    chart_profile()
    print('ALL CHARTS DONE ->', OUT)
