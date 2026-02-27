const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

const EMAIL = 'chauvgongza@gmail.com';
const PASSWORD = 'vqiakulid---Kerr31052@outlook.com';

async function autoLogin() {
  console.log('🚀 启动无头浏览器...');
  
  const browser = await puppeteer.launch({
    headless: 'new', // 新版无头模式
    args: [
      '--no-sandbox', 
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--disable-gpu',
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
    
    // 检查是否已经登录
    const isLoggedIn = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('button, a'));
      return buttons.some(b => 
        b.textContent.toLowerCase().includes('sign out') ||
        b.textContent.toLowerCase().includes('退出')
      );
    });
    
    if (isLoggedIn) {
      console.log('✅ 已经登录！');
    } else {
      console.log('🔘 尝试自动登录...');
      
      // 点击登录按钮
      await page.evaluate(() => {
        const btn = Array.from(document.querySelectorAll('button, a')).find(b => 
          b.textContent.toLowerCase().includes('sign in')
        );
        if (btn) {
          btn.click();
          return true;
        }
        return false;
      });
      
      await new Promise(r => setTimeout(r, 3000));
      
      // 填写邮箱和密码
      try {
        await page.waitForSelector('input[type="email"], input[name="email"]', { timeout: 10000 });
        
        console.log('✉️  填写邮箱...');
        await page.type('input[type="email"], input[name="email"]', EMAIL, { delay: 30 });
        
        console.log('🔒 填写密码...');
        await page.type('input[type="password"], input[name="password"]', PASSWORD, { delay: 30 });
        
        console.log('🔘 点击登录...');
        await page.evaluate(() => {
          const btn = Array.from(document.querySelectorAll('button')).find(b => 
            b.textContent.toLowerCase().includes('sign in')
          );
          if (btn) btn.click();
        });
        
        // 等待登录成功
        await page.waitForFunction(() => {
          const buttons = Array.from(document.querySelectorAll('button, a'));
          return buttons.some(b => 
            b.textContent.toLowerCase().includes('sign out') ||
            b.textContent.toLowerCase().includes('退出')
          );
        }, { timeout: 30000 });
        
        console.log('✅ 登录成功！');
      } catch (e) {
        console.log('⚠️  登录过程出错:', e.message);
      }
    }
    
    // 保存所有cookies
    const cookies = await page.cookies();
    fs.writeFileSync('.skillsmp_session.json', JSON.stringify(cookies, null, 2));
    console.log(`💾 已保存 ${cookies.length} 个cookies`);
    
    // 保存为Netscape格式（供其他工具使用）
    const cookieStr = cookies.map(c => `${c.name}=${c.value}`).join('; ');
    fs.writeFileSync('.skillsmp_cookie', cookieStr);
    console.log('💾 Cookie字符串已保存');
    
    // 测试搜索
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
          name: a.innerText?.split('\n')[0]?.substring(0, 50) || 'Unknown'
        }));
    });
    
    console.log(`✅ 找到 ${skills.length} 个技能！`);
    
    if (skills.length > 0) {
      console.log('\n前5个技能:');
      skills.slice(0, 5).forEach((s, i) => {
        console.log(`  ${i+1}. ${s.name}`);
      });
      
      // 保存技能列表
      fs.writeFileSync('.skillsmp_all_skills.json', JSON.stringify(skills, null, 2));
      console.log(`\n💾 已保存 ${skills.length} 个技能到 .skillsmp_all_skills.json`);
    } else {
      console.log('⚠️  未找到技能，可能需要手动处理验证码');
      await page.screenshot({ path: 'login_error.png' });
      console.log('📸 截图已保存: login_error.png');
    }
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    try {
      await page.screenshot({ path: 'error.png' });
      console.log('📸 错误截图: error.png');
    } catch(e) {}
  }
  
  await browser.close();
  console.log('\n✅ 完成！');
}

autoLogin();
