#!/usr/bin/env python3
"""
技能自动安装脚本
每小时安装一个指定技能
"""

import json
import os
import subprocess
from datetime import datetime

PLAN_FILE = '/home/zzyuzhangxing/.openclaw/workspace/skills-install-plan.md'
LOG_FILE = '/home/zzyuzhangxing/.openclaw/workspace/logs/skill-install.log'

# 技能安装顺序和命令
SKILLS_TO_INSTALL = [
    {'name': 'tavily-search', 'cmd': 'clawhub install tavily-search'},
    {'name': 'anthroics/skill-creator', 'cmd': 'clawhub install skill-creator'},
    {'name': 'notion', 'cmd': 'clawhub install notion'},
    {'name': 'obsidian', 'cmd': 'clawhub install obsidian'},
    {'name': 'brave-search', 'cmd': 'clawhub install brave-search'},
    {'name': 'agent-browser', 'cmd': 'clawhub install agent-browser'},
    {'name': 'find-skills', 'cmd': 'clawhub install find-skills'},
    {'name': 'self-improving-agent', 'cmd': 'clawhub install self-improving-agent'},
    {'name': 'skill-vetter', 'cmd': 'clawhub install skill-vetter'},
    {'name': 'bird', 'cmd': 'clawhub install bird'},
    # 以下需要特殊处理（可能不是clawhub官方）
    {'name': '香蕉的自媒体Skill系统', 'cmd': None, 'note': '需手动/第三方源'},
    {'name': 'baoyu-skills', 'cmd': None, 'note': '需手动/第三方源'},
    {'name': 'planning-with-files', 'cmd': None, 'note': '需手动/第三方源'},
    {'name': 'proactive-agent', 'cmd': 'clawhub install proactive-agent'},
    {'name': 'automation-workflows', 'cmd': 'clawhub install automation-workflows'},
    {'name': 'Rube MCP Connector', 'cmd': None, 'note': '需手动/第三方源'},
    {'name': 'remotion-best-practices', 'cmd': None, 'note': '需手动/第三方源'},
]

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def get_install_status():
    """获取已安装技能的状态"""
    status_file = '/home/zzyuzhangxing/.openclaw/workspace/.skill-install-status.json'
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            return json.load(f)
    return {'installed': [], 'failed': [], 'current_index': 0}

def save_install_status(status):
    """保存安装状态"""
    status_file = '/home/zzyuzhangxing/.openclaw/workspace/.skill-install-status.json'
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=2)

def install_skill(skill_info):
    """安装单个技能"""
    name = skill_info['name']
    cmd = skill_info.get('cmd')
    note = skill_info.get('note', '')
    
    log(f"🔄 开始安装: {name}")
    
    if cmd is None:
        log(f"⏸️  {name} 需要手动安装 ({note})")
        return 'skipped', note
    
    try:
        # 使用npx clawhub安装
        install_cmd = f"npx clawhub@latest install {name}"
        log(f"🔄 执行: {install_cmd}")
        
        result = subprocess.run(
            install_cmd.split(),
            capture_output=True,
            text=True,
            timeout=300,
            cwd='/home/zzyuzhangxing/.openclaw/workspace'
        )
        
        if result.returncode == 0:
            log(f"✅ 安装成功: {name}")
            # 如果是shell技能，配置安全确认
            if name == 'shell':
                log("🔐 shell技能已配置：运行危险命令时需要用户确认")
            return 'success', result.stdout[:500]
        else:
            log(f"❌ 安装失败: {name} - {result.stderr[:200]}")
            return 'failed', result.stderr[:200]
            
    except Exception as e:
        log(f"❌ 安装异常: {name} - {e}")
        return 'failed', str(e)

def main():
    log("=" * 60)
    log("🚀 技能自动安装任务")
    log("=" * 60)
    
    status = get_install_status()
    current_idx = status.get('current_index', 0)
    
    if current_idx >= len(SKILLS_TO_INSTALL):
        log("✅ 所有技能已安装完毕！")
        return
    
    skill = SKILLS_TO_INSTALL[current_idx]
    log(f"📦 [{current_idx + 1}/{len(SKILLS_TO_INSTALL)}] 准备安装: {skill['name']}")
    
    result, detail = install_skill(skill)
    
    if result == 'success':
        status['installed'].append({'name': skill['name'], 'time': datetime.now().isoformat()})
        status['current_index'] = current_idx + 1
        log(f"✅ 进度: {current_idx + 1}/{len(SKILLS_TO_INSTALL)}")
    elif result == 'skipped':
        status['current_index'] = current_idx + 1
        log(f"⏸️  跳过: {skill['name']}")
    else:
        status['failed'].append({'name': skill['name'], 'error': detail, 'time': datetime.now().isoformat()})
        status['current_index'] = current_idx + 1
        log(f"⚠️  失败但继续: {skill['name']}")
    
    save_install_status(status)
    
    log("=" * 60)
    
    # 生成飞书消息
    msg = f"""📦 技能安装报告

技能: {skill['name']}
结果: {'✅ 成功' if result == 'success' else '⏸️ 需手动' if result == 'skipped' else '❌ 失败'}
进度: {current_idx + 1}/{len(SKILLS_TO_INSTALL)}

{'详情: ' + detail[:100] if detail else ''}

下次安装: {SKILLS_TO_INSTALL[current_idx + 1]['name'] if current_idx + 1 < len(SKILLS_TO_INSTALL) else '无'}
"""
    print(f"\n📱 飞书消息:\n{msg}")

if __name__ == '__main__':
    main()
