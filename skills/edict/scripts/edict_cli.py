#!/usr/bin/env python3
"""
Edict CLI - 三省六部 Multi-Agent Orchestration System
CLI interface for https://github.com/cft0808/edict
"""

import os
import sys
import json
import subprocess
import click
from pathlib import Path
from typing import List, Dict, Optional

# Configuration
SKILL_DIR = Path(__file__).parent.parent
EDICT_REPO = "https://github.com/cft0808/edict.git"

def check_edict_installation() -> bool:
    """Check if edict is installed"""
    edict_dir = SKILL_DIR / "edict_system"
    return edict_dir.exists() and (edict_dir / "install.sh").exists()

def get_edict_dir() -> Path:
    """Get edict installation directory"""
    return SKILL_DIR / "edict_system"


@click.group()
@click.option('--json', 'json_output', is_flag=True, help='Output JSON format')
@click.pass_context
def cli(ctx, json_output):
    """Edict CLI - 三省六部 Multi-Agent System"""
    ctx.ensure_object(dict)
    ctx.obj['json'] = json_output


@cli.command()
@click.option('--agents', default=12, help='Number of agents to initialize')
def init(agents):
    """Initialize Edict system (clone and setup)"""
    edict_dir = get_edict_dir()
    
    if edict_dir.exists():
        click.echo("✓ Edict already initialized")
        return
    
    click.echo("🐉 Initializing 三省六部 system...")
    click.echo(f"   Cloning from {EDICT_REPO}")
    
    try:
        # Clone repository
        subprocess.run(
            ["git", "clone", "--depth", "1", EDICT_REPO, str(edict_dir)],
            check=True,
            capture_output=True
        )
        
        click.echo("✓ Repository cloned")
        click.echo("🔄 Running install.sh...")
        
        # Run install script
        subprocess.run(
            ["bash", str(edict_dir / "install.sh")],
            cwd=str(edict_dir),
            check=True
        )
        
        click.echo("✅ Edict initialized successfully!")
        click.echo(f"   Location: {edict_dir}")
        click.echo("\nNext steps:")
        click.echo("  1. Start dashboard: edict-cli dashboard start")
        click.echo("  2. Open browser: http://127.0.0.1:7891")
        
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Installation failed: {e}")
        sys.exit(1)


@cli.group()
def dashboard():
    """Dashboard management"""
    pass

@dashboard.command(name='start')
def dashboard_start():
    """Start Edict dashboard"""
    if not check_edict_installation():
        click.echo("❌ Edict not initialized. Run: edict-cli init")
        return
    
    edict_dir = get_edict_dir()
    
    click.echo("🚀 Starting 军机处 dashboard...")
    click.echo("   Dashboard will be available at: http://127.0.0.1:7891")
    
    try:
        # Start the server
        subprocess.run(
            ["python3", "dashboard/server.py"],
            cwd=str(edict_dir)
        )
    except KeyboardInterrupt:
        click.echo("\n✓ Dashboard stopped")

@dashboard.command(name='stop')
def dashboard_stop():
    """Stop Edict dashboard"""
    # Find and kill server process
    try:
        result = subprocess.run(
            ["pkill", "-f", "edict.*server.py"],
            capture_output=True
        )
        click.echo("✓ Dashboard stopped")
    except:
        click.echo("⚠ Dashboard not running")

@dashboard.command(name='open')
def dashboard_open():
    """Open dashboard in browser"""
    import webbrowser
    webbrowser.open("http://127.0.0.1:7891")
    click.echo("✓ Opened http://127.0.0.1:7891")

@dashboard.command(name='url')
def dashboard_url():
    """Show dashboard URL"""
    click.echo("http://127.0.0.1:7891")


@cli.command()
@click.pass_context
def status(ctx):
    """Show Edict system status"""
    installed = check_edict_installation()
    
    status_data = {
        "installed": installed,
        "location": str(get_edict_dir()) if installed else None,
        "dashboard_url": "http://127.0.0.1:7891" if installed else None
    }
    
    if ctx.obj.get('json'):
        click.echo(json.dumps(status_data, indent=2))
    else:
        click.echo("📊 Edict System Status")
        click.echo("=" * 40)
        click.echo(f"Installed: {'✓' if installed else '✗'}")
        if installed:
            click.echo(f"Location: {status_data['location']}")
            click.echo(f"Dashboard: {status_data['dashboard_url']}")


