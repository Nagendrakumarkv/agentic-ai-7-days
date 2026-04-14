import os
import re
from google import genai
from google.genai import types

SYSTEM_PROMPT = """You are a backend API generators specialized in FastAPI.
Your goal is to scaffold complete FastAPI project directories based on user commands.
Always structure your output as Markdown.
For each file you generate, use the following format exactly:

### `path/to/file.py`
```python
# code here
```

For requirements.txt:
### `requirements.txt`
```text
fastapi
uvicorn
```

Ensure the root `main.py` is present and functional. All routes should be fully implemented and correct. 
Do not provide extra conversational filler. Only output files and their contents.
"""

def generate_project(prompt: str, chat_history: list = None) -> list[dict]:
    """Calls Gemini and parses the markdown into a list of file dictionaries: [{'path': '...', 'content': '...'}]"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)
    
    # Format history for genai SDK
    contents = []
    
    if chat_history:
        for msg in chat_history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
            )
            
    # Add Current Prompt
    contents.append(
                types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
            )
            
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2
        )
    )
    
    generated_text = response.text
    return parse_markdown_to_files(generated_text), generated_text

def parse_markdown_to_files(markdown_text: str) -> list[dict]:
    # Look for ### `path` followed by ```lang\ncontent```
    pattern = r"###\s*\*?\*?`?([^`\*\n]+)`?\*?\*?\s*```[^\n]*\n(.*?)```"
    matches = re.finditer(pattern, markdown_text, re.DOTALL)
    
    files = []
    for match in matches:
        filepath = match.group(1).strip()
        content = match.group(2).strip()
        files.append({"path": filepath, "content": content})
    return files
