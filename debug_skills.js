const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
puppeteer.use(StealthPlugin());

async function debug() {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  
  // 读取Cookie
  let authCookie = fs.readFileSync('.skillsmp_cookie', 'utf8').trim();
  
  // 设置Cookie
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
  console.log(`设置了 ${cookies.length} 个Cookie`);
  
  // 访问搜索页面
  await page.goto('https://skillsmp.com/zh?q=ai', { 
    waitUntil: 'networkidle2', 
    timeout: 60000 
  });
  await new Promise(r => setTimeout(r, 5000));
  
  // 截图
  await page.screenshot({ path: 'debug_search.png', fullPage: false });
  console.log('截图已保存: debug_search.png');
  
  // 检查技能链接
  const skills = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('a[href*="/skills/"]'))
      .filter(a => !a.href.includes('facebook'))
      .map(a => ({ href: a.href, text: a.innerText?.substring(0, 50) }));
  });
  console.log(`找到 ${skills.length} 个技能`);
  console.log(skills.slice(0, 5));
  
  await browser.close();
}

debug();
