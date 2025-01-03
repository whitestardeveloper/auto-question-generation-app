from firebase_application import get_generated_question_list, add_question_ai_reviewer
import json
import ollama

def get_json_array_question(question_raw_list):
    if isinstance(question_raw_list, str):
        question_raw_list = question_raw_list.replace("```json", "").replace("```", "")
        question_raw_list = question_raw_list.replace("False", "false").replace("True", "true")
    try:
        parsed_json = json.loads(question_raw_list)
        return parsed_json if isinstance(parsed_json, list) else []
    except json.JSONDecodeError as error:
        print("JSON decode error:", error)
        return [] 

def get_question_evaluation_prompt(questionType, questionDiffLevel):
    return f"""
        Sana verdiğim JSON formatındaki soruları aşağı şekilde ayrı ayrı değerlendirmeni istiyorum. 
        Değerlendirmeleri aşağıdaki sorulara göre yap.
        Değerlendirmelerde **evaluation_value** alanlarında 1-5 arası score'lar ver. Puan verirken adil ve dengeli olmaya özen göster. Lütfen her soruyu aşağıdaki yönergelere uygun olarak değerlendir:

        1. **Sorular anlamlı mı ve soru formatına uygun mu?**
        - Sorunun dil bilgisi, yapısı ve ifadesi doğru mu?
        - Sorunun ifade biçimi açık ve net mi, gereksiz karmaşıklıktan arındırılmış mı?
        
        **Puanlama Kriteri:**
        - **1:** Anlamsız, dil bilgisi hataları içeriyor.
        - **2:** Bazı anlam belirsizlikleri veya dil bilgisi hataları var.
        - **3:** Anlamlı fakat dil veya formatta küçük sorunlar var.
        - **4:** Dil ve format doğru, ancak küçük eksiklikler olabilir.
        - **5:** Mükemmel, hiçbir dil hatası veya eksiklik yok.

        2. **Soruların tipi uygun mu?**
        - Sorular belirlenen tip "{questionType}" kriterine uygun şekilde yapılandırılmış mı?
        - Sorunun tipi ile içerik uyumlu mu? Örneğin, çoktan seçmeli bir soru için şıkların birbirinden ayrıştırılabilir olması sağlanmış mı?

        **Puanlama Kriteri:**
        - **1:** Sorunun tipi tamamen uyumsuz, format hatalı.
        - **2:** Tip uyumsuzluğu var, ama yine de anlaşılabilir.
        - **3:** Tip uyumu orta düzeyde, bazı ufak hatalar mevcut.
        - **4:** Tip uygun, ancak küçük düzenlemeler gerekebilir.
        - **5:** Tam anlamıyla doğru tipte ve içerik uyumlu.

        3. **Soruların zorluk seviyesi uygun mu?**
        - Sorular, "{questionDiffLevel}" olarak belirlenen zorluk seviyesine uygun mu?
        - Sorunun çözümü için gereken bilgi ve bilişsel süreçler Bloom Taksonomisi’ne göre doğru seviyede mi? (Hatırlama, anlama, uygulama, analiz, değerlendirme, yaratma).
        
        **Puanlama Kriteri:**
        - **1:** Zorluk çok düşük veya çok yüksek, tamamen uyumsuz.
        - **2:** Zorluk seviyesi yeterince uygun değil.
        - **3:** Ortalama zorluk seviyesi, ancak daha fazla derinlik veya karmaşıklık eklenebilirdi.
        - **4:** Zorluk uygun, ama biraz daha zorlaştırılabilir.
        - **5:** Tam olarak belirtilen zorluk seviyesine uygun, ideal.

        4. **Soruların doğru cevabı gerçekten doğru mu?**
        - Sorunun doğru cevabı, doğrulanabilir ve kaynaklarla desteklenebilir bir bilgiye dayanıyor mu?
        - Doğru cevap, sorunun açıkça istediği bilgiye uyum sağlıyor mu?

        **Puanlama Kriteri:**
        - **1:** Doğru cevap tamamen yanlış veya yanıltıcı.
        - **2:** Doğru cevap eksik veya hatalı.
        - **3:** Cevap doğru fakat bazı eksiklikler veya belirsizlikler mevcut.
        - **4:** Cevap doğru, ancak küçük bir detay eksik.
        - **5:** Mükemmel doğru cevap, tam uyumlu.

        5. **Soruların cevap seçenekleri anlamlı ve birbiriyle alakalı mı?**
        - Tüm seçenekler, sorunun bağlamına uygun mu ve yanıltıcı (trick) şıklardan kaçınılmış mı?
        - Seçenekler, aralarında net bir şekilde doğru cevabı ayırt etmeyi mümkün kılıyor mu?

        **Puanlama Kriteri:**
        - **1:** Seçenekler yanıltıcı veya anlamsız.
        - **2:** Seçeneklerin bazıları uyumsuz ve kafa karıştırıcı.
        - **3:** Seçenekler çoğunlukla anlamlı, ancak bir veya iki yanıltıcı seçenek var.
        - **4:** Seçenekler anlamlı ve aralarındaki doğru cevabı ayırt etmek mümkün.
        - **5:** Seçenekler mükemmel uyumlu ve doğru cevabı net bir şekilde ayrıştırabiliyor.

        6. **Sorular tek başına cevaplanabilir mi?**
        - Sorunun metni, gerekli tüm bilgiyi içeriyor mu, yoksa eksik veya bağlam dışı bilgi nedeniyle cevapsız kalma riski taşıyor mu?
        - Verilmeyen ancak cevap istenen şeyler mevcut mu? (Örneğin soru metninde olmayan bir bilgiden cevap istenmiş mi?)

        **Puanlama Kriteri:**
        - **1:** Cevaplanamaz, eksik veya yanlış bilgi var.
        - **2:** Cevaplanabilir ama eksik bilgi mevcut.
        - **3:** Cevaplanabilir, ancak bazı detaylar eksik veya belirsiz.
        - **4:** Çoğunlukla tek başına cevaplanabilir, küçük eksiklikler olabilir.
        - **5:** Sorunun metni yeterli ve tam, tek başına cevaplanabilir.
        ---

        ### **Önemli Notlar:**

        - Eğer **parça**, **metin** veya **belirli bir bilgi** soruda verilmemişse, o sorunun eksik olduğu ve doğru değerlendirme yapmanın zor olduğu belirtilmelidir. Bu durumda **evaluation_value** daha düşük verilmelidir. Bu durumda şu şekilde bir ekleme yapın:

        ---

        **Özel Durumlar (Eksiklik Bildirimi)**
        - Eğer **parça**, **metin** veya **belirli bir bilgi** verilmeden "parçada ne anlatılmak isteniyor?" veya "bu metni analiz edin" gibi sorular sorulmuşsa:
        - **Eksik Bilgi Durumu**: Soruda gerekli parça veya metin verilmemişse, bu durum eksiklik olarak belirtilmeli ve değerlendirme puanı buna göre verilmelidir.
        - **Puanlama Kriteri**: 
            - **1**: Soruda verilen parça veya metin eksik, soruya cevap vermek imkansız.
            - **2**: Soruda verilen parça veya metin eksik, ama genel bir değerlendirme yapılabilir.
            - **3**: Soruda eksiklik var ama yine de soru kısmen anlaşılabilir.
            - **4**: Soruda eksiklik var, ancak verilen ipuçlarıyla bir çözüm üretilebilir.
            - **5**: Eksiklik yok, gerekli tüm bilgi verilmiş ve soruya doğru cevap verilebilir.
       
        ---

       ### **JSON Çıktısı Formatı:**
        Her soru için aşağıdaki gibi bir JSON çıktısı bekleniyor. Tüm değerlendirme başlıkları mutlaka dolu olmalıdır:

        ```
        [
            {{
                "question-index": 1,
                "evaluations": {{
                    "q1": {{
                        "evaluation_type": "Relevance and Format Appropriateness",
                        "evaluation_question": "Sorular anlamlı mı ve soru formatına uygun mu?",
                        "evaluation_value": 4,
                        "description": "Açıklama..."
                    }},
                    "q2": {{
                        "evaluation_type": "Question Type Appropriateness",
                        "evaluation_question": "Soruların tipi uygun mu?",
                        "evaluation_value": 5,
                        "description": "Açıklama..."
                    }},
                    "q3": {{
                        "evaluation_type": "Difficulty Level Appropriateness",
                        "evaluation_question": "Soruların zorluk seviyesi uygun mu?",
                        "evaluation_value": 3,
                        "description": "Açıklama..."
                    }},
                    "q4": {{
                        "evaluation_type": "Correct Answer Validity",
                        "evaluation_question": "Soruların doğru cevabı gerçekten doğru mu?",
                        "evaluation_value": 3,
                        "description": "Açıklama..."
                    }},
                    "q5": {{
                        "evaluation_type": "Answer Choices Coherence",
                        "evaluation_question": "Soruların cevap seçenekleri anlamlı ve birbiriyle alakalı mı?",
                        "evaluation_value": 5,
                        "description": "Açıklama..."
                    }},
                    "q6": {{
                        "evaluation_type": "Self-Containment",
                        "evaluation_question": "Sorular tek başına cevaplanabilir mi?",
                        "evaluation_value": 2,
                        "description": "Açıklama..."
                    }}
                }}
            }},
            ...
        ]
        ```
    """

def ai_generate_evaluation(system_prompt, user_propmt):
    selected_model = 'gemma2:27b'

    generate_params = {
        "model": selected_model,
        # 'options': Options(temperature=0.7),
        "prompt": user_propmt,
        # 'system': system_prompt,
        "system": system_prompt,  # rates_json verisini prompt içinde gönder
        "format": "json",
        # "format": Rates.model_json_schema(),
    }   

    response = ollama.generate(**generate_params)
    return response["response"]


def run():
    question_list = get_generated_question_list()
    for key, obj_item in question_list.items():
        questions = obj_item['data']['generated_questions']
        question_type = obj_item['questions_info']['question_type']
        question_difficulty_level = obj_item['questions_info']['question_difficulty_level']

        key_index = int(key.replace('question-', ''))
        if key_index > 1:
            system_prompt = get_question_evaluation_prompt(question_type, question_difficulty_level)
            generated_evaluation = ai_generate_evaluation(system_prompt, questions)
            add_question_ai_reviewer(generated_evaluation, key)
            print(generated_evaluation)
            print(f" completed => {key}")
         
run()
