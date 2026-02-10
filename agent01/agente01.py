
from mcpclient import MCPClient
import asyncio
from dotenv import load_dotenv
from fastmcp import Client
from simple_memory import SimpleMemory
from groq import Groq
import json
import os

SYSTEM_PROMPT = f"""
Eres un asistente que habla en español y responde de manera muy breve y concisa.

Solo puedes realizar las siguientes acciones y pude confirmación del usuario
- Abrir puertas a demanda del usuario, si no indican la puerta manda 1.
- Cerrar puertas a demanda del usuario, si no indican la puerta manda 1


Herramientas disponibles: 
- Cuentas con una herramienta openDoor para abrir puertas de un departamento, debes enviar los parametros:
   * houseId: Id de la casa
   * doorId: Id de la puerta, el valor por defecto 1.
- Cuentas con una herramienta closeDoor para cerrar puertas de un departamento, debes enviar los parametros:
   * houseId: Id de la casa
   * doorId: Id de la puerta, el valor por defecto 1.
"""

class Agent:
   def __init__(self):
      self.mcpclient = MCPClient()
      self.setup_tools()
      self.memory = SimpleMemory(max_messages=20)
 
   def setup_tools(self):
      self.tools = []
      mis_tools = asyncio.run(self.mcpclient.get_mcp_client_tools())
      [self.tools.append(tc) for tc in mis_tools]

   def process_response(self,client:Groq, memory_messages: list[dict], user_text:str):
       #Obtener la memoria
      messages = [{"role": "system", "content": SYSTEM_PROMPT}]
      messages.extend(memory_messages)
      messages.append({"role": "user", "content": user_text})
   
      while True:
        resp = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=messages,
            tools=self.tools
        )
        msg = resp.choices[0].message
        
        #Si no hay llamados a herramientas, entonces ya regresamos la respuesta
        if not getattr(msg, "tool_calls", None):
            return msg.content or ""
        
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [tc.model_dump() for tc in msg.tool_calls]
        })
        
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")
            
            result = asyncio.run(self.mcpclient.call_tool(name,arguments=args))
                
            #Agregar a los mensajes el resultao del llamado de la herramienta.
            #Esto lo recibirá el modelo al continuar la iteración
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False)
            })

   
      
if __name__ == "__main__":
   agente = Agent()
   api_key = os.environ.get("GROQ_API_KEY")
   client = Groq(api_key=api_key)
   memory = SimpleMemory(max_messages=100)

   while True:
         user_text = input("Tú: ").strip()
         if not user_text:
            continue
         
         if user_text.lower() in ("exit", "salir"):
            print("Hasta luego!")
            break
         
         assistant_text = agente.process_response(client, memory.messages(), user_text)
         print(f"Asistente: {assistant_text}")
         
         #Actualizar la memoria
         memory.add("user", user_text)
         memory.add("assistant", assistant_text)