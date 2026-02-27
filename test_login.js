const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

async function test() {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  
  // 访问首页
  await page.goto('https://skillsmp.com/zh', { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 3000));
  
  // 截图查看页面
  await page.screenshot({ path: 'test_home.png', fullPage: false });
  console.log('首页截图已保存: test_home.png');
  
  // 检查是否有登录按钮
  const hasLogin = await page.evaluate(() => {
    const buttons = Array.from(document.querySelectorAll('button, a'));
    const loginBtn = buttons.find(b => b.textContent.toLowerCase().includes('sign in'));
    return loginBtn ? loginBtn.textContent : '未找到';
  });
  console.log('登录按钮:', hasLogin);
  
  // 尝试访问搜索页面
  await page.goto('https://skillsmp.com/zh?q=ai', { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 5000));
  
  await page.screenshot({ path: 'test_search.png', fullPage: false });
  console.log('搜索页截图已保存: test_search.png');
  
  // 检查技能链接
  const skills = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('a[href*="/skills/"]'))
      .filter(a => !a.href.includes('facebook'))
      .map(a => ({ href: a.href, text: a.innerText?.substring(0, 50) }));
  });
  console.log('找到技能数:', skills.length);
  console.log(skills.slice(0, 5));
  
  await browser.close();
}

test();
