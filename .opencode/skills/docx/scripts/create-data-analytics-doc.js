const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, HeadingLevel, BorderStyle } = require("docx");
const fs = require("fs");
const path = require("path");

// 颜色定义
const colors = {
  darkBlue: "1E3A5F",
  midBlue: "2E5A8B",
  lightBlue: "5479A2",
  cyan: "00A8CC",
  orange: "FF7A00",
  green: "00B050",
  darkGray: "212121",
  lightGray: "F5F6F8"
};

function createSection(title, subtitle, color = colors.darkBlue) {
  return [
    new Paragraph({
      text: title,
      heading: HeadingLevel.HEADING_1,
      style: {
        color: color === colors.darkBlue ? "FFFFFF" : color,
        bold: true,
        size: 32
      },
      shading: color === colors.darkBlue ? { fill: color } : undefined,
      spacing: { before: 400, after: 200 }
    }),
    subtitle ? new Paragraph({
      text: subtitle,
      style: {
        color: "666666",
        size: 24,
        bold: true
      },
      spacing: { after: 300 }
    }) : null
  ].filter(Boolean);
}

function createHeading2(text) {
  return new Paragraph({
    text,
    heading: HeadingLevel.HEADING_2,
    style: {
      color: colors.darkBlue,
      bold: true,
      size: 28
    },
    spacing: { before: 400, after: 200 }
  });
}

function createHeading3(text) {
  return new Paragraph({
    text,
    heading: HeadingLevel.HEADING_3,
    style: {
      color: colors.cyan,
      bold: true,
      size: 24
    },
    spacing: { before: 300, after: 150 }
  });
}

function createBulletPoint(text, level = 0) {
  return new Paragraph({
    text,
    bullet: { level },
    style: {
      color: colors.darkGray,
      size: 22
    },
    spacing: { after: 100 }
  });
}

function createTextParagraph(text, options = {}) {
  const runs = [];
  
  if (Array.isArray(text)) {
    text.forEach((item, index) => {
      runs.push(new TextRun({
        text: item.text,
        bold: item.bold,
        color: item.color || colors.darkGray,
        size: item.size || 22
      }));
    });
  } else {
    runs.push(new TextRun({
      text,
      bold: options.bold,
      color: options.color || colors.darkGray,
      size: options.size || 22
    }));
  }
  
  return new Paragraph({
    children: runs,
    spacing: { after: options.after || 150 }
  });
}

function createComparisonTable() {
  return new Table({
    rows: [
      new TableRow({
        children: [
          new TableCell({
            children: [new Paragraph({
              text: "对比维度",
              style: { bold: true, color: "FFFFFF", size: 20 }
            })],
            shading: { fill: colors.darkBlue },
            width: { size: 30, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "传统方式",
              style: { bold: true, color: "FFFFFF", size: 20 }
            })],
            shading: { fill: colors.darkBlue },
            width: { size: 35, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "Data-Analytics 技能",
              style: { bold: true, color: "FFFFFF", size: 20 }
            })],
            shading: { fill: colors.darkBlue },
            width: { size: 35, type: WidthType.PERCENTAGE }
          })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({
            children: [createTextParagraph("查询方式")],
            shading: { fill: colors.lightGray }
          }),
          new TableCell({
            children: [createTextParagraph("编写 SQL/代码")]
          }),
          new TableCell({
            children: [createTextParagraph("自然语言描述", { bold: true, color: colors.darkBlue })]
          })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({
            children: [createTextParagraph("学习成本")],
            shading: { fill: colors.lightGray }
          }),
          new TableCell({
            children: [createTextParagraph("需掌握 SQL + 业务")]
          }),
          new TableCell({
            children: [createTextParagraph("无需技术背景", { bold: true, color: colors.darkBlue })]
          })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({
            children: [createTextParagraph("执行效率")],
            shading: { fill: colors.lightGray }
          }),
          new TableCell({
            children: [createTextParagraph("分钟级")]
          }),
          new TableCell({
            children: [createTextParagraph("秒级响应", { bold: true, color: colors.darkBlue })]
          })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({
            children: [createTextParagraph("结果展示")],
            shading: { fill: colors.lightGray }
          }),
          new TableCell({
            children: [createTextParagraph("原始数据")]
          }),
          new TableCell({
            children: [createTextParagraph("智能分析报告", { bold: true, color: colors.darkBlue })]
          })
        ]
      }),
      new TableRow({
        children: [
          new TableCell({
            children: [createTextParagraph("多轮对话")],
            shading: { fill: colors.lightGray }
          }),
          new TableCell({
            children: [createTextParagraph("不支持")]
          }),
          new TableCell({
            children: [createTextParagraph("上下文自动复用", { bold: true, color: colors.darkBlue })]
          })
        ]
      })
    ],
    width: { size: 100, type: WidthType.PERCENTAGE }
  });
}

