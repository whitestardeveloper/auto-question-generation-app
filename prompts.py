# models = ["GOOGLE (gemini-1.5-flash)", "GOOGLE (gemma2) [27b]", "MISTRAL (mistral-small) [22b]", "META (llama3.1) [70b]",  "ALIBABA (qwen2.5) [32b]", "NVIDIA (nvidia/nemotron-4-340b-instruct)", "Cohere For AI (aya-expanse)[32b]"]
# q_diff_levels = ['kolay', 'orta', 'zor']
# q_types=["Çoktan Seçmeli", "Doğru Yanlış", "Boşluk doldurma", "Açık Soru", "Eşleştirme", "Kısa Cevaplı"]

def question_type_prompt(q_type):
      # Çoktan Seçmeli Soru Promtu
    if q_type == "Çoktan Seçmeli":
        prompt = """
            Bu direktiflerle çoktan seçmeli soru tipinde sorular üreteceksin. Şık sayısı 4 adet olacak. Yani answers length 4 olacak.
            Her sorunun en sonunda doğru cevabı belirt.
            Bu soruları üretirken json array bir çıktı bekliyorum. 
            Bu arrayda toplam 3 soru olmalı.
            Yorum yapma, ek bilgi verme. Yanlızca aşağıdaki şekilde json çıktı ver.
        
            **Output Format:**
            ```
                [
                    {
                        "question_body": "",
                        "answers": [
                            {"content": ".....", "correct": False},
                            {"content": ".....", "correct": False},
                            {"content": ".....", "correct": False},
                            {"content": ".....", "correct": True},
                            ...
                        ]
                        "question_diffucult_level": "",
                    },
                    ...
                ]
            ```
        """

    # Doğru Yanlış Soru Promtu
    elif q_type == "Doğru Yanlış":
        prompt = """
        Bu direktiflerle doğru-yanlış soruları üret.
        Her sorunun cevabı "Doğru" veya "Yanlış" olarak belirtilmeli.
        Her sorunun en sonunda doğru cevabı belirt.
        Bu soruları üretirken json array bir çıktı bekliyorum. 
        Bu arrayda toplam 3 soru olmalı.
        Yorum yapma, ek bilgi verme. Yanlızca aşağıdaki şekilde json çıktı ver.

        **Output Format:**
            ```
                [
                    {
                        "question_body": "",
                        "answers": [
                            {"content": "Doğru", "correct": True},
                            {"content": "Yanlış", "correct": False},
                        ]
                        "question_diffucult_level": "",
                    },
                    ...
                ]
            ```
        """

    # Boşluk Doldurma Soru Promtu
    elif q_type == "Boşluk doldurma":
        prompt = """
        Bu direktiflerle boşluk doldurma soruları üret:
        Her soru, öğrencinin tamamlaması gereken boşluklar içermeli. Birden çok boşluk doldurma kısmı olabilir.
        Answers'ta yalnızca sorunun doğru cevabı olmalı. Birden çok boşluk varsa, birden çok answer olmalı.
        Her sorunun en sonunda doğru cevabı belirtBu soruları üretirken json array bir çıktı bekliyorum. 
        Bu arrayda toplam 3 soru olmalı.
        Yorum yapma, ek bilgi verme. Yanlızca aşağıdaki şekilde json çıktı ver.

        **Output Format:**
            ```
                [
                    {
                        "question_body": "Soru metni ________ olarak tamamlanmalıdır...?",
                        "answers": [
                            {"content": "...", "correct": True},
                        ]
                        "question_diffucult_level": "",
                    },
                    ...
                ]
            ```
        """

    # Açık Soru Promtu
    elif q_type == "Açık Soru":
        prompt = """
         Bu direktiflerle açık uçlu soru üret(Türkçe'de buna klasik soruda deniyor.):
        Sorular, öğrencinin detaylı yanıt verebileceği şekilde olsun.
        Answers'ta yalnızca sorunun doğru cevabı olmalı.
        Her sorunun en sonunda doğru cevabı belirt.
        Bu soruları üretirken json array bir çıktı bekliyorum. 
        Bu arrayda toplam 3 soru olmalı.
        Yorum yapma, ek bilgi verme. Yanlızca aşağıdaki şekilde json çıktı ver.

        **Output Format:**
            ```
                [
                    {
                        "question_body": "Soru metni...?",
                        "answers": [
                            {"content": "...", "correct": True},
                        ]
                        "question_diffucult_level": "",
                    },
                    ...
                ]
            ```
        """

    # Eşleştirme Soru Promtu
    elif q_type == "Eşleştirme":
        prompt = """
        Vereceğim direktifleri uygulayarak, eşleştirme soruları üret:
        Her soru, iki grup arasında doğru eşleştirme yapmayı gerektirmeli.
        Answers'taki cevapları ';' noktalı virgül ile ayır. Answers'ta yalnızca sorunun doğru cevabı olmalı.
        Her sorunun en sonunda doğru cevabı belirt.
        Bu soruları üretirken json array bir çıktı bekliyorum. 
        Bu arrayda toplam 3 soru olmalı.
        Yorum yapma, ek bilgi verme. Yanlızca aşağıdaki şekilde json çıktı ver.

        **Output Format:**
        ```
        [
            {
                "question_body": "Verilen eşleştirme gruplarını doğru bir şekilde eşleştirin...?",
                "group_a": ["Grup A - 1", "Grup A - 2", ...],
                "group_b": ["Grup B - 1", "Grup B - 2", ...],
                ...
                "answers": [
                    {"content": "Grup A - 1 ; Grup B - 2", "correct": True},
                    {"content": "Grup A - 2 ; Grup B - 1", "correct": True},
                    ...
                ]
            }
        ]
        """

    # Kısa Cevaplı Soru Promtu
    elif q_type == "Kısa Cevaplı":
        prompt = """
        Bu direktiflerle kısa cevaplı soru üret:
        Her soru, öğrencinin kısa bir yanıtla cevaplayabileceği şekilde olmalı.
        Answers'ta yalnızca sorunun doğru cevabı olmalı.
        Her sorunun en sonunda doğru cevabı belirt.
        Bu soruları üretirken json array bir çıktı bekliyorum. 
        Bu arrayda toplam 3 soru olmalı.
        Yorum yapma, ek bilgi verme. Yanlızca aşağıdaki şekilde json çıktı ver.

        **Output Format:**
        ```
            [
                {
                    "question_body": "Soru metni...?",
                    "answers": [
                        {"content": "...", "correct": True},
                    ]
                    "question_diffucult_level": "",
                },
                ...
            ]
        ```
        """
    return prompt


