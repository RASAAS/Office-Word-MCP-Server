### **详细改造方案**

#### **第一步：确认并准备项目文件**

确保您在本地的编程工具中打开了 Office-Word-MCP-Server 项目的完整代码。我们需要修改的主要文件是 word\_document\_server/main.py。

#### **第二步：修改 word\_document\_server/main.py**

这是改造的核心。

1. 打开文件：  
   在您的编辑器中，打开路径为 word\_document\_server/main.py 的文件。  
2. 导入 os 模块：  
   在文件的开头部分，我们需要导入 os 模块，以便能够读取环境变量。如果 import os 已经存在，则无需重复添加。  
   Python  
   import os  
   import sys \# 通常已存在  
   from mcp.server.fastmcp import FastMCP  
   from word\_document\_server.tools import (  
       document\_tools,  
       content\_tools,  
       format\_tools,  
       protection\_tools,  
       footnote\_tools,  
       extended\_document\_tools  
   )

3. 修改 run\_server() 函数：  
   找到 run\_server() 函数。当前它看起来是这样的：  
   Python  
   def run\_server():  
       """Run the Word Document MCP Server."""  
       \# Register all tools  
       register\_tools()

       \# Run the server  
       mcp.run(transport='stdio')  
       return mcp

   我们需要修改 mcp.run() 这一行，让它从环境变量读取配置，并使用网络传输模式。  
   **修改后的 run\_server() 函数如下：**  
   Python  
   def run\_server():  
       """Run the Word Document MCP Server."""  
       \# Register all tools  
       register\_tools()

       \# 从环境变量读取配置，如果未设置则使用默认值  
       \# 对于 n8n 的 SSE Endpoint，我们通常使用 'sse' 作为传输方式。  
       \# 'streamable-http' 是 FastMCP 推荐的较新标准，也可以尝试，但 'sse' 更直接。  
       server\_transport \= os.environ.get('MCP\_TRANSPORT', 'sse')  
       server\_host \= os.environ.get('MCP\_HOST', '0.0.0.0')  \# 监听所有可用网络接口  
       server\_port \= int(os.environ.get('MCP\_PORT', 8000)) \# 默认监听 8000 端口

       \# 添加日志输出，方便部署时确认配置  
       print(f"Attempting to start MCP server with transport: {server\_transport}, host: {server\_host}, port: {server\_port}")  
       sys.stdout.flush() \# 确保print能立即输出

       try:  
           \# Run the server with network transport  
           mcp.run(  
               transport=server\_transport,  
               host=server\_host,  
               port=server\_port  
           )  
       except Exception as e:  
           print(f"Error starting MCP server: {e}") \# 打印启动错误  
           sys.stdout.flush()  
           \# 可以选择在这里重新抛出异常或退出  
           \# raise

       return mcp

   * **改动说明**：  
     * 我们使用 os.environ.get('VARIABLE\_NAME', 'default\_value') 来读取环境变量。  
     * MCP\_TRANSPORT: 设置为 sse，这是 n8n SSE 节点期望的模式。  
     * MCP\_HOST: 设置为 0.0.0.0，使得服务器可以从容器外部被访问。  
     * MCP\_PORT: 设置为 8000 作为默认端口，您可以根据需要修改。  
     * 增加了 print 语句，这样当服务通过 pm2 启动时，我们可以在日志中看到它实际使用的配置。  
     * 增加了 try...except 块来捕获并打印 mcp.run() 可能抛出的启动时错误。

#### **第三步：检查并可能更新 requirements.txt**

FastMCP 在网络模式下（如 sse 或 http）通常依赖于 uvicorn 和 starlette。

1. **检查 mcp\[cli\] 的依赖**： mcp\[cli\] 这个依赖项本身可能已经包含了 uvicorn 和 starlette 作为其子依赖。我们先假设它包含了。  
2. **如果部署时报错缺少 uvicorn 或 starlette**： 如果后续部署时，日志显示找不到这些模块，您需要回到您的项目中，编辑 requirements.txt 文件，在其中添加：  
   uvicorn  
   starlette  
   然后重新在虚拟环境中运行 pip install \-r requirements.txt。

#### **第四步：准备部署（PM2 Ecosystem File）**

为了方便地通过 pm2 管理这个改造后的服务并设置环境变量，我们将在项目根目录（与 word\_mcp\_server.py 同级）创建一个 ecosystem.config.js 文件。

1. 在 /opt/Office-Word-MCP-Server/ (服务器上的路径) 或您本地项目根目录下，创建 ecosystem.config.js 文件，内容如下：  
   JavaScript  
   module.exports \= {  
     apps : \[{  
       name        : "mcp-network-server", // 给您的服务起个新名字  
       script      : "word\_mcp\_server.py",  
       interpreter : ".venv/bin/python3",  // 确保指向虚拟环境的python  
       env: {  
         "PYTHONUNBUFFERED": "1",          // 确保Python的输出能立即被pm2捕获  
         "MCP\_DEBUG": "1",                 // 启用MCP的调试日志  
         "MCP\_HOST": "0.0.0.0",  
         "MCP\_PORT": "8000",               // 您希望服务监听的端口  
         "MCP\_TRANSPORT": "sse"            // 传输模式  
       }  
     }\]  
   }

   * PYTHONUNBUFFERED=1: 确保 print 语句的输出能被 pm2 实时捕获。  
   * 这里我们直接在 ecosystem.config.js 中设置了环境变量。

### ---

**改造后的部署流程**

1. 将修改后的代码同步到服务器：  
   如果您是在本地修改的代码，请将修改后的 word\_document\_server/main.py 和新增的 ecosystem.config.js 文件上传到服务器的 /opt/Office-Word-MCP-Server/ 目录下（覆盖原有文件）。  
2. **登录服务器并进入项目目录**。  
   Bash  
   cd /opt/Office-Word-MCP-Server

3. **确保虚拟环境和依赖最新**：  
   Bash  
   source .venv/bin/activate  
   pip install \-r requirements.txt \# 如果您修改了 requirements.txt，务必执行此步  
   deactivate \# 可以退出虚拟环境，因为pm2会用指定的解释器

4. **使用 PM2 启动服务**：  
   Bash  
   pm2 start ecosystem.config.js

5. **验证服务**：  
   * pm2 list: 检查 mcp-network-server 状态是否为 online。  
   * pm2 logs mcp-network-server: 查看日志。您应该能看到我们添加的 print 语句，显示它尝试启动的 host、port 和 transport。如果启动失败，这里会有详细的 Python Traceback。  
   * sudo ss \-lntp | grep 8000 (或者您设置的其他端口)：确认进程正在监听指定端口。  
6. **配置 1panel 反向代理**：  
   * 在 1panel 中创建反向代理，将您的域名指向 http://127.0.0.1:8000 (或您在 ecosystem.config.js 中设置的 MCP\_PORT)。  
7. **在 n8n 中配置**：  
   * n8n 节点的 "SSE Endpoint" 应该填写为您的域名，加上 / （因为 FastMCP SSE 通常直接在根路径提供服务，除非其文档另有说明）。例如：http://your-mcp-domain.com/

---

这个详细的方案是要将项目改造成一个网络服务器。最关键的是查阅 FastMCP 库关于 mcp.run() 网络传输模式的确切用法，以确保我们使用的 transport, host, port 参数是正确的。我提供的 'sse' 和 'streamable-http' 是基于通用 MCP 实现的推测，具体请以 FastMCP 的文档为准。