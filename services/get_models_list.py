from config.settings import Settings

settings = Settings()

def get_groq_models_list():                      # was: get_ollama_models_list
    models_list = settings.GROQ_MODELS           # was: settings.OLLAMA_MODELS
    groq_models = [model.strip() for model in models_list.split(",") if model.strip()]
    return groq_models