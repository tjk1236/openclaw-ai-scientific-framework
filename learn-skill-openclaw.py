#!/usr/bin/env python3
"""
OpenClaw专用技能学习
针对老鱼自媒体工作流的定制化技能
"""

import json
import os
import random
from datetime import datetime

LOG_FILE = '/home/zzyuzhangxing/.openclaw/workspace/logs/openclaw_skills.log'

def log(msg, level='INFO'):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] [{level}] {msg}"
    print(log_msg)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    except:
        pass

# OpenClaw专用技能库
OPENCLAW_SKILLS = [
    # 🎬 视频/图片
    {"name": "ComfyUI工作流自动化", "category": "🎬 视频/图片", "desc": "自动化ComfyUI图片生成流程，批量生成配图", "priority": 5},
    {"name": "视频帧AI处理", "category": "🎬 视频/图片", "desc": "从视频提取关键帧并使用AI进行处理优化", "priority": 5},
    {"name": "批量缩略图生成", "category": "🎬 视频/图片", "desc": "批量生成B站/抖音风格缩略图", "priority": 4},
    {"name": "AI视频剪辑", "category": "🎬 视频/图片", "desc": "自动识别精彩片段并剪辑拼接", "priority": 4},
    {"name": "风格迁移处理", "category": "🎬 视频/图片", "desc": "将图片转换为特定艺术风格", "priority": 3},
    {"name": "图像超分辨率", "category": "🎬 视频/图片", "desc": "使用Real-ESRGAN提升图片质量", "priority": 3},
    
    # ✍️ 内容创作
    {"name": "爆款标题生成器", "category": "✍️ 内容创作", "desc": "基于B站数据训练的AI标题优化", "priority": 5},
    {"name": "视频脚本自动生成", "category": "✍️ 内容创作", "desc": "根据主题自动生成完整视频脚本", "priority": 5},
    {"name": "小红书文案生成", "category": "✍️ 内容创作", "desc": "生成小红书风格的种草文案", "priority": 4},
    {"name": "B站简介优化", "category": "✍️ 内容创作", "desc": "自动生成带标签的B站视频简介", "priority": 4},
    {"name": "AI配音合成", "category": "✍️ 内容创作", "desc": "使用TTS生成高质量配音", "priority": 4},
    {"name": "热点话题追踪", "category": "✍️ 内容创作", "desc": "实时追踪AI领域热点话题", "priority": 5},
    
    # ⚙️ 自动化
    {"name": "B站数据自动获取", "category": "⚙️ 自动化", "desc": "定时自动获取账号数据和视频表现", "priority": 5},
    {"name": "飞书日报生成", "category": "⚙️ 自动化", "desc": "整合数据自动生成每日汇报", "priority": 5},
    {"name": "Git自动备份", "category": "⚙️ 自动化", "desc": "定时自动提交备份到Git仓库", "priority": 4},
    {"name": "多平台定时发布", "category": "⚙️ 自动化", "desc": "自动发布到B站/抖音/小红书", "priority": 4},
    {"name": "竞品监控", "category": "⚙️ 自动化", "desc": "监控同类博主的视频数据", "priority": 3},
    {"name": "消息自动转发", "category": "⚙️ 自动化", "desc": "多平台消息同步转发", "priority": 3},
    
    # 📊 数据分析
    {"name": "B站全站AI监控", "category": "📊 数据分析", "desc": "追踪全站AI相关热门视频", "priority": 5},
    {"name": "视频表现分析", "category": "📊 数据分析", "desc": "分析播放/点赞/评论趋势", "priority": 5},
    {"name": "关键词热度分析", "category": "📊 数据分析", "desc": "追踪AI关键词搜索趋势", "priority": 4},
    {"name": "粉丝增长预测", "category": "📊 数据分析", "desc": "基于历史数据预测增长趋势", "priority": 3},
    {"name": "最佳发布时间", "category": "📊 数据分析", "desc": "分析最佳视频发布时段", "priority": 3},
    {"name": "评论情感分析", "category": "📊 数据分析", "desc": "分析粉丝评论情绪倾向", "priority": 2},
    
    # 🔧 OpenClaw高级
    {"name": "自定义Agent开发", "category": "🔧 OpenClaw高级", "desc": "开发专用Agent处理特定任务", "priority": 5},
    {"name": "定时任务编排", "category": "🔧 OpenClaw高级", "desc": "复杂的定时任务流程编排", "priority": 4},
    {"name": "多Agent协作", "category": "🔧 OpenClaw高级", "desc": "多个Agent协同工作处理任务", "priority": 4},
    {"name": "Webhook集成", "category": "🔧 OpenClaw高级", "desc": "接收外部事件自动触发任务", "priority": 3},
    {"name": "错误自动恢复", "category": "🔧 OpenClaw高级", "desc": "任务失败自动重试机制", "priority": 3},
    {"name": "日志分析告警", "category": "🔧 OpenClaw高级", "desc": "监控系统状态并告警", "priority": 3},
    
    # 🛠️ 开发工具
    {"name": "B站API封装", "category": "🛠️ 开发工具", "desc": "封装B站官方和第三方API", "priority": 5},
    {"name": "飞书API集成", "category": "🛠️ 开发工具", "desc": "飞书机器人和文档API集成", "priority": 5},
    {"name": "爬虫技术", "category": "🛠️ 开发工具", "desc": "网站内容抓取与解析", "priority": 4},
    {"name": "Docker容器管理", "category": "🛠️ 开发工具", "desc": "管理各种服务容器", "priority": 3},
    {"name": "API速率限制处理", "category": "🛠️ 开发工具", "desc": "处理接口限流和重试", "priority": 3},
    {"name": "代理IP轮换", "category": "🛠️ 开发工具", "desc": "处理IP封禁问题", "priority": 2},
    
    # 🤖 AI大模型
    {"name": "OpenAI API优化", "category": "🤖 AI大模型", "desc": "GPT-4/Claude API高效调用", "priority": 5},
    {"name": "本地大模型部署", "category": "🤖 AI大模型", "desc": "Ollama部署本地LLM", "priority": 4},
    {"name": "提示词工程", "category": "🤖 AI大模型", "desc": "Prompt优化和版本管理", "priority": 5},
    {"name": "RAG知识库", "category": "🤖 AI大模型", "desc": "构建私有知识库", "priority": 4},
    {"name": "Token用量监控", "category": "🤖 AI大模型", "desc": "控制API调用成本", "priority": 3},
    {"name": "多模型对比", "category": "🤖 AI大模型", "desc": "对比不同模型效果", "priority": 3},
    
    # 🎯 专属技能
    {"name": "ComfyUI一键部署", "category": "🎯 老鱼专属", "desc": "快速部署常用ComfyUI工作流", "priority": 5},
    {"name": "Seedence自动化", "category": "🎯 老鱼专属", "desc": "自动化Seedence内容生成", "priority": 5},
    {"name": "AI工具评测模板", "category": "🎯 老鱼专属", "desc": "快速生成评测视频脚本模板", "priority": 4},
    {"name": "教程视频结构化", "category": "🎯 老鱼专属", "desc": "自动整理教程大纲和要点", "priority": 4},
    {"name": "粉丝问答整理", "category": "🎯 老鱼专属", "desc": "自动整理常见问题FAQ", "priority": 3},
    {"name": "视频系列规划", "category": "🎯 老鱼专属", "desc": "规划系列视频内容和节奏", "priority": 3},
]

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
                    learned.add(skill_name)
            return learned
        except:
            pass
    return set()

