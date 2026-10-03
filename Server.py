from fastmcp import FastMCP

mcp = FastMCP("Security Helper")

@mcp.tool()
def ping() -> str:
    """Работа сервера"""
    return "Сервер работает"

if __name__ == "__main__":
    mcp.run()