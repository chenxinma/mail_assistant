# MCP Server 模块

## 主要功能

- 初始化 FastMCP 服务器
- 管理 Chroma 客户端连接
- 提供文档查询功能

## 依赖关系

- 使用 chromadb 进行向量数据存储
- 依赖 dotenv 加载环境变量
- 使用 mcp.server.fastmcp 实现 FastMCP 服务器

## 使用示例

```python
from mcp.server.fastmcp import FastMCP

# 初始化服务器
server = FastMCP("fsg_project_assistant")

# 查询文档
result = await server.call_tool("query_documents",
    arguments={
        "query_texts": ["项目进展", "基础人事及法定福利服务交付系统"],
        "n_results": 5,
        "include": ["metadatas", "documents"]
    })
```

## 配置说明

- `CHROMA_HOST`: Chroma 服务器地址
- `CHROMA_PORT`: Chroma 服务器端口
- `CHROMA_COLLECTION_NAME`: Chroma 集合名称