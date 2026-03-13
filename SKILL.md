---
name: load-local-mem0
description: |
  快速加载和恢复 LOCAL-MEM0 无限记忆系统。用于 OpenClaw 版本升级、重启或安装后重新接入 LOCAL-MEM0。
  
  使用场景：
  1. OpenClaw 版本升级后需要重新接入 LOCAL-MEM0
  2. OpenClaw 服务重启后恢复记忆系统连接
  3. 新环境首次配置 LOCAL-MEM0
  4. 检测到记忆系统连接中断时自动恢复
  
  触发词："load local-mem0", "恢复记忆系统", "重新接入 LOCAL-MEM0", "记忆系统重连", "setup local-mem0"
---

# Load LOCAL-MEM0 Skill

快速加载和恢复 LOCAL-MEM0 无限记忆系统。

## 使用场景

1. **OpenClaw 版本升级后** - 重新配置集成
2. **OpenClaw 服务重启后** - 恢复记忆系统连接
3. **新环境首次配置** - 初始化 LOCAL-MEM0
4. **连接中断恢复** - 自动诊断和修复

## 快速使用

当用户需要恢复 LOCAL-MEM0 时：

```bash
# 运行自动恢复脚本
python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py
```

或直接告诉用户：
> "正在为你恢复 LOCAL-MEM0 记忆系统..."

## 恢复流程

1. **检测 LOCAL-MEM0 安装状态**
2. **检查 OpenClaw API 版本**
3. **适配当前 API 版本**
4. **重新配置集成**
5. **加载历史记忆**
6. **验证连接状态**

## 文件结构

```
skills/load-local-mem0/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── restore.py              # 主恢复脚本
│   ├── api_adapter.py          # API适配器
│   └── check_status.py         # 状态检查
└── references/
    └── api_versions.md         # API版本对照表
```

## 集成原理

LOCAL-MEM0 与 OpenClaw 是松耦合关系：
- 数据存储: `~/Documents/claw_memory/` (独立于 OpenClaw)
- 搜索索引: `~/.claw_memory_index/` (SQLite 数据库)
- 定时任务: LaunchAgent (系统级)
- CLI 工具: `claw` 命令

恢复过程主要是重新建立 OpenClaw 与 LOCAL-MEM0 的集成层。

## 故障排除

如果自动恢复失败：
1. 检查 LOCAL-MEM0 是否完整安装：`ls ~/Documents/claw_memory/`
2. 检查数据库是否存在：`ls ~/.claw_memory_index/main.db`
3. 手动运行 setup：`cd ~/.openclaw/workspace/infinite_memory && python3 scripts/setup.py`
4. 重建索引：`claw reindex`

---

# 🚀 LOCAL-MEM0 系统优化指南

系统已完成5步优化：分类体系、存储分层、检索增强、自动化、备份迁移。

## 1. 分类体系 (已优化)

### 目录结构

```
~/Documents/claw_memory/
├── daily/              # 日常记录
│   ├── work/           # 工作相关
│   └── personal/       # 个人日常
├── core/               # 核心配置
├── bank/               # 银行/金融项目
├── decisions/          # 关键决策 (永久保留)
├── learnings/          # 经验总结 (永久保留)
├── people/             # 人员信息
├── projects/           # 项目相关
├── ideas/              # 想法/灵感
├── summaries/          # 汇总报告
├── archive/            # 归档数据
└── cold/               # 冷存储
    └── frozen/         # 冻结数据
```

### 标签别名映射

配置位于 `~/.claw_memory_index/config.json`：

```json
{
  "tag_aliases": {
    "银行项目": ["bank", "BANK-AI"],
    "AI": ["ai", "artificial-intelligence", "llm"],
    "重要": ["important", "critical", "priority"],
    "待办": ["todo", "task", "pending"],
    "决定": ["decision", "decided"]
  }
}
```

## 2. 存储分层 (已优化)

### 分层策略

| 层级 | 描述 | 保留时间 | 同步频率 |
|------|------|----------|----------|
| hot | 热数据 - 最近访问 | 30天 | 即时 |
| warm | 温数据 - 定期访问 | 90天 | 每日 |
| cold | 冷数据 - 归档存储 | 365天 | 每周 |
| frozen | 冻结数据 - 极少访问 | 730天 | 每月 |

