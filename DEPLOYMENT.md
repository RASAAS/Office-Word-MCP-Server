# Office Word MCP Server - 部署说明

## 项目概述

Office Word MCP Server 是一个基于Model Context Protocol (MCP)的Word文档操作服务器，提供31个验证可用的Word文档处理工具，专为n8n等自动化平台设计。

## 核心文件说明

### 必要文件
- `simple_server.py` - 主服务器文件（推荐使用）
- `pm2.config.js` - PM2进程管理配置
- `requirements.txt` - Python依赖列表
- `pyproject.toml` - 项目配置文件
- `word_document_server/` - 核心功能模块目录

### 可选文件
- `word_document_server/main.py` - 备用服务器启动文件

## 快速部署

### 1. 环境准备

**系统要求：**
- Python 3.8+
- pip包管理器
- PM2进程管理器（生产环境推荐）

**安装PM2（如果需要）：**
```bash
npm install -g pm2
```

### 2. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 或者手动安装核心依赖
pip install mcp python-docx msoffcrypto-tool docx2pdf uvicorn starlette
```

### 3. 启动服务

**开发环境（直接启动）：**
```bash
python3 simple_server.py
```

**生产环境（PM2管理）：**
```bash
# 启动服务
pm2 start pm2.config.js

# 查看状态
pm2 status

# 查看日志
pm2 logs office-word-mcp-server
```

### 4. 验证部署

```bash
# 测试HTTP连接
curl http://127.0.0.1:8000
# 预期返回：HTTP 404 Not Found（正常，说明服务器运行中）

# 检查端口监听
netstat -tlnp | grep 8000
```

## n8n集成配置

### MCP Client Tool节点配置

在n8n工作流中添加MCP Client Tool节点，配置如下：

**基本配置：**
- **Server URL**: `http://YOUR_SERVER_IP:8000`
- **Transport**: `streamable-http`
- **Timeout**: `30000` (30秒)

**示例配置JSON：**
```json
{
  "serverUrl": "http://192.168.1.100:8000",
  "transport": "streamable-http",
  "timeout": 30000
}
```

### 可用工具分类

**文档管理工具 (7个)：**
- create_document, get_document_info, get_document_text
- get_document_outline, list_available_documents
- copy_document, merge_documents

**内容操作工具 (9个)：**
- add_heading, add_paragraph, add_table, add_picture
- add_page_break, add_table_of_contents
- search_and_replace, get_document_text_content, delete_paragraph

**格式化工具 (3个)：**
- format_text, create_custom_style, format_table

**文档保护工具 (5个)：**
- protect_document, unprotect_document, verify_document
- add_restricted_editing, add_digital_signature

**脚注管理工具 (4个)：**
- add_footnote_to_document, add_endnote_to_document
- convert_footnotes_to_endnotes_in_document, customize_footnote_style

**扩展功能工具 (3个)：**
- get_paragraph_text_from_document, find_text_in_document, convert_to_pdf

## 监控和维护

### 日志管理

**PM2日志：**
```bash
# 查看实时日志
pm2 logs office-word-mcp-server

# 查看最近50行日志
pm2 logs office-word-mcp-server --lines 50

# 清空日志
pm2 flush office-word-mcp-server
```

**直接运行日志：**
```bash
# 前台运行查看日志
python3 simple_server.py
```

### 进程管理

**PM2常用命令：**
```bash
# 查看状态
pm2 status

# 重启服务
pm2 restart office-word-mcp-server

# 停止服务
pm2 stop office-word-mcp-server

# 删除服务
pm2 delete office-word-mcp-server

# 监控面板
pm2 monit
```

### 性能监控

**系统资源：**
```bash
# 查看内存使用
pm2 list

# 查看详细信息
pm2 show office-word-mcp-server
```

**网络连接：**
```bash
# 检查端口状态
netstat -tlnp | grep 8000

# 测试连接
curl -I http://127.0.0.1:8000
```

## 故障排除

### 常见问题

**1. 服务无法启动**
```bash
# 检查Python版本
python3 --version

# 检查MCP安装
python3 -c "import mcp; print('MCP OK')"

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

**2. 端口冲突**
```bash
# 查找占用进程
sudo lsof -i :8000

# 杀死进程
sudo kill -9 <PID>
```

**3. PM2进程异常**
```bash
# 完全重启PM2
pm2 kill
pm2 start pm2.config.js
```

### 错误代码说明

- **HTTP 404**: 正常响应，服务器运行中
- **HTTP 500**: 服务器内部错误，检查日志
- **连接拒绝**: 服务未启动或端口被占用
- **超时**: 网络问题或服务器负载过高

## 安全配置

### 网络安全

**防火墙配置：**
```bash
# 允许8000端口（Ubuntu/Debian）
sudo ufw allow 8000

# 或者只允许特定IP访问
sudo ufw allow from 192.168.1.0/24 to any port 8000
```

**反向代理（可选）：**
使用Nginx或Apache作为反向代理，提供HTTPS支持。

### 文件权限

```bash
# 设置适当的文件权限
chmod 755 simple_server.py
chmod 644 pm2.config.js
chmod 644 requirements.txt
```

## 备份和恢复

### 备份重要文件

```bash
# 创建备份目录
mkdir -p backup/$(date +%Y%m%d)

# 备份核心文件
cp simple_server.py backup/$(date +%Y%m%d)/
cp pm2.config.js backup/$(date +%Y%m%d)/
cp requirements.txt backup/$(date +%Y%m%d)/
cp -r word_document_server backup/$(date +%Y%m%d)/
```

### 恢复服务

```bash
# 停止当前服务
pm2 delete office-word-mcp-server

# 恢复文件
cp -r backup/YYYYMMDD/* ./

# 重新安装依赖
pip install -r requirements.txt

# 启动服务
pm2 start pm2.config.js
```

## 技术规格

**服务器规格：**
- 传输协议: Streamable HTTP
- 默认端口: 8000
- 进程管理: PM2
- 日志级别: INFO

**依赖版本：**
- Python: 3.8+
- MCP: 最新版本
- python-docx: 0.8.11+
- uvicorn: 0.24.0+

**系统要求：**
- 内存: 最少512MB，推荐1GB+
- 磁盘: 最少100MB可用空间
- 网络: 支持HTTP协议

## 联系支持

如遇到部署问题：
1. 检查日志文件获取详细错误信息
2. 确认所有依赖正确安装
3. 验证网络配置和防火墙设置
4. 提供完整的错误日志和系统信息
