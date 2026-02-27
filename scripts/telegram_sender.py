#!/usr/bin/env python3
"""
Telegram 汇报发送脚本
用途: 将每日汇报发送到 Telegram
"""

import requests
import sys

# Telegram配置
TELEGRAM_BOT_TOKEN = '8754268528:AAFmE4FYl884g8sJ7OrT8nUZbrpVZhd6R2A'
TELEGRAM_CHAT_ID = '8466094649'
TELEGRAM_API = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

def send_message(text, parse_mode='Markdown'):
    """发送文本消息"""
    url = f"{TELEGRAM_API}/sendMessage"
    
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': parse_mode,
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        
        if data.get('ok'):
            print("✅ Telegram消息发送成功")
            return True
        else:
            print(f"❌ 发送失败: {data.get('description', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 请求错误: {e}")
        return False

def send_daily_report(report_file):
    """发送每日汇报"""
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Telegram消息长度限制4096字符，需要分段
        max_length = 4000  # 留一些余量
        
        # 发送标题
        header = "📊 *每日汇报* \n\n"
        
        if len(content) <= max_length:
            send_message(header + content)
        else:
            # 分段发送
            send_message(header + "汇报内容较长，分多条发送...")
            
            # 按行分割，尽量保持段落完整
            lines = content.split('\n')
            current_msg = ""
            
            for line in lines:
                if len(current_msg) + len(line) + 1 > max_length:
                    send_message(current_msg)
                    current_msg = line + '\n'
                else:
                    current_msg += line + '\n'
            
            if current_msg:
                send_message(current_msg)
        
        return True
    except Exception as e:
        print(f"❌ 读取报告失败: {e}")
        return False

def send_summary(summary_text):
    """发送汇报摘要"""
    return send_message(summary_text)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        # 测试模式
        test_msg = """🤖 *WF助手测试消息*

✅ Telegram连接正常！
✅ 汇报发送功能已配置

*下次汇报*: 明日 09:40"""
        
        print("发送测试消息...")
        send_message(test_msg)
        return
    
    report_file = sys.argv[1]
    print(f"发送报告: {report_file}")
    send_daily_report(report_file)

if __name__ == "__main__":
    main()