function createProcessFlowTable() {
  return new Table({
    rows: [
      new TableRow({
        children: [
          new TableCell({
            children: [new Paragraph({
              text: "步骤 1",
              style: { bold: true, color: colors.cyan, size: 24 }
            }), new Paragraph({ text: "获取模型", style: { color: "FFFFFF", size: 20 } })],
            shading: { fill: colors.midBlue },
            width: { size: 20, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "→",
              style: { color: colors.cyan, size: 32, bold: true }
            })],
            width: { size: 5, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "步骤 2",
              style: { bold: true, color: colors.cyan, size: 24 }
            }), new Paragraph({ text: "选择模型", style: { color: "FFFFFF", size: 20 } })],
            shading: { fill: colors.lightBlue },
            width: { size: 20, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "→",
              style: { color: colors.cyan, size: 32, bold: true }
            })],
            width: { size: 5, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "步骤 3",
              style: { bold: true, color: colors.cyan, size: 24 }
            }), new Paragraph({ text: "拆分问题", style: { color: "FFFFFF", size: 20 } })],
            shading: { fill: colors.midBlue },
            width: { size: 20, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "→",
              style: { color: colors.cyan, size: 32, bold: true }
            })],
            width: { size: 5, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "步骤 4",
              style: { bold: true, color: colors.cyan, size: 24 }
            }), new Paragraph({ text: "执行查询", style: { color: "FFFFFF", size: 20 } })],
            shading: { fill: colors.lightBlue },
            width: { size: 20, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "→",
              style: { color: colors.cyan, size: 32, bold: true }
            })],
            width: { size: 5, type: WidthType.PERCENTAGE }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "步骤 5",
              style: { bold: true, color: colors.cyan, size: 24 }
            }), new Paragraph({ text: "结果汇总", style: { color: "FFFFFF", size: 20 } })],
            shading: { fill: colors.midBlue },
            width: { size: 20, type: WidthType.PERCENTAGE }
          })
        ]
      })
    ],
    width: { size: 100, type: WidthType.PERCENTAGE }
  });
}

function createMetricsTable() {
  return new Table({
    rows: [
      new TableRow({
        children: [
          new TableCell({
            children: [new Paragraph({
              text: "学习成本",
              style: { size: 18, color: "666666" }
            }), new Paragraph({
              text: "降低 90%",
              style: { bold: true, color: colors.green, size: 28 }
            }), new Paragraph({
              text: "无需 SQL 基础",
              style: { size: 16, color: "666666" }
            })],
            shading: { fill: colors.lightGray },
            borders: {
              top: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              bottom: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              left: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              right: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan }
            }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "查询效率",
              style: { size: 18, color: "666666" }
            }), new Paragraph({
              text: "提升 10 倍",
              style: { bold: true, color: colors.green, size: 28 }
            }), new Paragraph({
              text: "分钟级→秒级",
              style: { size: 16, color: "666666" }
            })],
            shading: { fill: "FFFFFF" },
            borders: {
              top: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              bottom: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              left: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              right: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan }
            }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "人力成本",
              style: { size: 18, color: "666666" }
            }), new Paragraph({
              text: "节省 80%",
              style: { bold: true, color: colors.green, size: 28 }
            }), new Paragraph({
              text: "业务人员自主分析",
              style: { size: 16, color: "666666" }
            })],
            shading: { fill: colors.lightGray },
            borders: {
              top: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              bottom: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              left: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              right: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan }
            }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "报告生成",
              style: { size: 18, color: "666666" }
            }), new Paragraph({
              text: "自动化 100%",
              style: { bold: true, color: colors.green, size: 28 }
            }), new Paragraph({
              text: "智能生成 Markdown",
              style: { size: 16, color: "666666" }
            })],
            shading: { fill: "FFFFFF" },
            borders: {
              top: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              bottom: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              left: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              right: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan }
            }
          }),
          new TableCell({
            children: [new Paragraph({
              text: "准确率",
              style: { size: 18, color: "666666" }
            }), new Paragraph({
              text: "接近 100%",
              style: { bold: true, color: colors.green, size: 28 }
            }), new Paragraph({
              text: "计算器保障",
              style: { size: 16, color: "666666" }
            })],
            shading: { fill: colors.lightGray },
            borders: {
              top: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              bottom: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              left: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan },
              right: { style: BorderStyle.SINGLE, size: 1, color: colors.cyan }
            }
          })
        ]
      })
    ],
    width: { size: 100, type: WidthType.PERCENTAGE }
  });
}

