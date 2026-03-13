# Edict (三省六部) 详细架构文档

## 核心设计理念

### 为什么用古代官制？

现代 Multi-Agent 框架的问题：
- **CrewAI**: 自由协作，无审核 → 质量不可控
- **AutoGen**: Human-in-loop → 需要人工一直盯着
- **MetaGPT**: 可选审核 → 不强制

**三省六部的解决**:
```
皇上(你) → 太子(分拣) → 中书省(规划) → 门下省(审议) → 尚书省(派发) → 六部(执行)
```

这是**制度化的分权制衡**，不是可选功能。

## 十二部制 Agent 架构

### 1. 太子 (taizi) - 消息分拣
**职责**: 区分闲聊和旨意
- 闲聊：自动回复
- 旨意：创建任务，进入流程

### 2. 中书省 (zhongshu) - 规划中枢
**职责**: 
- 理解旨意
- 任务分解
- 制定执行方案

### 3. 门下省 (menxia) - 审议把关 ⭐
**职责**: 
- 审核方案质量
- 风险识别
- **可以封驳** (veto)

这是与其他框架的核心差异！

### 4. 尚书省 (shangshu) - 调度大脑
**职责**:
- 任务派发
- 协调六部
- 进度跟踪
- 结果汇总

### 5. 六部 (执行层)

| 部门 | Agent ID | 职责 | 擅长 |
|------|----------|------|------|
| 户部 | hubu | 数据、资源、核算 | 数据处理、报表、成本分析 |
| 礼部 | libu | 文档、规范、报告 | 技术文档、API文档、规范 |
| 兵部 | bingbu | 代码、算法、工程 | 功能开发、Bug修复、审查 |
| 刑部 | xingbu | 安全、合规、审计 | 安全扫描、合规检查 |
| 工部 | gongbu | CI/CD、部署、工具 | Docker、流水线、自动化 |
| 吏部 | libu_hr | 人事、Agent管理 | Agent注册、权限、培训 |
| 早朝官 | zaochao | 每日简报、新闻 | 定时播报、数据汇总 |

## 权限矩阵

```
From ↓ \ To →    太子  中书  门下  尚书  六部
太子              —     ✅
中书省            ✅    —     ✅    ✅
门下省            ✅          —     ✅
尚书省            ✅    ✅    —     ✅
六部              ✅
```

**关键规则**:
- 中书省不能直接命令六部
- 必须经过门下省审核
- 尚书省统一调度

## 任务状态流转

```
皇上
  ↓
太子分拣 (pending)
  ↓
中书规划 (planning)
  ↓
门下审议 (reviewing)
  ├─→ 封驳 (blocked) ──┐
  ↓                    │
已派发 (dispatched)    │
  ↓                    │
执行中 (executing)     │
  ↓                    │
待审查 (auditing)      │
  ↓                    │
✅ 已完成 (completed)  │
  ↑────────────────────┘
```

### 五阶段奏折存档

每个完成的任务自动归档为"奏折"，包含：
1. **圣旨**: 原始需求
2. **中书**: 规划方案
3. **门下**: 审核意见
4. **六部**: 执行记录
5. **回奏**: 最终结果

## 军机处看板 (10大功能)

### 1. 旨意看板 · Kanban
- 按状态列展示全部任务
- 省部过滤 + 全文搜索
- 心跳徽章 (🟢活跃 🟡停滞 🔴告警)
- 叫停/取消/恢复操作

### 2. 省部调度 · Monitor
- 可视化各状态任务数量
- 部门分布横向条形图
- Agent健康状态实时卡片

### 3. 奏折阁 · Memorials
- 已完成旨意自动归档
- 五阶段时间线
- 一键复制为 Markdown

### 4. 旨库 · Templates
- 9个预设圣旨模板
- 分类筛选、参数表单
- 预估时间和费用

### 5. 官员总览 · Officials
- Token消耗排行榜
- 活跃度、完成数统计

### 6. 天下要闻 · News
- 每日自动采集科技/财经资讯
- 飞书推送

