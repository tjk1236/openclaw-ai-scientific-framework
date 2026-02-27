const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

async function loginWithGoogle() {
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
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    // 访问首页
    console.log('📱 访问 SkillsMP...');
    await page.goto('https://skillsmp.com/zh', { 
      waitUntil: 'networkidle2', 
      timeout: 60000 
    });
    await new Promise(r => setTimeout(r, 3000));
    
    // 点击登录按钮
    console.log('🔘 点击登录按钮...');
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button, a')).find(b => 
        b.textContent.toLowerCase().includes('sign in')
      );
      if (btn) btn.click();
    });
    
    await new Promise(r => setTimeout(r, 3000));
    
    // 点击"Continue with Google"
    console.log('🔘 点击 Continue with Google...');
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => 
        b.textContent.includes('Google')
      );
      if (btn) btn.click();
    });
    
    console.log('⏳ 等待Google登录页面...');
    await new Promise(r => setTimeout(r, 5000));
    
    // 检查是否打开了新窗口（Google登录）
    const pages = await browser.pages();
    console.log(`📑 当前有 ${pages.length} 个页面`);
    
    // 截图
    await page.screenshot({ path: 'google_login.png' });
    console.log('📸 截图: google_login.png');
    
    // 由于Google登录可能有验证码/2FA，这里暂停让用户手动处理
    console.log('\n⚠️  请手动完成Google登录（如果有验证码请处理）');
    console.log('⏳ 等待30秒...');
    
    await new Promise(r => setTimeout(r, 30000));
    
    // 保存cookies
    const cookies = await page.cookies();
    fs.writeFileSync('.skillsmp_session.json', JSON.stringify(cookies, null, 2));
    console.log(`💾 已保存 ${cookies.length} 个cookies`);
    
    // 尝试获取技能
    const skills = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('a[href*="/skills/"]'))
        .filter(a => !a.href.includes('facebook'))
        .map(a => ({
          href: a.href,
          name: a.innerText?.split('\n')[0]?.trim() || 'Unknown'
        }));
    });
    
    console.log(`\n找到 ${skills.length} 个技能`);
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
  }
  
  console.log('\n⏳ 保持浏览器打开，请手动检查...');
  console.log('完成后按 Ctrl+C 关闭');
  
  // 保持运行
  await new Promise(() => {});
}

loginWithGoogle();
