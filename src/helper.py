from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
import logging

load_dotenv()
api_key = os.getenv("GROQ_API_KEY", "")

def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)

def get_llm():
    try:
        print("Initializing Primary Model")
        llm = init_chat_model(
            model=os.getenv("PRIMARY_MODEL"),
            model_provider=os.getenv("MODEL_PROVIDER"),
            api_key=api_key,
            temperature=0.2,
            max_tokens=2000
        )
        print("Model Initialized")
        response = llm.invoke("Hi")
        if response and response.content:
            print("Primary Model Checked and Working")
            return llm
        raise Exception
    except Exception as e:
        print(f"Error ocurred while initializing PRIMARY MODEL: {e}")
        try:
            print("Initializing Secondary Model")
            llm = init_chat_model(
                model=os.getenv("SECONDARY_MODEL"),
                model_provider=os.getenv("MODEL_PROVIDER"),
                api_key=api_key,
                temperature=0.2,
                max_tokens=2000
            )
            print("Model Initialized")
            response = llm.invoke("Hi")
            if response and response.context:
                print("Secondary Model Checked and Working")
                return llm
            raise Exception
        except Exception as e:
            print(f"Error ocurred while initalizing both models check the Web Interface for new model\n Error message: {e}")