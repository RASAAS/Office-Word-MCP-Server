#!/usr/bin/env python3
"""
Simple MCP server using streamable-http transport only.
"""

import sys
from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("Office Word MCP Server")

# Add a simple test tool to verify it's working
@mcp.tool()
def echo_test(message: str) -> str:
    """Simple echo test tool"""
    return f"Server is working! Echo: {message}"

# Import and register all the Word document tools
try:
    from word_document_server.tools import (
        document_tools,
        content_tools,
        format_tools,
        protection_tools,
        footnote_tools,
        extended_document_tools
    )
    
    # Content Tools
    mcp.add_tool(content_tools.search_and_replace)
    mcp.add_tool(content_tools.get_document_text_content)
    mcp.add_tool(content_tools.delete_paragraph)
    mcp.add_tool(content_tools.add_heading)
    mcp.add_tool(content_tools.add_paragraph)
    mcp.add_tool(content_tools.add_table)
    mcp.add_tool(content_tools.add_picture)
    mcp.add_tool(content_tools.add_page_break)
    mcp.add_tool(content_tools.add_table_of_contents)

    # Document Tools
    mcp.add_tool(document_tools.create_document)
    mcp.add_tool(document_tools.get_document_info)
    mcp.add_tool(document_tools.get_document_text)
    mcp.add_tool(document_tools.get_document_outline)
    mcp.add_tool(document_tools.list_available_documents)
    mcp.add_tool(document_tools.copy_document)
    mcp.add_tool(document_tools.merge_documents)

    # Extended Document Tools
    mcp.add_tool(extended_document_tools.get_paragraph_text_from_document)
    mcp.add_tool(extended_document_tools.find_text_in_document)
    mcp.add_tool(extended_document_tools.convert_to_pdf)

    # Format Tools
    mcp.add_tool(format_tools.format_text)
    mcp.add_tool(format_tools.create_custom_style)
    mcp.add_tool(format_tools.format_table)

    # Protection Tools
    mcp.add_tool(protection_tools.protect_document)
    mcp.add_tool(protection_tools.unprotect_document)
    mcp.add_tool(protection_tools.verify_document)
    mcp.add_tool(protection_tools.add_restricted_editing)
    mcp.add_tool(protection_tools.add_digital_signature)

    # Footnote Tools
    mcp.add_tool(footnote_tools.add_footnote_to_document)
    mcp.add_tool(footnote_tools.add_endnote_to_document)
    mcp.add_tool(footnote_tools.convert_footnotes_to_endnotes_in_document)
    mcp.add_tool(footnote_tools.customize_footnote_style)
    
    print("✅ All Word document tools registered successfully")
    
except Exception as e:
    print(f"⚠️ Warning: Could not register some tools: {e}")
    print("Server will still start with basic functionality")

if __name__ == "__main__":
    print("🚀 Starting Office Word MCP Server with Streamable HTTP")
    print("=" * 55)
    
    try:
        # Use streamable-http transport directly
        mcp.run(transport="streamable-http")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)
