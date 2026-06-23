from llama_index.llms.groq import Groq          # was: from llama_index.llms.ollama import Ollama
from config.settings import Settings

settings = Settings()
GROQ_API_KEY = settings.GROQ_API_KEY             # was: OLLAMA_URL = settings.OLLAMA_URL

_current_model_name = None
_current_llm_instance = None

def get_groq_llm(model_name: str):               # was: def get_ollama_llm(...)
    global _current_model_name, _current_llm_instance
    if _current_model_name == model_name and _current_llm_instance is not None:
        return _current_llm_instance
    llm = Groq(model=model_name, api_key=GROQ_API_KEY)   # was: Ollama(base_url=OLLAMA_URL, model=model_name)
    _current_model_name = model_name
    _current_llm_instance = llm
    return llm