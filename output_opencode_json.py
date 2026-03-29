# ========================== 配置参数说明 ==========================
# OUTPUT_PATH: 生成的配置文件保存路径（相对/绝对路径均可）
# NPM/SCHEMA: 固定配置，无需修改
# MID_PROVIDERS: 中转站列表，【每个中转站独立一套 API Key/BaseURL】
#   ├─ apiKey: 当前中转站专属密钥
#   ├─ baseURL: 当前中转站专属接口地址
#   └─ services: 当前中转下的模型服务（同中转所有服务共用上述密钥/地址）
#       ├─ code: 服务唯一标识（自定义）
#       ├─ name: 服务显示名称
#       └─ models: 服务下的模型列表
#           ├─ id: 模型调用ID
#           ├─ name: 模型显示名
#           ├─ ctx: 上下文最大长度
#           └─ out: 输出最大长度
# ==================================================================
import json

# ===================== 【固定配置 - 请勿修改】 =====================
SCHEMA = "https://opencode.ai/config.json"
NPM = "@ai-sdk/openai-compatible"

# ===================== 【用户配置 - 仅修改此处】 =====================
OUTPUT_PATH = "./opencode.json"

# 多中转站配置列表
MID_PROVIDERS = [
    # 中转站1
    {
        "apiKey": "",
        "baseURL": "https://apic1.ohmycdn.com/api/v1/ai/openai/cc-omg/v1",
        "services": [
            {
                "code": "ohmygpt-claude",
                "name": "OhMyGPT Claude",
                "models": [
                    # Claude 4.6 模型
                    {"id": "claude-sonnet-4-6", "name": "Claude Sonnet 4.6", "ctx": 200000, "out": 64000},
                    {"id": "claude-opus-4-6", "name": "Claude Opus 4.6", "ctx": 200000, "out": 64000},
                    # Claude 4.5 模型
                    {"id": "claude-sonnet-4-5", "name": "Claude Sonnet 4.5", "ctx": 200000, "out": 64000},
                    {"id": "claude-opus-4-5", "name": "Claude Opus 4.5", "ctx": 200000, "out": 64000},
                    {"id": "claude-haiku-4-5", "name": "Claude Haiku 4.5", "ctx": 200000, "out": 64000},
                ]
            }
        ]
    },
    # 中转站2
    {
        "apiKey": "",
        "baseURL": "https://apic1.ohmycdn.com/v1",
        "services": [
            {
                "code": "ohmygpt-openai",
                "name": "OhMyGPT OpenAI",
                "models": [
                    # GPT-5.4 模型
                    {"id": "gpt-5.4", "name": "GPT-5.4", "ctx": 200000, "out": 64000},
                    {"id": "gpt-5.4-nano", "name": "GPT-5.4 Nano", "ctx": 200000, "out": 64000},
                    {"id": "gpt-5.4-mini", "name": "GPT-5.4 Mini", "ctx": 200000, "out": 64000},
                    # GPT-5.3 模型
                    {"id": "gpt-5.3-codex", "name": "GPT-5.3 Codex", "ctx": 200000, "out": 64000},
                ]
            },
            {
                "code": "ohmygpt-gemini",
                "name": "OhMyGPT Gemini",
                "models": [
                    # Gemini-3.1 模型
                    {"id": "gemini-3.1-pro-preview", "name": "Gemini-3.1 Pro Preview", "ctx": 200000, "out": 64000},
                    {"id": "gemini-3.1-flash-image-preview", "name": "Gemini-3.1 Flash Image Preview", "ctx": 200000, "out": 64000},
                    {"id": "gemini-3.1-flash-lite-preview", "name": "Gemini-3.1 Flash Lite Preview", "ctx": 200000, "out": 64000},
                    # Gemini-3 模型
                    {"id": "gemini-3-pro-image-preview", "name": "Gemini-3 Pro Image Preview", "ctx": 200000, "out": 64000},
                    {"id": "gemini-3-flash-preview", "name": "Gemini-3 Flash Preview", "ctx": 200000, "out": 64000},
                ]
            }
        ]
    }
]

# ===================== 【生成逻辑 - 无需修改】 =====================
config = {"$schema": SCHEMA, "provider": {}}
for mid in MID_PROVIDERS:
    for srv in mid["services"]:
        config["provider"][srv["code"]] = {
            "npm": NPM,
            "name": srv["name"],
            "options": {"apiKey": mid["apiKey"], "baseURL": mid["baseURL"]},
            "models": {m["id"]: {"name": m["name"], "limit": {"context": m["ctx"], "output": m["out"]}} for m in srv["models"]}
        }

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)