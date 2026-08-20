# Hermes Skills 通用技能包

由 Hermes Agent 在实战任务中提炼的可复用技能集合,遵循 [Hermes Agent 技能规范](https://hermes-agent.nousresearch.com/docs)(YAML frontmatter + markdown body)。

## 技能列表

| 技能 | 用途 | 触发场景 |
|---|---|---|
| [longterm-memory](skills/longterm-memory/) | Hermes 原生长期记忆纪律(分层文件存储 + WAL 先写后答 + 每周卫生清理) | 用户纠正、决策、偏好需要跨会话留存;长任务推进中不想丢上下文;“我们之前关于 X 怎么定的” |
| [website-research](skills/website-research/) | 网站/平台调研与投放评估 | “调研这个网站”、“它的访问量、用户画像”、“领导想在上面投作品/投放/合作”、“整理一份报告,尽量以图表形式展现” |

## 安装方法

把对应技能目录复制到 Hermes 的 skills 目录即可:

```bash
# 安装 longterm-memory 技能(注意分类目录可自选,这里用 note-taking)
mkdir -p ~/.hermes/skills/note-taking/
cp -r skills/longterm-memory ~/.hermes/skills/note-taking/

# 安装 website-research 技能
mkdir -p ~/.hermes/skills/research/
cp -r skills/website-research ~/.hermes/skills/research/
```

重启/刷新 Hermes 后技能即可被自动加载。

## 技能速览

### longterm-memory 🧠

Hermes 原生的长期记忆纪律,剥离了 clawdbot/LanceDB 等外部依赖,叠加在 Hermes 自带 `memory` 工具 + `session_search` + 本地 markdown 文件之上:

```
longterm-memory/
├── SKILL.md                        # 工作流:分层存储、WAL 协议、会话例行、每周卫生
└── scripts/
    ├── init_memory.py              # 幂等初始化存储库(不覆盖已有内容)
    └── status.py                   # 存储健康检查(体积/陈旧度/日志数)
```

默认存储根目录:`$HERMES_HOME/memory`(本机即 `~/.hermes/memory`),可用环境变量 `MEMORY_ROOT` 覆盖。

```bash
# 初始化(幂等,重复运行只跳过已存在文件)
python3 scripts/init_memory.py
# 检查存储健康
python3 scripts/status.py
```

核心纪律:**WAL 先写后答** —— 遇到用户偏好/纠正/决策/截止时间,先落盘再回复。短小事实(≤2 行)写进 Hermes `memory` 工具(每轮自动注入),结构化/大段内容落 markdown 文件,跨会话回忆用 `session_search`。

### website-research 🌐

网站/平台调研与投放评估工作流:

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

```bash
# 1. 探针目标网站公开信号
./skills/website-research/scripts/site_signals.sh <domain> <search_term>

# 2. 复制模板到项目目录,填入调研数据
cp skills/website-research/templates/*.py /path/to/project/
cd /path/to/project && python3 charts_template.py && python3 report_template.py

# 3. 产出:单文件自包含 HTML 报告(图表 base64 内嵌,可打印 PDF)+ charts/*.png
```

完整工作流与报告规范见各技能 `SKILL.md`。

## 报告产出规格(website-research 领导层验收标准)

- 自包含 HTML(单文件、浏览器直接打开、可转 PDF)+ 关键图表 PNG
- 中文呈现,图表优先
- 结构:执行摘要 → 平台信息 → 流量规模 → 用户画像 → 商业模式 → SWOT 投放建议 → 数据来源与局限性
- 所有数据附来源,推断内容明确标注“推断”
- 结论先行,附分档建议(品牌曝光 / 作品试水 / B 端接单)

## License

MIT
