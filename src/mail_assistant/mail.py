import pandas as pd
from imapclient import IMAPClient
from datetime import datetime, timedelta
import email

def fetch_emails(host, username, password, last_uid=0):
    """从IMAP服务器获取邮件
    Args:
        host: IMAP服务器地址
        username: 邮箱用户名
        password: 邮箱密码
        last_uid: 上次获取的最后一条邮件的UID，默认为0表示获取所有邮件
    Returns:
        pandas.DataFrame: 包含邮件信息的DataFrame
        int: 本次获取的最后一条邮件的UID
    """
    with IMAPClient(host) as server:
        server.login(username, password)
        server.select_folder('INBOX')
        
        # 获取所有大于last_uid的邮件
        messages = server.search(['UID', f'{last_uid+1}:*'])
        
        emails_df = pd.DataFrame(columns=['subject', 'from', 'body'])
        current_max_uid = last_uid
        
        for uid, message_data in server.fetch(messages, ['RFC822']).items():
            msg = email.message_from_bytes(message_data[b'RFC822'])
            
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode(encoding='utf-8', errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode(encoding='utf-8', errors='ignore')
            
            emails_df.loc[len(emails_df)] = {
                'subject': msg['subject'],
                'from': msg['from'],
                'body': body
            }
            
            # 更新最大UID
            if uid > current_max_uid:
                current_max_uid = uid
    
    return emails_df, current_max_uid