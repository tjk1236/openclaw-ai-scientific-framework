const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 使用stealth插件绕过Cloudflare检测
puppeteer.use(StealthPlugin());

// 技能分类关键词映射
const CATEGORY_KEYWORDS = {
  video_image: ['video', 'image', 'frame', 'camera', 'photo', 'picture', 'visual', 'comfyui', 'generate', 'ai', 'animation', 'render', 'ffmpeg', 'prompt'],
  content: ['summarize', 'content', 'write', 'blog', 'social', 'media', 'article', 'text', 'copy', 'tweet', 'chinese', 'writer'],
  automation: ['github', 'coding', 'agent', 'script', 'automate', 'workflow', 'bot', 'cron', 'activecampaign', 'netsuite', 'googlephotos'],
  data: ['analysis', 'log', 'usage', 'data', 'google', 'workspace', 'excel', 'sheet', 'csv', 'polars', 'eda', 'gh-issues', 'session-logs']
};

// 已学习的技能（去重）
function getLearnedSkills() {
  const logPath = path.join(process.env.HOME, '.openclaw/workspace/skills-learning-log.json');
  if (fs.existsSync(logPath)) {
    try {
      const logs = JSON.parse(fs.readFileSync(logPath, 'utf8'));
      const learned = new Set();
      logs.forEach(log => {
        const skillName = log.skillLearned?.name;
        if (skillName && skillName !== '搜索中' && skillName !== '搜索中...' && skillName !== '未找到新技能') {
          learned.add(skillName.toLowerCase());
          learned.add(skillName.toLowerCase().replace(/\s+/g, '-').replace('.md', ''));
        }
      });
      return learned;
    } catch (e) {
      console.error('  ✗ 读取学习记录失败:', e.message);
    }
  }
  return new Set();
}

// 判断技能属于哪个类别
function categorizeSkill(skillName, skillDesc = '') {
  const text = (skillName + ' ' + skillDesc).toLowerCase();
  
  for (const [category, keywords] of Object.entries(CATEGORY_KEYWORDS)) {
    if (keywords.some(kw => text.includes(kw))) {
      return category;
    }
  }
  return 'other';
}

