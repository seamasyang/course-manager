import sys
from pathlib import Path

# Add the backend/ directory to sys.path so "app" is recognized as a top-level package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8100, reload=True)
