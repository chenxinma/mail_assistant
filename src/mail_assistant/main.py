from .mail import fetch_emails

def main():
    # 配置邮箱信息
    host = 'imap.example.com'  # 替换为实际的IMAP服务器地址
    username = 'your_email@example.com'
    password = 'your_password'
    
    # 获取邮件
    emails_df = fetch_emails(host, username, password)
    
    # 打印结果
    print(emails_df)


if __name__ == "__main__":
    main()
