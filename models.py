import openai
import ollama
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

def get_model(model_key):
    model_dict = {
        "GOOGLE (gemini-1.5-flash)": "gemini-1.5-flash", 
        "GOOGLE (gemma2)": "gemma2", 
        "Cohere For AI (aya-expanse)[8B]": "aya-expanse",
        "MISTRAL (mistral-nemo)": "mistral-nemo",
        "META (llama3.1)": "llama3.1", 
        "ALIBABA (qwen2.5)": "qwen2.5",
        "NVIDIA (nvidia/nemotron-4-340b-instruct)": "nvidia/nemotron-4-340b-instruct",
        # "MICROSOFT (phi3.5)": "phi3.5",
        # "NVIDIA (nemotron-mini)": "nemotron-mini",
        # "IBM (granite3-moe:3b)[3B]": "granite3-moe:3b",
        # "IBM (granite3-dense:3b)[2B]": "granite3-dense",
        # "OPEN-AI (o1-mini)": "o1-mini", 
        # "CLAUDE (claude-3-5-sonnet-20240620)": "claude-3-5-sonnet-20240620",
    }
    return model_dict[model_key]

def generate_question(model_key, promt):
    selected_model = get_model(model_key)
    if selected_model in ['gemini-1.5-flash']:
        print(os.environ.get("GOOGLE_API_KEY"))
        print(selected_model)
        genai.configure(api_key='AIzaSyCYoC2JHVdk8Ji0vLxbspHVhScCQIO9dRs')
        llm = genai.GenerativeModel(selected_model)
        response = llm.generate_content(promt)
        return response.text
    elif selected_model in ['llama3.1', 'mistral-nemo', 'phi3.5', 'qwen2.5', 'gemma2', 'granite3-moe:3b' , 'granite3-dense', 'aya-expanse', 'nemotron-mini']:
        print(selected_model)
        response = ollama.generate(model=selected_model, prompt=promt)
        return response['response']
    elif selected_model == 'nvidia/nemotron-4-340b-instruct': 
        print(selected_model)
        print(os.environ.get("NVIDIA_API_KEY")) 
        client = openai.OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = os.environ.get("NVIDIA_API_KEYasd", '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')
        )

        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role":"user","content": promt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=4096,
            stream=True
        )
        response_text =''
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
                response_text+=chunk.choices[0].delta.content
        return response_text
    # elif selected_model == 'claude-3-5-sonnet-20240620':
    #     client = .(api_key=os.environ.get('_API_KEY'))
    #     response = client.messages.create(
    #         model=selected_model,
    #         max_tokens=4096,
    #         messages=[
    #             {"role": "user", "content": promt}
    #         ]
    #     )
    #     return response.content
    else:
    #     client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    #     response = client.chat.completions.create(
    #         model="o1-mini",
    #         messages=[
    #             {"role": "user", "content": promt}
    #         ]
    #     )
    # return response.content
        print('GEÇERSİZ MODEL...')
        return
