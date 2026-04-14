import os
import subprocess
import time
import shutil

class SandboxManager:
    def __init__(self, workspace_path: str, port: int = 8001):
        self.workspace_path = workspace_path
        self.port = port
        self.process = None
        
        if not os.path.exists(self.workspace_path):
            os.makedirs(self.workspace_path)

    def write_files(self, files: list[dict]):
        # Clear existing workspace except __pycache__ etc (to allow iterative replace)
        for d in os.listdir(self.workspace_path):
            dp = os.path.join(self.workspace_path, d)
            if os.path.isdir(dp) and d != '__pycache__':
                shutil.rmtree(dp)
            elif os.path.isfile(dp):
                os.remove(dp)
                
        # Write new files
        for f in files:
            full_path = os.path.join(self.workspace_path, f['path'])
            # Ensure directories exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as file:
                file.write(f['content'])

    def restart_server(self):
        self.stop_server()
        
        main_file = os.path.join(self.workspace_path, "main.py")
        if not os.path.exists(main_file):
            print("No main.py found, cannot start server")
            return False

        print(f"Starting server in {self.workspace_path} on port {self.port}...")
        self.process = subprocess.Popen(
            ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(self.port)],
            cwd=self.workspace_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        time.sleep(1) # wait for startup
        return self.process.poll() is None # true if still running

    def stop_server(self):
        if self.process is not None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None

    def get_logs(self):
        # We could implement a non-blocking read here, but for simplicity, 
        # we'll just let uvicorn print to console, or read until empty.
        pass
