# Load LOCAL-MEM0

[![GitHub](https://img.shields.io/badge/GitHub-zwybirth%2Fload--local--mem0-blue)](https://github.com/zwybirth/load-local-mem0)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/zwybirth/load-local-mem0/releases)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

快速加载和恢复 [LOCAL-MEM0](https://github.com/zwybirth/local-mem0) 无限记忆系统的 OpenClaw Skill。

## 功能特性

- ✅ **自动检测** LOCAL-MEM0 安装状态
- ✅ **API 适配** 自动检测并适配 OpenClaw API 版本 (支持 1.x, 2.x, current)
- ✅ **重新配置** 恢复 LaunchAgent 和 CLI 工具
- ✅ **加载记忆** 自动加载所有历史记忆
- ✅ **验证连接** 测试搜索和保存功能

## 使用场景

1. **OpenClaw 版本升级后** - 重新配置 LOCAL-MEM0 集成
2. **OpenClaw 服务重启后** - 恢复记忆系统连接
3. **新环境首次配置** - 初始化 LOCAL-MEM0
4. **连接中断恢复** - 自动诊断和修复

## 快速开始

### 方法一：运行恢复脚本

```bash
python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py
```

### 方法二：使用触发词

告诉你的 AI 助手：
> "帮我恢复 LOCAL-MEM0 记忆系统"

## 安装

### 方式一：通过 Git 克隆

```bash
# 克隆到 OpenClaw skills 目录
git clone https://github.com/zwybirth/load-local-mem0.git ~/.openclaw/workspace/skills/load-local-mem0
```

### 方式二：手动下载

1. 下载本仓库代码
2. 解压到 `~/.openclaw/workspace/skills/load-local-mem0/`

## 恢复流程

运行恢复脚本后，会执行以下步骤：

```
🔹 步骤 1/6: 检查 LOCAL-MEM0 安装
   ✅ 项目目录
   ✅ 记忆存储
   ✅ 索引目录
   ✅ CLI工具

🔹 步骤 2/6: 检测 OpenClaw API
   ✅ OpenClaw 已安装
   ✅ 版本: OpenClaw 2026.3.8

🔹 步骤 3/6: 适配 API 版本
   ✅ 适配器模块存在
   ✅ 适配器可正常导入

🔹 步骤 4/6: 重新配置集成
   ✅ LaunchAgent 服务
   ✅ CLI 工具

🔹 步骤 5/6: 加载历史记忆
   ✅ 索引加载成功
   📊 记忆统计: X 篇文档

🔹 步骤 6/6: 验证连接状态
   ✅ 搜索功能正常
   ✅ 保存功能正常
```

## 支持的 OpenClaw 版本

| OpenClaw 版本 | 记忆模块路径 | 适配方式 |
|--------------|--------------|----------|
| 1.x | `scripts.memory_store` | 直接导入 |
| 2.x | `openclaw.memory` | 插件系统 |
| current | `skills.custom_memory.scripts.memory_store` | Bootstrap |

## 文件结构

```
load-local-mem0/
├── SKILL.md                    # 技能定义（触发条件）
├── USAGE.md                    # 使用说明
├── README.md                   # 本文件
├── scripts/
│   ├── restore.py              # 🚀 主恢复脚本（一键恢复）
│   ├── api_adapter.py          # 🔧 API适配器（自动适配版本）
│   └── check_status.py         # 🔍 状态检查
└── references/
    └── api_versions.md         # API版本对照表
```

## 触发词

以下关键词会触发此技能：
- "load local-mem0"
- "恢复记忆系统"
- "重新接入 LOCAL-MEM0"
- "记忆系统重连"
- "setup local-mem0"

## 相关项目

- [LOCAL-MEM0](https://github.com/zwybirth/local-mem0) - 无限记忆存储系统

## 许可证

MIT License

---

**LOCAL-MEM0** - Never forget anything. 🧠
