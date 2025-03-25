import warnings
from tqdm.rich import tqdm
from tqdm import TqdmExperimentalWarning
from typing import Tuple
import os
import pandas as pd
from imapclient import IMAPClient
from datetime import datetime, timedelta
import email
from email.header import decode_header

# 过滤 TqdmExperimentalWarning 警告
warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

def decode_text(text) -> Tuple[str, str]:
    """
    对邮件的主题或正文进行解码处理
    :param text: 待解码的文本
    :return: 解码后的文本
    """
    decoded_parts = decode_header(text)
    decoded_text:str = ""
    _encoding:str = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            if encoding:
                _encoding = encoding
                decoded_text += part.decode(encoding, errors='ignore')
            else:
                decoded_text += part.decode(errors='ignore')
        else:
            decoded_text += part
    return decoded_text, _encoding

def fetch_emails(host, username, password, specific_cc_email, last_uid=0):
    """从IMAP服务器获取邮件
    Args:
        host: IMAP服务器地址
        username: 邮箱用户名
        password: 邮箱密码
        specific_cc_email: 需要筛选的抄送邮箱地址
        last_uid: 上次获取的最后一条邮件的UID，默认为0表示获取所有邮件
    Returns:
        pandas.DataFrame: 包含邮件信息的DataFrame
        int: 本次获取的最后一条邮件的UID
    """
    mailbox = os.getenv('MAILBOX')
    with IMAPClient(host) as server:
        server.login(username, password)
        server.select_folder(mailbox)

        if last_uid == 0:
            # 获取近3天的日期
            three_days_ago = (datetime.now() - timedelta(days=6)).strftime('%d-%b-%Y')
            # 获取近3天的邮件
            messages = server.search(['SINCE', three_days_ago]) # pyright:ignore 
        else:
            # 获取所有大于last_uid的邮件
            messages = server.search(['UID', f'{last_uid + 1}:*']) # pyright:ignore 
        # 添加 'date' 列
        emails_df = pd.DataFrame(columns=['uid', 'subject', 'from', 'body', 'mail_date']) # pyright:ignore 
        current_max_uid = last_uid

        for uid, message_data in tqdm(
            server.fetch(messages, ['RFC822']).items(),
            desc="Fetching emails",):

            # pyright:ignore
            msg = email.message_from_bytes(message_data[b'RFC822'])# pyright:ignore 
            
            # 对subject进行解码
            subject, encoding = decode_text(msg['subject'])
            
            # 检查CC字段是否包含特定邮箱
            cc = msg['CC']
            if cc and specific_cc_email in cc:
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = \
                                part.get_payload(decode=True).decode( # pyright:ignore 
                                    encoding=encoding, errors='ignore') 
                            break
                else:
                    body = \
                        msg.get_payload(decode=True).decode( # pyright:ignore 
                            encoding=encoding, errors='ignore')
                # 提取邮件时间
                date_str = msg['Date']
                if date_str:
                    try:
                        # 解析日期字符串
                        mail_date = \
                            email.utils.parsedate_to_datetime(date_str) # pyright:ignore 
                    except (TypeError, ValueError):
                        mail_date = None
                else:
                    mail_date = None
                
                emails_df.loc[len(emails_df)] = {
                    'uid': uid,
                    'subject': subject,
                    'from': msg['from'],
                    'body': body,
                    'mail_date': mail_date
                }
            
            # 更新最大UID
            if uid > current_max_uid:
                current_max_uid = uid
    return emails_df, current_max_uid