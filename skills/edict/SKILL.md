---
name: edict
description: |
  三省六部 · Edict - AI Multi-Agent Orchestration System (4.5★ Skill)
  
  Based on the ancient Chinese "Three Departments and Six Ministries" system, providing
  institutionalized multi-agent collaboration with real-time dashboard, audit trails,
  and hierarchical task dispatch.
  
  Transformed from https://github.com/cft0808/edict using cli-anything.
  
  Key Features:
  - 12 specialized agents (Crown Prince + 3 Departments + 6 Ministries + Morning Report)
  - Real-time Kanban dashboard with 10 functional panels
  - Institutional review and veto system (like ancient Chinese government)
  - Task dispatch with complete audit trails
  - Skills management and remote skill loading
  - Multi-agent concurrent execution support
  
  Rating: ★★★★☆ (4.5/5) - Optimized for complex multi-agent workflows
---

# Edict Skill - 三省六部 Multi-Agent System

**Source**: https://github.com/cft0808/edict  
**License**: MIT  
**Rating**: ★★★★☆ (4.5/5)

## Overview

> 我用 1300 年前的帝国制度，重新设计了 AI 多 Agent 协作架构。结果发现，古人比现代 AI 框架更懂分权制衡。

Edict (三省六部) implements a hierarchical multi-agent orchestration system based on the ancient Chinese imperial bureaucracy:

```
皇上 (You) → 太子 (Sorting) → 中书省 (Planning) → 门下省 (Review) → 尚书省 (Dispatch) → 六部 (Execution)
```

### Architecture

| Component | Role | Responsibility |
|-----------|------|----------------|
| 👑 **皇上** | User | Issues commands/requests |
| 🐉 **太子** | Crown Prince | Message sorting, filters small talk |
| 📜 **中书省** | Secretariat | Planning, task decomposition |
| 🔍 **门下省** | Chancellery | Review, quality control, can veto |
| 📮 **尚书省** | Department of State Affairs | Task dispatch, coordination |
| 💰 **户部** | Revenue | Data processing, analytics |
| 📝 **礼部** | Rites | Documentation, API specs |
| ⚔️ **兵部** | War | Code implementation, engineering |
| ⚖️ **刑部** | Justice | Security, compliance, auditing |
| 🔧 **工部** | Works | CI/CD, deployment, infrastructure |
| 📋 **吏部** | Personnel | Agent management, HR |
| 🌅 **早朝官** | Morning Report | Daily briefings, news aggregation |

## Features (4.5★ Rated)

### 1. Institutional Review System ⭐
Unlike CrewAI/AutoGen, Edict has a dedicated review layer (门下省) that can:
- Review and approve/reject plans
- Veto poor quality proposals (封驳)
- Ensure quality before execution

### 2. Real-Time Dashboard ⭐
- **10 functional panels** in 军机处 (War Room)
- Kanban board with status columns
- Agent health monitoring (heartbeat badges)
- Complete task lifecycle visibility

### 3. Multi-Agent Concurrency ⭐
- Parallel execution by Six Ministries
- Task coordination by 尚书省
- Progress tracking and result aggregation

### 4. Audit Trail ⭐
- Complete memorial archive (奏折阁)
- Five-stage timeline: Imperial Edict → Secretariat → Chancellery → Ministries → Report
- Full traceability of decisions

### 5. Skills Ecosystem ⭐
- Remote skill loading from GitHub
- CLI/API/UI management
- Version control for skills

## Quick Start

```bash
# Install skill
openclaw skill install edict

# Initialize edict system
python3 ~/.openclaw/workspace/skills/edict/scripts/edict_cli.py init

# Start dashboard
python3 ~/.openclaw/workspace/skills/edict/scripts/edict_cli.py dashboard

# Issue a command (下旨)
python3 ~/.openclaw/workspace/skills/edict/scripts/edict_cli.py edict \
  --title "Design user registration API" \
  --content "RESTful API with FastAPI, PostgreSQL, JWT auth"
```

## CLI Commands

### System Management
```bash
# Initialize edict workspace
edict-cli init [--agents 12]

# Start/stop dashboard
edict-cli dashboard start
edict-cli dashboard stop

# Check system status
edict-cli status
```

### Task Management (旨意)
```bash
# Issue new edict
edict-cli edict create --title "Task Title" --content "Detailed requirements"

# List all edicts
edict-cli edict list [--status pending|reviewing|executing|completed]

# Get edict details
edict-cli edict show --id <edict_id>

# Cancel edict
edict-cli edict cancel --id <edict_id>
```

### Agent Management (官员)
```bash
# List all agents
edict-cli agents list

# Show agent status
edict-cli agent status --id <agent_id>

# Configure agent model
edict-cli agent config --id <agent_id> --model <model_name>
```

### Skills Management
```bash
# List installed skills
edict-cli skills list [--agent <agent_id>]

# Add remote skill
edict-cli skills add-remote \
  --agent <agent_id> \
  --name <skill_name> \
  --url <github_url>

# Update skill
edict-cli skills update --agent <agent_id> --name <skill_name>
```

### Dashboard Access
```bash
# Open dashboard in browser
edict-cli dashboard open

# Get dashboard URL
edict-cli dashboard url
```

## Multi-Agent Workflows (4.5★ Feature)

### Workflow Example: API Design

