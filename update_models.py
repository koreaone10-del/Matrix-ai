import json
import urllib.request
from datetime import datetime

def fetch_openrouter_models():
    print("🔄 جلب أحدث النماذج والأسعار من OpenRouter...")
    url = "https://openrouter.ai/api/v1/models"
    
    free_models = []
    paid_models = []
    
    try:
        # إرسال طلب لخوادم OpenRouter
        req = urllib.request.Request(url, headers={'User-Agent': 'MatrixAI-AutoBot/1.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            
            for m in data.get('data', []):
                model_id = m['id']
                
                # فحص التسعير لمعرفة هل هو مجاني أم مدفوع
                try:
                    price_prompt = float(m.get('pricing', {}).get('prompt', 0))
                    price_completion = float(m.get('pricing', {}).get('completion', 0))
                except (ValueError, TypeError):
                    price_prompt, price_completion = 0, 0
                
                # فرز النماذج
                if model_id.endswith(':free') or (price_prompt == 0 and price_completion == 0):
                    free_models.append(model_id)
                else:
                    paid_models.append(model_id)
            
            print(f"✅ تم العثور على {len(free_models)} نموذج مجاني و {len(paid_models)} نموذج مدفوع.")
            
            # الترتيب الذكي: المجاني أولاً، ثم المدفوع
            return free_models + paid_models

    except Exception as e:
        print(f"❌ فشل الاتصال بمزود OpenRouter: {e}")
        return []

def main():
    # 1. القوائم الافتراضية الثابتة للمزودين الآخرين
    pollinations_models = ["openai", "qwen", "qwen-coder", "llama", "mistral", "claude", "deepseek", "deepseek-reasoner"]
    gemini_models = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash", "gemma-3-27b-it"]
    groq_models = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it", "llama3-70b-8192"]

    # 2. التشغيل الذكي لجلب نماذج OpenRouter الحية
    all_openrouter_models = fetch_openrouter_models()
    
    # قائمة احتياطية في حال تعطل سيرفرات OpenRouter أثناء الفحص
    if not all_openrouter_models:
        all_openrouter_models = ["google/gemma-2-9b-it:free", "meta-llama/llama-3-8b-instruct:free", "openai/gpt-4o", "anthropic/claude-3.5-sonnet"]

    # 3. بناء الهيكل النهائي لملف الإعدادات
    config_data = {
        "version": "3.0",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "providers": [
            {
                "id": "pollinations",
                "defaultModel": "openai",
                "staticModels": pollinations_models
            },
            {
                "id": "openrouter",
                "defaultModel": all_openrouter_models[0], # النموذج الافتراضي سيكون أول نموذج مجاني
                "staticModels": all_openrouter_models
            },
            {
                "id": "gemini",
                "defaultModel": "gemini-2.5-flash",
                "staticModels": gemini_models
            },
            {
                "id": "groq",
                "defaultModel": "llama-3.3-70b-versatile",
                "staticModels": groq_models
            }
        ]
    }

    # 4. طباعة وكتابة الملف النهائي
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    print("🎉 تم بناء ملف config.json بنجاح وبأحدث تقنيات الذكاء الاصطناعي!")

if __name__ == "__main__":
    main()
