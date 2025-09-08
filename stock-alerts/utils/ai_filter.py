import os, openai

def is_bullish(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"You are a financial sentiment analyzer. Answer 'yes' if bullish, 'no' otherwise."},
                      {"role":"user","content":text}]
        )
        result = response["choices"][0]["message"]["content"].strip().lower()
        return "yes" in result
    except Exception as e:
        return False
