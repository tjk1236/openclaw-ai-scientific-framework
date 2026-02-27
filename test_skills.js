const puppeteer = require('puppeteer');

async function test() {
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  await page.goto('https://skillsmp.com/zh', { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 5000));
  
  // 关闭登录弹窗
  try {
    const cancelBtn = await page.$('button:has-text("Cancel")');
    if (cancelBtn) await cancelBtn.click();
  } catch(e){}
  
  await new Promise(r => setTimeout(r, 2000));
  
  // 截图
  await page.screenshot({ path: 'skillsmp_home.png', fullPage: true });
  console.log('截图已保存: skillsmp_home.png');
  
  // 获取页面所有链接
  const links = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('a'))
      .filter(a => a.href.includes('/skills/'))
      .map(a => ({ href: a.href, text: a.innerText?.substring(0, 50) }));
  });
  
  console.log('找到的技能链接:', links.length);
  console.log(links.slice(0, 10));
  
  await browser.close();
}

test();
