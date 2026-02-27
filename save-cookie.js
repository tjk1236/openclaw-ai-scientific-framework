// 保存Cookie到文件
const fs = require('fs');

const cookie = process.argv[2];
if (!cookie) {
  console.error('请提供Cookie作为参数');
  process.exit(1);
}

fs.writeFileSync('.skillsmp_cookie', cookie);
console.log('Cookie已保存到 .skillsmp_cookie');