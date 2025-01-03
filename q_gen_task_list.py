from io import BytesIO
from firebase_application import get_source_list, add_question_gen_data
from models import generate_question
from prompts import get_prompt
from summarization import summarize_text
import time


# 3 seviye zorluk derecesi
diff_levels = ["kolay", "orta", "zor"]

# 6 soru şekli
q_types = [
    "Çoktan Seçmeli",
    "Doğru Yanlış",
    "Boşluk doldurma",
    "Açık Soru",
    "Eşleştirme",
    "Kısa Cevaplı",
]

# 7 farklı model
# models = [
#     "GOOGLE (gemini-1.5-flash)",
#     "GOOGLE (gemma2)",
#     "MISTRAL (mistral-nemo)",
#     "META (llama3.1)",
#     "ALIBABA (qwen2.5)",
#     "Cohere For AI (aya-expanse)[8B]",
#     "NVIDIA (nvidia/nemotron-4-340b-instruct)",
# ]

models = [
    "GOOGLE (gemini-1.5-flash)",
    "GOOGLE (gemma2) [27b]",
    "MISTRAL (mistral-small) [22b]",
    "META (llama3.1) [70b]",
    "ALIBABA (qwen2.5) [32b]",
    "Cohere For AI (aya-expanse)[32b]",
    "NVIDIA (nvidia/nemotron-4-340b-instruct)",
]


# 60 farklı soru heterojen soru kaynağı
def build_source_list():
    index = 0
    source_list = get_source_list()
    source_list_group_by_class_category = {}

    for key, obj_item in source_list.items():
        class_category = f"{obj_item['class']}-{obj_item['category']}"
        if class_category not in source_list_group_by_class_category:
            source_list_group_by_class_category[class_category] = []
        source_list_group_by_class_category[class_category].append(obj_item)

    return source_list_group_by_class_category

    # for key, group_item_list in source_list_group_by_class_category.items():
    #     index += 1
    #     source_text=''
    #     for list_item in group_item_list:
    #         source_text += list_item['text_content']
    #     source_token_size = len(source_text)

    #     print(f"{index}. => {key} - {source_token_size}")


# Kaynakların eğitim seviyeleri => Ortaokul (5, 6, 7, 8)
# Kaynakların dersleri (Türkçe, Sosyal Bilgiler ve Fen Bilimleri)
# Kaynakların hetorajen  olarak karıştığı vakit 60 adet oluyor. Yani soru üretiminde 60 heterojen kaynak kullanılacak.
# Her üretimde 3 adet soru üretilecek.
# Üretim ayrı ayrı olmak üzere "Çoktan Seçmeli", "Doğru Yanlış", "Boşluk doldurma", "Açık Soru", "Eşleştirme" ve "Kısa Cevaplı" soru tiplerinden olacak.
# Sorular 3 ayrı zorluk düzeyinde gerçekleşecek. (Kolay, Orta ve Zor)
# Yukarıdaki sayılan özelliklerin hepsi ayrı ayrı 7 model üzerinde denenecek. ("GOOGLE (gemini-1.5-flash)", "GOOGLE (gemma2) [27b]", "MISTRAL (mistral-small) [22b]", "META (llama3.1) [70b]",  "ALIBABA (qwen2.5) [32b]", "NVIDIA (nvidia/nemotron-4-340b-instruct)", "Cohere For AI (aya-expanse)[32b])
# Toplamda 3 * 6 * 60 * 7 = 7560 * 3(soru adedi) => 22.680 adet soru üretilmiş olacak.


def get_question_choice_count(q_type):
    if q_type == "Çoktan Seçmeli":
        return 4
    return None


def run():
    question_index = 0
    heterogenius_sources = build_source_list()
    for diff_level in diff_levels:
        for q_type in q_types:
            for key, group_item_list in heterogenius_sources.items():
                source_text = ""
                source_ids = []
                for list_item in group_item_list:
                    source_text += list_item["text_content"]
                    source_ids.append(list_item["id"])
                source_token_size = len(source_text)

                for model in models:
                    question_index += 1

                    if question_index > 0:
                        print('*' * 50)
                        print(
                            f"{question_index}-{diff_level}-{q_type}-{model}-{group_item_list[0]['course']}-{group_item_list[0]['class']}-{group_item_list[0]['category']}- {source_token_size} STARTED!"
                        )

                        system_prompt = get_prompt(q_type, 3, diff_level)

                        # q gen started
                        token_size = len(source_text + system_prompt)
                        print(token_size)

                        summarized_text = None
                        is_limited = True if "NVIDIA" in model or "gemini" in model else False
                        if is_limited and token_size > 4096:  # max_token_size for nvidia models
                            summarized_text = summarize_text(source_text)
                            user_propmt = summarized_text
                        else:
                            user_propmt = source_text


                        try:
                            start_time = time.time()
                            response_text = generate_question(model, system_prompt, user_propmt)
                            end_time = time.time()
                            elapsed_time = end_time - start_time

                            # q gen ended
                            question_gen_data = {
                                "gen_version": 2,
                                "index": question_index,
                                "query_id": question_index,
                                "source_info": {
                                    "course": group_item_list[0]["course"],
                                    "class": group_item_list[0]["class"],
                                    "category": group_item_list[0]["category"],
                                    "source_ids": source_ids,
                                    "source_token_size": source_token_size,
                                },
                                "questions_info": {
                                    "question_count": 3,
                                    "choices_count": get_question_choice_count(q_type),
                                    "question_type": q_type,
                                    "question_difficulty_level": diff_level,
                                },
                                "data": {
                                    "generation_model": model,
                                    "prompt": system_prompt,
                                    "data_transaction": (
                                        "SUMMARIZATION" if summarized_text else None
                                    ),  # SUMMARIZATION, SPLITTING, None
                                    "text_from_transaction": summarized_text,
                                    "generated_questions": response_text,
                                    "generation_elapsed_time": elapsed_time,
                                },
                            }

                            add_question_gen_data(question_gen_data)
                            print(response_text)
                            print(
                                f"{question_index}-{diff_level}-{q_type}-{model}-{group_item_list[0]['course']}-{group_item_list[0]['class']}-{group_item_list[0]['category']}- {source_token_size} DONE!"
                            )
                            print('#' * 50)
                        except Exception as e:
                            print(e)
                            pass

run()