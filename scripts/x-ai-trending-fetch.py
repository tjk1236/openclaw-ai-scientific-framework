#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X(Twitter) RSS监控脚本 - RSSHub方案
通过RSSHub免费获取AI相关Twitter账号的推文

频率: 每天4次 (06:00, 12:00, 18:00, 00:00)
输出: data/x-ai-trending/x_trending_YYYYMMDD_HH.json
"""

import os
import sys
import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.parse import quote

# 尝试导入requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    print("[ERROR] requests 库未安装")
    sys.exit(1)

# 数据目录
DATA_DIR = os.path.expanduser("~/.openclaw/workspace/data/x-ai-trending")

# RSSHub实例列表 (按优先级排序)
RSSHub_INSTANCES = [
    "https://rsshub.app",
    "https://rsshub.rssforever.com",
    "https://rss.shab.fun",
    "https://rsshub.pseudoyu.com",
    "https://rsshub.diygod.dev",
]

# 监控的AI账号列表 (精心挑选)
AI_ACCOUNTS = [
    # === AI官方账号 ===
    {"name": "OpenAI", "type": "official", "priority": "P0"},
    {"name": "xai", "type": "official", "priority": "P0"},  # xAI (Elon Musk)
    {"name": "AnthropicAI", "type": "official", "priority": "P0"},
    {"name": "midjourney", "type": "official", "priority": "P0"},
    {"name": "runwayml", "type": "official", "priority": "P0"},
    {"name": "pika_labs", "type": "official", "priority": "P1"},
    {"name": "StabilityAI", "type": "official", "priority": "P1"},
    {"name": "heygenofficial", "type": "official", "priority": "P1"},
    
    # === AI大V/研究者 ===
    {"name": "DrJimFan", "type": "researcher", "priority": "P0"},  # Jim Fan (NVIDIA)
    {"name": "ylecun", "type": "researcher", "priority": "P0"},    # Yann LeCun
    {"name": "karpathy", "type": "researcher", "priority": "P0"},   # Andrej Karpathy
    {"name": "bindureddy", "type": "researcher", "priority": "P1"}, # Bindu Reddy
    {"name": "goodside", "type": "researcher", "priority": "P1"},  # Riley Goodside
    {"name": "swyx", "type": "researcher", "priority": "P1"},       # Shawn Wang
    {"name": "nickfloats", "type": "researcher", "priority": "P1"}, # Nick St. Pierre
    
    # === 中文AI社区 ===
    {"name": "op7418", "type": "cn_community", "priority": "P1"},   # 歸藏
    {"name": "dotey", "type": "cn_community", "priority": "P1"},    # 宝玉
]

def fetch_rss_feed(instance, username):
    """获取单个Twitter账号的RSS Feed"""
    url = f"{instance}/twitter/user/{username}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"[WARN] {instance} returned {response.status_code} for @{username}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Failed to fetch @{username} from {instance}: {e}")
        return None

def parse_rss_feed(xml_content, account_info):
    """解析RSS Feed，提取推文数据"""
    if not xml_content:
        return []
    
    tweets = []
    
    try:
        root = ET.fromstring(xml_content.encode('utf-8'))
        
        # RSS 2.0格式
        channel = root.find('channel')
        if channel is None:
            return tweets
        
        items = channel.findall('item')
        
        for item in items[:10]:  # 每个账号取最近10条
            try:
                title = item.find('title')
                link = item.find('link')
                pub_date = item.find('pubDate')
                description = item.find('description')
                guid = item.find('guid')
                
                # 提取推文ID
                tweet_id = ""
                if guid is not None and guid.text:
                    # guid格式: https://twitter.com/username/status/1234567890
                    parts = guid.text.split('/')
                    if len(parts) >= 6:
                        tweet_id = parts[-1]
                
                # 解析发布时间
                created_at = ""
                if pub_date is not None and pub_date.text:
                    try:
                        # RSS日期格式: Tue, 25 Feb 2026 12:34:56 GMT
                        from email.utils import parsedate_to_datetime
                        dt = parsedate_to_datetime(pub_date.text)
                        created_at = dt.isoformat()
                    except:
                        created_at = pub_date.text
                
                # 清理推文文本 (去除HTML标签)
                text = ""
                if title is not None and title.text:
                    text = title.text
                elif description is not None and description.text:
                    # 去除HTML标签
                    import re
                    text = re.sub(r'<[^>]+>', '', description.text)
                    text = re.sub(r'\s+', ' ', text).strip()
                
                # 只保留当天和昨天的推文
                try:
                    tweet_date = datetime.fromisoformat(created_at.replace('Z', '+00:00')).date()
                    today = datetime.now(timezone.utc).date()
                    yesterday = today - timedelta(days=1)
                    
                    if tweet_date not in [today, yesterday]:
                        continue
                except:
                    pass
                
                tweet = {
                    'id': tweet_id,
                    'author': account_info['name'],
                    'author_type': account_info['type'],
                    'priority': account_info['priority'],
                    'text': text[:500] if text else "",
                    'created_at': created_at,
                    'url': link.text if link is not None and link.text else f"https://twitter.com/{account_info['name']}/status/{tweet_id}",
                    'fetched_at': datetime.now().isoformat()
                }
                
                tweets.append(tweet)
                
            except Exception as e:
                print(f"[WARN] Failed to parse item: {e}")
                continue
                
    except Exception as e:
        print(f"[ERROR] Failed to parse RSS: {e}")
    
    return tweets

def fetch_all_accounts():
    """抓取所有监控账号的推文"""
    print("[INFO] Starting RSS fetch for all AI accounts...")
    print(f"[INFO] Total accounts: {len(AI_ACCOUNTS)}")
    print(f"[INFO] P0 (High Priority): {len([a for a in AI_ACCOUNTS if a['priority'] == 'P0'])}")
    
    all_tweets = []
    success_count = 0
    fail_count = 0
    
    # 优先抓取P0账号
    priority_order = sorted(AI_ACCOUNTS, key=lambda x: 0 if x['priority'] == 'P0' else 1)
    
    for account in priority_order:
        username = account['name']
        print(f"\n[INFO] Fetching @{username} ({account['priority']})...")
        
        xml_content = None
        used_instance = None
        
        # 尝试所有RSSHub实例
        for instance in RSSHub_INSTANCES:
            xml_content = fetch_rss_feed(instance, username)
            if xml_content:
                used_instance = instance
                break
            time.sleep(1)
        
        if xml_content:
            tweets = parse_rss_feed(xml_content, account)
            if tweets:
                print(f"[SUCCESS] Got {len(tweets)} tweets from @{username}")
                all_tweets.extend(tweets)
                success_count += 1
            else:
                print(f"[INFO] No recent tweets from @{username}")
                success_count += 1
        else:
            print(f"[ERROR] Failed to fetch @{username} from all instances")
            fail_count += 1
        
        # 请求间隔，避免触发限流
        time.sleep(2)
    
    print(f"\n{'='*50}")
    print(f"[SUMMARY] Success: {success_count}, Failed: {fail_count}")
    print(f"[SUMMARY] Total tweets: {len(all_tweets)}")
    
    return all_tweets

def rank_tweets(tweets):
    """根据内容质量/热度对推文排序"""
    
    # 关键词权重 (出现这些词说明内容重要)
    HOT_KEYWORDS = [
        'announce', 'launch', 'release', 'new', 'update',
        'breakthrough', 'major', 'important', 'significant',
        'GPT', 'Claude', 'Midjourney', 'Runway', 'Sora',
        'paper', 'research', 'model', 'training',
        '免费', '开源', '发布', '更新'
    ]
    
    def score_tweet(tweet):
        score = 0
        text = tweet.get('text', '').lower()
        
        # P0账号加权
        if tweet.get('priority') == 'P0':
            score += 10
        
        # 官方账号加权
        if tweet.get('author_type') == 'official':
            score += 5
        
        # 关键词匹配
        for keyword in HOT_KEYWORDS:
            if keyword.lower() in text:
                score += 2
        
        # 长度加权 (有内容的推文)
        score += min(len(text) / 100, 5)
        
        return score
    
    # 按分数降序排列
    scored_tweets = [(t, score_tweet(t)) for t in tweets]
    scored_tweets.sort(key=lambda x: x[1], reverse=True)
    
    return [t[0] for t in scored_tweets]

def save_data(tweets):
    """保存数据到文件"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 按分数排序
    ranked_tweets = rank_tweets(tweets)
    
    timestamp = datetime.now()
    filename = f"x_trending_{timestamp.strftime('%Y%m%d_%H')}.json"
    filepath = os.path.join(DATA_DIR, filename)
    
    # 同时更新latest
    latest_path = os.path.join(DATA_DIR, "x_trending_latest.json")
    
    data = {
        'fetch_time': timestamp.isoformat(),
        'status': 'success',
        'source': 'RSSHub',
        'total_accounts': len(AI_ACCOUNTS),
        'total_tweets': len(tweets),
        'tweets': ranked_tweets[:30]  # Top 30
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    with open(latest_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[INFO] Data saved to: {filepath}")
    print(f"[INFO] Latest updated: {latest_path}")
    
    return filepath

def main():
    """主函数"""
    print("=" * 60)
    print("X(Twitter) AI Trending Monitor (RSSHub)")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        tweets = fetch_all_accounts()
        
        if tweets:
            filepath = save_data(tweets)
            
            print(f"\n{'='*60}")
            print(f"✅ SUCCESS! Fetched {len(tweets)} tweets")
            print(f"✅ Top accounts:")
            
            # 显示Top 5
            for i, t in enumerate(rank_tweets(tweets)[:5], 1):
                preview = t['text'][:60].replace('\n', ' ')
                print(f"   {i}. @{t['author']}: {preview}...")
            
            print(f"{'='*60}")
            return 0
        else:
            print("\n[WARNING] No tweets fetched")
            return 1
            
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
