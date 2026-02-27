#!/usr/bin/env python3
"""
技能自动安装脚本 v2.0 - 修复版
每小时从ClawHub安装一个技能，并验证安装结果
"""

import json
import os
import subprocess
from datetime import datetime
import sys

LOG_FILE = '/home/zzyuzhangxing/.openclaw/workspace/logs/skill-install.log'
STATUS_FILE = '/home/zzyuzhangxing/.openclaw/workspace/.skill-install-status-v2.json'
SKILLS_DIR = '/home/zzyuzhangxing/.openclaw/workspace/skills'

# 技能安装清单（按优先级排序）
SKILLS_TO_INSTALL = [
    # 第一梯队：核心能力
    {'name': 'tavily-search', 'installed': False},
    {'name': 'skill-creator', 'installed': False},
    {'name': 'proactive-agent', 'installed': False},
    {'name': 'automation-workflows', 'installed': False},
    # 第二梯队：生产力
    {'name': 'notion', 'installed': False},
    {'name': 'obsidian', 'installed': False},
    {'name': 'brave-search', 'installed': False},
    {'name': 'agent-browser', 'installed': False},
    # 第三梯队：AI增强
    {'name': 'find-skills', 'installed': False},
    {'name': 'self-improving-agent', 'installed': False},
    {'name': 'skill-vetter', 'installed': False},
    {'name': 'planning-with-files', 'installed': False},
    # 第四梯队：社媒与工具
    {'name': 'bird-twitter', 'installed': False},
    {'name': 'x-twitter', 'installed': False},
    {'name': 'gmail', 'installed': False},
    {'name': 'calendar', 'installed': False},
    {'name': 'spotify', 'installed': False},
    {'name': 'home-assistant', 'installed': False},
    {'name': 'gog', 'installed': False},
    {'name': 'github', 'installed': False},
    {'name': 'remotion', 'installed': False},
    {'name': 'mcp-skill', 'installed': False},
]

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def get_status():
    """获取安装状态"""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    return {
        'current_index': 0,
        'installed': [],
        'failed': [],
        'total_attempts': 0
    }

def save_status(status):
    """保存安装状态"""
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=2)

def verify_installation(skill_name):
    """验证技能是否真正安装到WORKSPACE目录"""
    skill_path = os.path.join(SKILLS_DIR, skill_name)
    skill_md = os.path.join(skill_path, 'SKILL.md')
    
    if os.path.exists(skill_path) and os.path.exists(skill_md):
        return True, f"目录存在，包含SKILL.md"
    elif os.path.exists(skill_path):
        return False, f"目录存在但缺少SKILL.md"
    else:
        return False, f"目录不存在"

def install_skill(skill_name):
    """安装单个技能"""
    log(f"🔄 开始安装: {skill_name}")
    
    try:
        # 使用clawhub安装
        install_cmd = f"npx clawhub@latest install {skill_name} --force"
        log(f"  执行: {install_cmd}")
        
        result = subprocess.run(
            install_cmd.split(),
            capture_output=True,
            text=True,
            timeout=300,
            cwd='/home/zzyuzhangxing/.openclaw/workspace'
        )
        
        # 验证安装结果
        verified, verify_msg = verify_installation(skill_name)
        
        if verified:
            log(f"✅ 安装成功并验证: {skill_name} - {verify_msg}")
            return 'success', verify_msg
        else:
            log(f"⚠️  安装命令成功但验证失败: {skill_name} - {verify_msg}")
            return 'partial', verify_msg
            
    except Exception as e:
        log(f"❌ 安装异常: {skill_name} - {e}")
        return 'failed', str(e)

def main():
    log("=" * 70)
    log("🚀 技能自动安装任务 v2.0 (ClawHub版)")
    log("=" * 70)
    
    status = get_status()
    current_idx = status.get('current_index', 0)
    status['total_attempts'] = status.get('total_attempts', 0) + 1
    
    # 初始化结果变量
    result = 'skipped'
    detail = '无技能需要安装'
    skill_name = '无'
    
    # 跳过已安装的技能
    while current_idx < len(SKILLS_TO_INSTALL):
        skill = SKILLS_TO_INSTALL[current_idx]
        skill_name = skill['name']
        
        # 先验证是否已经安装
        verified, _ = verify_installation(skill_name)
        if verified:
            log(f"⏭️  已安装，跳过: {skill_name}")
            status['installed'].append({
                'name': skill_name, 
                'time': datetime.now().isoformat(),
                'note': '已存在'
            })
            current_idx += 1
            continue
        
        # 安装当前技能
        log(f"📦 [{current_idx + 1}/{len(SKILLS_TO_INSTALL)}] 准备安装: {skill_name}")
        
        result, detail = install_skill(skill_name)
        
        if result == 'success':
            status['installed'].append({
                'name': skill_name, 
                'time': datetime.now().isoformat(),
                'note': '安装并验证成功'
            })
            current_idx += 1
            log(f"✅ 进度: {current_idx}/{len(SKILLS_TO_INSTALL)}")
        elif result == 'partial':
            # 部分成功，可能需要重试
            status['failed'].append({
                'name': skill_name, 
                'error': detail, 
                'time': datetime.now().isoformat()
            })
            current_idx += 1  # 继续下一个
            log(f"⚠️  部分成功但继续: {skill_name}")
        else:
            status['failed'].append({
                'name': skill_name, 
                'error': detail, 
                'time': datetime.now().isoformat()
            })
            current_idx += 1  # 失败也继续
            log(f"❌ 失败但继续: {skill_name}")
        
        break  # 每小时只安装一个
    
    status['current_index'] = current_idx
    save_status(status)
    
    log("=" * 70)
    
    # 生成报告
    if current_idx >= len(SKILLS_TO_INSTALL):
        # 所有技能已安装完成
        msg = f"""📦 技能安装报告

✅ 所有技能安装完成！

总进度: {current_idx}/{len(SKILLS_TO_INSTALL)}
已安装: {len(status['installed'])}
失败: {len(status['failed'])}

任务状态: 完成 🎉
"""
    else:
        msg = f"""📦 技能安装报告

本次安装: {skill_name}
结果: {'✅ 成功' if result == 'success' else '⚠️ 部分' if result == 'partial' else '⏭️ 跳过' if result == 'skipped' else '❌ 失败'}
验证: {detail[:50] if detail else 'N/A'}

总进度: {current_idx}/{len(SKILLS_TO_INSTALL)}
已安装: {len([s for s in status['installed'] if '已存在' not in s.get('note', '')])}
失败: {len(status['failed'])}

下次安装: {SKILLS_TO_INSTALL[current_idx]['name'] if current_idx < len(SKILLS_TO_INSTALL) else '完成'}
"""
    log(msg)
    print(f"\n📱 飞书消息:\n{msg}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f"❌ 脚本异常: {e}")
        import traceback
        traceback.print_exc()
