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

# Initialize FastMCP instance globally
mcp = FastMCP("Office Word MCP Server")

def register_tools():
    """Register all toolsets with the MCP server."""

    # Content Tools - Only register tools that actually exist
    mcp.add_tool(content_tools.search_and_replace)
    mcp.add_tool(content_tools.get_document_text_content)
    mcp.add_tool(content_tools.delete_paragraph)
    mcp.add_tool(content_tools.add_heading)
    mcp.add_tool(content_tools.add_paragraph)
    mcp.add_tool(content_tools.add_table)
    mcp.add_tool(content_tools.add_picture)
    mcp.add_tool(content_tools.add_page_break)
    mcp.add_tool(content_tools.add_table_of_contents)

    # Document Tools - Only register tools that actually exist
    mcp.add_tool(document_tools.create_document)
    mcp.add_tool(document_tools.get_document_info)
    mcp.add_tool(document_tools.get_document_text)
    mcp.add_tool(document_tools.get_document_outline)
    mcp.add_tool(document_tools.list_available_documents)
    mcp.add_tool(document_tools.copy_document)
    mcp.add_tool(document_tools.merge_documents)

    # Extended Document Tools - Only register tools that actually exist
    mcp.add_tool(extended_document_tools.get_paragraph_text_from_document)
    mcp.add_tool(extended_document_tools.find_text_in_document)
    mcp.add_tool(extended_document_tools.convert_to_pdf)

    # Format Tools - Only register tools that actually exist
    mcp.add_tool(format_tools.format_text)
    mcp.add_tool(format_tools.create_custom_style)
    mcp.add_tool(format_tools.format_table)

    # Protection Tools - Only register tools that actually exist
    mcp.add_tool(protection_tools.protect_document)
    mcp.add_tool(protection_tools.unprotect_document)
    mcp.add_tool(protection_tools.verify_document)
    mcp.add_tool(protection_tools.add_restricted_editing)
    mcp.add_tool(protection_tools.add_digital_signature)

    # Footnote Tools - Only register tools that actually exist
    mcp.add_tool(footnote_tools.add_footnote_to_document)
    mcp.add_tool(footnote_tools.add_endnote_to_document)
    mcp.add_tool(footnote_tools.convert_footnotes_to_endnotes_in_document)
    mcp.add_tool(footnote_tools.customize_footnote_style)

    print("All verified tools registered successfully.")
    sys.stdout.flush()

def run_server():
    """Run the Word Document MCP Server."""
    register_tools()

    server_transport = os.environ.get('MCP_TRANSPORT', 'sse')
    # Prefer UVICORN_HOST/PORT if set, otherwise MCP_HOST/PORT, then defaults
    server_host = os.environ.get('UVICORN_HOST', os.environ.get('MCP_HOST', '0.0.0.0'))
    server_port_str = os.environ.get('UVICORN_PORT', os.environ.get('MCP_PORT', '8000'))
    
    try:
        server_port = int(server_port_str)
    except ValueError:
        print(f"Warning: Port environment variable '{server_port_str}' is not a valid integer. Using default 8000.")
        sys.stdout.flush()
        server_port = 8000

    print(f"Attempting to start MCP server.")
    print(f"Transport: {server_transport}")
    print(f"Host: {server_host}")
    print(f"Port: {server_port}")
    sys.stdout.flush()

    try:
        if server_transport == 'sse':
            print(f"Using SSE transport. Starting server with mcp.run().")
            sys.stdout.flush()
            # For SSE transport, use default configuration without mount_path
            mcp.run(transport="sse")
        elif server_transport == 'stdio':
            print(f"Using STDIO transport. Starting server with mcp.run().")
            sys.stdout.flush()
            mcp.run(transport="stdio")
        elif server_transport == 'streamable-http':
            print(f"Using Streamable HTTP transport. Starting server with mcp.run().")
            sys.stdout.flush()
            # Streamable HTTP is the recommended transport for production
            mcp.run(transport="streamable-http")
        else:
            # Default to stdio for unknown transports
            print(f"Unknown transport '{server_transport}', falling back to STDIO.")
            sys.stdout.flush()
            mcp.run(transport="stdio")
    except TypeError as te:
        # This might still occur for non-SSE transports if mcp.run has issues
        print(f"TypeError during server startup for transport '{server_transport}': {te}")
        print("This likely means host/port are not accepted for this transport or were passed incorrectly by mcp.run itself.")
        sys.stdout.flush()
        # Fallback for non-stdio transports if host/port caused TypeError with mcp.run
        if server_transport not in ['stdio', 'sse']: # SSE is now handled by uvicorn.run directly
             print(f"Attempting fallback for '{server_transport}': mcp.run(transport='{server_transport}') without host/port.")
             sys.stdout.flush()
             try:
                 mcp.run(transport=server_transport)
             except Exception as e_fallback:
                 print(f"Error during fallback mcp.run for transport '{server_transport}': {e_fallback}")
                 sys.stdout.flush()
    except Exception as e:
        print(f"Generic error starting MCP server with transport '{server_transport}': {e}")
        sys.stdout.flush()
        # raise # Optionally re-raise to make PM2 mark as errored

    # This return is not strictly necessary if the server runs indefinitely
    # return mcp 

# The entry point for PM2 is word_mcp_server.py, which should import and call run_server().
if __name__ == '__main__':
    print(f"{__file__} executed directly. Starting server...")
    sys.stdout.flush()
    run_server()
