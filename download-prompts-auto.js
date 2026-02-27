const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const PROMPTS_DIR = '/home/zzyuzhangxing/.openclaw/workspace/prompts/video';
const WIKI_URL = 'https://acnh7t5exjqh.feishu.cn/wiki/KCfnwKbb6ivlo0kwBeWcDb00nMC';

async function downloadFromWiki() {
  console.log('尝试从飞书Wiki下载提示词文件...\n');
  
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  try {
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
    
    // 访问Wiki页面
    console.log('访问Wiki页面...');
    await page.goto(WIKI_URL, { waitUntil: 'networkidle2', timeout: 60000 });
    await new Promise(r => setTimeout(r, 8000));
    
    // 获取页面上的所有文件链接
    const files = await page.evaluate(() => {
      const fileElements = document.querySelectorAll('a[href*="file"], a[download], .file-item, [data-file-token]');
      const results = [];
      fileElements.forEach(el => {
        const name = el.innerText?.trim() || el.getAttribute('data-file-name') || '';
        const href = el.href || '';
        if (name && (name.endsWith('.txt') || name.endsWith('.json') || name.endsWith('.md'))) {
          results.push({ name, href });
        }
      });
      return results;
    });
    
    console.log(`找到 ${files.length} 个文件:\n`);
    files.forEach((f, i) => console.log(`  ${i + 1}. ${f.name}`));
    
    // 尝试下载每个文件
    for (const file of files.slice(0, 3)) { // 先测试前3个
      try {
        console.log(`\n尝试下载: ${file.name}`);
        
        // 点击文件链接
        const fileLink = await page.$(`a[href="${file.href}"]`);
        if (fileLink) {
          await fileLink.click();
          await new Promise(r => setTimeout(r, 3000));
          
          // 等待下载（在headless模式下无法直接捕获下载）
          console.log(`  → 已触发下载`);
        }
      } catch (err) {
        console.log(`  ✗ 下载失败: ${err.message}`);
      }
    }
    
    // 截图记录
    await page.screenshot({ 
      path: '/home/zzyuzhangxing/.openclaw/workspace/prompts/wiki-page.png',
      fullPage: true 
    });
    console.log('\n✓ 已截图保存到 prompts/wiki-page.png');
    
  } catch (error) {
    console.error('错误:', error.message);
  } finally {
    await browser.close();
  }
}

downloadFromWiki();
