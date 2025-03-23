from .mail import fetch_emails

import os
from dotenv import load_dotenv
import duckdb
import pandas as pd

def main():
    # 加载.env文件
    load_dotenv()
    # 从环境变量读取配置
    host = os.getenv('IMAP_HOST')
    username = os.getenv('IMAP_USERNAME')
    password = os.getenv('IMAP_PASSWORD')
    
    if not all([host, username, password]):
        raise ValueError("请正确配置.env文件中的IMAP_HOST, IMAP_USERNAME和IMAP_PASSWORD")
    
    # 确保db目录存在
    os.makedirs('db', exist_ok=True)
    
    # 获取最新的last_uid
    last_uid = 0
    if os.path.exists('db'):
        con = duckdb.connect()
        try:
            result = \
                con.execute("SELECT MAX(uid) FROM read_parquet('db/*.parquet')").fetchone()
            if result is not None:
                last_uid = result[0]
        finally:
            con.close()
    
    # 获取邮件
    emails_df, current_max_uid = fetch_emails(host, username, password, last_uid)
    
    # 保存为parquet文件
    if not emails_df.empty:
        emails_df.to_parquet(f'db/{current_max_uid}.parquet')
    
    # 打印结果
    print(emails_df)


if __name__ == "__main__":
    main()
