import os
from dotenv import load_dotenv
import duckdb
import schedule
import time
from datetime import datetime
from mail import fetch_emails

def main():
    # 加载.env文件
    load_dotenv()
    # 从环境变量读取配置
    host = os.getenv('IMAP_HOST')
    username = os.getenv('IMAP_USERNAME')
    password = os.getenv('IMAP_PASSWORD')
    specific_cc_email = 'itpmgroup@fsg.com.cn'
    
    if not all([host, username, password]):
        raise ValueError("请正确配置.env文件中的IMAP_HOST, IMAP_USERNAME和IMAP_PASSWORD")
    
    print("Begin mail receiving... ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
    
    # 确保db目录存在
    os.makedirs('db', exist_ok=True)
    
    # 获取邮件
    emails_df, current_max_uid = fetch_emails(host, username, password, 
                            specific_cc_email, last_uid)
    
    # 保存为parquet文件
    if not emails_df.empty:
        emails_df.to_parquet(f'db/{current_max_uid}.parquet')
    
    # 打印结果
    print("Received mails: ", emails_df.shape[0])

if __name__ == "__main__":
    # 每15分钟运行一次 main 函数
    schedule.every(15).minutes.do(main)
    print("Running...", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)
