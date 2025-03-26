import marimo

__generated_with = "0.11.20"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(mo):
    df_mail = mo.sql(
        f"""
        SELECT * FROM read_parquet('./db/*.parquet')
        """
    )
    return (df_mail,)


@app.cell
def _(pd):
    df_set_project = pd.read_excel('./files/IT建设项目清单250320.xlsx', sheet_name=None)
    projects = df_set_project['双周会组']['项目名称'].to_list()
    projects.extend(df_set_project['其他组']['项目名称'].to_list())
    project_list = "\n".join(["+ " + p for p in projects])
    return df_set_project, project_list, projects


@app.cell
def _(project_list):
    project_list
    return


@app.cell
def _(project_list):
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIModel
    from pydantic_ai.providers.openai import OpenAIProvider

    _model = OpenAIModel('qwq', provider=OpenAIProvider(
                      base_url="http://172.16.37.21:8000/v1",
                      api_key="fsg-abc123"
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
    """
                  ))

    agent_summary = Agent(_model, 
                  result_type=str,
                  system_prompt=(
                      f"""根据周报整理项目进展和风险事项。
    输出格式：

    * 项目进展：* XXXXXXX

    * 项目风险：* YYYYYYY
    """
                  ))
    return Agent, OpenAIModel, OpenAIProvider, agent, agent_summary


@app.cell
def wrap_output():
    def wrap_output(text:str) -> str:
        key = '</think>'
        return text.split(key)[1].replace('\n', '')
    return (wrap_output,)


@app.cell
async def _(agent, agent_summary, df_mail, wrap_output):
    from tqdm import tqdm
    import asyncio

    project_mark = []

    async def mark_mail(row):
        prompt = f"标题：{row.subject}"
        result = await agent.run(prompt)
        project_mark.append(wrap_output(result.data))

    df_mail_marked = df_mail.to_pandas()

    for row in tqdm(df_mail_marked.itertuples(), 
                    total=df_mail_marked.shape[0]):
        await mark_mail(row)

    df_mail_marked["project"] = project_mark

    summary = []

    async def summary_mail(row):
        prompt = f"周报：{row.body}"
        result = await agent_summary.run(prompt)
        summary.append(wrap_output(result.data))

    for _row in tqdm(df_mail_marked.itertuples(), 
                    total=df_mail_marked.shape[0]):
        await summary_mail(_row)

    df_mail_marked["summary"] = summary

    df_mail_marked.to_parquet("./files/mail.parquet")
    return (
        asyncio,
        df_mail_marked,
        mark_mail,
        project_mark,
        row,
        summary,
        summary_mail,
        tqdm,
    )


@app.cell
def _(df_mail_marked, mo):
    df_summary = mo.sql(
        f"""
        SELECT project,summary FROM
        df_mail_marked
        """
    )
    return (df_summary,)


@app.cell
def _(df_summary):
    df_summary.to_pandas().to_excel("files/项目摘要.xlsx")
    return


@app.cell
def _():
    import chromadb
    chroma_client = chromadb.HttpClient(host='rke2.fsg.local', port=31302)
    return chroma_client, chromadb


@app.cell
def _():
    # chroma_client.delete_collection("fsg_project_mail")
    # collection = chroma_client.create_collection(name="fsg_project_mail")
    return


@app.cell
def _(chroma_client):
    collection = chroma_client.get_collection(name="fsg_project_mail")
    return (collection,)


@app.cell
def _():
    # df_mail.to_pandas().apply(lambda x: f"{x['subject']} \n {x['body']}", axis=1).to_list()
    # collection.add(
    #     documents=df_mail.to_pandas().apply(lambda x: f"{x['subject']} \n {x['body']}", axis=1).to_list(),
    #     ids=[str(id) for id in df_mail["uid"].to_list()]
    # )
    return


@app.cell
def _(collection):
    results = collection.query(
        query_texts=["基础人事及法定福利服务交付系统的项目进展"], # Chroma will embed this for you
        n_results=2 # how many results to return
    )
    for doc in results['documents'][0]:
        print(doc[:100])
        print("------------------")
    return doc, results


@app.cell
def _(collection):
    collection.get(include=["metadatas"])
    return


@app.cell
def _(collection):
    collection.query(
        query_texts=["速创解耦项目进展"], # Chroma will embed this for you
        where={"project": "速创解耦项目（一期）-订单中心一期"},
        n_results=2 # how many results to return
    )
    return


if __name__ == "__main__":
    app.run()
