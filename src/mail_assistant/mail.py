import pandas as pd
from imapclient import IMAPClient
from datetime import datetime, timedelta
import email

def fetch_emails(host, username, password):
    """从IMAP服务器获取过去10小时的邮件"""
    with IMAPClient(host) as server:
        server.login(username, password)
        server.select_folder('INBOX')
        
        since_time = datetime.now() - timedelta(hours=10)
        messages = server.search(['SINCE', since_time])
        
        emails_df = pd.DataFrame(columns=['subject', 'from', 'body'])
        
        for uid, message_data in server.fetch(messages, ['RFC822']).items():
            msg = email.message_from_bytes(message_data[b'RFC822'])
            
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()
            
            emails_df.loc[len(emails_df)] = {
                'subject': msg['subject'],
                'from': msg['from'],
                'body': body
            }
    
    return emails_df