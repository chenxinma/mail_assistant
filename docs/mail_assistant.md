# Mail 模块

## 功能描述

- 负责处理邮件相关的操作
- 主要功能包括：
  - 邮件接收：通过IMAP协议从邮件服务器获取邮件，支持增量获取
  - 邮件解析：自动解码邮件主题和正文，支持多种编码格式
  - 邮件分类：根据邮件内容进行自动分类
  - 邮件存储：将邮件信息保存为Parquet文件格式，并支持向量数据库存储

## 依赖关系

- 依赖 log_config.py 进行日志记录
- 依赖 dotenv 加载环境变量
- 使用 imapclient 进行邮件接收
- 使用 pandas 进行数据处理
- 使用 duckdb 进行本地数据存储
- 使用 chromadb 进行向量数据存储
- 与 main.py 和 vector_save.py 有交互

## 使用示例

```python
from mail_assistant.fetch_mail import main
from mail_assistant.vector_save import save_to_vector_db

# 获取邮件并保存为Parquet文件
main()

# 将邮件内容保存到向量数据库
save_to_vector_db()
```