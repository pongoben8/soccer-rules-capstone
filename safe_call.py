"""Safe model call: no tracebacks or secrets exposed to visitors."""
import time
from groq import Groq, RateLimitError, APIError, AuthenticationError

MODEL = 'llama-3.1-8b-instant'

def ask_model(api_key, messages, retries=2):
    try:
        client = Groq(api_key=api_key)
        for attempt in range(retries + 1):
            try:
                response = client.chat.completions.create(model=MODEL, messages=messages, temperature=0.2, max_tokens=220)
                return response.choices[0].message.content, None
            except RateLimitError:
                if attempt < retries:
                    time.sleep(2 ** attempt)
                else:
                    return None, 'The service is busy. Please try again in a minute.'
            except AuthenticationError:
                return None, 'The language service is not configured correctly. Please contact the app owner.'
            except APIError:
                return None, 'The language service is temporarily unavailable. Please try again later.'
    except Exception:
        return None, 'The language service could not start. Please contact the app owner.'
