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
