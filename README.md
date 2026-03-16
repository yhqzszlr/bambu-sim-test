# <你的仓库名>

本项目用于 <一句话说明：例如“模拟 bambusim 行为并进行自动化测试/生成报告/分析错误日志”>。  
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
- Tests：![tests](../../actions/workflows/tests.yml/badge.svg)
- Pages：![pages](../../actions/workflows/pages-report.yml/badge.svg)

### 在线 pytest 报告（GitHub Pages）
- https://<你的GitHub用户名>.github.io/<仓库名>/

> 若仓库未启用 Pages 或为受限环境，上述链接可能不可用；仍可通过 Actions 的 **Artifacts** 下载报告。

---

##  项目结构

```text
.
├── <你的包名>/                       # 核心 Python 包源码（示例）
├── web/                              # Web 服务（如 FastAPI）相关（若有）
├── tools/                            # 工具脚本（如 run_demo.py）
├── test/                             # pytest 测试用例
├── analyze_log.sh                    # 错误日志分析脚本
├── Makefile                          # 常用命令入口
├── pytest.ini                        # pytest 配置
├── requirements.txt / pyproject.toml # 依赖（按实际二选一或都有）
├── reports/                          #（生成物）pytest_report.html / error_analysis.txt
└── third_party/
    └── bambulabs_api/                # vendored 第三方代码（MIT）
    ├── LICENSE
    └── NOTICE