async function learnSkill() {
  const now = new Date();
  const hour = now.getHours();
  const timeStr = now.toLocaleString('zh-CN', { hour12: false });
  
  console.log(`[${timeStr}] 📚 开始学习新技能...`);
  
  let browser;
  let bestSkill = null;
  let skillDetails = '';
  let categoryName = '';
  
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    // 从文件读取Cookie
    let authCookie = '';
    try {
      authCookie = fs.readFileSync('.skillsmp_cookie', 'utf8').trim();
      console.log(`  → 已加载Cookie (${authCookie.length} 字符)`);
    } catch (e) {
      console.log(`  → 未找到Cookie文件，将使用未登录模式`);
    }
    
    // 确定当前小时要学习的类别
    let targetCategory;
    if (hour % 2 === 0) {
      targetCategory = 'video_image';
      categoryName = '🎬 视频/图片';
    } else {
      const otherCats = [
        { key: 'content', name: '✍️ 内容创作' },
        { key: 'automation', name: '⚙️ 自动化' },
        { key: 'data', name: '📊 数据分析' }
      ];
      const selected = otherCats[Math.floor(hour / 2) % 3];
      targetCategory = selected.key;
      categoryName = selected.name;
    }
    
    console.log(`  → 目标类别: ${categoryName}`);
    
    // 获取已学习技能列表
    const learnedSkills = getLearnedSkills();
    console.log(`  → 已学习技能数: ${learnedSkills.size}`);
    
    // 设置Cookie到页面（如果存在）
    if (authCookie) {
      // 解析Cookie字符串并设置
      const cookies = authCookie.split(';').map(c => {
        const [name, ...valueParts] = c.trim().split('=');
        return {
          name: name.trim(),
          value: valueParts.join('=').trim(),
          domain: 'skillsmp.com',
          path: '/'
        };
      }).filter(c => c.name && c.value);
      
      await page.setCookie(...cookies);
      console.log(`  → 已设置登录Cookie (${cookies.length} 个)`);
    }
    
    // 使用搜索获取更多技能
    const searchKeywords = ['ai', 'video', 'image', 'automation', 'data', 'write', 'code', 'bot', 'python', 'ml', 'nlp', 'vision'];
    const randomKeyword = searchKeywords[Math.floor(Math.random() * searchKeywords.length)];
    
    await page.goto(`https://skillsmp.com/zh?q=${encodeURIComponent(randomKeyword)}`, { 
      waitUntil: 'networkidle2', 
      timeout: 60000 
    });
    await new Promise(r => setTimeout(r, 3000));
    
    // 点击 AI 搜索按钮
    try {
      const hasAiSearch = await page.evaluate(() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        return buttons.some(b => b.textContent.includes('AI') && b.textContent.includes('搜索'));
      });
      
      if (hasAiSearch) {
        await page.evaluate(() => {
          const btn = Array.from(document.querySelectorAll('button')).find(b => 
            b.textContent.includes('AI') && b.textContent.includes('搜索')
          );
          if (btn) btn.click();
        });
        console.log(`  → 点击 AI 搜索按钮...`);
        await new Promise(r => setTimeout(r, 8000));
      }
    } catch (e) {}
    
    // 关闭可能的登录弹窗
    try {
      const cancelExists = await page.evaluate(() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        return buttons.some(b => b.textContent.toLowerCase().includes('cancel'));
      });
      if (cancelExists) {
        await page.evaluate(() => {
          const btn = Array.from(document.querySelectorAll('button')).find(b => 
            b.textContent.toLowerCase().includes('cancel')
          );
          if (btn) btn.click();
        });
        await new Promise(r => setTimeout(r, 1000));
      }
    } catch (e) {}
    
    // 滚动加载更多技能
    console.log(`  → 滚动加载更多技能 (搜索: ${randomKeyword})...`);
    let allSkillLinks = new Set();
    let previousHeight = 0;
    let noChangeCount = 0;
    
    for (let i = 0; i < 20; i++) {
      // 获取当前技能链接
      const skills = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('a[href*="/skills/"]'))
          .map(a => ({
            href: a.href,
            text: a.innerText?.substring(0, 200) || ''
          }))
          .filter(s => !s.href.includes('facebook'));
      });
      
      skills.forEach(s => allSkillLinks.add(JSON.stringify(s)));
      console.log(`    滚动 ${i+1}/20, 累计找到 ${allSkillLinks.size} 个技能`);
      
      // 检查是否还有新内容
      const currentHeight = await page.evaluate(() => document.body.scrollHeight);
      if (currentHeight === previousHeight) {
        noChangeCount++;
        if (noChangeCount >= 3) break;
      } else {
        noChangeCount = 0;
        previousHeight = currentHeight;
      }
      
      // 滚动到底部
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await new Promise(r => setTimeout(r, 2500));
    }
    
    console.log(`  → 搜索 "${randomKeyword}" 共找到 ${allSkillLinks.size} 个技能`);
    
    // 解析技能数据
    const skills = Array.from(allSkillLinks).map(s => {
      const skill = JSON.parse(s);
      const match = skill.href.match(/\/skills\/(.+?)(?:\?|$)/);
      const skillPath = match ? match[1] : '';
      const lines = skill.text.split('\n').map(l => l.trim()).filter(l => l);
      
      let name = skillPath.replace('.md', '').replace(/-/g, ' ');
      let stars = '';
      
      for (const line of lines) {
        if (/^\d+\.?\d*k$/i.test(line)) {
          stars = line;
        } else if (line.length > 3 && line.length < 60 && !stars) {
          name = line;
        }
      }
      
      return {
        name: name,
        path: skillPath,
        link: skill.href,
        stars: stars,
        description: '',
        fullText: skill.text
      };
    });
    
    console.log(`  → 页面共找到 ${skills.length} 个技能`);
    
    // 分类并过滤已学习的技能
    const categorizedSkills = skills.map(s => ({
      ...s,
      category: categorizeSkill(s.name, s.description)
    }));
    
    // 筛选目标类别且未学习的技能
    const availableSkills = categorizedSkills.filter(s => {
      if (s.category !== targetCategory) return false;
      const skillKey = s.name.toLowerCase().replace(/\s+/g, '-').replace('.md', '');
      const pathKey = s.path.toLowerCase().replace('.md', '');
      return !learnedSkills.has(s.name.toLowerCase()) && 
             !learnedSkills.has(skillKey) && 
             !learnedSkills.has(pathKey);
    });
    
    console.log(`  → 目标类别可用技能: ${availableSkills.length} 个`);
    
    // 如果有可用技能，选择热度最高的
    if (availableSkills.length > 0) {
      bestSkill = availableSkills.sort((a, b) => {
        const getValue = (s) => {
          const match = s.stars?.match(/([\d.]+)k/i);
          return match ? parseFloat(match[1]) : 0;
        };
        return getValue(b) - getValue(a);
      })[0];
      
      console.log(`  → 选择学习: ${bestSkill.name} (${bestSkill.stars || '热度未知'})`);
      
      // 访问技能详情页
      await page.goto(bestSkill.link, { waitUntil: 'networkidle2', timeout: 60000 });
      await new Promise(r => setTimeout(r, 6000));
      
      // 获取详情页内容
      skillDetails = await page.evaluate(() => {
        const title = document.querySelector('h1')?.innerText?.trim() || '';
        let description = '';
        const selectors = ['.prose', '[class*="content"]', '[class*="description"]', 'article', 'main'];
        for (const sel of selectors) {
          const el = document.querySelector(sel);
          if (el) {
            description = el.innerText?.substring(0, 1000) || '';
            if (description.length > 100) break;
          }
        }
        if (description.length < 100) {
          description = document.body.innerText?.substring(0, 1000) || '';
        }
        return description;
      });
      
      console.log(`  → 学习完成 (${skillDetails.length} 字符内容)`);
      
    } else {
      // 如果没有找到目标类别的技能，尝试其他类别
      console.log(`  → 目标类别技能不足，尝试其他类别...`);
      
      const otherSkills = categorizedSkills.filter(s => {
        const skillKey = s.name.toLowerCase().replace(/\s+/g, '-').replace('.md', '');
        const pathKey = s.path.toLowerCase().replace('.md', '');
        return !learnedSkills.has(s.name.toLowerCase()) && 
               !learnedSkills.has(skillKey) && 
               !learnedSkills.has(pathKey);
      });
      
      if (otherSkills.length > 0) {
        bestSkill = otherSkills.sort((a, b) => {
          const getValue = (s) => {
            const match = s.stars?.match(/([\d.]+)k/i);
            return match ? parseFloat(match[1]) : 0;
          };
          return getValue(b) - getValue(a);
        })[0];
        
        categoryName = '📦 其他';
        console.log(`  → 选择学习: ${bestSkill.name} (${bestSkill.stars || '热度未知'})`);
      } else {
        console.log(`  ⚠️ 所有技能都已学习过`);
      }
    }
    
  } catch (error) {
    console.error(`  ✗ 错误: ${error.message}`);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
  
  // 记录学习结果
  try {
    const logEntry = {
      timestamp: now.toISOString(),
      hour: hour,
      category: categoryName,
      skillLearned: bestSkill || { name: '未找到新技能', stars: '-', link: '', path: '' },
      details: skillDetails.substring(0, 800)
    };
    
    // 保存到JSON日志
    const logPath = path.join(process.env.HOME, '.openclaw/workspace/skills-learning-log.json');
    let logs = [];
    if (fs.existsSync(logPath)) {
      logs = JSON.parse(fs.readFileSync(logPath, 'utf8'));
    }
    logs.push(logEntry);
    fs.writeFileSync(logPath, JSON.stringify(logs, null, 2));
    
    // 更新学习计划文件
    const planPath = path.join(process.env.HOME, '.openclaw/workspace/skills-learning-plan.md');
    if (fs.existsSync(planPath) && bestSkill) {
      let plan = fs.readFileSync(planPath, 'utf8');
      
      const skillName = bestSkill.name || '未找到';
      const skillStars = bestSkill.stars || '-';
      const newRow = `| ${hour}:00 | ${skillName} | ${categoryName} | ✓ 已学习 | 热度:${skillStars} |\n`;
      
      // 查找今日学习进度表格并添加新行
      const tableHeader = '## 今日学习进度';
      
      if (plan.includes(tableHeader)) {
        const lines = plan.split('\n');
        const headerIndex = lines.findIndex(l => l.includes(tableHeader));
        
        if (headerIndex >= 0) {
          // 查找表格分隔行
          let insertIndex = -1;
          for (let i = headerIndex + 1; i < Math.min(headerIndex + 10, lines.length); i++) {
            if (lines[i].includes('|--')) {
              insertIndex = i + 1;
              break;
            }
          }
          
          // 检查是否已存在该小时的记录
          const hourExists = lines.some(l => l.includes(`| ${hour}:00 |`));
          
          if (insertIndex > 0 && !hourExists) {
            lines.splice(insertIndex, 0, newRow.trim());
            plan = lines.join('\n');
            fs.writeFileSync(planPath, plan);
            console.log(`  → 已更新学习计划`);
          }
        }
      }
    }
    
  } catch (err) {
    console.error(`  ✗ 记录失败: ${err.message}`);
  }
  
  // 最终汇报
  console.log(`\n╔════════════════════════════════════╗`);
  console.log(`║      📚 每小时技能学习汇报      ║`);
  console.log(`╠════════════════════════════════════╣`);
  console.log(`║ ⏰ 时间: ${String(hour).padStart(2, '0')}:00                      ║`);
  console.log(`║ 📂 类别: ${categoryName.padEnd(20)} ║`);
  if (bestSkill) {
    const name = bestSkill.name.substring(0, 20).padEnd(20);
    const stars = (bestSkill.stars || '-').padEnd(20);
    console.log(`║ 📚 技能: ${name} ║`);
    console.log(`║ ⭐ 热度: ${stars} ║`);
  } else {
    console.log(`║ 📚 技能: 未找到新技能${' '.repeat(10)} ║`);
  }
  console.log(`╚════════════════════════════════════╝\n`);
  
  console.log(`[${timeStr}] ✅ 学习周期完成\n`);
  
  // 发送飞书通知
  if (bestSkill && bestSkill.name !== '未找到新技能') {
    try {
      const messageText = `🎓 技能学习完成\n\n⏰ 时间: ${String(hour).padStart(2, '0')}:00\n📂 类别: ${categoryName}\n📚 技能: ${bestSkill.name}\n⭐ 热度: ${bestSkill.stars || '-'}\n\n学习笔记已更新到 skills-learning-plan.md`;
      
      execSync(`openclaw message send --channel feishu --target "ou_f17427a7518faa014659589d89db4d8b" --message "${messageText}"`, {
        stdio: 'pipe',
        timeout: 30000
      });
      console.log(`  → 已发送飞书通知`);
    } catch (e) {
      console.error(`  ✗ 发送通知失败: ${e.message}`);
    }
  }
}

learnSkill();