### 7. 模型配置 · Models
- 每个Agent独立切换LLM
- 热切换 (~5秒生效)

### 8. 技能配置 · Skills
- 查看已安装Skills
- 添加新技能

### 9. 小任务 · Sessions
- 会话实时监控
- 心跳、消息预览

### 10. 上朝仪式 · Ceremony
- 每日首次打开播放动画
- 今日统计

## 技术实现

### 数据流
```
User Input
  ↓
OpenClaw Gateway
  ↓
太子 Agent (分拣)
  ↓ (如果是旨意)
中书省 Agent (规划)
  ↓
门下省 Agent (审议)
  ↓ (通过)
尚书省 Agent (派发)
  ↓
六部 Agents (并行执行)
  ↓
结果汇总 → 用户
```

### 文件结构
```
edict_system/
├── agents/
│   ├── taizen/SOUL.md
│   ├── zhongshu/SOUL.md
│   ├── menxia/SOUL.md
│   ├── shangshu/SOUL.md
│   ├── hubu/SOUL.md
│   ├── libu/SOUL.md
│   ├── bingbu/SOUL.md
│   ├── xingbu/SOUL.md
│   ├── gongbu/SOUL.md
│   ├── libu_hr/
│   └── zaochao/SOUL.md
├── dashboard/
│   ├── server.py        # API服务器
│   └── dashboard.html   # 前端看板
├── scripts/
│   ├── run_loop.sh      # 数据刷新
│   ├── kanban_update.py # 看板CLI
│   └── skill_manager.py # 技能管理
└── data/                # 运行时数据
```

## 使用场景示例

### 场景1: API设计
```
皇上: "设计用户注册API，需要JWT鉴权"

太子: 识别为旨意，创建任务

中书省: 规划方案
  - 数据库设计
  - API端点规划
  - JWT实现方案
  - 测试策略

门下省: 审核
  - 安全检查: JWT密钥管理是否合规？
  - 风险评估: SQL注入防护？
  - 如果通过 → 准奏
  - 如果不通过 → 封驳，退回中书省修改

尚书省: 派发
  - 兵部: 实现代码
  - 礼部: 编写API文档
  - 工部: 配置CI/CD
  - 刑部: 安全审计

六部并行执行，尚书省协调进度

最终: 回奏皇上，交付完整API + 文档 + 部署方案
```

### 场景2: 代码审查
```
皇上: "审查这段代码的安全性"

流程同上，但主要涉及:
- 刑部: 安全扫描
- 兵部: 代码审查
- 礼部: 文档化问题清单
```

## 与其他框架对比

| 特性 | CrewAI | AutoGen | Edict |
|------|--------|---------|-------|
| 审核机制 | ❌ | ⚠️ | ✅ 门下省专职 |
| 实时看板 | ❌ | ❌ | ✅ 军机处 |
| 任务干预 | ❌ | ❌ | ✅ 叫停/取消/恢复 |
| 流转审计 | ⚠️ | ❌ | ✅ 完整奏折 |
| 健康监控 | ❌ | ❌ | ✅ 心跳检测 |
| 热切换模型 | ❌ | ❌ | ✅ 一键切换 |
| 技能管理 | ❌ | ❌ | ✅ 远程Skills |

## 安装和运行

```bash
# 克隆仓库
git clone https://github.com/cft0808/edict.git
cd edict

# 一键安装
chmod +x install.sh && ./install.sh

# 启动
tmux new -s edict-dashboard -d 'python3 dashboard/server.py'
tmux new -s edict-loop -d 'bash scripts/run_loop.sh'

# 访问
open http://127.0.0.1:7891
```

## Docker运行

```bash
docker run -p 7891:7891 cft0808/sansheng-demo
```

## 扩展阅读

- 完整架构文档: https://github.com/cft0808/edict/blob/main/docs/task-dispatch-architecture.md
- 远程Skills指南: https://github.com/cft0808/edict/blob/main/docs/remote-skills-guide.md
- 快速入门: https://github.com/cft0808/edict/blob/main/docs/getting-started.md
