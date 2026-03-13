# 会话自动加载配置

确保每次 OpenClaw 会话启动时自动加载 LOCAL-MEM0。

## 方法一: AGENTS.md 配置（推荐）

编辑 `~/.openclaw/workspace/AGENTS.md`，在 "Every Session" 部分添加：

```markdown
## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. **Load LOCAL-MEM0** — 加载本地记忆系统:
   ```bash
   python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py
   ```
4. Load LOCAL-MEM0 — 搜索相关记忆: `claw search "最近的活动" --limit 5`
5. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
```

## 方法二: 系统启动脚本

创建启动钩子脚本：

```bash
# 创建启动脚本
mkdir -p ~/.openclaw/workspace/hooks
cat > ~/.openclaw/workspace/hooks/on_session_start.sh << 'EOF'
#!/bin/bash
# OpenClaw 会话启动钩子

echo "🧠 加载 LOCAL-MEM0 记忆系统..."
python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py

echo "✅ 记忆系统加载完成"
EOF

chmod +x ~/.openclaw/workspace/hooks/on_session_start.sh
```

## 方法三: 手动加载别名

在 shell 配置中添加别名：

```bash
# ~/.zshrc 或 ~/.bashrc
alias load-mem0='python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py'
```

使用时只需输入：
```bash
load-mem0
```

## 方法四: OpenClaw 配置文件

如果 OpenClaw 支持启动钩子，在配置中添加：

```json
{
  "session": {
    "on_start": [
      "python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py"
    ]
  }
}
```

## 验证自动加载

测试配置是否生效：

```bash
# 1. 检查脚本是否存在
ls -la ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py

# 2. 手动运行测试
python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py

# 3. 验证加载结果
claw stats
```

## 故障排除

### 问题: 会话启动时未自动加载

**检查**:
1. 脚本路径是否正确
2. 脚本是否有执行权限
3. Python3 是否可用

**解决**:
```bash
# 确保脚本可执行
chmod +x ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py

# 测试直接运行
/usr/bin/env python3 ~/.openclaw/workspace/skills/load-local-mem0/scripts/restore.py
```

### 问题: 加载失败

**症状**: `ModuleNotFoundError` 或 `ImportError`

**解决**:
```bash
# 重新安装依赖
cd ~/.openclaw/workspace/infinite_memory
pip3 install -r requirements.txt --user

# 或运行完整安装
python3 scripts/setup.py
```

### 问题: 加载成功但无记忆

**症状**: `Total Documents: 0`

**解决**:
```bash
# 重建索引
claw reindex

# 检查记忆目录
ls -la ~/Documents/claw_memory/
```

## 推荐配置

对于 MacBook Pro M5 + 32GB 用户，建议使用 **方法一** (AGENTS.md) + **方法三** (别名)：

1. AGENTS.md 确保 AI 助手每次都知道要加载记忆
2. Shell 别名方便手动快速加载

## 验证清单

- [ ] restore.py 脚本存在且可执行
- [ ] AGENTS.md 包含加载指令
- [ ] 运行 `claw stats` 显示正确文档数
- [ ] 运行 `claw search "测试"` 正常工作
- [ ] GitHub 仓库已更新到最新版本

---

**配置日期**: 2026-03-14  
**版本**: v2.0  
**GitHub**: https://github.com/zwybirth/load-local-mem0
