const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
const path = require('path');

// 使用stealth插件绕过检测
puppeteer.use(StealthPlugin());

const EMAIL = 'chauvgongza@gmail.com';
const PASSWORD = 'vqiakulid---Kerr31052@outlook.com';

async function loginAndSaveSession() {
  console.log('🚀 启动浏览器...');
  
  const browser = await puppeteer.launch({
    headless: false, // 非无头模式，可以看到浏览器窗口
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1280,800'],
    slowMo: 100 // 放慢操作速度，便于观察
  });
  
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    // 访问首页
    console.log('📱 访问 SkillsMP...');
    await page.goto('https://skillsmp.com/zh', { 
      waitUntil: 'networkidle2', 
      timeout: 60000 
    });
    
    // 等待登录按钮出现
    console.log('⏳ 等待登录按钮...');
    await page.waitForFunction(() => {
      const buttons = Array.from(document.querySelectorAll('button, a'));
      return buttons.some(b => b.textContent.toLowerCase().includes('sign in'));
    }, { timeout: 10000 });
    
    // 点击登录按钮
    console.log('🔘 点击登录按钮...');
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button, a')).find(b => 
        b.textContent.toLowerCase().includes('sign in')
      );
      if (btn) btn.click();
    });
    
    // 等待登录表单
    console.log('⏳ 等待登录表单...');
    await page.waitForSelector('input[type="email"], input[name="email"]', { timeout: 10000 });
    
    // 填写邮箱
    console.log('✉️  填写邮箱...');
    const emailInput = await page.$('input[type="email"], input[name="email"]');
    await emailInput.type(EMAIL, { delay: 50 });
    
    // 填写密码
    console.log('🔒 填写密码...');
    const passwordInput = await page.$('input[type="password"], input[name="password"]');
    await passwordInput.type(PASSWORD, { delay: 50 });
    
    // 点击登录
    console.log('🔘 点击登录...');
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => 
        b.textContent.toLowerCase().includes('sign in')
      );
      if (btn) btn.click();
    });
    
    // 等待登录成功（检测是否有用户头像或登出按钮）
    console.log('⏳ 等待登录成功...');
    await page.waitForFunction(() => {
      // 检测是否已登录（找用户菜单或退出按钮）
      const buttons = Array.from(document.querySelectorAll('button, a'));
      return buttons.some(b => 
        b.textContent.toLowerCase().includes('sign out') ||
        b.textContent.toLowerCase().includes('退出') ||
        document.querySelector('[class*="avatar"]') !== null
      );
    }, { timeout: 30000 });
    
    console.log('✅ 登录成功！');
    
    // 保存cookies
    const cookies = await page.cookies();
    fs.writeFileSync('.skillsmp_session.json', JSON.stringify(cookies, null, 2));
    console.log(`💾 已保存 ${cookies.length} 个 cookies 到 .skillsmp_session.json`);
    
    // 截图确认
    await page.screenshot({ path: 'login_success.png' });
    console.log('📸 截图已保存: login_success.png');
    
    // 访问搜索页面测试
    console.log('🔍 测试搜索页面...');
    await page.goto('https://skillsmp.com/zh?q=ai', { 
      waitUntil: 'networkidle2', 
      timeout: 60000 
    });
    await new Promise(r => setTimeout(r, 5000));
    
    // 获取技能列表
    const skills = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('a[href*="/skills/"]'))
        .filter(a => !a.href.includes('facebook'))
        .map(a => ({
          href: a.href,
          name: a.innerText?.split('\n')[0]?.substring(0, 50)
        }));
    });
    
    console.log(`✅ 找到 ${skills.length} 个技能`);
    console.log(skills.slice(0, 5));
    
    await page.screenshot({ path: 'search_result.png' });
    console.log('📸 搜索结果截图: search_result.png');
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    await page.screenshot({ path: 'error.png' });
  }
  
  // 保持浏览器打开，让用户可以看到
  console.log('\n⚠️  浏览器保持打开状态，请手动关闭或按 Ctrl+C');
  console.log('完成后，请运行: node learn-skill.js');
}

loginAndSaveSession();
