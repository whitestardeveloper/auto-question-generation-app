import ollama


def get_model(model_key):
    model_dict = {
        "GOOGLE (gemma2)": "gemma2",
        "Cohere For AI (aya-expanse)[8B]": "aya-expanse",
        "MISTRAL (mistral-nemo)": "mistral-nemo",
        "META (llama3.1)": "llama3.1",
        "ALIBABA (qwen2.5)": "qwen2.5",
    }
    return model_dict[model_key]


def generate_question(model_key, promt):
    selected_model = get_model(model_key)

    # Message history
    system_prompt = """
        Yukarıdaki verdiğim kaynaktan 3 adet çoktan seçmeli soru üretmeni istiyorum. Soruları üretirken kolay, orta ve zor olarak 3 adet zorluk seviyemiz var. Üreteceğin bütün  sorular zor seviyede olsun.

        Bu soruları üretirken json bir çıktı bekliyorum. Direk veritabanıma alacağım. Aşağıdaki gibi çıktı vermelisin. Yorum yapma, ek bilgi verme. Yanlızca json çıktıyı ver. Hiç bir yorum yapma yanlızca aşağıdaki json'u ver.

        "questions": [
            {
                "question_body": "",
                "answers": [
                    {"content": ".....", "correct": False},
                    {"content": ".....", "correct": False},
                    {"content": ".....", "correct": False},
                    {"content": ".....", "correct": False},
                    {"content": ".....", "correct": True}
                ]
                "question_diffucult_level": "",
            },
            ...
        ]
    """
    generate_params = {
        'model': selected_model,
        # 'options': Options(temperature=0.7),
        'prompt': promt,
        'system': system_prompt
        # 'format': 'json'
    }


    response = ollama.generate(generate_params)
    return response['text']


promt = """
add source text for question generation
"""


resp = generate_question("META (llama3.1)", promt)
print(resp)