# def get_diff_level_promt(q_diff_level):
    # diff_list = {
    #     "kolay": "Temel bilgileri test eden ve anlaşılır sorular. Örnekler arasında basit tanımlar, yaygın olarak bilinen gerçekler veya temel aritmetik yer almaktadır.",
    #     "orta": "Biraz eleştirel düşünme veya orta düzeyde anlayış gerektiren sorular. Bunlar kavramların birleştirilmesini veya biraz daha az yaygın bilgiyi içerebilir.",
    #     "zor": "İleri düzeyde bilgi veya derin eleştirel düşünme gerektiren sorular. Bunlar genellikle karmaşık problemleri çözmeyi, incelikli konuları anlamayı veya uzmanlık bilgisini kullanmayı içerir.",
    # }
    # diff_level_main_message = f"Soruları üretirken kolay, orta ve zor olarak 3 adet zorluk seviyemiz var. Soruların hepsini {q_diff_level} seviyede üret. {q_diff_level} seviyesindeki sorular şu şekilde olur; {diff_list[q_diff_level]}"
    # return diff_level_main_message
    # return f"Soruları üretirken kolay, orta ve zor olarak 3 adet zorluk seviyemiz var. Soruların hepsi {q_diff_level} zorluk seviyesinde olsun."


def get_prompt(q_type, question_count, q_diff_level):
    system_message_content = f"""
        Sana verilen bilgileri kullanarak {question_count} adet soru üret. Kendi yorumunu veya önceden bildiklerini kullanmadan, sadece verilen bilgilerden sorular oluştur. Soruları yalnızca Türkçe dilinde üret.
        Soruların içerisindeki soru kaynağını göstermiyoruz. Bundan dolayı soruların içerisinde 'metne dayanarak' veya 'metinde geçen' vs. gibi ifadeler kullanma.
        Soruları üretirken kolay, orta ve zor olarak 3 adet zorluk seviyemiz var. Soruların hepsi {q_diff_level} seviyede olsun.
        Sorularda metin görünmeyecek, bunu bilerek üret. Yani metni soruda göstermediğimiz için; metinde geçen, metindeki ... şekilde ifadeler soruda olmamalı.

        Soruların gövdesi soru formatında olsun. Yani soru cümlesi olsun.
        Bu bilgilerle {question_count} adet soru üreteceksin.
        {question_type_prompt(q_type)}
    """
    return system_message_content