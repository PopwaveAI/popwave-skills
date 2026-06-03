# OAuth Flow Reference

Complete code to obtain `user_access_token` with `refresh_token`, plus persistence setup.

## Full OAuth Script (with auto-save)

```python
import requests, webbrowser, http.server, urllib.parse, threading, json, os, time

APP_ID = "..."
APP_SECRET = "..."
BASE = "https://open.feishu.cn"
PORT = 18080
REDIRECT = f"http://127.0.0.1:{PORT}/callback"
SCOPE = "offline_access docx:document docx:document:create bitable:app"

# --- Step 1: Local HTTP server ---
result = {}
done = threading.Event()

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global result
        p = urllib.parse.urlparse(self.path)
        if p.path == "/callback":
            params = urllib.parse.parse_qs(p.query)
            code = params.get("code", [None])[0]
            if code:
                app_tk = requests.post(
                    f"{BASE}/open-apis/auth/v3/app_access_token/internal",
                    json={"app_id": APP_ID, "app_secret": APP_SECRET}
                ).json()["app_access_token"]
                r = requests.post(
                    f"{BASE}/open-apis/authen/v1/oidc/access_token",
                    headers={"Authorization": f"Bearer {app_tk}"},
                    json={"grant_type": "authorization_code", "code": code})
                result = r.json()
            done.set()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<h1>{'OK' if result.get('code')==0 else 'FAIL'}</h1>".encode())
    def log_message(self, *a): pass

server = http.server.HTTPServer(("127.0.0.1", PORT), CallbackHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()

# --- Step 2: Open OAuth URL ---
auth_url = (
    "https://accounts.feishu.cn/open-apis/authen/v1/authorize"
    f"?client_id={APP_ID}&response_type=code"
    f"&redirect_uri={urllib.parse.quote(REDIRECT, safe='')}"
    f"&scope={urllib.parse.quote(SCOPE, safe='')}&state=feishu")
webbrowser.open(auth_url)

# --- Step 3: Wait ---
done.wait(timeout=120); server.shutdown()

if result and result.get("code") == 0:
    d = result["data"]
    user_token = d["access_token"]
    refresh_token = d.get("refresh_token", "")
    print(f"user: {user_token}")
    print(f"refresh: {refresh_token}")

    # --- Step 4: Auto-save to feishu_tokens.json ---
    user = requests.get(f"{BASE}/open-apis/authen/v1/user_info",
        headers={"Authorization": f"Bearer {user_token}"}).json()["data"]
    token_file = os.path.join(os.path.dirname(__file__), "feishu_tokens.json")
    with open(token_file, "w") as f:
        json.dump({
            "user_access_token": user_token,
            "refresh_token": refresh_token,
            "updated_at": int(time.time()),
            "open_id": user["open_id"]
        }, f, indent=2)
    print(f"Saved to {token_file}")
```

## Using the Auto-Manager

After OAuth, `feishu_tokens.json` and `feishu_token.py` are in place. Any conversation just does:

```python
from feishu_token import headers
H = headers()  # auto-refresh, auto-save new refresh_token
```

## Token Lifecycle

```
OAuth → feishu_tokens.json
           ↓
      get_token()
           ├── valid → return it
           └── expired → refresh → save new pair → return
```

## refresh_token Behavior

- **One-time use**: each refresh returns a NEW refresh_token, old one invalidated
- `feishu_token.py` auto-saves the new one, so you never lose it
- If lost/corrupted → re-run OAuth once

## Manual Refresh

```python
r = requests.post(f"{BASE}/open-apis/authen/v1/oidc/refresh_access_token",
    headers={"Authorization": f"Bearer {app_token}"},
    json={"grant_type": "refresh_token", "refresh_token": refresh_token})
new_token = r.json()["data"]["access_token"]
new_refresh = r.json()["data"]["refresh_token"]  # save this!
```

## Scopes

| Scope | Purpose |
|-------|---------|
| `offline_access` | Long-term refresh_token |
| `docx:document` | Document CRUD |
| `docx:document:create` | Create docs |
| `bitable:app` | Bitable read/write |
