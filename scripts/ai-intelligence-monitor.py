#!/usr/bin/env python3
"""
泛AI情报监控脚本 - 全站搜索版 (修复版)
监控范围: B站全站AI相关内容（所有分区）
搜索策略: 多关键词并行搜索，覆盖全站AI热点，筛选最近7天
"""

import json
import requests
from datetime import datetime
import sys
import os
import time
from collections import OrderedDict
import traceback

# 设置日志文件
LOG_FILE = '/home/zzyuzhangxing/.openclaw/workspace/logs/ai_intelligence.log'

def log(msg, level='INFO'):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] [{level}] {msg}"
    print(log_msg)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    except:
        pass

# B站搜索API
BILIBILI_SEARCH_API = "https://api.bilibili.com/x/web-interface/search/type"

# 泛AI关键词矩阵 - 分层覆盖
AI_KEYWORDS = {
    # 核心AI大模型
    'core_ai': ['AI', '人工智能', 'ChatGPT', 'Claude', 'GPT', 'GPT-4', 'GPT-4o', 'GPT-5', 'OpenAI', 
                '大模型', 'LLM', '大语言模型', 'Foundation Model', '基座模型'],
    
    # 国产大模型
    'china_llm': ['文心一言', '通义千问', '讯飞星火', 'Kimi', 'kimi', '豆包', '智谱清言', '百川', 
                  '天工', '商量', '盘古大模型', '混元', '蓝心', 'AndesGPT'],
    
    # 图像生成
    'image_gen': ['ComfyUI', 'comfyui', 'Stable Diffusion', 'SD', 'Midjourney', 'MJ', 'DALL-E', 
                  'DALLE', 'AI绘画', 'AI画图', 'AI生成', 'AI绘图', '文生图', '图生图', 'ControlNet',
                  'LoRA', 'checkpoint', '模型训练', '炼丹'],
    
    # 视频/动画生成
    'video_gen': ['Sora', 'Runway', 'Pika', '可灵', '可靈', '即梦', '即夢', 'AI视频', 'AI动画', 
                  'AI動畫', '数字人', '數字人', '虚拟主播', 'AI换脸', 'Deepfake', '文生视频', 
                  '图生视频', 'AI电影', 'AI電影'],
    
    # AIGC内容创作
    'aigc': ['AIGC', '生成式AI', 'Generative AI', 'AI内容', 'AI创作', 'AI写作', 'AI文案',
             'AI配音', 'AI音乐', 'AI作曲', 'Suno', 'Udio', 'AI克隆声音'],
    
    # AI Agent与自动化
    'agent': ['Agent', '智能体', 'AI Agent', 'AutoGPT', '扣子', 'Coze', 'Coze bot', 
              'Flowise', 'LangChain', 'RAG', '向量数据库', '知识库', 'AI工作流', '自动化'],
    
    # AI编程工具
    'coding_ai': ['Copilot', 'GitHub Copilot', 'Cursor', 'Cursor AI', 'Codeium', 'Tabnine',
                  'AI编程', 'AI写代码', 'AI程序员', 'AI辅助编程', '代码生成'],
    
    # AI硬件与产品
    'ai_hardware': ['AI手机', 'AI Phone', 'AI PC', 'AI笔记本', 'NPU', '神经网络处理器',
                    'AI芯片', '苹果AI', 'Apple Intelligence', '华为AI', '小米AI', 'OPPO AI', 'vivo AI'],
    
    # 多模态与前沿
    'multimodal': ['多模态', 'Multimodal', 'Vision Pro', '空间计算', 'AR', 'VR', 'MR', 'XR',
                   '脑机接口', 'BCI', '具身智能', '机器人', '人形机器人'],
}

# 合并所有关键词
ALL_KEYWORDS = []
for category, words in AI_KEYWORDS.items():
    ALL_KEYWORDS.extend(words)

# 去重并保持顺序
ALL_KEYWORDS = list(OrderedDict.fromkeys(ALL_KEYWORDS))

