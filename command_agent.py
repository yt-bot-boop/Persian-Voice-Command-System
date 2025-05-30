# To fix the error caused by Streamlit's file watcher conflicting with PyTorch,
# disable the file watcher by setting this environment variable.
# Alternatively, updating Streamlit to version 1.45.1 or later may resolve the issue.
import os
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict
import subprocess
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    transcription: str
    command: str
    result: str

class CommandAgent:
    def __init__(self):
        self.llm = OllamaLLM(
            model="qwen2.5:latest",
            temperature=0.3,
            num_gpu=1
        )
        
        self.prompt = ChatPromptTemplate.from_template("""
        Persian Voice Command Assistant - Convert to Windows Commands
        
        Examples:
        - "مرورگر را باز کن" → start chrome
        - "کد را ببند" → taskkill /im code.exe
        - "دانلودها" → explorer C:\\Users\\$USER\\Downloads
        
        Request: {transcription}. Do not explain more details. just command.""")
        
        workflow = StateGraph(AgentState)
        workflow.add_node("analyze_transcription", self.analyze_transcription)
        workflow.add_node("execute_system_command", self.execute_system_command)
        
        workflow.set_entry_point("analyze_transcription")
        workflow.add_edge("analyze_transcription", "execute_system_command")
        workflow.add_edge("execute_system_command", END)
        
        self.agent = workflow.compile()

    def analyze_transcription(self, state: AgentState) -> AgentState:
        chain = self.prompt | self.llm | StrOutputParser()
        command = chain.invoke({"transcription": state["transcription"]})
        return {"transcription": state["transcription"], "command": command, "result": ""}

    def execute_system_command(self, state: AgentState) -> AgentState:
        ALLOWED_COMMANDS = {
            "start": ["chrome", "firefox", "code", "explorer"],
            "explorer": ["downloads", "documents"],
            "taskkill": ["code.exe", "chrome.exe"]
        }
        
        parts = state["command"].strip().split()
        print(parts)
        if not parts or parts[0] not in ALLOWED_COMMANDS:
            return {"transcription": state["transcription"], "command": state["command"], "result": "Error: Command not allowed"}
        
        if len(parts) > 1 and parts[1] not in ALLOWED_COMMANDS.get(parts[0], []):
            return {"transcription": state["transcription"], "command": state["command"], "result": "Error: Invalid target"}
        
        try:
            result = subprocess.run(
                parts[0]+" "+parts[1],
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            return {"transcription": state["transcription"], "command": state["command"], "result": result.stdout or "Command executed"}
        except subprocess.TimeoutExpired:
            return {"transcription": state["transcription"], "command": state["command"], "result": "Error: Command timed out"}
        except subprocess.CalledProcessError as e:
            return {"transcription": state["transcription"], "command": state["command"], "result": f"Error: {e.stderr.strip()}"}
        except Exception as e:
            return {"transcription": state["transcription"], "command": state["command"], "result": f"Error: {str(e)}"}
            
    def process_command(self, text_command):
        initial_state = AgentState(
            transcription=text_command,
            command="",
            result=""
        )
        result = self.agent.invoke(initial_state)
        return {"output": result["result"]}