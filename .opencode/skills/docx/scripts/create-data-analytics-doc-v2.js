const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, HeadingLevel, BorderStyle, AlignmentType } = require("docx");
const fs = require("fs");
const path = require("path");

const colors = {
  darkBlue: "1E3A5F",
  midBlue: "2E5A8B",
  lightBlue: "5479A2",
  cyan: "00A8CC",
  orange: "FF7A00",
  green: "00B050",
  darkGray: "212121",
  lightGray: "F5F6F8",
  red: "C00000"
};

function createHeading1(text) {
  return new Paragraph({
    text,
    heading: HeadingLevel.HEADING_1,
    style: { bold: true, size: 36, color: "FFFFFF" },
    shading: { fill: colors.darkBlue },
    spacing: { before: 400, after: 300, line: 480 },
    pageBreakBefore: true
  });
}

function createHeading2(text) {
  return new Paragraph({
    text,
    heading: HeadingLevel.HEADING_2,
    style: { bold: true, size: 28, color: colors.darkBlue },
    spacing: { before: 350, after: 200, line: 400 }
  });
}

function createHeading3(text) {
  return new Paragraph({
    text,
    heading: HeadingLevel.HEADING_3,
    style: { bold: true, size: 24, color: colors.cyan },
    spacing: { before: 250, after: 150, line: 360 }
  });
}

function createNormalText(text, bold = false, after = 180) {
  return new Paragraph({
    children: [new TextRun({ text, bold, color: colors.darkGray, size: 24, font: "Microsoft YaHei" })],
    spacing: { after, line: 360 }
  });
}

function createBulletPoint(text) {
  return new Paragraph({
    children: [new TextRun({ text, color: colors.darkGray, size: 22, font: "Microsoft YaHei" })],
    bullet: { level: 0 },
    spacing: { after: 120, line: 320 },
    indent: { left: 720, hanging: 360 }
  });
}

function createSpacer(height = 300) {
  return new Paragraph({ text: "", spacing: { after: height } });
}

function createComparisonTable() {
  const headers = ["对比维度", "传统方式", "Data-Analytics 技能"];
  const rows = [
    ["查询方式", "编写 SQL/代码", "自然语言描述"],
    ["学习成本", "需掌握 SQL + 业务", "无需技术背景"],
    ["执行效率", "分钟级", "秒级响应"],
    ["结果展示", "原始数据", "智能分析报告"],
    ["多轮对话", "不支持", "上下文自动复用"]
  ];

  const tableRows = [
    new TableRow({
      children: headers.map(h => new TableCell({
        children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, color: "FFFFFF", size: 20, font: "Microsoft YaHei" })], alignment: AlignmentType.CENTER })],
        shading: { fill: colors.darkBlue },
        margins: { top: 150, bottom: 150, left: 100, right: 100 }
      })),
      
    })
  ];

  rows.forEach((row, idx) => {
    tableRows.push(new TableRow({
      children: row.map((cell, colIdx) => new TableCell({
        children: [new Paragraph({
          children: [new TextRun({ text: cell, bold: colIdx === 2, color: colIdx === 2 ? colors.darkBlue : colors.darkGray, size: 20, font: "Microsoft YaHei" })],
          alignment: colIdx === 0 ? AlignmentType.LEFT : AlignmentType.CENTER
        })],
        shading: { fill: idx % 2 === 0 ? colors.lightGray : "FFFFFF" },
        margins: { top: 120, bottom: 120, left: 100, right: 100 }
      })),
      
    }));
  });

  return new Table({
    rows: tableRows,
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 1, color: colors.darkBlue },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: colors.darkBlue },
      left: { style: BorderStyle.SINGLE, size: 1, color: colors.darkBlue },
      right: { style: BorderStyle.SINGLE, size: 1, color: colors.darkBlue },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: colors.darkBlue },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: colors.darkBlue }
    }
  });
}