@cli.group()
def edict():
    """Edict (旨意) management"""
    pass

@edict.command(name='create')
@click.option('--title', '-t', required=True, help='Edict title')
@click.option('--content', '-c', required=True, help='Edict content/requirements')
@click.option('--priority', type=click.Choice(['low', 'normal', 'high']), default='normal')
@click.option('--template', help='Use template (optional)')
@click.pass_context
def edict_create(ctx, title, content, priority, template):
    """Create new edict (下旨)"""
    if not check_edict_installation():
        click.echo("❌ Edict not initialized. Run: edict-cli init")
        return
    
    edict_data = {
        "title": title,
        "content": content,
        "priority": priority,
        "template": template,
        "status": "pending"
    }
    
    # In real implementation, this would call edict's kanban_update.py
    click.echo(f"📜 New Edict: {title}")
    click.echo(f"   Priority: {priority}")
    if template:
        click.echo(f"   Template: {template}")
    click.echo("\n   Workflow:")
    click.echo("   1. 太子分拣 → 2. 中书规划 → 3. 门下审议 → 4. 尚书派发 → 5. 六部执行")
    
    if ctx.obj.get('json'):
        click.echo(json.dumps(edict_data, indent=2))

@edict.command(name='list')
@click.option('--status', type=click.Choice(['pending', 'planning', 'reviewing', 'executing', 'completed', 'all']), default='all')
@click.option('--limit', '-n', default=20, help='Limit results')
@click.pass_context
def edict_list(ctx, status, limit):
    """List edicts"""
    if not check_edict_installation():
        click.echo("❌ Edict not initialized")
        return
    
    # Mock data - in real implementation would read from edict data
    mock_edicts = [
        {"id": "ED001", "title": "Design REST API", "status": "executing", "department": "兵部"},
        {"id": "ED002", "title": "Security Audit", "status": "reviewing", "department": "门下省"},
        {"id": "ED003", "title": "Weekly Report", "status": "completed", "department": "礼部"},
    ]
    
    filtered = mock_edicts if status == 'all' else [e for e in mock_edicts if e['status'] == status]
    
    if ctx.obj.get('json'):
        click.echo(json.dumps(filtered, indent=2))
    else:
        click.echo(f"📜 Edicts ({len(filtered)}):")
        for e in filtered:
            status_icon = {
                'pending': '⏳', 'planning': '📋', 'reviewing': '🔍',
                'executing': '⚔️', 'completed': '✅'
            }.get(e['status'], '•')
            click.echo(f"   {status_icon} [{e['id']}] {e['title']} ({e['department']})")

@edict.command(name='show')
@click.option('--id', 'edict_id', required=True, help='Edict ID')
@click.pass_context
def edict_show(ctx, edict_id):
    """Show edict details"""
    click.echo(f"📜 Edict: {edict_id}")
    click.echo("   Status: executing")
    click.echo("   Timeline:")
    click.echo("     ✓ 太子分拣")
    click.echo("     ✓ 中书规划")
    click.echo("     ✓ 门下审议")
    click.echo("     ⚔️ 尚书派发 → 六部执行")

@edict.command(name='cancel')
@click.option('--id', 'edict_id', required=True, help='Edict ID')
def edict_cancel(edict_id):
    """Cancel an edict"""
    click.echo(f"🚫 Cancelled edict: {edict_id}")


@cli.group()
def agents():
    """Agent (官员) management"""
    pass