### 自动分层规则

```json
{
  "auto_tiering": {
    "enabled": true,
    "rules": [
      {"condition": "age > 90 days AND access_count < 3", "action": "move_to_cold"},
      {"condition": "age > 365 days AND access_count < 1", "action": "move_to_frozen"},
      {"condition": "category = 'decisions' OR category = 'learnings'", "action": "keep_hot"},
      {"condition": "tagged 'important'", "action": "keep_hot"}
    ]
  }
}
```

## 3. 检索增强 (已优化)

### 新增搜索功能

```python
from search_enhanced import get_enhanced_search

# 获取增强搜索实例
esearch = get_enhanced_search()

# 支持别名的搜索
results = esearch.search_with_aliases("银行项目", limit=10)

# 时间线视图
timeline = esearch.search_timeline(
    category="daily",
    from_date="2026-03-01",
    to_date="2026-03-31"
)

# 查找相似文档
similar = esearch.find_similar("doc_id_here", limit=5)
```

### 搜索别名支持

搜索时会自动扩展查询词：
- 搜索"银行项目" → 同时搜索 "bank", "BANK-AI"
- 搜索"重要" → 同时搜索 "important", "critical", "priority"

## 4. 自动化钩子 (已优化)

### 自动摘要与标签

```python
from auto_summary import auto_process_document

# 自动处理文档
result = auto_process_document(content, title)
# 返回: {summary, suggested_tags, importance}
```

### 自动检测的关键词标签

| 关键词模式 | 标签 |
|-----------|------|
| 决定/结论/拍板 | decision |
| 重要/关键/核心 | important |
| 问题/bug/错误 | issue |
| 待办/todo/任务 | todo |
| 想法/灵感/创意 | idea |
| 学习/经验/总结 | learning |
| 项目/工程/开发 | project |
| 会议/讨论/沟通 | meeting |

### 每日自动报告

- **脚本位置**: `~/.openclaw/workspace/infinite_memory/scripts/daily_report.py`
- **运行时间**: 每天 23:30
- **输出位置**: `summaries/` 分类
- **触发条件**: 当天超过5篇文档 或 2篇以上重要内容

## 5. 备份与迁移 (已优化)

### iCloud 同步

```bash
# 手动同步到 iCloud
~/.openclaw/workspace/infinite_memory/scripts/sync_icloud.sh
```

同步内容：
- `~/Documents/claw_memory/` → `iCloud Drive/claw_memory/memory/`
- `~/.claw_memory_index/backup/` → `iCloud Drive/claw_memory/backup/`

### Markdown 导出

```bash
# 导出为可读的 Markdown 合集
python3 ~/.openclaw/workspace/infinite_memory/scripts/export_markdown.py \
  ~/Desktop/claw_export \
  --category daily
```

导出格式：按月份分文件 (`claw_memory_2026-03.md`)，人类可读。

### 完整备份

```bash
# 创建完整备份 (包含记忆数据和索引)
tar czf ~/claw_memory_backup_$(date +%Y%m%d).tar.gz \
  ~/Documents/claw_memory \
  ~/.claw_memory_index
```

## CLI 命令参考

```bash
# 基础命令
claw stats                    # 查看统计信息
claw search "关键词"          # 关键词搜索
claw list --category daily    # 列出分类文档

# 保存文档
claw save \
  --content "内容" \
  --title "标题" \
  --category decisions \
  --tags "重要,决定"

# 维护命令
claw reindex                  # 重新索引所有文件
claw backup                   # 手动备份索引
claw snapshot                 # 创建 APFS 快照

# 快捷命令
claw today                    # 查看今天的文档
claw yesterday                # 查看昨天的文档
```

## 配置文件

**主配置**: `~/.claw_memory_index/config.json`

```json
{
  "version": "1.0.0",
  "embedding_model": "all-MiniLM-L6-v2",
  "embedding_dim": 384,
  "hot_days": 30,
  "warm_days": 90,
  "categories": { ... },
  "tag_aliases": { ... },
  "storage_layers": { ... },
  "auto_tiering": { ... }
}
```

## 优化脚本

如需重新运行优化：

```bash
python3 ~/.openclaw/workspace/infinite_memory/scripts/optimizer.py
```

优化日志：`~/.claw_memory_index/optimization.log`
