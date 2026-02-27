const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

puppeteer.use(StealthPlugin());

const EMAIL = 'chauvgongza@gmail.com';
const PASSWORD = 'vqiakulid---Kerr31052@outlook.com';

async function loginAndFetch() {
  console.log('🚀 启动虚拟显示...');
  
  // 使用xvfb-run启动浏览器
  const { spawn } = require('child_process');
  
  const browser = await puppeteer.launch({
    headless: false, // 非无头，使用xvfb
    args: [
      '--no-sandbox', 
      '--disable-setuid-sandbox',
      '--window-size=1280,800'
    ],
    executablePath: '/usr/bin/google-chrome'
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
    
    // 截图检查状态
    await page.screenshot({ path: 'step1_home.png' });
    console.log('📸 首页截图: step1_home.png');
    
    // 点击登录按钮
    console.log('🔘 点击登录按钮...');
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button, a')).find(b => 
        b.textContent.toLowerCase().includes('sign in')
      );
      if (btn) btn.click();
    });
    
    await new Promise(r => setTimeout(r, 3000));
    await page.screenshot({ path: 'step2_login_form.png' });
    console.log('📸 登录表单截图: step2_login_form.png');
    
    // 填写邮箱和密码
    console.log('✉️  填写邮箱...');
    const emailInput = await page.$('input[type="email"], input[name="email"]');
    if (emailInput) {
      await emailInput.type(EMAIL, { delay: 50 });
    }
    
    console.log('🔒 填写密码...');
    const passwordInput = await page.$('input[type="password"], input[name="password"]');
    if (passwordInput) {
      await passwordInput.type(PASSWORD, { delay: 50 });
    }
    
    await new Promise(r => setTimeout(r, 1000));
    await page.screenshot({ path: 'step3_filled.png' });
    console.log('📸 填写完成截图: step3_filled.png');
    
    // 点击登录
    console.log('🔘 点击登录...');
    await page.evaluate(() => {
      const btn = Array.from(document.querySelectorAll('button')).find(b => 
        b.textContent.toLowerCase().includes('sign in')
      );
      if (btn) btn.click();
    });
    
    // 等待登录成功
    console.log('⏳ 等待登录成功...');
    await new Promise(r => setTimeout(r, 5000));
    await page.screenshot({ path: 'step4_logged_in.png' });
    console.log('📸 登录后截图: step4_logged_in.png');
    
    // 保存cookies
    const cookies = await page.cookies();
    fs.writeFileSync('.skillsmp_session.json', JSON.stringify(cookies, null, 2));
    console.log(`💾 已保存 ${cookies.length} 个cookies`);
    
    // 滚动加载所有技能
    console.log('📜 滚动加载技能...');
    let allSkills = [];
    let previousCount = 0;
    let noChangeCount = 0;
    
    for (let i = 0; i < 100; i++) {
      const skills = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('a[href*="/skills/"]'))
          .filter(a => !a.href.includes('facebook') && !a.href.includes('example'))
          .map(a => ({
            href: a.href,
            name: a.innerText?.split('\n')[0]?.trim() || 'Unknown',
            stars: (a.innerText?.match(/(\d+\.?\d*k)/) || [''])[0]
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
      console.log(`  滚动 ${i+1}/100: ${allSkills.length} 个技能`);
      
      if (allSkills.length === previousCount) {
        noChangeCount++;
        if (noChangeCount >= 5) break;
      } else {
        noChangeCount = 0;
        previousCount = allSkills.length;
      }
      
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await new Promise(r => setTimeout(r, 3000));
    }
    
    console.log(`\n✅ 共找到 ${allSkills.length} 个技能！`);
    fs.writeFileSync('.skillsmp_all_skills.json', JSON.stringify(allSkills, null, 2));
    
    // 显示前20个
    console.log('\n前20个技能:');
    allSkills.slice(0, 20).forEach((s, i) => {
      console.log(`  ${i+1}. ${s.name} ${s.stars ? '(' + s.stars + ')' : ''}`);
    });
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    await page.screenshot({ path: 'error.png' });
  }
  
  await browser.close();
  console.log('\n✅ 完成！');
}

loginAndFetch();
