#!/usr/bin/env python3
"""
本地GitHub技能库学习脚本
从预定义的技能列表中学习
"""

import random
import json
import os
from datetime import datetime

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

# 技能数据库
SKILLS_DB = {
    '🎬 视频/图片': [
        {'name': 'opencv-python', 'description': 'OpenCV的Python接口，计算机视觉库', 'stars': '5.8k'},
        {'name': 'ffmpeg-python', 'description': 'FFmpeg的Python封装，视频处理', 'stars': '3.2k'},
        {'name': 'Pillow', 'description': 'Python图像处理库', 'stars': '11.2k'},
        {'name': 'imageio', 'description': '读写图像/视频', 'stars': '1.8k'},
        {'name': 'scikit-image', 'description': '图像处理算法库', 'stars': '5.4k'},
        {'name': 'moviepy', 'description': '视频编辑Python库', 'stars': '12.5k'},
        {'name': 'rembg', 'description': '自动去除图片背景', 'stars': '8.2k'},
    ],
    '✍️ 内容创作': [
        {'name': 'transformers', 'description': 'Hugging Face的NLP模型库', 'stars': '125.6k'},
        {'name': 'langchain', 'description': 'LLM应用开发框架', 'stars': '86.4k'},
        {'name': 'openai-python', 'description': 'OpenAI API客户端', 'stars': '22.1k'},
        {'name': 'anthropic', 'description': 'Claude API客户端', 'stars': '4.5k'},
        {'name': 'llama-cpp-python', 'description': 'LLaMA模型Python绑定', 'stars': '6.8k'},
        {'name': 'sentence-transformers', 'description': '句子嵌入库', 'stars': '14.2k'},
        {'name': 'spacy', 'description': '工业级NLP库', 'stars': '28.6k'},
    ],
    '⚙️ 自动化': [
        {'name': 'selenium', 'description': '浏览器自动化', 'stars': '28.9k'},
        {'name': 'playwright-python', 'description': '现代浏览器自动化', 'stars': '12.4k'},
        {'name': 'requests', 'description': 'HTTP请求库', 'stars': '50.2k'},
        {'name': 'scrapy', 'description': '爬虫框架', 'stars': '49.8k'},
        {'name': 'schedule', 'description': 'Python定时任务', 'stars': '11.5k'},
        {'name': 'celery', 'description': '分布式任务队列', 'stars': '23.6k'},
        {'name': 'airflow', 'description': '工作流编排平台', 'stars': '35.2k'},
    ],
    '📊 数据分析': [
        {'name': 'pandas', 'description': '数据分析核心库', 'stars': '42.8k'},
        {'name': 'numpy', 'description': '数值计算库', 'stars': '25.6k'},
        {'name': 'scipy', 'description': '科学计算库', 'stars': '12.4k'},
        {'name': 'matplotlib', 'description': '数据可视化', 'stars': '18.9k'},
        {'name': 'seaborn', 'description': '统计数据可视化', 'stars': '12.1k'},
        {'name': 'plotly', 'description': '交互式可视化', 'stars': '15.8k'},
        {'name': 'scikit-learn', 'description': '机器学习库', 'stars': '57.3k'},
        {'name': 'xgboost', 'description': '梯度提升库', 'stars': '25.6k'},
        {'name': 'lightgbm', 'description': '轻量级梯度提升', 'stars': '16.2k'},
        {'name': 'catboost', 'description': 'Yandex梯度提升库', 'stars': '7.8k'},
    ],
    '🔧 开发工具': [
        {'name': 'pytest', 'description': 'Python测试框架', 'stars': '11.2k'},
        {'name': 'black', 'description': 'Python代码格式化', 'stars': '38.5k'},
        {'name': 'flake8', 'description': 'Python代码检查', 'stars': '3.2k'},
        {'name': 'mypy', 'description': 'Python类型检查', 'stars': '16.8k'},
        {'name': 'pre-commit', 'description': 'Git钩子管理', 'stars': '11.4k'},
    ],
    '🌐 Web开发': [
        {'name': 'fastapi', 'description': '现代Web框架', 'stars': '72.5k'},
        {'name': 'django', 'description': '全功能Web框架', 'stars': '78.2k'},
        {'name': 'flask', 'description': '轻量级Web框架', 'stars': '66.8k'},
        {'name': 'tornado', 'description': '异步Web框架', 'stars': '21.5k'},
    ],
    '🗄️ 数据库': [
        {'name': 'sqlalchemy', 'description': 'ORM框架', 'stars': '8.2k'},
        {'name': 'pymongo', 'description': 'MongoDB驱动', 'stars': '4.2k'},
        {'name': 'redis-py', 'description': 'Redis客户端', 'stars': '12.8k'},
        {'name': 'psycopg2', 'description': 'PostgreSQL驱动', 'stars': '3.1k'},
    ],
    '🔐 安全': [
        {'name': 'cryptography', 'description': '加密库', 'stars': '6.2k'},
        {'name': 'pycryptodome', 'description': '加密工具集', 'stars': '2.8k'},
        {'name': 'pyjwt', 'description': 'JSON Web Token', 'stars': '4.8k'},
    ],
    '📦 部署运维': [
        {'name': 'docker-py', 'description': 'Docker Python SDK', 'stars': '6.8k'},
        {'name': 'kubernetes-client', 'description': 'K8s Python客户端', 'stars': '6.5k'},
        {'name': 'ansible', 'description': '自动化运维', 'stars': '60.2k'},
        {'name': 'fabric', 'description': 'SSH部署工具', 'stars': '13.8k'},
    ],
}

