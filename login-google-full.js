const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

const EMAIL = 'chauvgongza@gmail.com';
const PASSWORD = 'vqiakulid---Kerr31052@outlook.com';

async function completeGoogleLogin() {
  console.log('🚀 启动浏览器...');
  
  const browser = await puppeteer.launch({
    headless: false,
    args: [
      '--no-sandbox', 
      '--disable-setuid-sandbox',
      '--window-size=1280,800'
    ]
  });
  
  try {
    const pages = await browser.pages();
    const page = pages[0];
    await page.setViewport({ width: 1280, height: 800 });
    
    // 访问SkillsMP并点击Google登录
    console.log('📱 访问 SkillsMP...');
    await page.goto('https://skillsmp.com/zh', { waitUntil: 'networkidle2', timeout: 60000 });
    await new Promise(r => setTimeout(r, 3000));
    
    // 点击登录
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button, a')).find(b => 
        b.textContent.toLowerCase().includes('sign in')
      );
      if (btn) btn.click();
    });
    await new Promise(r => setTimeout(r, 3000));
    
    // 点击Google登录
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => 
        b.textContent.includes('Google')
      );
      if (btn) btn.click();
    });
    
    console.log('⏳ 等待Google登录页面...');
    await new Promise(r => setTimeout(r, 5000));
    
    // 获取所有页面，找到Google登录页
    const allPages = await browser.pages();
    console.log(`📑 共 ${allPages.length} 个页面`);
    
    let googlePage = allPages.find(p => p.url().includes('google.com'));
    
    if (!googlePage) {
      console.log('⚠️ 未找到Google登录页，使用当前页');
      googlePage = page;
    }
    
    console.log('✉️  填写Google邮箱...');
    await googlePage.waitForSelector('input[type="email"]', { timeout: 10000 });
    await googlePage.type('input[type="email"]', EMAIL, { delay: 50 });
    await new Promise(r => setTimeout(r, 1000));
    
    // 点击Next
    await googlePage.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => 
        b.textContent.includes('Next') || b.textContent.includes('下一步')
      );
      if (btn) btn.click();
    });
    
    console.log('⏳ 等待密码输入...');
    await new Promise(r => setTimeout(r, 3000));
    
    // 填写密码
    console.log('🔒 填写密码...');
    await googlePage.waitForSelector('input[type="password"]', { timeout: 10000 });
    await googlePage.type('input[type="password"]', PASSWORD, { delay: 50 });
    await new Promise(r => setTimeout(r, 1000));
    
    // 点击Next
    await googlePage.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => 
        b.textContent.includes('Next') || b.textContent.includes('下一步')
      );
      if (btn) btn.click();
    });
    
    console.log('⏳ 等待登录完成（可能有验证码）...');
    await new Promise(r => setTimeout(r, 10000));
    
    // 截图检查
    await page.screenshot({ path: 'after_google_login.png' });
    console.log('📸 截图: after_google_login.png');
    
    // 保存cookies
    const cookies = await page.cookies();
    fs.writeFileSync('.skillsmp_session.json', JSON.stringify(cookies, null, 2));
    console.log(`💾 已保存 ${cookies.length} 个cookies`);
    
    // 获取技能
    const skills = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('a[href*="/skills/"]'))
        .filter(a => !a.href.includes('facebook'))
        .map(a => ({
          href: a.href,
          name: a.innerText?.split('\n')[0]?.trim() || 'Unknown'
        }));
    });
    
    console.log(`\n✅ 找到 ${skills.length} 个技能！`);
    
    if (skills.length > 0) {
      fs.writeFileSync('.skillsmp_all_skills.json', JSON.stringify(skills, null, 2));
      console.log('💾 已保存技能列表');
    }
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    await page.screenshot({ path: 'error.png' });
  }
  
  await browser.close();
  console.log('\n✅ 完成！');
}

completeGoogleLogin();
