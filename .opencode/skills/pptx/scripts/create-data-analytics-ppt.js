const fs = require('fs');
const path = require('path');
const html2pptx = require('./html2pptx.js');
const pptxgenjs = require('pptxgenjs');

async function createPresentation() {
  console.log('🎨 开始创建 Data-Analytics 技能汇报 PPT...');

  // Create presentation
  const pptx = new pptxgenjs();
  pptx.layout = 'LAYOUT_16x9';
  pptx.title = 'Data-Analytics 技能汇报';
  pptx.author = '技能中心';

  // Read HTML file
  const htmlFile = path.join(__dirname, '..', '..', '..', '..', 'workspace', 'data-analytics-presentation.html');
  
  // Process HTML file
  console.log('⏳ 处理 HTML 幻灯片...');
  const { slide, placeholders } = await html2pptx(htmlFile, pptx);

  // Save presentation
  const outputPath = path.join(__dirname, '..', '..', '..', '..', 'workspace', 'Data-Analytics 技能汇报.pptx');
  await pptx.writeFile({ 
    fileName: 'Data-Analytics 技能汇报.pptx'
  });

  console.log(`✅ PPT 创建完成：${outputPath}`);
}

createPresentation().catch(console.error);