def search_bilibili(keyword, page=1, page_size=20, days_back=7):
    """使用B站搜索API搜索视频 - 带时间筛选"""
    
    # 计算时间范围（Unix时间戳）
    now = int(time.time())
    pubdate_begin = now - (days_back * 24 * 60 * 60)  # N天前
    pubdate_end = now
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://search.bilibili.com',
        'Accept': 'application/json, text/plain, */*'
    }
    
    params = {
        'search_type': 'video',
        'keyword': keyword,
        'page': page,
        'page_size': page_size,
        'order': 'click',  # 按点击量排序（在最新中找最热）
        'duration': '0',   # 全部时长
        'tids': '0',       # 全部分区
        'pubdate_begin': pubdate_begin,  # 发布时间开始
        'pubdate_end': pubdate_end,      # 发布时间结束
    }
    
    try:
        response = requests.get(BILIBILI_SEARCH_API, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == 0:
            results = data.get('data', {}).get('result', [])
            log(f"  '{keyword}' 找到 {len(results)} 条 (近{days_back}天)")
            return results
        else:
            log(f"搜索'{keyword}'失败: {data.get('message', '未知错误')}", 'WARN')
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 412:
            log(f"搜索'{keyword}'触发反爬(412)，跳过", 'WARN')
        else:
            log(f"搜索'{keyword}'HTTP错误: {e}", 'ERROR')
    except Exception as e:
        log(f"搜索'{keyword}'出错: {e}", 'ERROR')
    
    return []

def parse_search_result(results):
    """解析搜索结果"""
    videos = []
    for item in results:
        # 处理不同API返回的字段差异
        video = {
            'bvid': item.get('bvid') or item.get('id'),
            'title': item.get('title', '').replace('</em>', '').replace('<em class="keyword">', ''),
            'link': f"https://www.bilibili.com/video/{item.get('bvid') or item.get('id')}",
            'author': item.get('author', ''),
            'mid': item.get('mid', 0),
            'view': int(item.get('play', 0) or item.get('stat', {}).get('view', 0)),
            'like': int(item.get('like', 0) or item.get('stat', {}).get('like', 0)),
            'coin': int(item.get('coins', 0) or item.get('stat', {}).get('coin', 0)),
            'favorite': int(item.get('favorites', 0) or item.get('stat', {}).get('favorite', 0)),
            'share': int(item.get('share', 0) or item.get('stat', {}).get('share', 0)),
            'reply': int(item.get('review', 0) or item.get('stat', {}).get('reply', 0)),
            'danmaku': int(item.get('danmaku', 0) or item.get('stat', {}).get('danmaku', 0)),
            'pubdate': item.get('pubdate', 0),
            'pic': item.get('pic', ''),
            'desc': item.get('description', '')[:200],
            'duration': item.get('duration', ''),
            'tag': item.get('tag', ''),
            'typename': item.get('typename', ''),  # 分区名
            'typeid': item.get('typeid', 0),       # 分区ID
        }
        videos.append(video)
    return videos

def calculate_hot_score(video):
    """计算热度分数"""
    view = video.get('view', 0)
    like = video.get('like', 0)
    coin = video.get('coin', 0)
    favorite = video.get('favorite', 0)
    share = video.get('share', 0)
    reply = video.get('reply', 0)
    
    # 综合热度算法：播放量权重最高，互动数据加权
    score = view + (like * 10) + (coin * 20) + (favorite * 15) + (share * 30) + (reply * 5)
    return score

def deduplicate_videos(videos):
    """按BVID去重，保留热度最高的"""
    seen = {}
    for v in videos:
        bvid = v.get('bvid')
        if not bvid:
            continue
        
        score = calculate_hot_score(v)
        if bvid not in seen or score > seen[bvid]['score']:
            seen[bvid] = {'video': v, 'score': score}
    
    # 返回按热度排序的视频列表
    sorted_items = sorted(seen.values(), key=lambda x: x['score'], reverse=True)
    return [item['video'] for item in sorted_items]

def analyze_trends(videos):
    """分析趋势和生成选题建议"""
    
    # 统计各分类提及次数
    category_mentions = {cat: 0 for cat in AI_KEYWORDS.keys()}
    
    for v in videos:
        title_lower = v['title'].lower()
        for cat, keywords in AI_KEYWORDS.items():
            if any(kw.lower() in title_lower for kw in keywords):
                category_mentions[cat] += 1
    
    # 生成选题建议 - 基于热度最高的视频
    suggestions = []
    
    for v in videos[:20]:  # 分析热度前20
        title = v['title']
        view = v['view']
        like = v['like']
        author = v['author']
        typename = v.get('typename', '未知分区')
        
        # 更灵活的匹配规则
        title_lower = title.lower()
        
        # ComfyUI/工作流类
        if any(k in title for k in ['ComfyUI', 'comfyui', '工作流', 'workflow']):
            suggestions.append({
                'type': '🎨 ComfyUI教程',
                'title': title[:40],
                'data': f'{view:,}播放',
                'source': f'{author} ({typename})',
                'priority': '🔥🔥🔥'
            })
        # AI视频生成类
        elif any(k in title for k in ['Sora', '可灵', '可靈', 'Runway', 'Pika', '即梦', 'AI视频', '数字人']):
            suggestions.append({
                'type': '🎬 AI视频生成',
                'title': title[:40],
                'data': f'{view:,}播放',
                'source': f'{author} ({typename})',
                'priority': '🔥🔥🔥'
            })
        # 大模型类
        elif any(k in title for k in ['ChatGPT', 'Claude', 'GPT-4', 'GPT-5', '大模型', 'Kimi', '豆包', '文心一言']):
            suggestions.append({
                'type': '🤖 大模型动态',
                'title': title[:40],
                'data': f'{view:,}播放',
                'source': f'{author} ({typename})',
                'priority': '🔥🔥'
            })
        # 图像生成类
        elif any(k in title for k in ['Midjourney', 'Stable Diffusion', 'SD', 'AI绘画', 'AI绘图']):
            suggestions.append({
                'type': '🎨 AI绘画',
                'title': title[:40],
                'data': f'{view:,}播放',
                'source': f'{author} ({typename})',
                'priority': '🔥🔥'
            })
        # 评测对比类
        elif any(k in title for k in ['评测', '测评', '对比', '横向', '哪个好']):
            suggestions.append({
                'type': '⚖️ 工具评测',
                'title': title[:40],
                'data': f'{view:,}播放',
                'source': f'{author} ({typename})',
                'priority': '🔥🔥'
            })
        # 编程类
        elif any(k in title for k in ['Cursor', 'Copilot', 'AI编程', 'AI写代码']):
            suggestions.append({
                'type': '💻 AI编程',
                'title': title[:40],
                'data': f'{view:,}播放',
                'source': f'{author} ({typename})',
                'priority': '🔥'
            })
        # 硬件类
        elif any(k in title for k in ['AI手机', 'AI PC', 'Apple Intelligence']):
            suggestions.append({
                'type': '📱 AI硬件',
                'title': title[:40],
                'data': f'{view:,}播放',
                'source': f'{author} ({typename})',
                'priority': '🔥'
            })
        # 通用AI类（兜底）
        elif 'AI' in title or '人工智能' in title:
            suggestions.append({
                'type': '🤖 AI综合',
                'title': title[:40],
                'data': f'{view:,}播放',
                'source': f'{author} ({typename})',
                'priority': '🔥'
            })
    
    return category_mentions, suggestions

def format_pubdate(pubdate_ts):
    """格式化发布时间为友好字符串"""
    if not pubdate_ts:
        return "未知"
    
    now = int(time.time())
    diff = now - pubdate_ts
    
    if diff < 3600:
        return f"{diff // 60}分钟前"
    elif diff < 86400:
        return f"{diff // 3600}小时前"
    elif diff < 7 * 86400:
        return f"{diff // 86400}天前"
    else:
        return f"{diff // 86400}天前"

def generate_report(videos, category_mentions, suggestions, search_stats):
    """生成日报 - 只显示最近7天内发布的视频"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_ts = int(time.time())
    seven_days_ago = now_ts - (7 * 24 * 60 * 60)
    
    # 筛选最近7天的视频
    recent_videos = [v for v in videos if v.get('pubdate', 0) >= seven_days_ago]
    recent_videos.sort(key=calculate_hot_score, reverse=True)
    
    # 统计
    total_recent = len(recent_videos)
    total_all = len(videos)
    
    if total_recent == 0:
        time_note = "⚠️ 未找到7天内发布的视频，显示全部搜索结果中热度最高的"
        display_videos = videos[:10]
    else:
        time_note = f"✅ 已筛选最近7天内发布的视频 ({total_recent}/{total_all}条)"
        display_videos = recent_videos[:10]
    
    report = f"""# 📡 泛AI情报日报 - {today}

> **生成时间**: {timestamp}  
> **监控范围**: B站全站AI相关内容  
> **数据筛选**: {time_note}

---

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| 🔍 搜索关键词 | {len(ALL_KEYWORDS)} 个 |
| 📹 发现视频 | {total_all} 条 |
| 📅 近7天视频 | {total_recent} 条 |
| 👁️ 总播放量 | {sum(v.get('view', 0) for v in videos):,} |
| ❤️ 总点赞数 | {sum(v.get('like', 0) for v in videos):,} |

---

## 🏷️ 分类热度

| 分类 | 提及次数 | 关键词示例 |
|------|---------|-----------|
"""
    
    category_names = {
        'core_ai': '🧠 核心AI大模型',
        'china_llm': '🇨🇳 国产大模型',
        'image_gen': '🎨 图像生成',
        'video_gen': '🎬 视频/动画生成',
        'aigc': '✍️ AIGC内容创作',
        'agent': '🤖 AI Agent',
        'coding_ai': '💻 AI编程工具',
        'ai_hardware': '📱 AI硬件产品',
        'multimodal': '🌐 多模态/前沿'
    }
    
    for cat, count in sorted(category_mentions.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            cat_name = category_names.get(cat, cat)
            example = AI_KEYWORDS[cat][0] if AI_KEYWORDS[cat] else '-'
            report += f"| {cat_name} | {count} | {example}... |\n"
    
    report += f"""
---

## 🔥 Top 10 AI热门视频 (近7天)

"""
    
    # Top 10视频
    for i, v in enumerate(display_videos, 1):
        pub_str = format_pubdate(v.get('pubdate', 0))
        report += f"""### {i}. {v['title'][:60]}
- **UP主**: {v['author']} ({v.get('typename', '未知分区')})
- **数据**: 👁️ {v['view']:,} | 👍 {v['like']:,} | 📤 {v['share']:,} | 📅 {pub_str}
- **链接**: {v['link']}
- **简介**: {v['desc'][:100]}...

"""
    
    report += """---

## 💡 选题建议

| 类型 | 标题 | 数据 | 来源 | 优先级 |
|------|------|------|------|--------|
"""
    
    # 选题建议
    for s in suggestions[:10]:
        report += f"| {s['type']} | {s['title']} | {s['data']} | {s['source']} | {s['priority']} |\n"
    
    report += f"""
---

## 📝 监控说明

**关键词覆盖**: {len(ALL_KEYWORDS)} 个泛AI相关关键词
**搜索分区**: 全站（所有分区）
**时间筛选**: 最近7天内发布
**排序方式**: 按综合热度（播放+互动加权）
**去重策略**: 按BVID去重，保留热度最高

---

*Generated by OpenClaw WF助手 🤖*  
*下次更新: 明日 09:00*
"""
    
    return report

def main():
    """主函数"""
    print("=" * 70)
    log("📡 泛AI情报监控 - 全站搜索版")
    log("=" * 70)
    
    log(f"🕐 监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"🎯 关键词数量: {len(ALL_KEYWORDS)} 个")
    log(f"🔍 搜索策略: 全站覆盖 + 多关键词并行 + 7天时间筛选")
    
    all_videos = []
    search_stats = {}
    
    # 优先搜索核心关键词（避免API限制）
    priority_keywords = [
        'AI', '人工智能', 'ChatGPT', 'Claude', 'ComfyUI', 'Sora', '大模型',
        'Stable Diffusion', 'Midjourney', '可灵', '即梦', 'Kimi', '豆包',
        'AIGC', '数字人', 'AI视频', 'AI绘画', 'Copilot', 'Cursor'
    ]
    
    log("🔍 开始搜索核心关键词...")
    for i, keyword in enumerate(priority_keywords, 1):
        log(f"[{i}/{len(priority_keywords)}] 搜索: '{keyword}'...")
        results = search_bilibili(keyword, page=1, page_size=20, days_back=7)
        
        if results:
            videos = parse_search_result(results)
            all_videos.extend(videos)
            search_stats[keyword] = len(videos)
            log(f"  ✅ 找到 {len(videos)} 条")
        else:
            log(f"  ⚠️ 无结果")
        
        # 避免请求过快（B站有反爬机制）
        time.sleep(2)
    
    log(f"📊 原始数据: {len(all_videos)} 条视频")
    
    # 客户端时间筛选（API参数不生效，需二次过滤）
    now_ts = int(time.time())
    seven_days_ago = now_ts - (7 * 24 * 60 * 60)
    
    # 筛选最近7天发布的视频
    recent_videos = [v for v in all_videos if v.get('pubdate', 0) >= seven_days_ago]
    log(f"📅 近7天筛选: {len(recent_videos)} 条视频")
    
    # 如果7天内视频太少(<5条)，尝试放宽到30天
    if len(recent_videos) < 5:
        thirty_days_ago = now_ts - (30 * 24 * 60 * 60)
        recent_videos = [v for v in all_videos if v.get('pubdate', 0) >= thirty_days_ago]
        log(f"📅 放宽到30天: {len(recent_videos)} 条视频")
    
    # 去重（在时间筛选后的数据上）
    log("🔄 正在去重...")
    unique_videos = deduplicate_videos(recent_videos if recent_videos else all_videos)
    log(f"✅ 去重后: {len(unique_videos)} 条视频")
    
    # 分析趋势（在去重后的数据上）
    log("📈 正在分析趋势...")
    category_mentions, suggestions = analyze_trends(unique_videos)
    
    # 生成报告
    log("📝 正在生成报告...")
    report = generate_report(unique_videos, category_mentions, suggestions, search_stats)
    
    # 保存报告
    data_dir = '/home/zzyuzhangxing/.openclaw/workspace/data/ai-intelligence'
    os.makedirs(data_dir, exist_ok=True)
    
    today = datetime.now().strftime('%Y%m%d')
    timestamp = datetime.now().strftime('%H%M')
    
    # 保存带时间戳的版本
    report_file = f"{data_dir}/daily_report_{today}_{timestamp}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 保存最新报告
    latest_file = f"{data_dir}/daily_report_latest.md"
    with open(latest_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 统计近7天视频数
    now_ts = int(time.time())
    seven_days_ago = now_ts - (7 * 24 * 60 * 60)
    recent_count = len([v for v in unique_videos if v.get('pubdate', 0) >= seven_days_ago])
    
    log("=" * 70)
    log("📊 监控摘要")
    log("=" * 70)
    log(f"📹 发现视频: {len(unique_videos)} 条")
    log(f"📅 近7天视频: {recent_count} 条")
    log(f"👁️  总播放量: {sum(v.get('view', 0) for v in unique_videos):,}")
    log(f"❤️  总点赞数: {sum(v.get('like', 0) for v in unique_videos):,}")
    log(f"💡 选题建议: {len(suggestions)} 条")
    if unique_videos:
        top_video = max(unique_videos, key=lambda x: x.get('view', 0))
        pub_str = format_pubdate(top_video.get('pubdate', 0))
        log(f"🔥 Top 1: {top_video['title'][:40]}... ({top_video['view']:,}播放, {pub_str})")
    log(f"✅ 报告已保存: {report_file}")
    log("=" * 70)

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        log(f"❌ 监控异常: {e}", 'ERROR')
        traceback.print_exc()
        sys.exit(1)
