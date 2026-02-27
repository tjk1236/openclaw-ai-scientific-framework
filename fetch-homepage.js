const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

async function fetchAllSkills() {
  console.log('🚀 启动浏览器...');
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox', 
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--window-size=1280,800'
    ]
  });
  
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    // 加载之前保存的cookies
    if (fs.existsSync('.skillsmp_session.json')) {
      const cookies = JSON.parse(fs.readFileSync('.skillsmp_session.json', 'utf8'));
      await page.setCookie(...cookies);
      console.log(`📂 已加载 ${cookies.length} 个cookies`);
    }
    
    // 访问首页
    console.log('🔍 访问首页...');
    await page.goto('https://skillsmp.com/zh', { 
      waitUntil: 'networkidle2', 
      timeout: 60000 
    });
    await new Promise(r => setTimeout(r, 5000));
    
    // 滚动加载所有技能
    console.log('📜 滚动加载技能...');
    let allSkills = [];
    let previousCount = 0;
    let noChangeCount = 0;
    
    for (let i = 0; i < 50; i++) {
      // 获取当前技能
      const skills = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('a[href*="/skills/"]'))
          .filter(a => !a.href.includes('facebook') && !a.href.includes('example'))
          .map(a => ({
            href: a.href,
            name: a.innerText?.split('\n')[0]?.trim() || 'Unknown',
            stars: (a.innerText?.match(/(\d+\.?\d*k)/) || [''])[0],
            fullText: a.innerText?.substring(0, 200) || ''
          }));
      });
      
      // 去重
      const seen = new Set();
      const uniqueSkills = [];
      for (const s of skills) {
        if (!seen.has(s.href)) {
          seen.add(s.href);
          uniqueSkills.push(s);
        }
      }
      
      allSkills = uniqueSkills;
      console.log(`  滚动 ${i+1}/50: 找到 ${allSkills.length} 个技能`);
      
      // 检查是否有新内容
      if (allSkills.length === previousCount) {
        noChangeCount++;
        if (noChangeCount >= 5) break;
      } else {
        noChangeCount = 0;
        previousCount = allSkills.length;
      }
      
      // 滚动到底部
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await new Promise(r => setTimeout(r, 3000));
    }
    
    console.log(`\n✅ 共找到 ${allSkills.length} 个技能！`);
    
    // 保存技能列表
    fs.writeFileSync('.skillsmp_all_skills.json', JSON.stringify(allSkills, null, 2));
    console.log(`💾 已保存到 .skillsmp_all_skills.json`);
    
    // 显示前20个
    console.log('\n前20个技能:');
    allSkills.slice(0, 20).forEach((s, i) => {
      console.log(`  ${i+1}. ${s.name} ${s.stars ? '(' + s.stars + ')' : ''}`);
    });
    
    await page.screenshot({ path: 'skills_homepage.png', fullPage: true });
    console.log('\n📸 截图已保存: skills_homepage.png');
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
  }
  
  await browser.close();
  console.log('\n✅ 完成！');
}

fetchAllSkills();
