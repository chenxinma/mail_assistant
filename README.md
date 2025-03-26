# 邮件助手项目

## 项目简介
本项目是一个邮件助手工具，旨在帮助用户高效地读取个人邮箱中的邮件，并对特定范围内的邮件内容进行整理。借助大语言模型，该工具能够对整理后的邮件内容进行汇总，生成易于查询的摘要信息，从而提升用户处理邮件的效率和便捷性。

## 项目用途
- **邮件读取**：支持连接到多种主流邮箱服务，如 Gmail、Outlook、QQ 邮箱等，方便用户读取个人邮箱中的邮件。
- **内容整理**：允许用户指定特定的邮件范围，如日期区间、发件人、主题等，工具会自动筛选并整理符合条件的邮件内容。
- **大模型汇总**：利用先进的大语言模型对整理后的邮件内容进行分析和汇总，生成简洁明了的摘要信息，便于用户快速了解邮件的核心内容。
- **便捷查询**：提供方便的查询接口，用户可以根据关键词、时间等条件快速定位和查看所需的邮件摘要。

## 安装与使用
### 安装依赖
在项目根目录下运行以下命令安装所需的依赖：
```bash
pip install -e .
```

### 配置环境变量
1. 在项目根目录下创建一个名为`.env`的文件。
2. 在`.env`文件中添加以下环境变量：
```
IMAP_HOST=imap.example.com
IMAP_USERNAME=your_email@example.com
IMAP_PASSWORD=your_password
MAILBOX=INBOX/example

LLM_BASE_URL=http://example.com/v1
LLM_API_KEY=your_api_key

CHROMA_HOST=example.com
CHROMA_PORT=31302
```
3. 将`IMAP_HOST`、`IMAP_USERNAME`和`IMAP_PASSWORD`替换为你实际使用的邮箱服务信息。
4. 确保`.env`文件不被提交到版本控制系统中（例如，将其添加到`.gitignore`文件中）。

## 使用场景
- **个人邮件管理**：帮助用户快速整理和汇总个人邮箱中的邮件，节省阅读时间。
- **团队协作**：团队成员可以通过该工具快速了解邮件讨论的核心内容，提高沟通效率。
- **邮件归档**：对历史邮件进行整理和归档，便于后续查询和参考。

## 注意事项
- 请确保`.env`文件中的邮箱信息准确无误，否则可能导致无法正常读取邮件。
- 使用大模型汇总功能时，建议在本地环境中运行，以确保数据安全。
- chroma 在windows运行需要复制
    api-ms-win-core-console-l1-1-0.dll
    api-ms-win-core-console-l1-2-0.dll
    api-ms-win-core-datetime-l1-1-0.dll
    api-ms-win-core-debug-l1-1-0.dll
    api-ms-win-core-errorhandling-l1-1-0.dll
    api-ms-win-core-fibers-l1-1-0.dll
    api-ms-win-core-file-l1-1-0.dll
    api-ms-win-core-file-l1-2-0.dll
    api-ms-win-core-file-l2-1-0.dll
    api-ms-win-core-handle-l1-1-0.dll
    api-ms-win-core-heap-l1-1-0.dll
    api-ms-win-core-interlocked-l1-1-0.dll
    api-ms-win-core-libraryloader-l1-1-0.dll
    api-ms-win-core-localization-l1-2-0.dll
    api-ms-win-core-memory-l1-1-0.dll
    api-ms-win-core-namedpipe-l1-1-0.dll
    api-ms-win-core-processenvironment-l1-1-0.dll
    api-ms-win-core-processthreads-l1-1-0.dll
    api-ms-win-core-processthreads-l1-1-1.dll
    api-ms-win-core-profile-l1-1-0.dll
    api-ms-win-core-rtlsupport-l1-1-0.dll
    api-ms-win-core-string-l1-1-0.dll
    api-ms-win-core-synch-l1-1-0.dll
    api-ms-win-core-synch-l1-2-0.dll
    api-ms-win-core-sysinfo-l1-1-0.dll
    api-ms-win-core-timezone-l1-1-0.dll
    api-ms-win-core-util-l1-1-0.dll
    api-ms-win-crt-conio-l1-1-0.dll
    api-ms-win-crt-convert-l1-1-0.dll
    api-ms-win-crt-environment-l1-1-0.dll
    api-ms-win-crt-filesystem-l1-1-0.dll
    api-ms-win-crt-heap-l1-1-0.dll
    api-ms-win-crt-locale-l1-1-0.dll
    api-ms-win-crt-math-l1-1-0.dll
    api-ms-win-crt-multibyte-l1-1-0.dll
    api-ms-win-crt-private-l1-1-0.dll
    api-ms-win-crt-process-l1-1-0.dll
    api-ms-win-crt-runtime-l1-1-0.dll
    api-ms-win-crt-stdio-l1-1-0.dll
    api-ms-win-crt-string-l1-1-0.dll
    api-ms-win-crt-time-l1-1-0.dll
    api-ms-win-crt-utility-l1-1-0.dll
    concrt140.dll
    LICENSE_PYTHON.txt
    list.txt
    msvcp140.dll
    msvcp140_1.dll
    msvcp140_2.dll
    msvcp140_atomic_wait.dll
    msvcp140_codecvt_ids.dll
    ucrtbase.dll
    vccorlib140.dll
    vcomp140.dll
    vcruntime140_threads.dll
    zlib.dll
