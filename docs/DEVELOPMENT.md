# 开发

使用 Python 3.12，执行 `pip install -e ".[dev]"`。入口是 `python -m cleantext_studio.main`。版本单一来源为 `src/cleantext_studio/version.py`。清洗规则和残留检测位于 `cleaners`，会话与块模型位于 `models`，导入导出彼此隔离。提交前运行 Ruff、MyPy 和 pytest；新增规则必须有幂等、残留和保护结构测试。