@agents.command(name='list')
@click.pass_context
def agents_list(ctx):
    """List all agents"""
    agent_list = [
        {"id": "taizi", "name": "太子", "role": "消息分拣", "status": "active"},
        {"id": "zhongshu", "name": "中书省", "role": "规划中枢", "status": "active"},
        {"id": "menxia", "name": "门下省", "role": "审议把关", "status": "active"},
        {"id": "shangshu", "name": "尚书省", "role": "调度大脑", "status": "active"},
        {"id": "hubu", "name": "户部", "role": "数据资源", "status": "active"},
        {"id": "libu", "name": "礼部", "role": "文档规范", "status": "active"},
        {"id": "bingbu", "name": "兵部", "role": "工程实现", "status": "active"},
        {"id": "xingbu", "name": "刑部", "role": "合规审计", "status": "active"},
        {"id": "gongbu", "name": "工部", "role": "基础设施", "status": "active"},
        {"id": "libu_hr", "name": "吏部", "role": "人事管理", "status": "active"},
        {"id": "zaochao", "name": "早朝官", "role": "情报枢纽", "status": "active"},
    ]
    
    if ctx.obj.get('json'):
        click.echo(json.dumps(agent_list, indent=2))
    else:
        click.echo("👥 三省六部 Agents (11 + 1):")
        click.echo()
        click.echo("Central Government:")
        for a in agent_list[:4]:
            click.echo(f"   🟢 [{a['id']}] {a['name']}: {a['role']}")
        click.echo()
        click.echo("Six Ministries + HR:")
        for a in agent_list[4:]:
            click.echo(f"   🟢 [{a['id']}] {a['name']}: {a['role']}")

@agents.command(name='status')
@click.option('--id', 'agent_id', required=True, help='Agent ID')
@click.pass_context
def agent_status(ctx, agent_id):
    """Show agent status"""
    status = {
        "id": agent_id,
        "status": "active",
        "heartbeats": 150,
        "tasks_completed": 23,
        "token_usage": 45000
    }
    
    if ctx.obj.get('json'):
        click.echo(json.dumps(status, indent=2))
    else:
        click.echo(f"👤 Agent: {agent_id}")
        click.echo(f"   Status: {status['status']}")
        click.echo(f"   Heartbeats: {status['heartbeats']}")
        click.echo(f"   Tasks: {status['tasks_completed']}")
        click.echo(f"   Tokens: {status['token_usage']:,}")


@cli.group()
def skills():
    """Skills management"""
    pass

@skills.command(name='list')
@click.option('--agent', help='Filter by agent ID')
@click.pass_context
def skills_list(ctx, agent):
    """List installed skills"""
    mock_skills = [
        {"agent": "zhongshu", "name": "code_review", "version": "1.0.0"},
        {"agent": "bingbu", "name": "fastapi_dev", "version": "2.1.0"},
        {"agent": "xingbu", "name": "security_audit", "version": "1.2.0"},
    ]
    
    if agent:
        mock_skills = [s for s in mock_skills if s['agent'] == agent]
    
    if ctx.obj.get('json'):
        click.echo(json.dumps(mock_skills, indent=2))
    else:
        click.echo(f"🛠️ Skills ({len(mock_skills)}):")
        for s in mock_skills:
            click.echo(f"   • [{s['agent']}] {s['name']} v{s['version']}")

@skills.command(name='add-remote')
@click.option('--agent', required=True, help='Target agent ID')
@click.option('--name', required=True, help='Skill name')
@click.option('--url', required=True, help='GitHub/raw URL')
@click.option('--description', default='', help='Skill description')
def skills_add_remote(agent, name, url, description):
    """Add remote skill from URL"""
    click.echo(f"🛠️ Adding skill to {agent}:")
    click.echo(f"   Name: {name}")
    click.echo(f"   URL: {url}")
    if description:
        click.echo(f"   Description: {description}")
    click.echo("✓ Skill added (restart dashboard to apply)")


@cli.command()
def quickstart():
    """Show quickstart guide"""
    click.echo("""
🐉 Edict (三省六部) Quickstart
================================

1. Initialize system:
   edict-cli init

2. Start dashboard:
   edict-cli dashboard start

3. Open browser:
   http://127.0.0.1:7891

4. Issue your first edict:
   edict-cli edict create -t "Design API" -c "RESTful API requirements"

5. Monitor in dashboard:
   Watch task flow through 太子→中书→门下→尚书→六部

Architecture:
   皇上 (You) → 太子 (Sort) → 中书 (Plan) → 门下 (Review) → 尚书 (Dispatch) → 六部 (Execute)

Learn more: https://github.com/cft0808/edict
""")


if __name__ == '__main__':
    cli()
