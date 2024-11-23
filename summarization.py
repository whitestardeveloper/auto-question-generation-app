import nltk
nltk.download('punkt_tab')
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer


# # Input text to be summarized
# input_text = """
#     OSMANLI DEVLETI’NDE DIN VE INANIŞ
#     Osmanlı Devleti topraklarında din olarak Islamiyet benimsenmiştir. Osmanlı padişahları da Islamiyet’i din olarak seçmiş ve Islam’ın getirdiği kurallara harfiyen uymuşlardır. Osmanlı padişahları Islamiyet’i yaymayı kendilerine vazife bilmişler ve yaptıkları seferler sonunda ele geçirdikleri yerlerde Islamiyet’in yayılması için çalışmışlardır.
#     Osmanlı Devleti’nde kanunlar belirlenip, uygulanırken Kuran ve Hadis temel kaynak olarak belirlenmiş ve Şer’i Hukuk ile Örfi Hukuk birlikte uygulanmıştır.
#     Büyük topların, surları yıktığı görüldü. Topun savaşlardaki önemi arttı. Bu durum, Avrupa’da feodalite rejiminin yıkılmasını kralların güçlenmesini sağladı.
# """

def summarize_text(input_text):
        
    # Parse the input text
    parser = PlaintextParser.from_string(input_text, Tokenizer("turkish"))

    # ###### with lsa sum
    # Create an LSA summarizer
    summarizer = LsaSummarizer()
    # Generate the summary 
    # sentences_count same as token_size
    summary = summarizer(parser.document, sentences_count=15)  # You can adjust the number of sentences in the summary


    # ####### with Lex_rank sum
    # # token limit
    # max_chars = 2000 # chatgpd 3.5 token size
    # # Create an Lex_rank summarizer
    # summarizer_lex_rank = LexRankSummarizer()
    # # Özetleme
    # summary = summarizer_lex_rank(parser.document, 5)




    # # Output the summary
    # # print("Original Text:")
    # # print(input_text)

    # print("\nSummary:")

    output_text = ''
    for sentence in summary:
        output_text += f"{sentence} "

    # print(output_text)

    return output_text