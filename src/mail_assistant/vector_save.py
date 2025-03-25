"""将获取邮件内容的结果保存到向量数据库中"""
import os
import duckdb
import chromadb
from chromadb.api.types import IncludeEnum

chroma_client = chromadb.HttpClient(host='rke2.fsg.local', port=31302)
collect_name = "fsg_project_mail"

def get_last_uid_in_vector_db() -> int:
    """
    获取向量数据库中最后一条邮件的 uid。
    """
    collection = chroma_client.get_or_create_collection(name=collect_name)
    offset = collection.count() - 1
    if offset < 0:
        return 0

    result = collection.get(include=[IncludeEnum.metadatas],offset=offset)
    if result:
        return int(result['ids'][0])
    else:
        return 0

def save_mail2vector(last_uid: int = 0):
    """
    从 db 目录下读取 Parquet 文件，为每一行邮件信息增量地打上标签。
    """
    # 定义 db 目录路径
    db_dir = 'db'
    # 检查 db 目录是否存在
    if not os.path.exists(db_dir):
        print(f"目录 {db_dir} 不存在。")
        return

    # 连接到 duckdb 数据库
    with duckdb.connect() as conn:
        # 读取 Parquet 文件
        query = f"""SELECT * 
                                   FROM read_parquet('db/*.parquet')
                                   WHERE uid > $last_uid"""
        df = conn.execute(query, dict(last_uid=last_uid)).fetch_df()

    print("new mails: ", df.shape[0])
    if df.empty:
        return
    
    collection = chroma_client.get_collection(name=collect_name)
    collection.add(
        documents=df.apply(lambda x: f"{x['subject']} \n {x['body']}", axis=1).to_list(),
        ids=[str(id) for id in df["uid"].to_list()]
    )

if __name__ == "__main__":
    last_uid = get_last_uid_in_vector_db()
    save_mail2vector(last_uid)
