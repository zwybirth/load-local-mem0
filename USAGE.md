# Load LOCAL-MEM0 Skill 使用说明

## 快速开始

当 OpenClaw 升级后需要恢复 LOCAL-MEM0 时，只需运行：

```bash
python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py
```

或告诉 AI：
> "帮我恢复 LOCAL-MEM0 记忆系统"

## 功能特性

- ✅ **自动检测** LOCAL-MEM0 安装状态
- ✅ **API 适配** 自动检测并适配 OpenClaw API 版本
- ✅ **重新配置** 恢复 LaunchAgent 和 CLI 工具
- ✅ **加载记忆** 自动加载所有历史记忆
- ✅ **验证连接** 测试搜索和保存功能

## 脚本说明

### 主恢复脚本

`scripts/restore.py` - 一键恢复 LOCAL-MEM0

执行流程：
1. 检查 LOCAL-MEM0 安装状态
2. 检测 OpenClaw API 版本
3. 适配当前 API 版本
4. 重新配置集成
5. 加载历史记忆
6. 验证连接状态

### API 适配器

`scripts/api_adapter.py` - API 版本检测和适配

- 支持 OpenClaw 1.x, 2.x 和 current 版本
- 自动生成对应版本的启动脚本
- 创建版本标记文件 `.api_version`

### 状态检查

`scripts/check_status.py` - 诊断系统状态

```bash
# 运行状态检查
python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/check_status.py
```

检查项：
- 安装完整性
- 文件系统
- 数据库
- LaunchAgent 服务
- CLI 工具
- 集成状态

## API 版本对照

| OpenClaw 版本 | 记忆模块路径 | 集成方式 |
|--------------|--------------|----------|
| 1.x | scripts.memory_store | 直接导入 |
| 2.x | openclaw.memory | 插件系统 |
| current | skills.custom_memory.scripts.memory_store | Bootstrap |

## 故障排除

### 恢复失败

如果自动恢复失败：

1. **检查安装**
   ```bash
   ls ~/Documents/claw_memory/
   ls ~/.claw_memory_index/
   ```

2. **重新安装**
   ```bash
   cd ~/.openclaw/workspace/infinite_memory
   python3 scripts/setup.py
   ```

3. **重建索引**
   ```bash
   claw reindex
   ```

### API 不兼容

如果遇到 API 错误：

1. 运行 API 适配器：
   ```bash
   python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/api_adapter.py
   ```

2. 检查 API 版本：
   ```bash
   cat ~/.openclaw/workspace/infinite_memory/.api_version
   ```

## 触发词

以下关键词会触发此技能：
- "load local-mem0"
- "恢复记忆系统"
- "重新接入 LOCAL-MEM0"
- "记忆系统重连"
- "setup local-mem0"

---

*LOCAL-MEM0 - Never forget anything.* 🧠
