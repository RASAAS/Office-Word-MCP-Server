"""
Main entry point for the Word Document MCP Server.
Acts as the central controller for the MCP server that handles Word document operations.
"""

import os
import sys
from mcp.server.fastmcp import FastMCP
from word_document_server.tools import (
    document_tools,
    content_tools,
    format_tools,
    protection_tools,
    footnote_tools,
    extended_document_tools
)



# Initialize FastMCP server
mcp = FastMCP("word-document-server")

def register_tools():
    """Register all tools with the MCP server."""
    # Document tools (create, copy, info, etc.)
    mcp.tool()(document_tools.create_document)
    mcp.tool()(document_tools.copy_document)
    mcp.tool()(document_tools.get_document_info)
    mcp.tool()(document_tools.get_document_text)
    mcp.tool()(document_tools.get_document_outline)
    mcp.tool()(document_tools.list_available_documents)
    
    # Content tools (paragraphs, headings, tables, etc.)
    mcp.tool()(content_tools.add_paragraph)
    mcp.tool()(content_tools.add_heading)
    mcp.tool()(content_tools.add_picture)
    mcp.tool()(content_tools.add_table)
    mcp.tool()(content_tools.add_page_break)
    mcp.tool()(content_tools.delete_paragraph)
    mcp.tool()(content_tools.search_and_replace)
    
    # Format tools (styling, text formatting, etc.)
    mcp.tool()(format_tools.create_custom_style)
    mcp.tool()(format_tools.format_text)
    mcp.tool()(format_tools.format_table)
    
    # Protection tools
    mcp.tool()(protection_tools.protect_document)
    mcp.tool()(protection_tools.unprotect_document)
    
    # Footnote tools
    mcp.tool()(footnote_tools.add_footnote_to_document)
    mcp.tool()(footnote_tools.add_endnote_to_document)
    mcp.tool()(footnote_tools.convert_footnotes_to_endnotes_in_document)
    mcp.tool()(footnote_tools.customize_footnote_style)
    
    # Extended document tools
    mcp.tool()(extended_document_tools.get_paragraph_text_from_document)
    mcp.tool()(extended_document_tools.find_text_in_document)
    mcp.tool()(extended_document_tools.convert_to_pdf)


def run_server():
    """Run the Word Document MCP Server."""
    # Register all tools
    register_tools()

    # 从环境变量读取配置，如果未设置则使用默认值
    # 对于 n8n 的 SSE Endpoint，我们通常使用 'sse' 作为传输方式。
    # 'streamable-http' 是 FastMCP 推荐的较新标准，也可以尝试，但 'sse' 更直接。
    server_transport = os.environ.get('MCP_TRANSPORT', 'sse')
    server_host = os.environ.get('MCP_HOST', '0.0.0.0')  # 监听所有可用网络接口
    server_port = int(os.environ.get('MCP_PORT', 8000)) # 默认监听 8000 端口

    # 添加日志输出，方便部署时确认配置
    print(f"Attempting to start MCP server with transport: {server_transport}, host: {server_host}, port: {server_port}")
    sys.stdout.flush() # 确保print能立即输出

    try:
        # Run the server with network transport
        # Host and port are expected to be picked up from environment variables
        # by the underlying server (e.g., Uvicorn) when using network transport.
        mcp.run(
            transport=server_transport
        )
    except Exception as e:
        print(f"Error starting MCP server: {e}") # 打印启动错误
        sys.stdout.flush()
        # 可以选择在这里重新抛出异常或退出
        # raise

    return mcp

if __name__ == "__main__":
    run_server()
