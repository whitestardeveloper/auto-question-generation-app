import openai
import ollama
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

def get_model(model_key):

     #v2 model dict
    model_dict = {
        "GOOGLE (gemini-1.5-flash)": "gemini-1.5-flash",
        "GOOGLE (gemma2) [27b]": "gemma2:27b",
        "Cohere For AI (aya-expanse)[32b]": "aya-expanse:32b",
        "MISTRAL (mistral-small) [22b]": "mistral-small",
        "META (llama3.1) [70b]": "llama3.1:70b",
        "ALIBABA (qwen2.5) [32b]": "qwen2.5:32b",
        "NVIDIA (nvidia/nemotron-4-340b-instruct)": "nvidia/nemotron-4-340b-instruct",
    }
    #v1 model dict
    # model_dict = {
    #     "GOOGLE (gemini-1.5-flash)": "gemini-1.5-flash", 
    #     "GOOGLE (gemma2)": "gemma2", 
    #     "Cohere For AI (aya-expanse)[8B]": "aya-expanse",
    #     "MISTRAL (mistral-nemo)": "mistral-nemo",
    #     "META (llama3.1)": "llama3.1", 
    #     "ALIBABA (qwen2.5)": "qwen2.5",
    #     "NVIDIA (nvidia/nemotron-4-340b-instruct)": "nvidia/nemotron-4-340b-instruct",
    # }
    return model_dict[model_key]


def generate_question(model_key, user_prompt, system_prompt):
    selected_model = get_model(model_key)
    print(selected_model)

    if selected_model in ["gemini-1.5-flash"]:
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        llm = genai.GenerativeModel(
            "gemini-1.5-flash", system_instruction=system_prompt
        )
        response = llm.generate_content(
            user_prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
        )
        return response.text

    elif selected_model in [
        "llama3.1",
        "llama3.1:70b",
        "llama3.2",
        "mistral-nemo",
        "mistral-small",
        "phi3.5",
        "qwen2.5",
        "qwen2.5:32b",
        "gemma2",
        "gemma2:27b",
        "granite3-moe:3b",
        "granite3-dense",
        "aya-expanse",
        "aya-expanse:32b",
        "nemotron-mini",
    ]:
        
        generate_params = {
            "model": selected_model,
            # 'options': Options(temperature=0.7),
            "prompt": system_prompt + '**Soru üretimi için sana verilen kaynak bilgileri aşağıdakı şekildedir: **'+ user_prompt,
            # 'system': system_prompt,
            # "format": "json",
        }   
        response = ollama.generate(**generate_params)
        return response["response"]

    elif selected_model == "nvidia/nemotron-4-340b-instruct":
        client = openai.OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.environ.get("NVIDIA_API_KEY"),
        )

        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        response_text = response.choices[0].message.content
        return response_text
    else:
        print("GEÇERSİZ MODEL...")
        return