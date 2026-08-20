---
name: fund-analysis
description: "分析基金代码:抓取天天基金网数据并生成HTML分析报告。"
version: 1.0.0
author: Hermes Agent (adapted from coderzzy/agent-fund-analysis-skill, MIT)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [fund, 基金, investment, analysis, report, eastmoney]
    related_skills: [stock-analysis]
---

# 基金分析 fund-analysis

输入 6 位基金代码,抓取天天基金网历史净值,用确定性脚本计算多维指标(避免 LLM 幻觉),生成 PPT 风格 HTML 报告,再由 Agent 补充数据解读和投资建议。

## When to Use

- 用户给出 6 位基金代码并要"分析基金/基金分析/看看这只基金"
- 需要净值走势、压力/支撑位、持有周期收益、月度规律等历史数据分析
- 需要一份可交付/可导出的 HTML 分析报告

不适用:分析股票(用 stock-analysis)、不涉及具体代码的泛泛基金问答。

## 触发条件

用户输入以下任一 + 6 位基金代码时触发:
- "帮我分析基金 XXX"
- "分析基金 XXX" / "基金分析 XXX"
- 直接给出基金代码并表达分析意图

## 执行流程

### Step 1: 创建输出目录

```bash
mkdir -p output_fund/{基金代码}/raw output_fund/{基金代码}/analysis output_fund/{基金代码}/report
```

### Step 2: 抓取原始数据

```bash
curl -s "https://fund.eastmoney.com/pingzhongdata/{基金代码}.js?v=$(date +%Y%m%d%H%M%S)" \
  -H "Referer: https://fund.eastmoney.com/" \
  -o output_fund/{基金代码}/raw/{基金代码}_raw.js
```

### Step 3: 运行分析脚本

```bash
python3 scripts/fund_analyzer.py \
  --code {基金代码} \
  --input output_fund/{基金代码}/raw/{基金代码}_raw.js \
  --output output_fund/{基金代码}/report/report_{基金代码}.html \
  --json-output output_fund/{基金代码}/analysis/analysis_{基金代码}.json
```

脚本会自动解析 JS 变量并计算:净值走势、多周期统计、压力/支撑位、周期涨跌幅、收益反转周期、月度收益、最大回撤、年化波动率。

### Step 4: Agent 数据解读

同时读取 JSON(结构化数值)和 HTML 报告(可视化),将解读追加写入报告的"数据洞察"部分,替换"等待Agent解读..."占位文本。解读要点:
- 净值走势:整体趋势、波动幅度
- 压力指标:当前净值位于支撑还是压力位,最近的支撑/压力位在哪
- 周期收益:不同持有周期表现,短期 vs 长期
- 反转周期:正收益平均能持续多久,何时警惕
- 月度规律:是否有季节性
- 明确给出买入/持有/卖出建议 + 风险提示

## 压力位算法(供解读参考)

- 把历史最高~最低净值切成 10 个等宽档位
- 统计每档位内交易日买入后未来 5/10/20 天收益
- 上涨概率≥60% 且反弹概率≥55% → 支撑位;下跌概率≥60% 且回落概率≥55% → 压力位;否则中性
- 这是经验性统计,不是严格技术指标,须在报告里声明仅供参考

## 输出文件

| 类型 | 路径 |
|------|------|
| 原始数据 | output_fund/{代码}/raw/{代码}_raw.js |
| 分析结果 | output_fund/{代码}/analysis/analysis_{代码}.json |
| HTML 报告 | output_fund/{代码}/report/report_{代码}.html |

## 依赖

- python3 + numpy(脚本唯一第三方依赖,`pip install numpy` 或 `uv pip install numpy`)
- 报告自包含,浏览器打开即用,支持一键导出 PDF(需联网加载 ECharts CDN)
- 脚本不会自动创建 raw/analysis/report 目录,执行前务必先跑 Step 1 建目录

## 注意事项 / 陷阱

1. 数据源是非公开接口(fund.eastmoney.com/pingzhongdata/*.js),格式变化会导致解析失败 —— 失败时检查脚本正则与 data 字段是否对齐,或抓取失败给出明确报错而非乱报数字
2. 若 numpy 缺失:`pip install numpy`(本脚本只用到 numpy,无需其它包)
3. 抓取未经授权,仅供个人学习研究,勿高频调用规避风控
4. 报告含 AI 生成的投资建议,必须附免责声明,不构成投资建议