async function createDocument() {
  console.log("📄 开始创建 Data-Analytics 技能文档...");

  const doc = new Document({
    sections: [{
      properties: {},
      children: [
        // 封面
        new Paragraph({ text: "", spacing: { after: 200 } }),
        new Paragraph({ text: "", spacing: { after: 200 } }),
        new Paragraph({ text: "", spacing: { after: 200 } }),
        
        new Paragraph({
          text: "Data-Analytics 技能",
          heading: HeadingLevel.TITLE,
          style: {
            bold: true,
            size: 48,
            color: colors.darkBlue
          },
          spacing: { after: 300 }
        }),
        
        new Paragraph({
          text: "让数据分析像对话一样简单",
          style: {
            size: 28,
            color: colors.cyan,
            bold: true
          },
          spacing: { after: 400 }
        }),

        new Paragraph({
          text: "技能汇报文档",
          style: {
            size: 20,
            color: "666666"
          },
          spacing: { after: 600 }
        }),

        new Paragraph({ text: "", spacing: { after: 800 } }),

        // 标签
        new Paragraph({
          children: [
            new TextRun({ text: "零代码查询  ", bold: true, color: "FFFFFF", size: 20 }),
            new TextRun({ text: "  智能规划  ", bold: true, color: "FFFFFF", size: 20 }),
            new TextRun({ text: "  自动生成报告", bold: true, color: "FFFFFF", size: 20 })
          ],
          spacing: { after: 800 }
        }),

        new Paragraph({ text: "", spacing: { after: 600 } }),

        // 核心价值
        createHeading2("一、核心价值：为什么需要 Data-Analytics？"),

        createHeading3("1.1 传统数据分析痛点"),
        createBulletPoint("❌ 需要掌握 SQL 和数据库知识"),
        createBulletPoint("❌ 每次查询都要编写代码"),
        createBulletPoint("❌ 数据结果需要手动分析"),
        createBulletPoint("❌ 无法进行多轮递进分析"),
        createBulletPoint("❌ 业务人员依赖技术人员"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("1.2 Data-Analytics 解决方案"),
        createBulletPoint("✅ 自然语言交互：用日常语言描述需求"),
        createBulletPoint("✅ 智能模型推荐：自动匹配相关数据模型"),
        createBulletPoint("✅ 自主规划执行：大模型生成查询策略"),
        createBulletPoint("✅ 自动计算分析：调用计算器确保准确"),
        createBulletPoint("✅ 多轮对话支持：上下文自动复用"),

        new Paragraph({ text: "", spacing: { after: 400 } }),

        // 核心优势对比
        createHeading2("二、核心优势：相比传统方式的突破性优势"),
        createComparisonTable(),

        new Paragraph({ text: "", spacing: { after: 400 } }),

        createHeading3("2.2 效率提升指标"),
        createMetricsTable(),

        new Paragraph({ text: "", spacing: { after: 600 } }),

        // 核心逻辑 - 五步流程
        createHeading2("三、核心逻辑：五步标准化工作流程"),

        new Paragraph({
          text: "Data-Analytics 技能采用严格的五步流程，确保查询的准确性和可追溯性：",
          style: { size: 22, color: colors.darkGray },
          spacing: { after: 300 }
        }),

        createProcessFlowTable(),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("3.1 步骤 1：获取所有数据模型"),
        createTextParagraph("调用 API 获取完整模型列表和字段结构，生成会话 ID 用于后续日志追踪。"),
        createBulletPoint("输出：会话 ID + 6 个数据模型（收款登记模型、项目信息的模型、费用报销等）"),
        createBulletPoint("日志：自动保存到 logs/{session_id}/ 目录"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("3.2 步骤 2：选择相关模型"),
        createTextParagraph("根据用户问题智能推荐 1-3 个最相关模型，输出带表前缀的完整字段名。"),
        createBulletPoint("关键规则：字段名必须带表前缀（如 collectionReg3X.receivingAmount）"),
        createBulletPoint("输出格式：纯 JSON，包含 tableName、columns 等信息"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("3.3 步骤 3：拆分用户问题"),
        createTextParagraph("将复杂问题拆分为可执行子问题，分析依赖关系（链式/共同/独立）。"),
        createBulletPoint("依赖类型：链式依赖、共同依赖、完全独立"),
        createBulletPoint("输出格式：{\"question\": [\"问题 1\", \"问题 2\"]}"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("3.4 步骤 4：执行查询"),
        createTextParagraph("大模型生成 DSL 并执行，有依赖串行执行，无依赖可并行。"),
        createBulletPoint("DSL 生成：基于 DSL.md 提示词，大模型直接输出 JSON"),
        createBulletPoint("执行策略：链式依赖→串行，独立问题→并行"),
        createBulletPoint("上下文传递：后续查询传入 last_question 和 last_result"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("3.5 步骤 5：结果汇总"),
        createTextParagraph("调用计算器确保计算准确，大模型直接生成 Markdown 分析报告。"),
        createBulletPoint("计算器调用：[[\"描述\", \"表达式\"]] 格式"),
        createBulletPoint("报告生成：大模型直接输出 Markdown，不调用 Write 工具"),

        new Paragraph({ text: "", spacing: { after: 600 } }),

        // 技术架构
        createHeading2("四、技术架构：四层架构设计"),

        createHeading3("L1 - API 调用层"),
        createTextParagraph("负责与数据平台 API 通信，获取模型结构和执行 DSL 查询。"),
        createBulletPoint("核心脚本：call_api_get_models.py、execute_dsl_query.py"),
        createBulletPoint("功能：模型获取、DSL 改写、数据查询"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("L2 - DSL 生成层"),
        createTextParagraph("大模型根据用户问题生成标准 DSL 查询语句。"),
        createBulletPoint("提示词：基于 DSL.md，支持 table（查明细）和 chart（聚合分析）两种类型"),
        createBulletPoint("关键规则：字段名带表前缀、op 操作符合法、时间范围处理"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("L3 - 计算工具层"),
        createTextParagraph("提供数值计算能力和日志追踪管理。"),
        createBulletPoint("calculator.py：数值计算，避免大模型计算幻觉"),
        createBulletPoint("logger.py：日志记录，支持 DSL 日志和查询结果日志"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("L4 - 配置管理层"),
        createTextParagraph("统一管理 API 凭证、请求参数和会话配置。"),
        createBulletPoint("api_config.json：API 地址、accessToken、默认参数"),
        createBulletPoint("凭证过期处理：API 返回 401 时停止流程，等待更新 token"),

        new Paragraph({ text: "", spacing: { after: 600 } }),

        // 应用场景
        createHeading2("五、应用场景：四大核心业务场景"),

        createHeading3("5.1 财务分析 💰"),
        createBulletPoint("年度/月度收款总额统计"),
        createBulletPoint("项目收支对比分析"),
        createBulletPoint("客户收款趋势分析"),
        createBulletPoint("费用报销明细查询"),
        createTextParagraph("示例：查询 2024 年收款总金额，自动筛选 2024-01-01 到 2024-12-31 的数据"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("5.2 项目管理 📊"),
        createBulletPoint("项目基本信息查询"),
        createBulletPoint("项目收款/费用关联分析"),
        createBulletPoint("多项目对比分析"),
        createBulletPoint("项目进度跟踪"),
        createTextParagraph("示例：查询 24 年开工的项目，然后分析这些项目的收款和费用情况"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("5.3 根因分析 🔍"),
        createBulletPoint("数据异常下钻分析"),
        createBulletPoint("按项目/时间/类型维度拆分"),
        createBulletPoint("假设驱动验证"),
        createBulletPoint("月度/季度趋势分析"),
        createTextParagraph("示例：3 月收款异常偏大？→ 按项目下钻 → 发现大额项目集中收款"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("5.4 多轮对话 📈"),
        createBulletPoint("上下文自动复用"),
        createBulletPoint("条件细化筛选"),
        createBulletPoint("对比分析报告"),
        createBulletPoint("递进式深度分析"),
        createTextParagraph("示例：第 1 轮查项目→第 2 轮查收款→第 3 轮查费用→第 4 轮对比分析"),

        new Paragraph({ text: "", spacing: { after: 600 } }),

        // 核心原则
        createHeading2("六、核心原则：设计哲学与约束机制"),

        createHeading3("🚫 禁令类原则"),
        createBulletPoint("禁用文件创建：所有步骤严禁调用 Write 工具"),
        createBulletPoint("严格分步执行：必须按顺序执行 1→2→3→4→5，不能跳过或合并"),
        createBulletPoint("执行连续性：每步完成后自动继续下一步，步骤 2 后不能等待确认"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("🛡️ 保障类原则"),
        createBulletPoint("熔断机制：DSL 生成或查询失败 3 次终止，防止无限重试"),
        createBulletPoint("上下文复用：多轮对话复用会话 ID 和模型，避免重复查询"),
        createBulletPoint("计算器保障：数值运算必须调用计算器，避免大模型计算幻觉"),

        new Paragraph({ text: "", spacing: { after: 600 } }),

        // 多轮对话优化
        createHeading2("七、多轮对话优化：上下文复用"),

        createHeading3("7.1 上下文复用清单"),
        createBulletPoint("会话 ID：步骤 1 输出，直接用于 logger.load_session()"),
        createBulletPoint("模型列表：步骤 2 输出，直接复制用于步骤 4"),
        createBulletPoint("查询结果：步骤 4 输出，作为 last_result 传递"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("7.2 常见场景"),
        createTextParagraph("追问同一个项目：复用步骤 2 模型，直接执行步骤 4"),
        createTextParagraph("细化查询条件：复用模型，调整查询条件执行步骤 4"),
        createTextParagraph("切换分析维度：复用会话 ID，添加新模型执行步骤 4"),
        createTextParagraph("对比分析：复用已有结果，执行步骤 5"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("7.3 跨轮次结果复用规则"),
        createTextParagraph("核心原则：如果后一轮的问题已经在上一轮得到答案，大模型直接从对话上下文获取结果，不再重复执行查询。"),
        
        new Paragraph({ text: "", spacing: { after: 200 } }),
        createTextParagraph("❌ 错误做法："),
        createBulletPoint("写 Python 代码读取 logs/{session_id}/step4-*.json 文件"),
        createBulletPoint("用 Bash 命令 cat 读取上一轮结果"),
        createBulletPoint("第 2 轮重新查询'24 年开工项目有哪些'"),

        new Paragraph({ text: "", spacing: { after: 200 } }),
        createTextParagraph("✅ 正确做法："),
        createBulletPoint("大模型直接从对话历史中找到第 1 轮的项目列表"),
        createBulletPoint("大模型基于上下文直接生成 DSL JSON"),
        createBulletPoint("第 2、3、4 轮都不再重复查询项目信息"),

        new Paragraph({ text: "", spacing: { after: 600 } }),

        // 总结
        createHeading2("八、总结与展望"),

        createTextParagraph("Data-Analytics 技能重新定义了数据分析的工作方式——让业务人员无需技术背景，用自然语言即可完成复杂的数据查询和分析。"),

        new Paragraph({ text: "", spacing: { after: 300 } }),

        createHeading3("三大突破"),
        
        new Paragraph({
          children: [
            new TextRun({ text: "🎯 零门槛：", bold: true, color: colors.darkBlue, size: 22 }),
            new TextRun({ text: "无需 SQL/编程基础，业务人员自主分析", size: 22 })
          ],
          spacing: { after: 200 }
        }),

        new Paragraph({
          children: [
            new TextRun({ text: "⚡ 高效率：", bold: true, color: colors.darkBlue, size: 22 }),
            new TextRun({ text: "自然语言→分析结果，分钟级变秒级", size: 22 })
          ],
          spacing: { after: 200 }
        }),

        new Paragraph({
          children: [
            new TextRun({ text: "📊 智能化：", bold: true, color: colors.darkBlue, size: 22 }),
            new TextRun({ text: "自动规划、计算准确、报告生成", size: 22 })
          ],
          spacing: { after: 400 }
        }),

        createHeading3("核心价值"),
        createBulletPoint("降低数据分析门槛，让业务人员摆脱对技术人员的依赖"),
        createBulletPoint("提升决策效率，从数据查询到分析结果只需秒级"),
        createBulletPoint("保证计算准确，通过计算器工具避免大模型幻觉"),
        createBulletPoint("支持深度分析，多轮对话和根因分析功能"),

        new Paragraph({ text: "", spacing: { after: 600 } }),

        // 底部标语
        new Paragraph({
          text: "让数据说话，让决策更智能",
          style: {
            bold: true,
            size: 28,
            color: colors.cyan
          },
          spacing: { after: 400 }
        }),

        new Paragraph({
          text: "技能中心 · 2026 年",
          style: {
            size: 18,
            color: "999999",
            italics: true
          }
        })
      ]
    }]
  });

  const buffer = await Packer.toBuffer(doc);
  const outputPath = path.join(__dirname, "..", "..", "..", "..", "workspace", "Data-Analytics 技能汇报.docx");
  fs.writeFileSync(outputPath, buffer);
  
  console.log(`✅ 文档创建完成：${outputPath}`);
}

createDocument().catch(console.error);
