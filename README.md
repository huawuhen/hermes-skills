# Hermes Skills 通用技能包

由 Hermes Agent 在实战任务中提炼的可复用技能集合,遵循 [Hermes Agent 技能规范](https://hermes-agent.nousresearch.com/docs)(YAML frontmatter + markdown body)。

## 技能列表

| 技能 | 用途 | 触发场景 |
|---|---|---|
| [website-research](skills/website-research/) | 网站/平台调研与投放评估 | "调研这个网站"、"它的访问量、用户画像"、"领导想在上面投作品/投放/合作"、"整理一份报告,尽量以图表形式展现" |

## 安装方法

把对应技能目录复制到 Hermes 的 skills 目录即可:

```bash
# 安装 website-research 技能
mkdir -p ~/.hermes/skills/research/
cp -r skills/website-research ~/.hermes/skills/research/
```

重启/刷新 Hermes 后,技能即可被自动加载。技能文件布局:

```
website-research/
├── SKILL.md                        # 技能主文件(工作流 + 报告格式 + 踩坑记录)
├── references/
│   └── chinese-matplotlib-charts.md  # matplotlib 中文字体 + 自包含 HTML 报告技术参考
├── scripts/
│   └── site_signals.sh             # 一键探针:WHOIS + 流量库缺失检测 + iTunes + YouTube
└── templates/
    ├── charts_template.py          # 8 类图表生成器(改 DATA 即用)
    └── report_template.py          # 自包含 HTML 报告生成器(改 DATA 即用)
```

## website-research 快速上手

```bash
# 1. 探针目标网站公开信号
./skills/website-research/scripts/site_signals.sh <domain> <search_term>

# 2. 复制模板到项目目录,填入调研数据
cp skills/website-research/templates/*.py /path/to/project/
cd /path/to/project && python3 charts_template.py && python3 report_template.py

# 3. 产出:单文件自包含 HTML 报告(图表 base64 内嵌,可打印 PDF)+ charts/*.png
```

完整工作流与报告规范见 `skills/website-research/SKILL.md`。

## 报告产出规格(领导层验收标准)

- 自包含 HTML(单文件、浏览器直接打开、可转 PDF)+ 关键图表 PNG
- 中文呈现,图表优先
- 结构:执行摘要 → 平台信息 → 流量规模 → 用户画像 → 商业模式 → SWOT 投放建议 → 数据来源与局限性
- 所有数据附来源,推断内容明确标注"推断"
- 结论先行,附分档建议(品牌曝光 / 作品试水 / B 端接单)

## License

MIT
