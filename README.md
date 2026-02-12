# 图书管理系统

这是一个基于 Python 的命令行图书管理系统，支持：

- 添加图书
- 删除图书
- 借阅与归还
- 按书名/作者/ISBN 搜索
- 本地 JSON 持久化保存

## 运行方式

```bash
python3 book_management_system.py
```

数据默认保存在当前目录下的 `books.json`。

## 运行测试

```bash
python3 -m unittest -v
```
