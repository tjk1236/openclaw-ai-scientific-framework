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
  
  await page.screenshot({ path: 'skillsmp_stealth.png', fullPage: true });
  
  const title = await page.title();
  console.log('页面标题:', title);
  
  const skills = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('a[href*="/skills/"]'))
      .map(a => a.href)
      .filter((v, i, a) => a.indexOf(v) === i);
  });
  
  console.log('找到技能数:', skills.length);
  console.log(skills.slice(0, 10));
  
  await browser.close();
}

test();
