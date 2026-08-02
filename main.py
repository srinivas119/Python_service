from fastapi import FastAPI, HTTPException
import asyncio

# Import your existing service modules
from services.codechef_service import fetch_codechef_data
from services.codeforces_service import fetch_codeforces_data
from services.gfg_service import fetch_gfg_data
from services.github_service import fetch_github_data
from services.leetcode_service import fetch_leetcode_data

app = FastAPI(title="UnifyCode Python Data Fetcher Service")

# Map platform strings to service handlers
SERVICES = {
    "codechef": fetch_codechef_data,
    "codeforces": fetch_codeforces_data,
    "gfg": fetch_gfg_data,
    "github": fetch_github_data,
    "leetcode": fetch_leetcode_data,
}

@app.get("/")
def read_root():
    return {"status": "Python fetcher service is online 🎉"}

@app.get("/fetch/{platform}/{username}")
async def fetch_platform_data(platform: str, username: str):
    handler = SERVICES.get(platform.lower())
    
    if not handler:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported platform: '{platform}'. Supported: {list(SERVICES.keys())}"
        )
    
    try:
        # Support both sync and async service functions smoothly
        if asyncio.iscoroutinefunction(handler):
            data = await handler(username)
        else:
            data = handler(username)
            
        return {"success": True, "platform": platform, "username": username, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing fetcher: {str(e)}")