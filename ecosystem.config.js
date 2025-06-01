module.exports = {
  apps : [{
    name        : "mcp-network-server", // 给您的服务起个新名字
    script      : "word_mcp_server.py",
    interpreter : ".venv/bin/python3",  // 确保指向虚拟环境的python
    env: {
      "PYTHONUNBUFFERED": "1",          // 确保Python的输出能立即被pm2捕获
      "MCP_DEBUG": "1",                 // 启用MCP的调试日志
      "MCP_HOST": "0.0.0.0",
      "MCP_PORT": "8000",               // 您希望服务监听的端口
      "MCP_TRANSPORT": "sse"            // 传输模式
    }
  }]
}
