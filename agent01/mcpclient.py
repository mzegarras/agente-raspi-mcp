from fastmcp import Client
from dotenv import load_dotenv


load_dotenv()

class MCPClient:
    def __init__(self):
        self.mcp_server_path = "http://localhost:9000/mcp"
        self.openai_tools = []
    
    async def _get_mcp_client(self):
        """Crea conexión con el servidor MCP"""
        return Client(self.mcp_server_path)
    
    async def get_system_info(self) -> dict:
        """Información del sistema MCP"""
        async with await self._get_mcp_client() as cliente:
            tools = await cliente.list_tools()
            resources = await cliente.list_resources()
            templates = await cliente.list_resource_templates()
            prompts = await cliente.list_prompts()

            return {
                "tools": [t.name for t in tools],
                "resources": [r.name for r in resources],
                "templates": [t.name for t in templates],
                "prompts": [p.name for p in prompts],
                "server": self.mcp_server_path
            }

    async def get_mcp_client_tools(self):
        async with await self._get_mcp_client() as cliente:
                # 2. Obtener herramientas del servidor MCP
                tools = await cliente.list_tools()

                # Convertir herramientas de MCP al formato de OpenAI
                
                for tool in tools:
                    self.openai_tools.append(
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.inputSchema,
                        },
                    })
                    
                return self.openai_tools

    async def call_tool(self, tool_name: str, arguments: dict):
        async with await self._get_mcp_client() as cliente:
            result = await cliente.call_tool(tool_name, arguments)
            # Verificar la estructura de la respuesta
            if result and result.content and len(result.content) > 0:
                if hasattr(result.content[0], 'text'):
                    return result.content[0].text
            return "Herramienta ejecutada sin resultados"
    
