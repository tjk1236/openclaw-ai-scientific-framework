const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

async function test() {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.goto('https://skillsmp.com/zh', { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 5000));
  
  // 关闭登录弹窗
  try {
    const cancel = await page.$('button:has-text("Cancel")');
    if (cancel) await cancel.click();
  } catch(e){}
  await new Promise(r => setTimeout(r, 2000));
  
  // 获取总技能数
  const totalText = await page.evaluate(() => {
    const el = document.querySelector('[class*="metric"]');
    return el ? el.innerText : 'N/A';
  });
  console.log('总技能数:', totalText);
  
  // 滚动多次加载更多
  let allSkills = new Set();
  for (let i = 0; i < 5; i++) {
    const skills = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('a[href*="/skills/"]'))
        .map(a => a.href)
        .filter(h => !h.includes('facebook'));
    });
    skills.forEach(s => allSkills.add(s));
    console.log(`滚动 ${i+1}/5, 当前找到 ${allSkills.size} 个技能`);
    
    // 滚动到底部
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await new Promise(r => setTimeout(r, 3000));
  }
  
  console.log('最终技能数:', allSkills.size);
  console.log(Array.from(allSkills).slice(0, 10));
  
  await browser.close();
}

test();
