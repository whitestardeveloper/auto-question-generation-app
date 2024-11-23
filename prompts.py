# models = ["GOOGLE (gemini-1.5-flash)", "GOOGLE (gemma2)", "MISTRAL (mistral-nemo)", "META (llama3.1)",  "ALIBABA (qwen2.5)", "NVIDIA (nvidia/nemotron-4-340b-instruct)", "Cohere For AI (aya-expanse)[8B]"]
# q_diff_levels = ['kolay', 'orta', 'zor']
# q_types=["Çoktan Seçmeli", "Doğru Yanlış", "Boşluk doldurma", "Açık Soru", "Eşleştirme", "Kısa Cevaplı"]

def get_prompt(q_type ,question_count, q_diff_level):
    # question_choice_count = "4 şıklı"
    # system_message_content = """
    #     Sana verilen bilgileri kullanarak hiç yorum yapmadan kendi fikirlerini veya önceden bildiklerini kullanmadan  cevap verirsin. 
    #     Sadece sana verilen bilgilerle cevap verirsin. 
    #     Hiçbir şekilde verilenlerin dışına çıkmazsın. 
    #     Cevaplarının en sonunda da doğru cevabı söylersin.
    #     """

    # ****** | ****** | ****** | ****** | ****** | ******
    system_message_content = """
        Sana verilen bilgileri kullanarak hiç yorum yapmadan kendi fikirlerini veya önceden bildiklerini kullanmadan cevap verirsin. 
        Sadece sana verilen bilgilerle cevap verirsin. 
        Hiçbir şekilde verilenlerin dışına çıkmazsın. 
        Cevaplarının en sonunda da doğru cevabı söylersin.
    """

    # Çoktan Seçmeli Soru Promtu
    if q_type == "Çoktan Seçmeli":
        prompt = f"""
        Vereceğim direktifleri uygulayarak, bu bilgilerle {q_diff_level} seviyesinde {question_count} adet çoktan seçmeli soru üret:
        Her soru {q_diff_level} seviyesinde olmalı ve dört seçenekli (A, B, C, D) olarak sunulmalı. Sadece verilen metne dayanarak soruları üret.
        En sonunda doğru cevabı belirt.
        """
    
    # Doğru Yanlış Soru Promtu
    elif q_type == "Doğru Yanlış":
        prompt = f"""
        Vereceğim direktifleri uygulayarak, bu bilgilerle {q_diff_level} seviyesinde {question_count} adet doğru-yanlış sorusu üret:
        Her sorunun cevabı "doğru" veya "yanlış" olarak belirtilmeli. Sadece verilen metne dayanarak soruları üret.
        Her sorunun en sonunda doğru cevabı belirt.
        """
    
    # Boşluk Doldurma Soru Promtu
    elif q_type == "Boşluk doldurma":
        prompt = f"""
        Vereceğim direktifleri uygulayarak, bu bilgilerle {q_diff_level} seviyesinde {question_count} adet boşluk doldurma sorusu üret:
        Her soru, öğrencinin verilen metindeki bilgiyi tamamlamasını sağlayacak bir boşluk içermeli. Sadece verilen metne dayanarak soruları üret.
        Her sorunun en sonunda doğru cevabı belirt.
        """

    # Açık Soru Promtu
    elif q_type == "Açık Soru":
        prompt = f"""
        Vereceğim direktifleri uygulayarak, bu bilgilerle {q_diff_level} seviyesinde {question_count} adet açık uçlu soru üret:
        Her soru, öğrencinin verilen metne dayalı olarak detaylı cevap vermesini sağlamalı. Sadece verilen metne dayanarak soruları üret.
        Her sorunun en sonunda doğru cevabı belirt.
        """

    # Eşleştirme Soru Promtu
    elif q_type == "Eşleştirme":
        prompt = f"""
        Vereceğim direktifleri uygulayarak, bu bilgilerle {q_diff_level} seviyesinde {question_count} adet eşleştirme sorusu üret:
        Her soru, iki grup arasında doğru eşleştirme yapmayı gerektirmeli. Sadece verilen metne dayanarak soruları üret.
        Her sorunun en sonunda doğru eşleştirmeleri belirt.
        """
    
    # Kısa Cevaplı Soru Promtu
    elif q_type == "Kısa Cevaplı":
        prompt = f"""
        Vereceğim direktifleri uygulayarak, bu bilgilerle {q_diff_level} seviyesinde {question_count} adet kısa cevaplı soru üret:
        Her soru, öğrencinin kısa bir yanıtla cevaplayabileceği şekilde olmalı. Sadece verilen metne dayanarak soruları üret.
        Her sorunun en sonunda doğru cevabı belirt.
        """
    
    # Sistem Mesajı ve Metin İçeriğini Birleştirme
    final_prompt = system_message_content + prompt
    return final_prompt


    # multiple_choices_promt = f"""
    #     Vereceğim direktifleri uygulayarak, bu verilen bilgilerle soru üteceksin;
    #     Üç adet zorluk seviyemiz var. Bu seviyeler kolay, orta ve zordur. Üreteceğin tüm sorular {q_diff_level} seviyesinde olsun.
    #     Çoktan seçmeli, {question_choice_count} şıklı olsun.
    #     Şimdi bu bilgilere dayanarak {question_count} adet soru üretir misin?
    # """

    # propmt = '"'+ text + '"'+  system_message_content + multiple_choices_promt
    # return propmt