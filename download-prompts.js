const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const PROMPTS_DIR = '/home/zzyuzhangxing/.openclaw/workspace/prompts/video';

// 文件清单 (从飞书Wiki获取)
const files = [
  { name: '超强自定义角色生成.json', token: 'S4Vsb4flBozyVAxKKW1cIzzkngd' },
  { name: '全能动作导演 Pro (15s 动作续航版).txt', token: 'Cb8fb78IKoN3Hlxjo3JcdRxInXc' },
  { name: '3x3分镜提示词模板系统_v5_台词声线版_修改版.md', token: 'ZO3xbM7EGogZsvxuV14cxPeln8N' },
  { name: '爆款开头.txt', token: 'Pe4LbkfnfoRdtax9PetcCkqon2b' },
  { name: '短剧名字和简介生成.txt', token: 'SE9HbO27poOTloxAxYWcBaf6ndb' },
  { name: '分镜-1214.txt', token: 'N6IRbr1ouorJrxxpHzwcP4wWnwc' },
  { name: '分镜-测试版.txt', token: 'Ppk8bIChLoqDf9xvjjFchOeNnSY' },
  { name: '分镜-多人对话-10条输出.txt', token: 'Pu2NboPN8oM0kexGfrpcESXhneh' },
  { name: '分镜-多人对话-30条输出版本.txt', token: 'GQXTb5awNoMxorxyPOucPIdjnic' },
  { name: '分镜正式版.txt', token: 'RNmkbEkaDoOakKxe0RWctjVbn8f' },
  { name: '分析图片提取参考词.txt', token: 'Nha3bjLzAovYIQxTiDzcFuAvnHf' },
  { name: '角色表-1214.txt', token: 'N9KEbUdLhoPRlax0MSYcJb2gnHb' },
  { name: '角色生成-测试版.txt', token: 'MdvPbji8UoYkZMxcBmScjWBVnTg' },
  { name: '剧本-1214.txt', token: 'L8CBb7h7OoEQ1exBPptcojGRnmh' },
  { name: '剧本-测试版.txt', token: 'M64abpijfo4PFBx1SEIcHgrOnSg' }
];

async function downloadPrompts() {
  console.log('开始下载视频提示词文件...\n');
  
  // 确保目录存在
  if (!fs.existsSync(PROMPTS_DIR)) {
    fs.mkdirSync(PROMPTS_DIR, { recursive: true });
  }
  
  // 创建清单文件
  const manifest = {
    download_time: new Date().toISOString(),
    total_files: files.length,
    files: files.map(f => ({
      name: f.name,
      token: f.token,
      status: 'pending'
    }))
  };
  
  fs.writeFileSync(
    path.join(PROMPTS_DIR, 'manifest.json'),
    JSON.stringify(manifest, null, 2)
  );
  
  console.log(`✓ 已创建清单文件 (${files.length} 个文件)`);
  console.log(`✓ 保存位置: ${PROMPTS_DIR}\n`);
  
  console.log('文件清单:');
  files.forEach((f, i) => {
    console.log(`  ${i + 1}. ${f.name}`);
  });
  
  console.log('\n注意: 由于飞书API限制，文件需要手动下载或通过微信分享导出。');
  console.log('清单已保存，请手动下载后放到上述目录。\n');
}

downloadPrompts();