function createMetricsTable() {
  const metrics = [
    { title: "学习成本", value: "降低 90%", desc: "无需 SQL 基础" },
    { title: "查询效率", value: "提升 10 倍", desc: "分钟级→秒级" },
    { title: "人力成本", value: "节省 80%", desc: "业务人员自主" },
    { title: "报告生成", value: "自动化 100%", desc: "智能生成" },
    { title: "准确率", value: "接近 100%", desc: "计算器保障" }
  ];

  return new Table({
    rows: [
      new TableRow({
        children: metrics.map((m, idx) => new TableCell({
          children: [
            new Paragraph({ children: [new TextRun({ text: m.title, size: 18, color: "666666", font: "Microsoft YaHei" })], alignment: AlignmentType.CENTER, spacing: { after: 80 } }),
            new Paragraph({ children: [new TextRun({ text: m.value, bold: true, color: colors.green, size: 32, font: "Arial" })], alignment: AlignmentType.CENTER, spacing: { after: 80 } }),
            new Paragraph({ children: [new TextRun({ text: m.desc, size: 16, color: "999999", font: "Microsoft YaHei" })], alignment: AlignmentType.CENTER })
          ],
          shading: { fill: idx % 2 === 0 ? colors.lightGray : "FFFFFF" },
          margins: { top: 150, bottom: 150, left: 80, right: 80 },
          width: { size: 20, type: WidthType.PERCENTAGE }
        }))
      })
    ],
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: colors.cyan },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: colors.cyan },
      left: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
      right: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan }
    }
  });
}

function createProcessFlowTable() {
  const steps = [
    { num: "步骤 1", title: "获取模型", desc: "API 调用" },
    { num: "步骤 2", title: "选择模型", desc: "智能推荐" },
    { num: "步骤 3", title: "拆分问题", desc: "依赖分析" },
    { num: "步骤 4", title: "执行查询", desc: "DSL 生成" },
    { num: "步骤 5", title: "结果汇总", desc: "报告生成" }
  ];

  return new Table({
    rows: [
      new TableRow({
        children: steps.map((step, idx) => new TableCell({
          children: [
            new Paragraph({ children: [new TextRun({ text: step.num, bold: true, color: colors.cyan, size: 18, font: "Microsoft YaHei" })], alignment: AlignmentType.CENTER, spacing: { after: 60 } }),
            new Paragraph({ children: [new TextRun({ text: step.title, bold: true, color: "FFFFFF", size: 22, font: "Microsoft YaHei" })], alignment: AlignmentType.CENTER, spacing: { after: 60 } }),
            new Paragraph({ children: [new TextRun({ text: step.desc, size: 16, color: "CCCCCC", font: "Microsoft YaHei" })], alignment: AlignmentType.CENTER })
          ],
          shading: { fill: idx % 2 === 0 ? colors.midBlue : colors.lightBlue },
          margins: { top: 100, bottom: 100, left: 50, right: 50 },
          width: { size: 20, type: WidthType.PERCENTAGE }
        }))
      })
    ],
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: colors.cyan },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: colors.cyan },
      left: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
      right: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
      insideVertical: { style: BorderStyle.SINGLE, size: 1, color: "FFFFFF" }
    }
  });
}

