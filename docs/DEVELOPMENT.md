# 开发

使用 Python 3.12，执行 `pip install -e ".[dev]"`。入口是 `python -m cleantext_studio.main`。清洗规则位于 `cleaners`，数据模型位于 `models`，导入导出彼此隔离。提交前运行 Ruff、MyPy 和 pytest；新增规则必须有幂等与保护结构测试。