```bash
# 1. Issue edict to Secretariat (中书省)
edict-cli edict create \
  --title "Design REST API for user service" \
  --content "Requirements: FastAPI, PostgreSQL, JWT, tests"

# 2. Secretariat plans and submits to Chancellery
# 3. Chancellery reviews and approves/vetoes
# 4. Department of State Affairs dispatches to:
#    - 兵部: Code implementation
#    - 礼部: API documentation
#    - 工部: CI/CD setup
#    - 刑部: Security review

# 5. Monitor progress
edict-cli edict show --id <edict_id>

# 6. Receive final report (奏折)
```

### Workflow Example: Code Review

```bash
# Issue security audit
edict-cli edict create \
  --title "Security audit for payment module" \
  --content "Review FastAPI code for SQL injection, XSS vulnerabilities" \
  --priority high

# Departments involved:
# - 刑部: Security audit
# - 兵部: Code review
# - 礼部: Document findings
```

## Configuration

### Agent Models
Each agent can have its own LLM model:

```json
{
  "agents": {
    "zhongshu": { "model": "gpt-4", "temperature": 0.7 },
    "menxia": { "model": "gpt-4", "temperature": 0.3 },
    "bingbu": { "model": "claude-3-opus", "temperature": 0.5 }
  }
}
```

### Permissions Matrix
```
From ↓ \ To →    太子  中书  门下  尚书  户礼兵刑工吏
太子              —     ✅
中书省            ✅    —     ✅    ✅
门下省            ✅          —     ✅
尚书省            ✅    ✅    —     ✅    ✅    ✅    ✅    ✅    ✅
六部+吏部         ✅
```

## Task Lifecycle

```
皇上 → 太子分拣 → 中书规划 → 门下审议 → 已派发 → 执行中 → 待审查 → ✅ 已完成
                     ↑                    │
                     └──── 封驳 ───────────┘
```

### Status Meanings
- **pending**: Awaiting sorting by Crown Prince
- **planning**: Secretariat decomposing task
- **reviewing**: Chancellery reviewing plan
- **dispatched**: Approved, awaiting execution
- **executing**: Ministries working on subtasks
- **blocked**: Blocked, needs intervention
- **completed**: Finished, archived as memorial

## Dashboard Features

### 10 Function Panels
1. **📋 旨意看板 (Kanban)**: Task board with status columns
2. **🔭 省部调度 (Monitor)**: Visual task count, agent health
3. **📜 奏折阁 (Memorials)**: Completed task archive
4. **📜 旨库 (Templates)**: 9 preset edict templates
5. **👥 官员总览 (Officials)**: Token usage, activity stats
6. **📰 天下要闻 (News)**: Daily tech/finance news aggregation
7. **⚙️ 模型配置 (Models)**: Per-agent LLM configuration
8. **🛠️ 技能配置 (Skills)**: Skill management
9. **💬 小任务 (Sessions)**: Real-time session monitoring
10. **🎬 上朝仪式 (Ceremony)**: Daily opening animation

## Integration with OpenClaw

### As a Skill
```python
# Use edict in OpenClaw
from skills.edict import EdictSystem

edict = EdictSystem()
edict.initialize()

# Issue command
result = edict.issue_edict(
    title="Create Python API",
    content="FastAPI + PostgreSQL + JWT"
)

# Monitor execution
status = edict.get_status(result.id)
```

### Multi-Agent Coordination
Edict excels at coordinating multiple OpenClaw agents:
- Each "Ministry" can be an OpenClaw agent
- Hierarchical task dispatch
- Clear responsibility boundaries

## Comparison with Other Frameworks

| Feature | CrewAI | MetaGPT | AutoGen | **Edict (三省六部)** |
|---------|--------|---------|---------|---------------------|
| Review Mechanism | ❌ None | ⚠️ Optional | ⚠️ Human-in-loop | ✅ **专职审核 (门下省)** |
| Real-time Dashboard | ❌ | ❌ | ❌ | ✅ **军机处看板** |
| Task Intervention | ❌ | ❌ | ❌ | ✅ **叫停/取消/恢复** |
| Audit Trail | ⚠️ | ⚠️ | ❌ | ✅ **完整奏折存档** |
| Agent Health Monitor | ❌ | ❌ | ❌ | ✅ **心跳+活跃度** |
| Hot Model Switch | ❌ | ❌ | ❌ | ✅ **一键切换LLM** |
| Skills Management | ❌ | ❌ | ❌ | ✅ **远程Skills** |
| Deployment | Medium | Hard | Medium | **Easy (One-command)** |

## Installation Requirements

- Python 3.9+
- OpenClaw installed
- Node.js 18+ (optional, for dashboard build)

## Files Structure

```
skills/edict/
├── SKILL.md              # This file
├── scripts/
│   └── edict_cli.py      # Main CLI interface
├── references/
│   └── edict_architecture.md  # Detailed architecture docs
└── docs/
    └── getting_started.md     # Quick start guide
```

## Roadmap

- [ ] 御批模式 (Manual approval mode)
- [ ] 功过簿 (Agent performance scoring)
- [ ] 急递铺 (Real-time agent messaging)
- [ ] 国史馆 (Knowledge base + citations)
- [ ] Notion/Linear integration
- [ ] Mobile adaptation + PWA

## Contributing

Original project: https://github.com/cft0808/edict

## License

MIT License - OpenClaw Community

---

**以古制御新技，以智慧驾驭 AI**  
Governing AI with the wisdom of ancient empires
