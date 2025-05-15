from enum import Enum
from typing import List
from fastmcp import FastMCP
import httpx

# Create an MCP server
mcp = FastMCP("Demo")

# Add empty list of dependencies to prevent TypeError
mcp.dependencies = []

base_url = "http://localhost:5143/api"

class Entity(str,Enum):
    Account = "Account",
    Customer = "Customer",
    Bill = "Bill",

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"Adding {a} and {b}")
    return a + b

@mcp.tool(name = "Available_Entities", description= "Fetch list of entities or tables", tags=["Entities", "table"])
async def fetch_entities() -> str:
    """Fetch list of entities or tables"""
    print("Fetching entities")
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{base_url}/Entity/",
            follow_redirects=True,
        )
        print(response.text)
        return response.text
    
@mcp.tool(name = "Available_Related_Entities", description= "Fetch list of related entities or related tables", tags=[" realted Entities", " related table"])
async def fetch_entities(entity : Entity) -> str:
    """Fetch list of related entities or tables"""
    print("Fetching related entities")
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{base_url}/Entity/{entity.value}/related",
            follow_redirects=True,
        )
        print(response.text)
        return response.text
    
@mcp.tool(name = "Available_Fields_For_entity", description= "Fetch list of fields for entity or table", tags=["fields", " coulmns"])
async def fetch_entities(entity : Entity) -> str:
    """Fetch list of fields or columns for entity"""
    print("Fetching fields")
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{base_url}/Entity/{entity.value}/fields",
            follow_redirects=True,
        )
        print(response.text)
        return response.text

if __name__ == "__main__":
    # Start the server
    try:
        mcp.run(transport="sse", host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        print("Server stopped.")
        mcp.stop()

