#!/usr/bin/env python3
"""
GitHub Awesome Lists 技能学习
来源: GitHub上的Awesome Lists
特点: 无需登录，API稳定，内容丰富
"""

import requests
import json
import os
from datetime import datetime
import random

# Awesome Lists 配置
AWESOME_REPOS = [
    # AI/ML 相关
    ('josephmisiti', 'awesome-machine-learning'),
    ('kjam', 'awesome-deep-learning'),
    ('ChristosChristofidis', 'awesome-deep-learning'),
    ('dvgodoy', 'awesome-deep-learning-resources'),
    ('mahmoud', 'awesome-python-applications'),
    ('terryum', 'awesome-deep-learning-papers'),
    ('guillaume-chevalier', 'awesome-deep-learning-resources'),
    ('markusschanta', 'awesome-jupyter'),
    ('jonathontoon', 'awesome-artificial-intelligence'),
    ('fregu856', 'awesome-artificial-intelligence'),
    ('richarduman', 'awesome-artificial-intelligence'),
    # 开发工具
    ('vinta', 'awesome-python'),
    ('tilkinsc', 'awesome-qt'),
    ('dkhamsing', 'open-source-ios-apps'),
    ('serhii-londar', 'open-source-mac-os-apps'),
    # 数据科学
    ('academic', 'awesome-datascience'),
    ('sindresorhus', 'awesome-nodejs'),
    # 自动化/DevOps
    ('InfrastructureAsCode-Awesome', 'Awesome-InfrastructureAsCode'),
    ('works-on-my-machine', 'awesome-open-source-supply-chain-security'),
]

LOG_FILE = '/home/zzyuzhangxing/.openclaw/workspace/logs/github_skills.log'

def log(msg, level='INFO'):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] [{level}] {msg}"
    print(log_msg)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    except:
        pass

def get_learned_skills():
    """获取已学习的技能"""
    log_path = '/home/zzyuzhangxing/.openclaw/workspace/skills-learning-log.json'
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r') as f:
                logs = json.load(f)
            learned = set()
            for log_entry in logs:
                skill_name = log_entry.get('skillLearned', {}).get('name', '')
                if skill_name and skill_name not in ['搜索中', '搜索中...', '未找到新技能']:
                    learned.add(skill_name.lower())
            return learned
        except:
            pass
    return set()

def fetch_awesome_repo(owner, repo):
    """获取Awesome List内容"""
    # 使用原始GitHub链接
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
    
    try:
        log(f"获取 {owner}/{repo} ...")
        response = requests.get(url, timeout=30, verify=False)
        
        if response.status_code == 200:
            return response.text
        else:
            log(f"  ⚠️ HTTP {response.status_code}", 'WARN')
            return None
    except Exception as e:
        log(f"  ✗ 错误: {e}", 'ERROR')
        return None

def parse_skills_from_readme(readme):
    """从README解析技能列表"""
    skills = []
    lines = readme.split('\n')
    
    for line in lines:
        # 匹配Markdown链接格式: [name](url) - description
        import re
        match = re.match(r'^\s*[-*]\s*\[([^\]]+)\]\(([^)]+)\)\s*-?\s*(.*)', line)
        if match:
            name = match.group(1).strip()
            url = match.group(2).strip()
            desc = match.group(3).strip()
            
            if name and url and not url.startswith('#'):
                skills.append({
                    'name': name[:100],
                    'url': url,
                    'description': desc[:200],
                    'source': 'github'
                })
    
    return skills

def categorize_skill(name, desc):
    """分类技能"""
    text = (name + ' ' + desc).lower()
    
    if any(kw in text for kw in ['video', 'image', 'cv', 'vision', 'camera', 'frame', 'generate', 'diffusion', 'comfyui', 'stable diffusion', 'photo', 'picture']):
        return '🎬 视频/图片'
    elif any(kw in text for kw in ['nlp', 'text', 'language', 'chat', 'llm', 'gpt', 'write', 'content', 'article', 'summarize']):
        return '✍️ 内容创作'
    elif any(kw in text for kw in ['auto', 'bot', 'script', 'workflow', 'deploy', 'ci/cd', 'github action', 'cron']):
        return '⚙️ 自动化'
    elif any(kw in text for kw in ['data', 'analysis', 'analytics', 'pandas', 'numpy', 'sql', 'database', 'visualization', 'chart']):
        return '📊 数据分析'
    else:
        return '📦 其他'

def save_skill_to_log(skill, category):
    """保存技能学习记录"""
    from datetime import datetime
    import os
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'hour': datetime.now().hour,
        'category': category,
        'skillLearned': {
            'name': skill['name'],
            'url': skill['url'],
            'description': skill['description'],
            'source': skill.get('source', 'github')
        }
    }
    
    log_path = '/home/zzyuzhangxing/.openclaw/workspace/skills-learning-log.json'
    logs = []
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            logs = json.load(f)
    logs.append(log_entry)
    
    with open(log_path, 'w') as f:
        json.dump(logs, f, indent=2)
    
    log(f"  → 已记录技能: {skill['name']}")

def main():
    """主函数"""
    log("=" * 60)
    log("📚 GitHub Awesome Lists 技能学习")
    log("=" * 60)
    
    # 获取已学习技能
    learned = get_learned_skills()
    log(f"已学习技能数: {len(learned)}")
    
    # 随机选择一个仓库
    owner, repo = random.choice(AWESOME_REPOS)
    log(f"\n🎯 选择仓库: {owner}/{repo}")
    
    # 获取README
    readme = fetch_awesome_repo(owner, repo)
    if not readme:
        log("❌ 无法获取仓库内容", 'ERROR')
        return 1
    
    # 解析技能
    skills = parse_skills_from_readme(readme)
    log(f"📖 解析到 {len(skills)} 个技能")
    
    if not skills:
        log("⚠️ 未找到技能", 'WARN')
        return 1
    
    # 过滤已学习的技能
    available_skills = [s for s in skills if s['name'].lower() not in learned]
    log(f"✅ 可用新技能: {len(available_skills)} 个")
    
    if not available_skills:
        log("⚠️ 所有技能都已学习过")
        return 0
    
    # 随机选择一个技能学习
    skill = random.choice(available_skills)
    category = categorize_skill(skill['name'], skill['description'])
    
    log("\n" + "=" * 60)
    log("🎓 技能学习完成")
    log("=" * 60)
    log(f"📚 技能: {skill['name']}")
    log(f"📂 类别: {category}")
    log(f"🔗 链接: {skill['url']}")
    if skill['description']:
        log(f"📝 描述: {skill['description'][:100]}...")
    
    # 保存记录
    save_skill_to_log(skill, category)
    
    log("\n✅ 完成！")
    log("=" * 60)
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
