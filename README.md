# Office Word MCP Server

一个用于Microsoft Word文档操作的Model Context Protocol (MCP)服务器。该服务器通过MCP协议提供全面的Word文档创建、编辑和管理工具，专为n8n等自动化平台设计。

## 功能特性

### 📄 文档管理 (7个工具)
- 创建新的Word文档
- 获取文档信息和元数据
- 复制和合并文档
- 列出可用文档
- 获取文档大纲结构

### ✏️ 内容操作 (9个工具)
- 添加标题（多级别）
- 插入段落文本
- 创建和管理表格
- 插入图片和图像
- 添加分页符
- 生成目录
- 查找和替换文本
- 删除段落

### 🎨 格式化 (3个工具)
- 文本格式化（粗体、斜体、下划线等）
- 创建自定义样式
- 表格格式化

### 🔒 文档保护 (5个工具)
- 文档密码保护
- 数字签名
- 限制编辑模式
- 文档验证

### 📝 脚注管理 (4个工具)
- 添加脚注和尾注
- 自定义脚注样式
- 脚注格式转换

### 🔧 扩展功能 (3个工具)
- PDF转换
- 文本搜索和提取
- 段落文本获取

**总计：31个验证可用的工具**

## 快速开始

### 环境要求
- Python 3.8+
- pip包管理器
- PM2进程管理器（可选，用于生产环境）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd Office-Word-MCP-Server
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **启动服务器**

**方法1：直接启动（开发环境）**
```bash
python3 simple_server.py
```

**方法2：使用PM2（生产环境推荐）**
```bash
# 安装PM2（如果未安装）
npm install -g pm2

# 启动服务
pm2 start pm2.config.js

# 查看状态
pm2 status

# 查看日志
pm2 logs office-word-mcp-server
```

4. **验证服务**
```bash
curl http://127.0.0.1:8000
# 应该返回HTTP 404（正常，说明服务器在运行）
```

## n8n集成配置

在n8n中使用MCP Client Tool节点：

### 配置参数
- **Server URL**: `http://YOUR_SERVER_IP:8000`
- **Transport**: `streamable-http` 或 `http`
- **Port**: `8000`

### 示例配置
```json
{
  "serverUrl": "http://192.168.1.100:8000",
  "transport": "streamable-http"
}
```

## 项目结构

```
Office-Word-MCP-Server/
├── simple_server.py              # 主服务器文件（推荐使用）
├── pm2.config.js                 # PM2配置文件
├── requirements.txt              # Python依赖
├── pyproject.toml               # 项目配置
├── LICENSE                      # 许可证
├── README.md                    # 项目说明
├── DEPLOYMENT.md                # 部署说明
└── word_document_server/        # 核心功能模块
    ├── main.py                  # 备用启动文件（支持多传输协议）
    ├── __init__.py
    ├── tools/                   # 工具实现（31个工具）
    ├── core/                    # 核心功能
    └── utils/                   # 工具函数
```

## 故障排除

### 常见问题

1. **服务器无法启动**
```bash
# 检查Python版本
python3 --version

# 检查依赖安装
pip list | grep mcp

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

2. **PM2进程异常**
```bash
# 查看PM2状态
pm2 status

# 查看详细日志
pm2 logs office-word-mcp-server --lines 50

# 重启服务
pm2 restart office-word-mcp-server
```

3. **端口占用**
```bash
# 检查端口使用
netstat -tlnp | grep 8000

# 杀死占用进程
sudo kill -9 <PID>
```

## 技术规格

- **传输协议**: Streamable HTTP (推荐)
- **端口**: 8000 (默认)
- **Python版本**: 3.8+
- **主要依赖**: python-docx, mcp, uvicorn
- **进程管理**: PM2 (生产环境)

## 许可证

MIT License - 详见LICENSE文件

## 支持

如有问题或建议：
1. 检查现有的GitHub Issues
2. 创建新的Issue并提供详细信息
3. 包含错误信息和重现步骤

## 更新日志

### Version 1.0.0 (当前版本)
- ✅ 31个验证可用的Word文档操作工具
- ✅ 稳定的Streamable HTTP传输
- ✅ 完整的n8n集成支持
- ✅ PM2生产环境部署
- ✅ 全面的错误处理和日志记录
