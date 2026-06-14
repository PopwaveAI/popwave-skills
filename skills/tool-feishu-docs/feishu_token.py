"""飞书 Token 自动管理 — 租户/用户双模式，所有权限"""
import requests, json, os, time

APP_ID = "cli_aa9d0a50363b9bb3"
APP_SECRET = "GeFPOFJduzYalKsTaD759cSSmt2JgDXH"
BASE = "https://open.feishu.cn"
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feishu_tokens.json")

def _load():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save(data):
    data["app_id"] = APP_ID
    data["app_secret"] = APP_SECRET
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_token():
    data = _load()
    token_type = data.get("token_type", "tenant")

    if token_type == "tenant":
        token = data.get("tenant_access_token", "")
        if token:
            r = requests.get(f"{BASE}/open-apis/docx/v1/documents",
                headers={"Authorization": f"Bearer {token}"})
            if r.json().get("code") == 0:
                return token
        print("[feishu] 租户 token 过期，重新获取...")
        r = requests.post(f"{BASE}/open-apis/auth/v3/tenant_access_token/internal",
            json={"app_id": APP_ID, "app_secret": APP_SECRET})
        if r.json().get("code") == 0:
            token = r.json()["tenant_access_token"]
            _save({"token_type": "tenant", "tenant_access_token": token, "updated_at": int(time.time())})
            return token
        raise Exception(f"获取租户 token 失败: {r.json()}")

    else:  # user
        token = data.get("user_access_token", "")
        if token:
            r = requests.get(f"{BASE}/open-apis/authen/v1/user_info",
                headers={"Authorization": f"Bearer {token}"})
            if r.json().get("code") == 0:
                return token
        refresh = data.get("refresh_token", "")
        if refresh:
            print("[feishu] 用户 token 过期，续期中...")
            at = requests.post(f"{BASE}/open-apis/auth/v3/app_access_token/internal",
                json={"app_id": APP_ID, "app_secret": APP_SECRET}).json()["app_access_token"]
            r = requests.post(f"{BASE}/open-apis/authen/v1/oidc/refresh_access_token",
                headers={"Authorization": f"Bearer {at}"},
                json={"grant_type": "refresh_token", "refresh_token": refresh})
            if r.json().get("code") == 0:
                d = r.json()["data"]
                _save({"token_type": "user", "user_access_token": d["access_token"],
                       "refresh_token": d.get("refresh_token", refresh),
                       "updated_at": int(time.time()), "open_id": data.get("open_id", "")})
                return d["access_token"]
            raise Exception(f"续期失败: {r.json()}")
        raise Exception("无可用 token。请运行 first_time_setup.py")

def headers():
    return {"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"}

def get_open_id():
    return _load().get("open_id", "")
