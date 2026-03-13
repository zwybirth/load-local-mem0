# Load LOCAL-MEM0 Skill

快速加载和恢复 LOCAL-MEM0 无限记忆系统。用于 OpenClaw 版本升级、重启或安装后重新接入 LOCAL-MEM0。

## 最新版本: v2.0 (2026-03-14)

### 新增特性
- ✅ M5 Pro 性能优化（SQLite 512MB 缓存 + 8GB MMap）
- ✅ HNSW 向量搜索（百万级毫秒响应）
- ✅ 并行索引（8 线程，2800+ docs/sec）
- ✅ FAISS 集成（ARM64 优化）
- ✅ 自动摘要与标签生成
- ✅ 增强搜索（别名、时间线）

## 使用场景

1. **OpenClaw 版本升级后** - 重新配置集成
2. **OpenClaw 服务重启后** - 恢复记忆系统连接
3. **新环境首次配置** - 初始化 LOCAL-MEM0
4. **连接中断恢复** - 自动诊断和修复

## 快速使用

### 每次会话启动时自动加载

```bash
# 运行自动恢复脚本
python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py
```

### 验证加载成功

```bash
claw stats
```

输出示例：
```
📊 Memory System Statistics
==================================================
Version:           1.0.0
Total Documents:   20
Today New:         2
Storage Path:      ~/Documents/claw_memory
Index Path:        ~/.claw_memory_index/main.db
```

## 完整恢复流程

运行 `restore.py` 将自动执行：

1. **检测 LOCAL-MEM0 安装状态**
2. **检查 OpenClaw API 版本** (支持 1.x, 2.x, current)
3. **适配当前 API 版本**
4. **重新配置集成**
   - LaunchAgent 服务
   - CLI 工具链接
5. **加载历史记忆**
6. **验证连接状态**

## 性能指标

| 指标 | 数值 |
|------|------|
| 索引速度 | 2,833 docs/sec |
| 关键词搜索 | < 1ms |
| 向量搜索 (10万) | 0.13ms |
| 向量搜索 (100万) | ~2ms |
| 支持最大文档数 | 1000万+ |

## 文件结构

```
skills/load-local-mem0/
├── SKILL.md                    # 本文件
├── README.md                   # 详细说明
├── UPGRADE.md                  # 升级指南
├── LICENSE
├── scripts/
│   ├── restore.py              # 主恢复脚本 ⭐
│   ├── api_adapter.py          # API适配器
│   └── check_status.py         # 状态检查
├── references/
│   └── api_versions.md         # API版本对照表
└── assets/
    └── logo.png
```

## GitHub 仓库

https://github.com/zwybirth/load-local-mem0

## 故障排除

如果自动恢复失败：
1. 检查 LOCAL-MEM0 是否完整安装：`ls ~/Documents/claw_memory/`
2. 检查数据库是否存在：`ls ~/.claw_memory_index/main.db`
3. 手动运行 setup：`cd ~/.openclaw/workspace/infinite_memory && python3 scripts/setup.py`
4. 重建索引：`claw reindex`

---

# 🚀 LOCAL-MEM0 v2.0 完整指南

## 系统架构

```
┌─────────────────────────────────────────┐
│           OpenClaw Agent                │
└─────────────┬───────────────────────────┘
              │ 加载
┌─────────────▼───────────────────────────┐
│      load-local-mem0 Skill              │
│  ┌─────────────────────────────────┐    │
│  │  restore.py                     │    │
│  │  - 检测安装                     │    │
│  │  - 配置集成                     │    │
│  │  - 验证连接                     │    │
│  └─────────────────────────────────┘    │
└─────────────┬───────────────────────────┘
              │ 初始化
┌─────────────▼───────────────────────────┐
│         LOCAL-MEM0 System               │
│  ┌─────────────────────────────────┐    │
│  │  SQLite + FTS5 (关键词搜索)     │    │
│  │  FAISS HNSW (向量语义搜索)      │    │
│  │  512MB Cache + 8GB MMap         │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

## 目录结构

```
~/Documents/claw_memory/
├── daily/              # 日常记录
│   ├── work/           # 工作相关
│   └── personal/       # 个人日常
├── core/               # 核心配置
├── bank/               # 银行/金融项目
├── decisions/          # 关键决策 (永久)
├── learnings/          # 经验总结 (永久)
├── people/             # 人员信息
├── projects/           # 项目相关
├── ideas/              # 想法/灵感
├── summaries/          # 汇总报告
├── archive/            # 归档数据
└── cold/frozen/        # 冻结数据

~/.claw_memory_index/
├── main.db             # SQLite 主数据库
├── config.json         # 配置文件
├── vector.index        # FAISS 向量索引
├── backup/             # 自动备份
└── performance.log     # 性能日志
```

## CLI 命令

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

## 高级功能

### 1. 向量语义搜索

```bash
# 构建向量索引
python3 ~/.openclaw/workspace/infinite_memory/src/vector_index.py

# 或使用增强版
python3 ~/.openclaw/workspace/infinite_memory/src/million_scale_search.py build
python3 ~/.openclaw/workspace/infinite_memory/src/million_scale_search.py search -q "银行项目"
```

### 2. 并行重新索引

```bash
python3 ~/.openclaw/workspace/infinite_memory/src/parallel_indexer.py
```

### 3. iCloud 同步

```bash
~/.openclaw/workspace/infinite_memory/scripts/sync_icloud.sh
```

## 配置说明

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

## 集成原理

LOCAL-MEM0 与 OpenClaw 是松耦合关系：
- **数据存储**: `~/Documents/claw_memory/` (独立于 OpenClaw)
- **搜索索引**: `~/.claw_memory_index/` (SQLite + FAISS)
- **定时任务**: LaunchAgent (系统级)
- **CLI 工具**: `claw` 命令

恢复过程主要是重新建立 OpenClaw 与 LOCAL-MEM0 的集成层。

## 自动化配置

### 每次会话自动加载

在 `~/.openclaw/workspace/AGENTS.md` 或会话启动脚本中添加：

```bash
# 自动加载 LOCAL-MEM0
python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py
```

### 每日自动报告

- **脚本**: `~/.openclaw/workspace/infinite_memory/scripts/daily_report.py`
- **运行时间**: 每天 23:30
- **输出**: `summaries/` 分类

## 性能优化

### M5 Pro 优化配置

| 配置项 | 优化值 | 效果 |
|--------|--------|------|
| SQLite Cache | 512MB | 256x 提升 |
| MMap Size | 2GB | 零拷贝访问 |
| 并行线程 | 8 | 利用多核 |
| FAISS | ARM64 优化 | 向量加速 |

### 存储分层

| 层级 | 保留时间 | 策略 |
|------|---------|------|
| Hot | 30天 | 内存缓存 |
| Warm | 90天 | 标准存储 |
| Cold | 365天 | 归档存储 |
| Frozen | 730天 | 压缩存储 |

## 贡献

欢迎提交 Issue 和 PR！

## 许可证

MIT License