def get_learned_skills():
    """获取已学习的技能"""
    log_file = '/home/zzyuzhangxing/.openclaw/workspace/skills-learning-log.json'
    learned = set()
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
            for log_entry in logs:
                skill_name = log_entry.get('skillLearned', {}).get('name', '')
                if skill_name and skill_name not in ['搜索中', '搜索中...', '未找到新技能']:
                    learned.add(skill_name.lower())
        except:
            pass
    return learned

def save_skill(skill, category):
    """保存学习的技能"""
    now = datetime.now()
    hour = now.hour
    
    log_entry = {
        'timestamp': now.isoformat(),
        'hour': hour,
        'category': category,
        'skillLearned': {
            'name': skill['name'],
            'link': f"https://github.com/{skill['name'].replace('-', '/')}",
            'description': skill['description'],
            'stars': skill['stars'],
            'source': 'github'
        },
        'details': skill['description']
    }
    
    # 保存到日志
    log_file = '/home/zzyuzhangxing/.openclaw/workspace/skills-learning-log.json'
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    logs.append(log_entry)
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    return log_entry

def main():
    """主函数"""
    log("=" * 60)
    log("🐙 GitHub技能学习 (离线版)")
    log("=" * 60)
    
    now = datetime.now()
    hour = now.hour
    
    # 确定类别（轮流）
    categories = list(SKILLS_DB.keys())
    category_name = categories[hour % len(categories)]
    
    log(f"⏰ 时间: {hour}:00")
    log(f"📂 目标类别: {category_name}")
    
    # 获取已学习技能
    learned = get_learned_skills()
    log(f"📚 已学习技能: {len(learned)} 个")
    
    # 获取该类别的技能
    category_skills = SKILLS_DB[category_name]
    
    # 过滤已学习
    new_skills = [s for s in category_skills if s['name'].lower() not in learned]
    log(f"🆕 新技能: {len(new_skills)} 个")
    
    if new_skills:
        # 随机选择一个
        best_skill = random.choice(new_skills)
        log(f"📖 学习: {best_skill['name']} ({best_skill['stars']} ⭐)")
        
        # 保存
        save_skill(best_skill, category_name)
        
        # 发送通知
        try:
            import subprocess
            message = f"""🎓 技能学习完成

⏰ 时间: {hour:02d}:00
📂 类别: {category_name}
📚 技能: {best_skill['name']}
⭐ 热度: {best_skill['stars']}

{best_skill['description']}

🔗 https://github.com/{best_skill['name'].replace('-', '/')}"""
            
            subprocess.run([
                'openclaw', 'message', 'send',
                '--channel', 'feishu',
                '--target', 'ou_f17427a7518faa014659589d89db4d8b',
                '--message', message
            ], capture_output=True, timeout=30)
            log("📱 已发送通知")
        except Exception as e:
            log(f"⚠️ 通知失败: {e}", 'WARN')
        
        log("✅ 学习完成！")
    else:
        # 如果该类别的都学完了，学其他类别
        log("⚠️ 该类别已学完，尝试其他类别...")
        all_skills = []
        for cat, skills in SKILLS_DB.items():
            for s in skills:
                if s['name'].lower() not in learned:
                    all_skills.append((cat, s))
        
        if all_skills:
            cat, skill = random.choice(all_skills)
            log(f"📖 学习: {skill['name']} ({cat})")
            save_skill(skill, cat)
            log("✅ 学习完成！")
        else:
            log("🎉 所有技能已学完！")
    
    log("=" * 60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f"❌ 错误: {e}", 'ERROR')
        import traceback
        traceback.print_exc()
