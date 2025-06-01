module.exports = {
  apps : [{
    name        : "office-word-mcp-server",
    script      : "simple_server.py",
    interpreter : "python3",
    env: {
      "PYTHONUNBUFFERED": "1"
    }
  }]
}
