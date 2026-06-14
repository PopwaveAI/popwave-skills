"""
tool-feishu-docs Skill — 首次安装（租户模式零配置 / 用户模式浏览器 OAuth）
Python: 3.7+  |  依赖: pip install requests
"""
import requests, webbrowser, http.server, urllib.parse, threading, json, os, time

APP_ID = "cli_aa9d0a50363b9bb3"
APP_SECRET = "GeFPOFJduzYalKsTaD759cSSmt2JgDXH"
BASE = "https://open.feishu.cn"
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(HERE, "feishu_tokens.json")

SCOPE_USER = ("offline_access docx:document docx:document:create bitable:app "
              "drive:drive docs:document:import docs:document:export "
              "contact:user.base:readonly wiki:wiki")


def save(data):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def mode_tenant():
    print(); print("=" * 50); print("  模式 1：租户 Token（零配置）"); print("=" * 50)
    r = requests.post(f"{BASE}/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": APP_ID, "app_secret": APP_SECRET})
    if r.json().get("code") != 0:
        print(f"\n❌ 获取失败: {r.json()}"); return False
    save({"token_type": "tenant", "tenant_access_token": r.json()["tenant_access_token"],
          "updated_at": int(time.time())})
    print(f"\n✅ 配置完成！\n   模式：租户 Token\n   文件：{TOKEN_FILE}")
    print("   📋 适用：创建/编辑文档、多维表格、评论列表")
    print("   ⚠️  不能：创建评论、管理文件夹权限（需升用户模式）")
    return True


def mode_user():
    print(); print("=" * 50); print("  模式 2：用户 Token（OAuth 授权）"); print("=" * 50)
    print("\n  ⚠️  请确认应用已开所有权限并发布版本")
    print(f"  权限管理: https://open.feishu.cn/app/{APP_ID}/auth\n")
    input("  按回车打开浏览器授权...")

    PORT = 18080
    REDIRECT = f"http://127.0.0.1:{PORT}/callback"
    result = {}
    done = threading.Event()

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            p = urllib.parse.urlparse(self.path)
            if p.path == "/callback":
                code = urllib.parse.parse_qs(p.query).get("code", [None])[0]
                if code:
                    at = requests.post(f"{BASE}/open-apis/auth/v3/app_access_token/internal",
                        json={"app_id": APP_ID, "app_secret": APP_SECRET}).json()["app_access_token"]
                    r = requests.post(f"{BASE}/open-apis/authen/v1/oidc/access_token",
                        headers={"Authorization": f"Bearer {at}"},
                        json={"grant_type": "authorization_code", "code": code})
                    result["d"] = r.json()
                done.set()
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<h1>OK</h1>")
        def log_message(self, *a): pass

    s = http.server.HTTPServer(("127.0.0.1", PORT), H)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    webbrowser.open(
        f"https://accounts.feishu.cn/open-apis/authen/v1/authorize"
        f"?client_id={APP_ID}&response_type=code"
        f"&redirect_uri={urllib.parse.quote(REDIRECT, safe='')}"
        f"&scope={urllib.parse.quote(SCOPE_USER, safe='')}&state=f")
    done.wait(120); s.shutdown()

    rd = result.get("d", {})
    if rd.get("code") != 0:
        print(f"\n❌ 授权失败\n{json.dumps(rd, indent=2, ensure_ascii=False)[:400]}"); return False
    d = rd["data"]
    token, refresh = d["access_token"], d.get("refresh_token", "")
    user = requests.get(f"{BASE}/open-apis/authen/v1/user_info",
        headers={"Authorization": f"Bearer {token}"}).json()["data"]
    save({"token_type": "user", "user_access_token": token, "refresh_token": refresh,
          "open_id": user["open_id"], "updated_at": int(time.time())})
    print(f"\n✅ 配置完成！{user['name']}")
    print(f"   模式：用户 Token（含 refresh 自动续期）")
    print(f"   📋 适用：全部文档 + 评论 + 文件夹 + 权限管理")
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("  tool-feishu-docs Skill — 首次安装 v2.0")
    print("=" * 50)
    print("\n选择模式：")
    print("  1. 租户 Token（推荐）— 零配置，无需浏览器")
    print("  2. 用户 Token — 浏览器 OAuth，全功能")
    c = input("\n输入 [1/2] [1]: ").strip() or "1"
    ok = mode_tenant() if c == "1" else mode_user() if c == "2" else False
    if ok:
        print(f"\n{'='*50}\n  现在对 AI 说「帮我在飞书写份文档」即可\n{'='*50}")