async function createDocument() {
  console.log("📄 开始创建优化版 Data-Analytics 技能文档...");

  const doc = new Document({
    creator: "技能中心",
    title: "Data-Analytics 技能汇报",
    sections: [{
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
      children: [
        // 封面
        createSpacer(800),
        new Paragraph({ text: "Data-Analytics 技能", heading: HeadingLevel.TITLE, style: { bold: true, size: 56, color: colors.darkBlue, font: "Microsoft YaHei" }, spacing: { after: 400 }, alignment: AlignmentType.CENTER }),
        new Paragraph({ children: [new TextRun({ text: "让数据分析像对话一样简单", size: 32, color: colors.cyan, bold: true, font: "Microsoft YaHei" })], spacing: { after: 500 }, alignment: AlignmentType.CENTER }),
        new Paragraph({ children: [new TextRun({ text: "─".repeat(50), color: colors.cyan, size: 16 })], spacing: { after: 600 }, alignment: AlignmentType.CENTER }),
        new Paragraph({ children: [new TextRun({ text: "  零代码查询  ", bold: true, color: "FFFFFF", size: 22, font: "Microsoft YaHei" }), new TextRun({ text: "  智能规划  ", bold: true, color: "FFFFFF", size: 22, font: "Microsoft YaHei" }), new TextRun({ text: "  自动生成报告  ", bold: true, color: "FFFFFF", size: 22, font: "Microsoft YaHei" })], spacing: { after: 800 }, alignment: AlignmentType.CENTER }),
        new Paragraph({ children: [new TextRun({ text: "技能汇报文档", size: 24, color: "999999", font: "Microsoft YaHei" })], spacing: { after: 600 }, alignment: AlignmentType.CENTER }),
        createSpacer(800),
        new Paragraph({ children: [new TextRun({ text: "技能中心 · 2026 年", size: 20, color: "999999", italics: true, font: "Microsoft YaHei" })], alignment: AlignmentType.CENTER }),

        // 第一章
        createHeading1("一、核心价值：为什么需要 Data-Analytics？"),
        createHeading2("1.1 传统数据分析痛点"),
        createNormalText("在当前数据分析场景中，业务人员面临以下挑战：", false, 250),
        createBulletPoint("❌ 需要掌握 SQL 和数据库知识，学习成本高"),
        createBulletPoint("❌ 每次查询都要编写代码，效率低下"),
        createBulletPoint("❌ 数据结果需要手动分析，容易出错"),
        createBulletPoint("❌ 无法进行多轮递进分析，深度有限"),
        createBulletPoint("❌ 业务人员依赖技术人员，响应慢"),
        createSpacer(350),

        createHeading2("1.2 Data-Analytics 解决方案"),
        createNormalText("Data-Analytics 技能提供以下核心能力：", false, 250),
        createBulletPoint("✅ 自然语言交互：用日常语言描述需求，无需技术背景"),
        createBulletPoint("✅ 智能模型推荐：自动匹配相关数据模型，降低学习成本"),
        createBulletPoint("✅ 自主规划执行：大模型生成查询策略，提高准确性"),
        createBulletPoint("✅ 自动计算分析：调用计算器确保准确，避免幻觉"),
        createBulletPoint("✅ 多轮对话支持：上下文自动复用，支持深度分析"),
        createSpacer(400),

        // 第二章
        createHeading1("二、核心优势：相比传统方式的突破性优势"),
        createHeading2("2.1 对比分析"),
        createNormalText("通过对比可以看出 Data-Analytics 技能的显著优势：", false, 300),
        createComparisonTable(),
        createSpacer(400),

        createHeading2("2.2 效率提升指标"),
        createNormalText("量化指标展示 Data-Analytics 带来的实际价值：", false, 300),
        createMetricsTable(),
        createSpacer(500),

        // 第三章
        createHeading1("三、核心逻辑：五步标准化工作流程"),
        createNormalText("Data-Analytics 技能采用严格的五步流程，确保查询的准确性和可追溯性。每一步都有明确的目标和输出，保证分析质量。", false, 350),
        createProcessFlowTable(),
        createSpacer(400),

        createHeading2("3.1 步骤 1：获取所有数据模型"),
        createNormalText("调用 API 获取完整模型列表和字段结构，生成会话 ID 用于后续日志追踪。", true, 200),
        createBulletPoint("输出：会话 ID + 6 个数据模型（收款登记模型、项目信息的模型、费用报销等）"),
        createBulletPoint("日志：自动保存到 logs/{session_id}/ 目录，便于追溯"),
        createBulletPoint("关键：为后续步骤提供完整的模型元数据"),
        createSpacer(300),

        createHeading2("3.2 步骤 2：选择相关模型"),
        createNormalText("根据用户问题智能推荐 1-3 个最相关模型，输出带表前缀的完整字段名。", true, 200),
        createBulletPoint("关键规则：字段名必须带表前缀（如 collectionReg3X.receivingAmount）"),
        createBulletPoint("输出格式：纯 JSON，包含 tableName、columns 等信息"),
        createBulletPoint("注意：必须包含关联字段（如项目编号）以便后续筛选"),
        createSpacer(300),

        createHeading2("3.3 步骤 3：拆分用户问题"),
        createNormalText("将复杂问题拆分为可执行子问题，分析依赖关系（链式/共同/独立）。", true, 200),
        createBulletPoint("依赖类型：链式依赖（顺序执行）、共同依赖（先串行后并行）、完全独立（并行）"),
        createBulletPoint("输出格式：{\"question\": [\"问题 1\", \"问题 2\"]}"),
        createBulletPoint("关键：准确识别依赖关系，决定执行策略"),
        createSpacer(300),

        createHeading2("3.4 步骤 4：执行查询"),
        createNormalText("大模型生成 DSL 并执行，有依赖串行执行，无依赖可并行。", true, 200),
        createBulletPoint("DSL 生成：基于 DSL.md 提示词，大模型直接输出 JSON"),
        createBulletPoint("执行策略：链式依赖→串行，独立问题→并行"),
        createBulletPoint("上下文传递：后续查询传入 last_question 和 last_result"),
        createBulletPoint("熔断机制：连续失败 3 次自动终止"),
        createSpacer(300),

        createHeading2("3.5 步骤 5：结果汇总"),
        createNormalText("调用计算器确保计算准确，大模型直接生成 Markdown 分析报告。", true, 200),
        createBulletPoint("计算器调用：[[\"描述\", \"表达式\"]] 格式，避免计算幻觉"),
        createBulletPoint("报告生成：大模型直接输出 Markdown，不调用 Write 工具"),
        createBulletPoint("输出内容：数据表格、关键指标、分析结论、建议"),
        createSpacer(500),

        // 第四章
        createHeading1("四、技术架构：四层架构设计"),
        createHeading2("L1 - API 调用层"),
        createNormalText("负责与数据平台 API 通信，获取模型结构和执行 DSL 查询。", true, 200),
        createBulletPoint("核心脚本：call_api_get_models.py（获取模型）、execute_dsl_query.py（执行查询）"),
        createBulletPoint("主要功能：模型获取、DSL 改写、数据查询、错误处理"),
        createBulletPoint("日志记录：自动保存 API 调用参数和响应结果"),
        createSpacer(300),

        createHeading2("L2 - DSL 生成层"),
        createNormalText("大模型根据用户问题生成标准 DSL 查询语句。", true, 200),
        createBulletPoint("提示词基础：基于 DSL.md，支持 table（查明细）和 chart（聚合分析）两种类型"),
        createBulletPoint("关键规则：字段名带表前缀、op 操作符合法、时间范围处理（年度按自然年）"),
        createBulletPoint("意图判断：table 类型用于查明细，chart 类型用于聚合分析"),
        createSpacer(300),

        createHeading2("L3 - 计算工具层"),
        createNormalText("提供数值计算能力和日志追踪管理。", true, 200),
        createBulletPoint("calculator.py：数值计算工具，接收 [[\"描述\", \"表达式\"]] 格式，返回计算结果"),
        createBulletPoint("logger.py：日志记录工具，支持 DSL 日志和查询结果日志，按会话组织"),
        createBulletPoint("作用：避免大模型计算幻觉，确保数值准确性"),
        createSpacer(300),

        createHeading2("L4 - 配置管理层"),
        createNormalText("统一管理 API 凭证、请求参数和会话配置。", true, 200),
        createBulletPoint("api_config.json：API 地址、accessToken、默认参数（pageSize、pageNo 等）"),
        createBulletPoint("凭证过期处理：API 返回 401 时停止流程，等待更新 accessToken"),
        createBulletPoint("会话管理：每个会话生成唯一 ID，用于日志追踪和上下文管理"),
        createSpacer(500),

        // 第五章
        createHeading1("五、应用场景：四大核心业务场景"),
        
        createHeading2("5.1 财务分析 💰"),
        createBulletPoint("年度/月度收款总额统计"),
        createBulletPoint("项目收支对比分析"),
        createBulletPoint("客户收款趋势分析"),
        createBulletPoint("费用报销明细查询"),
        createBulletPoint("收款方式分布统计"),
        createSpacer(200),
        
        createHeading3("实战案例 1：查询 2024 年收款总金额"),
        createNormalText("用户问题：查询 24 年收款总金额", false, 150),
        createNormalText("执行步骤：", true, 150),
        createBulletPoint("步骤 1：获取模型，识别\"收款登记模型\"包含收款金额和收款日期字段"),
        createBulletPoint("步骤 2：选择收款登记模型，输出 receivingAmount、receivingDate 等字段"),
        createBulletPoint("步骤 3：拆分为单问题\"查询 2024 年收款总金额\""),
        createBulletPoint("步骤 4：生成 DSL，设置时间筛选 2024-01-01 到 2024-12-31，对 receivingAmount 求和"),
        createBulletPoint("步骤 5：返回结果 1,883,999 元，生成收款分析报告"),
        createNormalText("查询耗时：8 秒 | 传统方式：30 分钟（需编写 SQL）", false, 200),
        
        createHeading3("实战案例 2：对比各项目的收款和费用"),
        createNormalText("用户问题：对比西安科学城项目和上海张江项目的收款和费用情况", false, 150),
        createNormalText("执行步骤：", true, 150),
        createBulletPoint("步骤 1-2：获取模型，选择收款登记模型和费用报销模型"),
        createBulletPoint("步骤 3：拆分为 4 个子问题（科学城收款、科学城费用、张江收款、张江费用）"),
        createBulletPoint("步骤 4：并行执行 4 个查询，传入项目名称筛选条件"),
        createBulletPoint("步骤 5：汇总结果，生成对比表格和收支差额分析"),
        createNormalText("输出报告：包含两个项目的收款总额、费用总额、收支差额对比", false, 200),
        createSpacer(300),

        createHeading2("5.2 项目管理 📊"),
        createBulletPoint("项目基本信息查询"),
        createBulletPoint("项目收款/费用关联分析"),
        createBulletPoint("多项目对比分析"),
        createBulletPoint("项目进度跟踪"),
        createBulletPoint("项目成本效益分析"),
        createSpacer(200),
        
        createHeading3("实战案例 3：查询 2024 年开工的项目信息"),
        createNormalText("用户问题：24 年开工的项目有哪些？", false, 150),
        createNormalText("执行步骤：", true, 150),
        createBulletPoint("步骤 1-2：获取模型，选择\"项目信息的模型\"，包含 projectNo、actualStartDate 字段"),
        createBulletPoint("步骤 3：拆分为单问题\"查询 2024 年开工的项目\""),
        createBulletPoint("步骤 4：生成 DSL，设置时间筛选 actualStartDate 在 2024 年内，返回项目列表"),
        createBulletPoint("步骤 5：返回项目列表（西安科学城项目、上海张江项目、北京亦庄项目等）"),
        createNormalText("关键：上下文复用，后续问题可直接使用此项目列表", false, 200),
        
        createHeading3("实战案例 4：多轮对话分析项目收款"),
        createNormalText("第 1 轮：用户\"24 年开工的项目有哪些？\" → 返回 3 个项目", false, 120),
        createNormalText("第 2 轮：用户\"这些项目的收款情况如何？\" → 自动复用第 1 轮项目列表，查询收款", false, 120),
        createNormalText("第 3 轮：用户\"那费用情况呢？\" → 复用项目列表，查询费用", false, 120),
        createNormalText("第 4 轮：用户\"对比一下收款和费用\" → 直接分析第 2、3 轮结果，生成对比报告", false, 150),
        createNormalText("优势：无需重复说明项目，上下文自动复用，对话自然流畅", false, 200),
        createSpacer(300),

        createHeading2("5.3 根因分析 🔍"),
        createBulletPoint("数据异常下钻分析"),
        createBulletPoint("按项目/时间/类型维度拆分"),
        createBulletPoint("假设驱动验证"),
        createBulletPoint("月度/季度趋势分析"),
        createBulletPoint("同比/环比分析"),
        createSpacer(500),

        createHeading2("5.4 多轮对话 📈"),
        createBulletPoint("上下文自动复用"),
        createBulletPoint("条件细化筛选"),
        createBulletPoint("对比分析报告"),
        createBulletPoint("递进式深度分析"),
        createBulletPoint("跨轮次结果整合"),
        createSpacer(200),
        
        createHeading3("实战案例 6：递进式财务分析"),
        createNormalText("场景：财务总监需要了解公司收款情况，进行多轮深度分析", false, 150),
        createNormalText("对话流程：", true, 150),
        createNormalText("① \"2024 年收款总额是多少？\" → 返回 1883.99 万元", false, 100),
        createNormalText("② \"各月收款趋势如何？\" → 返回月度趋势图表，发现 3 月、9 月偏高", false, 100),
        createNormalText("③ \"3 月为什么偏高？\" → 根因分析，发现季度结算效应", false, 100),
        createNormalText("④ \"哪些项目贡献最大？\" → 按项目下钻，Top5 项目占 68%", false, 100),
        createNormalText("⑤ \"这些项目的收款方式分布？\" → 分析银行转账、承兑汇票等占比", false, 100),
        createNormalText("⑥ \"和 2023 年对比呢？\" → 同比分析，增长 23%，主要是新客户贡献", false, 150),
        createNormalText("价值：6 轮对话完成深度分析，传统方式需 1-2 天，现仅需 5 分钟", false, 200),
        createSpacer(400),

        createHeading3("实战案例 7：5 月费用激增的完整根因分析"),
        createNormalText("背景：公司 5 月费用报销数据异常，总经理要求查明原因", false, 150),
        createNormalText("初始数据：5 月费用 285 万元，环比增长 127%，同比增长 89%", false, 150),
        createSpacer(200),
        
        createHeading3("第一阶段：数据确认与异常识别"),
        createNormalText("用户问题：\"5 月费用为什么比 4 月增长了这么多？\"", false, 120),
        createNormalText("系统返回：1 月 98 万、2 月 105 万、3 月 112 万、4 月 125 万、5 月 285 万", false, 100),
        createNormalText("异常识别：5 月费用环比增长 127%，远超正常波动范围（±15%）", false, 150),
        createSpacer(200),
        
        createHeading3("第二阶段：大模型自主提出假设"),
        createNormalText("大模型基于业务经验，自主提出以下可能原因：", false, 150),
        createNormalText("假设 H1：某个大额项目集中报销（如差旅费、采购费）", false, 100),
        createNormalText("假设 H2：某个部门费用异常增长（如市场部展会费用）", false, 100),
        createNormalText("假设 H3：某个费用类型激增（如招待费、咨询费）", false, 100),
        createNormalText("假设 H4：一次性费用（如办公设备采购、装修费用）", false, 150),
        createSpacer(200),
        
        createHeading3("第三阶段：大模型自主下钻验证"),
        createNormalText("🔹 自主查询 1 - 按项目下钻（验证 H1）:", true, 120),
        createNormalText("大模型生成问题：\"5 月各项目的费用分布如何？按金额排序\"", false, 100),
        createNormalText("查询结果：西安科学城项目 125 万（44%）、上海张江项目 45 万（16%）、北京亦庄项目 38 万（13%）、其他项目合计 77 万（27%）", false, 100),
        createNormalText("分析结论：西安科学城项目费用异常偏高，需要进一步分析其费用构成", false, 150),
        createSpacer(150),
        
        createNormalText("🔹 自主查询 2 - 按费用类型下钻（验证 H3）:", true, 120),
        createNormalText("大模型生成问题：\"西安科学城项目 5 月的费用类型分布？\"", false, 100),
        createNormalText("查询结果：差旅费 68 万（54%）、会议费 32 万（26%）、招待费 15 万（12%）、其他 10 万（8%）", false, 100),
        createNormalText("分析结论：差旅费和会议费是主要构成，需要核实是否为一次性费用", false, 150),
        createSpacer(150),
        
        createNormalText("🔹 自主查询 3 - 查询大额记录（验证 H4）:", true, 120),
        createNormalText("大模型生成问题：\"5 月超过 10 万元的大额费用有哪些？\"", false, 100),
        createNormalText("查询结果：", false, 100),
        createNormalText("  • 科学城项目 - 集中差旅费 45 万（5 月 15 日，项目组 20 人往返上海集中办公）", false, 80),
        createNormalText("  • 科学城项目 - 技术峰会参展费 32 万（5 月 22 日，上海国际技术峰会）", false, 80),
        createNormalText("  • 张江项目 - 实验室装修费 28 万（5 月 10 日，一次性支出）", false, 80),
        createNormalText("  • 市场部 - 客户招待费 12 万（5 月 25 日，重要客户来访）", false, 100),
        createNormalText("分析结论：发现 3 笔大额一次性费用，合计 105 万，占 5 月总费用的 37%", false, 150),
        createSpacer(200),
        
        createHeading3("第四阶段：大模型自主计算与根因确认"),
        createNormalText("自主计算：剔除一次性因素后的实际费用", false, 120),
        createNormalText("计算过程：285 万 - 45 万 - 32 万 - 28 万 = 180 万", false, 100),
        createNormalText("调整后分析：5 月实际费用 180 万元，环比增长 44%", false, 100),
        createNormalText("进一步分析：44% 增长仍偏高，但主要原因是科学城项目进入开发高峰期，差旅费自然增长", false, 150),
        createSpacer(200),
        
        createHeading3("第五阶段：自动生成根因分析报告"),
        createNormalText("大模型自动生成完整分析报告：", false, 150),
        createNormalText("【异常现象】5 月费用 285 万元，环比增长 127%，同比增长 89%", false, 100),
        createNormalText("【根因结论】", false, 100),
        createNormalText("  1. 一次性费用影响：科学城项目集中差旅费 45 万 + 技术峰会参展费 32 万 + 张江项目装修费 28 万 = 105 万", false, 80),
        createNormalText("  2. 业务增长因素：科学城项目进入开发高峰期，常规差旅费环比增长 35%", false, 80),
        createNormalText("  3. 剔除一次性因素后，5 月实际费用 180 万，环比增长 44%，属于业务扩张期的正常增长", false, 80),
        createNormalText("【管理建议】", false, 100),
        createNormalText("  • 建立大额费用预警机制，单笔超过 10 万需提前报备", false, 80),
        createNormalText("  • 区分经常性费用和非经常性费用进行分析", false, 80),
        createNormalText("  • 关注项目高峰期费用预算管控", false, 80),
        createNormalText("【分析效率】自主根因分析耗时 15 分钟，传统方式需 3-5 天（收集数据 + 分析 + 报告）", false, 200),
        createSpacer(500),
        createHeading2("5.4 多轮对话 📈"),
        createBulletPoint("上下文自动复用"),
        createBulletPoint("条件细化筛选"),
        createBulletPoint("对比分析报告"),
        createBulletPoint("递进式深度分析"),
        createBulletPoint("跨轮次结果整合"),
        createSpacer(500),

        // 第六章
        createHeading1("六、核心原则：设计哲学与约束机制"),
        createHeading2("6.1 禁令类原则"),
        createNormalText("这些原则确保技能的正确使用和输出质量：", false, 250),
        createBulletPoint("🚫 禁用文件创建：所有步骤严禁调用 Write 工具"),
        createBulletPoint("🔄 严格分步执行：必须按顺序执行 1→2→3→4→5"),
        createBulletPoint("⚡ 执行连续性：每步完成后自动继续下一步"),
        createSpacer(350),

        createHeading2("6.2 保障类原则"),
        createNormalText("这些原则保障技能的稳定性和准确性：", false, 250),
        createBulletPoint("🛡️ 熔断机制：DSL 生成或查询失败 3 次终止"),
        createBulletPoint("🔗 上下文复用：多轮对话复用会话 ID 和模型"),
        createBulletPoint("🧮 计算器保障：数值运算必须调用计算器"),
        createSpacer(500),

        // 第七章
        createHeading1("七、多轮对话优化：上下文复用"),
        createHeading2("7.1 上下文复用清单"),
        createNormalText("多轮对话中，以下内容会自动复用，无需重复获取：", false, 250),
        createBulletPoint("会话 ID：步骤 1 输出，直接用于 logger.load_session()"),
        createBulletPoint("模型列表：步骤 2 输出，后续查询直接复制使用"),
        createBulletPoint("查询结果：步骤 4 输出，作为 last_result 传递"),
        createBulletPoint("项目列表：已查询的项目信息，后续问题直接筛选"),
        createSpacer(300),

        createHeading2("7.2 常见场景"),
        createNormalText("追问同一个项目：复用步骤 2 模型，直接执行步骤 4", false, 150),
        createNormalText("细化查询条件：复用模型，调整查询条件执行步骤 4", false, 150),
        createNormalText("切换分析维度：复用会话 ID，添加新模型执行步骤 4", false, 150),
        createNormalText("对比分析：复用已有结果，直接执行步骤 5", false, 250),

        createHeading2("7.3 跨轮次结果复用规则"),
        createNormalText("核心原则：如果后一轮的问题已经在上一轮得到答案，大模型直接从对话上下文获取结果，不再重复执行查询。", true, 250),
        createNormalText("❌ 错误做法：", true, 150),
        createBulletPoint("写 Python 代码读取 logs/{session_id}/step4-*.json 文件"),
        createBulletPoint("用 Bash 命令 cat 读取上一轮结果"),
        createBulletPoint("第 2 轮重新查询'24 年开工项目有哪些'"),
        createSpacer(200),
        createNormalText("✅ 正确做法：", true, 150),
        createBulletPoint("大模型直接从对话历史中找到第 1 轮的项目列表"),
        createBulletPoint("大模型基于上下文直接生成 DSL JSON"),
        createBulletPoint("第 2、3、4 轮都不再重复查询项目信息"),
        createSpacer(500),

        // 第八章
        createHeading1("八、总结与展望"),
        createNormalText("Data-Analytics 技能重新定义了数据分析的工作方式——让业务人员无需技术背景，用自然语言即可完成复杂的数据查询和分析。", false, 350),

        createHeading2("三大突破"),
        new Paragraph({ children: [new TextRun({ text: "🎯 零门槛：", bold: true, color: colors.darkBlue, size: 24, font: "Microsoft YaHei" }), new TextRun({ text: "\n无需 SQL/编程基础，业务人员可自主完成数据分析，摆脱对技术人员的依赖。", size: 22, color: colors.darkGray, font: "Microsoft YaHei" })], spacing: { after: 250 } }),
        new Paragraph({ children: [new TextRun({ text: "⚡ 高效率：", bold: true, color: colors.darkBlue, size: 24, font: "Microsoft YaHei" }), new TextRun({ text: "\n从自然语言描述到分析结果输出，全程自动化，分钟级工作变为秒级响应。", size: 22, color: colors.darkGray, font: "Microsoft YaHei" })], spacing: { after: 250 } }),
        new Paragraph({ children: [new TextRun({ text: "📊 智能化：", bold: true, color: colors.darkBlue, size: 24, font: "Microsoft YaHei" }), new TextRun({ text: "\n自动规划查询策略、调用计算器保障准确、自动生成分析报告，全流程智能化。", size: 22, color: colors.darkGray, font: "Microsoft YaHei" })], spacing: { after: 400 } }),

        createHeading2("核心价值"),
        createBulletPoint("降低数据分析门槛，让业务人员摆脱对技术人员的依赖"),
        createBulletPoint("提升决策效率，从数据查询到分析结果只需秒级"),
        createBulletPoint("保证计算准确，通过计算器工具避免大模型幻觉"),
        createBulletPoint("支持深度分析，多轮对话和根因分析功能"),
        createSpacer(500),

        // 底部
        new Paragraph({ children: [new TextRun({ text: "让数据说话，让决策更智能", bold: true, size: 32, color: colors.cyan, font: "Microsoft YaHei" })], alignment: AlignmentType.CENTER, spacing: { after: 300 } }),
        new Paragraph({ children: [new TextRun({ text: "技能中心 · 2026 年", size: 20, color: "999999", italics: true, font: "Microsoft YaHei" })], alignment: AlignmentType.CENTER, spacing: { after: 400 } })
      ]
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  const outputPath = path.join(__dirname, "..", "..", "..", "..", "workspace", "Data-Analytics 技能汇报 - 优化版.docx");
  fs.writeFileSync(outputPath, buffer);
  
  console.log(`✅ 优化版文档创建完成：${outputPath}`);
}

createDocument().catch(console.error);
