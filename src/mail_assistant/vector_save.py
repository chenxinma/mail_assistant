"""将获取邮件内容的结果保存到向量数据库中"""
from dotenv import load_dotenv
import os
import warnings

import duckdb
import pandas as pd
from tqdm.rich import tqdm
from tqdm import TqdmExperimentalWarning
import chromadb
from chromadb.api.types import IncludeEnum

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# 过滤 TqdmExperimentalWarning 警告
warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

def make_agent():
    base_url = os.getenv('LLM_BASE_URL')
    api_key = os.getenv('LLM_API_KEY')

    df_set_project = pd.read_excel('./files/IT建设项目清单250320.xlsx', sheet_name=None)
    projects: list[str] = df_set_project['双周会组']['项目名称'].to_list() # pyright: ignore
    projects.extend(df_set_project['其他组']['项目名称'].to_list())
    project_list = "\n".join(["+ " + p for p in projects])

    _model = OpenAIModel('qwq', provider=OpenAIProvider(
                      base_url=base_url,
                      api_key=api_key
                  ))

    agent = Agent(_model, 
                  result_type=str,
                  system_prompt=(
                      f"""根据以下项目清单，简单标注所属项目。 
    ## 项目清单:
    {project_list}
    注意：仅输出项目名称，不包含其他内容。
    请尽量缩短思考过程。
    ## 输出样例：
    薪税生产系统二期建设项目
    """))

    return agent

def wrap_output(text:str) -> str:
    key = '</think>'
    return text.split(key)[1].replace('\n', '')

def get_last_uid_in_vector_db(chroma_client, collect_name) -> int:
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

def save_mail2vector():
    """
    从 db 目录下读取 Parquet 文件，为每一行邮件信息增量地打上标签。
    """
    chroma_host = os.getenv('CHROMA_HOST', '')
    chroma_port = int(os.getenv('CHROMA_PORT', '0'))
    chroma_client = \
        chromadb.HttpClient(host=chroma_host, port=chroma_port)
    collect_name = "fsg_project_mail"

    # 定义 db 目录路径
    db_dir = 'db'
    # 检查 db 目录是否存在
    if not os.path.exists(db_dir):
        print(f"目录 {db_dir} 不存在。")
        return

    last_uid = get_last_uid_in_vector_db(chroma_client, collect_name)
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

    agent = make_agent()
    def get_project(row) -> str:
        result = agent.run_sync(f"标题：{row['subject']}")
        return wrap_output(result.data)

    # 为每一行邮件信息打上项目标签
    tqdm.pandas(desc="Annotating projects...")
    df["project"] = df.progress_apply(get_project, axis=1)
    df["mail_date_str"] = df["mail_date"].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    collection = chroma_client.get_collection(name=collect_name)
    collection.add(
        documents = df.apply(lambda x: f"{x['project']} \n {x['subject']} \n {x['body']}", axis=1).to_list(),
        metadatas = df[["project", "from", "mail_date_str"]].to_dict(orient="records"), # pyright: ignore
        ids = [str(id) for id in df["uid"].to_list()]
    )

if __name__ == "__main__":
    # 加载.env文件
    load_dotenv()
    save_mail2vector()