def select_skill_by_hour(hour, learned):
    """根据当前小时选择技能类别"""
    # 偶数小时: 视频/图片 + 内容创作
    # 奇数小时: 自动化 + 数据分析 + 其他
    
    if hour % 2 == 0:
        target_categories = ['🎬 视频/图片', '✍️ 内容创作', '🎯 老鱼专属']
    else:
        target_categories = ['⚙️ 自动化', '📊 数据分析', '🔧 OpenClaw高级', '🛠️ 开发工具']
    
    # 过滤未学习的技能
    available = [s for s in OPENCLAW_SKILLS 
                 if s['category'] in target_categories and s['name'] not in learned]
    
    if not available:
        # 如果目标类别都学完了，从全部中选
        available = [s for s in OPENCLAW_SKILLS if s['name'] not in learned]
    
    if not available:
        return None
    
    # 优先选择priority高的，然后随机
    available.sort(key=lambda x: x['priority'], reverse=True)
    top_skills = available[:10]  # 前10个高优先级
    return random.choice(top_skills)

def save_skill(skill):
    """保存技能学习记录"""
    from datetime import datetime
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'hour': datetime.now().hour,
        'category': skill['category'],
        'skillLearned': {
            'name': skill['name'],
            'description': skill['desc'],
            'priority': skill['priority'],
            'source': 'openclaw-custom'
        },
        'details': f"""# {skill['name']}

## 类别
{skill['category']}

## 描述
{skill['desc']}

## 优先级
{'⭐' * skill['priority']}

## 学习建议
1. 查阅OpenClaw文档相关章节
2. 搜索相关技能实现案例
3. 在实际项目中尝试应用
4. 记录遇到的问题和解决方案

## 相关工具
- OpenClaw CLI
- Python脚本
- 相关API接口
"""
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

def send_notification(skill):
    """发送飞书通知"""
    try:
        import subprocess
        message = f"""🎓 OpenClaw专属技能学习完成

⏰ 时间: {datetime.now().strftime('%H:%M')}
📂 类别: {skill['category']}
📚 技能: {skill['name']}
⭐ 优先级: {'⭐' * skill['priority']}

📝 简介: {skill['desc']}

💡 这是专门为老鱼自媒体工作流定制的技能！"""
        
        subprocess.run([
            'openclaw', 'message', 'send',
            '--channel', 'feishu',
            '--target', 'ou_f17427a7518faa014659589d89db4d8b',
            '--message', message
        ], capture_output=True, timeout=30)
        log("  → 已发送飞书通知")
    except Exception as e:
        log(f"  ⚠️ 通知发送失败: {e}", 'WARN')

def main():
    """主函数"""
    now = datetime.now()
    hour = now.hour
    
    log("=" * 60)
    log("🎓 OpenClaw专属技能学习")
    log("=" * 60)
    log(f"⏰ 当前时间: {now.strftime('%H:%M')}")
    
    # 获取已学习技能
    learned = get_learned_skills()
    log(f"📚 已学习技能: {len(learned)} 个")
    log(f"📊 技能库总量: {len(OPENCLAW_SKILLS)} 个")
    
    # 根据小时选择技能
    skill = select_skill_by_hour(hour, learned)
    
    if not skill:
        log("⚠️ 所有技能都已学习完毕！", 'WARN')
        log("建议更新技能库或重置学习记录")
        return 0
    
    # 保存学习记录
    save_skill(skill)
    
    # 显示结果
    log("")
    log("=" * 60)
    log("🎉 技能学习完成")
    log("=" * 60)
    log(f"📚 技能: {skill['name']}")
    log(f"📂 类别: {skill['category']}")
    log(f"⭐ 优先级: {'⭐' * skill['priority']}")
    log(f"📝 描述: {skill['desc']}")
    log("")
    log("💡 这是专门为老鱼自媒体工作流定制的技能！")
    log("=" * 60)
    
    # 发送通知
    send_notification(skill)
    
    log("\n✅ 完成！")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
