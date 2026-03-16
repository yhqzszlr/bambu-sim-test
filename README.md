# <bambu-sim-test>

本项目用于模拟 bambusim 行为并进行自动化测试/生成报告/分析错误日志。  
包含：核心逻辑、脚本化 demo、pytest 测试、HTML 测试报告、错误日志分析，以及 GitHub Actions 自动化（Artifacts / GitHub Pages）。

---

##  功能概览

- **一键运行**：通过 `Makefile` 统一入口（demo / test / report / clean）
- **pytest 自动化测试**：本地与 CI 均可运行
- **HTML 测试报告**：`pytest-html` 生成 `reports/pytest_report.html`
- **错误日志分析**：`analyze_log.sh` 统计 `errors.log`（总量、Top action、异常类型、末尾预览）
- **CI 集成**：GitHub Actions 自动执行并发布报告（Artifact / Pages）

---

##  CI 状态与在线报告

### GitHub Actions
- Pages：![pages](../../actions/workflows/pages-report.yml/badge.svg)

### 在线 pytest 报告（GitHub Pages）
- https://yhqzszlr.github.io/bambu-sim-test/


##  项目结构

```text
.
├── .github/
│   └── workflows/
│       └── pages-report.yml          # GitHub Pages / 报告发布工作流
├── assets/
│   └── style.css                     # 报告样式等静态资源
├── bambusim/                         # 核心 Python 包
│   ├── __init__.py
│   ├── core.py
│   ├── faults.py
│   ├── logging_utils.py
│   ├── quality.py
│   └── tempCodeRunnerFile.py        ）
├── test/
│   └── test_simulator.py             # pytest 测试用例
├── third_party/
│   ├── bambulabs_api/                # 第三方代码（MIT），用于参考/对照
│   ├── docs/                         # 第三方项目文档
│   ├── examples/                     # 第三方项目示例
│   └── .github/                      # 第三方项目的 CI 配置
├── tools/
│   └── run_demo.py                   # 工具脚本
├── web/
│   ├── app.py                        # Web 服务入口
│   └── schemas.py                    # Web 数据结构/模型
├── .gitignore
├── analyze_log.sh                    # 错误日志分析脚本
├── Makefile                          # 常用命令入口
├── NOTICE.txt                        # 第三方代码来源/commit/许可声明
├── pyproject.toml                    # Python 项目配置与依赖
└── pytest.ini                        # pytest 配置

```



## 第三方代码说明

本仓库包含第三方代码（MIT）：`third_party/bambulabs_api/`  
来源与提交点信息见 `NOTICE.txt`。

