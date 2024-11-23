from ollama import  Options
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
    # selected_model in ['llama3.1', 'mistral','mistral-nemo', 'phi3.5', 'qwen2.5', 'gemma2', 'granite3-moe:3b' , 'granite3-dense', 'aya-expanse', 'nemotron-mini']:
    selected_model = get_model(model_key)
    print(selected_model)

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


    response = ollama.generate(model=selected_model, prompt=promt+system_prompt)
    return response['text']


promt = """
Sözcükte Anlam
Sözcükte Anlam Nedir?
Sözcükte anlam, bir kelimenin taşıdığı veya temsil ettiği anlamdır. Sözcüklerin anlamları, sözlüklerde veya dil bilgisi kitaplarında tanımlanabilir. Anlam, kelimenin içeriğinde ve kullanım bağlamında belirlenir. Kelimenin kökeni, kullanıldığı dönem veya bölge, yan anlamları ve kullanım amacı gibi faktörler, bir kelimenin anlamını etkileyebilir. Sözcüklerin anlamlarının doğru bir şekilde anlaşılması, dilin doğru kullanımı için çok önemlidir.

Anlam Bakımından Sözcükler
1. Gerçek (Temel) Anlam
Gerçek anlam, bir kelimenin veya ifadenin tam ve doğru anlamıdır. Bu, kelimenin veya ifadenin kullanıldığı bağlama ve amaca uygun olarak anlaşılması gerektiği anlamına gelir. Gerçek anlam, kelimenin sözlük tanımına ve etimolojisine uygun olan anlamdır. Ancak bazı durumlarda, bir kelimenin gerçek anlamı, günlük kullanımda farklı anlamlar kazanmış olabilir. Bu nedenle, bir kelimenin gerçek anlamını anlamak için, kullanıldığı bağlamı ve amacı dikkate almak önemlidir.

Gerçek Anlamlı Sözcükler
Bugün eve erken gittim.

Dün akşam yemek yedik.

Daha önce buraya hiç gelmedim.

Akşamları elma yemeyi severim.

Her sabah çay içiyorlar.

2. Yan Anlam (Yakıştırmaca)
Yan anlam, bir kelimenin gerçek anlamının dışında, ona benzer veya ilişkili bir anlam taşıyan ikincil bir anlamdır. Bu ikincil anlam, kelimeyle ilgili başka bir düşünceyi ya da çağrışımı anlatır. Yakıştırma, çağrışım, ilişki ve zıtlık yoluyla yan anlamlar oluşabilir.

Örneğin, “diksiyonu düzgün” ifadesinde, “düzgün” kelimesi kelimenin gerçek anlamı olan “düz” anlamını ifade etmek yerine, kişinin konuşmasının akıcı ve anlaşılır olmasıyla ilgili bir yan anlam taşır.

Başka bir örnek olarak, “beyaz atlı prens” ifadesinde, “beyaz atlı” kelimesi kelimenin gerçek anlamı olan atın rengi ve atın üstündeki kişinin giysisinin rengiyle ilgili bir yan anlam taşır. “Prens” kelimesi ise gerçek anlamı olan kraliyet ailesinden gelen erkeklerin unvanı yanında, kahramanlık, cesaret ve fedakarlıkla ilgili bir yan anlam taşır.

Yan anlam, metinlerde daha zengin ve çeşitli ifadeler kullanmak için kullanılır ve anlatımı güçlendirmek, okuyucunun dikkatini çekmek veya bir fikri daha iyi ifade etmek amacıyla kullanılır.

3. Mecaz Anlam (Değişmece)
Mecaz anlam, kelimenin gerçek veya sözlük anlamından farklı bir anlamda kullanılmasıdır. Bu, bir kelimenin gerçek anlamının ötesinde bir anlam ifade edilmesi anlamına gelir. Bu anlam türüne değişmece (figüratif anlam) denir. Mecaz anlam, bir kelimenin kullanıldığı bağlamdan ve metinden anlaşılabilir.

Örneğin, “sınavda çuvallamak” deyimi, gerçek anlamıyla sınavda bir çuvala girmek anlamına gelmez. Bu ifade, sınavda başarısız olmak, beklenen performansı gösterememek anlamlarında kullanılır. Bu kullanım, kelimenin gerçek anlamından farklı bir anlam taşıdığı için mecaz anlam olarak kabul edilir.

Mecaz anlam, dilin daha renkli, canlı ve etkileyici hale getirilmesine yardımcı olur. Şiir, edebiyat, hitabet ve günlük dil gibi birçok alanda kullanılır.

Gerçek Anlam ile Mecaz Anlam Arasındaki Farklar Nedir?
Gerçek anlam ve mecaz anlam arasındaki farklar şunlardır:

Anlam: Gerçek anlam, kelimenin sözlük anlamıdır ve kelimenin nesnel anlamını ifade ederken, mecaz anlam, kelimenin gerçek anlamından farklı, figüratif bir anlam taşır.
Kullanım: Gerçek anlam, kelimenin doğru ve nesnel kullanımını ifade ederken, mecaz anlam, kelimenin bir bağlamda gerçek anlamından farklı bir anlamda kullanımını ifade eder.
İfade: Gerçek anlam, kelimenin somut bir şeyi ifade ettiği anlamda kullanılırken, mecaz anlam, kelimenin soyut bir şeyi ifade ettiği anlamda kullanılır.
Düz anlam: Gerçek anlam, kelimenin en basit ve doğrudan anlamıdır ve çoğu zaman açık ve anlaşılırdır. Mecaz anlam ise, kelimenin gerçek anlamından farklı ve daha karmaşık bir anlam taşır ve anlamı genellikle bağlamdan ve kullanıldığı metinden anlaşılır.
Özetle, gerçek anlam, kelimenin doğru ve nesnel anlamını ifade ederken, mecaz anlam, kelimenin gerçek anlamında

4. Terim Anlam
Terim, belirli bir konuda kullanılan özel bir dil veya kelime kullanımıdır. Terimler, bir disiplinin ya da konunun uzmanları arasında anlaşılabilir ve kesin bir anlam taşırlar. Terimler, genellikle teknik, bilimsel veya hukuki alanda kullanılır ve bu alanlarda kullanılan özel jargonu ifade eder.

Terimlerin amacı, belirli bir alanda çalışan kişilerin aralarında daha kesin ve doğru bir iletişim kurmalarına yardımcı olmaktır. Terimler, aynı alanda çalışan farklı kişiler arasında da bir iletişim köprüsü oluşturur.

Örneğin, tıp alanında kullanılan terimler, doktorların hastalıklar hakkında kesin bir şekilde konuşmalarını sağlar. Benzer şekilde, hukuk terimleri, avukatların yasal konular hakkında kesin bir şekilde iletişim kurmalarına yardımcı olur.

Terimler, dilin zenginliğini artırır ve farklı konularda uzmanlaşmış insanlar arasında daha verimli bir iletişim sağlar.

Terim Anlamlı Sözcükler
Terim anlamlı sözcükler, bir disiplin veya konu ile ilgili özel bir dilde kullanılan ve belirli bir anlama sahip olan kelimelerdir. Bu sözcükler, belirli bir alanda çalışan kişiler arasında anlaşılır ve kesin bir anlam taşırlar.

Örneğin, tıp alanında kullanılan terim anlamlı sözcükler şunları içerebilir:

Biyopsi: bir doku örneğinin alınması
Onkoloji: kanser tedavisi
Anatomi: insan veya hayvan vücudunun yapısı ve bileşimi
Nöroloji: sinir sistemi hastalıkları ve tedavisi
Endokrinoloji: hormon sistemi hastalıkları ve tedavisi
Benzer şekilde, hukuk alanında kullanılan terim anlamlı sözcükler şunları içerebilir:

Davacı: bir dava açan kişi
Sanık: bir suçla suçlanan kişi
Ceza: bir suçun cezası
Miras: bir kişinin ölümünden sonra mal ve mülklerinin devri
Hakim: yargılamayı yapan kişi
Terim anlamlı sözcükler, belirli bir konu hakkında doğru ve kesin bir iletişim kurulmasına yardımcı olur ve o alanda çalışan kişiler arasında ortak bir dil oluşturur.

5. Somut ve Soyut Anlam
Somut anlam, duyularla algılanabilen, elle tutulur veya gözle görülür olan şeylerin anlamını ifade eder. Bu anlamda, somut anlamlı kelimeler fiziksel nesneler, varlıklar ve maddeler ile ilgilidir.

Örnek olarak, “masa”, “kitap”, “kedi” gibi kelimeler somut anlam taşırlar. Bu kelimelerin anlamları, gerçek dünyada var olan nesneler ve varlıklarla ilgilidir ve bu nesnelerin özellikleri, boyutları ve görünümleri ile ilgilidir.

Soyut anlam, duyularla algılanamayan ve elle tutulamayan kavramların anlamını ifade eder. Bu anlamda, soyut anlamlı kelimeler, fikirler, duygular, kavramlar, davranışlar ve ilişkiler ile ilgilidir.

Örnek olarak, “sevgi”, “adalet”, “mutluluk” gibi kelimeler soyut anlam taşırlar. Bu kelimelerin anlamları, somut nesnelere benzetilerek anlatılamaz ve kişinin kendi deneyimleri, duyguları ve düşünceleri ile ilişkilidir. Bu tür kelimelerin anlamı, kişiden kişiye değişebilir ve herkes tarafından aynı şekilde algılanmayabilir.

6. Nitel ve Nicel Anlam
Bir varlığın ölçülebilir bir başka deyişle sayılabilen özelliklerine ait anlamına nicel deriz.

Nitel anlam da tahmin edebileceğin gibi varlığın ölçülemeyeni sayılamayan özelliklerine aittir. Varlığın niteliğini, yani nasıl olduğunu gösterir.

3
Anlam İlişkisi Bakımından Sözcükler
1. Eş Anlamlı (Anlamdaş) Sözcükler
Eş anlam, aynı veya benzer anlama sahip olan kelimelerin veya ifadelerin kullanımıdır. Yani, bir kelimenin veya ifadenin yerine kullanılabilecek başka bir kelime veya ifadeye eş anlam denir. Örneğin, “mutlu” kelimesinin eş anlamlısı “neşeli” veya “mesut” olabilir. Eş anlamlı kelimelerin kullanımı, metinlerin veya konuşmaların daha zengin ve çeşitli olmasına yardımcı olabilir. Ancak, her eş anlamlı kelime veya ifade, tamamen aynı anlamı taşımaz ve kullanıldıkları bağlam ve cümleler farklılık gösterebilir.

Eş Anlamlı Sözcük Örnekleri
Eş anlamlı sözcükler aşağıdaki gibi sıralanabilir:

Mutlu: Neşeli, keyifli, mesut
Hüzünlü: Üzgün, kederli, gamlı
Büyük: Devasa, iri, kocaman
Küçük: Minik, ufak, çocukça
Güzel: Şık, hoş, estetik
Zayıf: Cılız, ince, nazik
Güçlü: Kuvvetli, sağlam, dayanıklı
Temiz: Sağlam, hijyenik, steril
Kirli: Pis, lekeli, paslı
Kolay: Basit, sade, rahat
Zor: Güç, meşakkatli, müşkül
Sevgi: Aşk, muhabbet, bağlılık
Saygı: İtibar, hürmet, onur
Doğru: Yanlışsız, gerçek, dürüst
Yanlış: Hatalı, yanıltıcı, yanılgılı.
Tabii, bu sadece birkaç örnek, ama Türkçe’de sayısız eş anlamlı kelime vardır. Ancak, belirtmek gerekir ki, her eş anlamlı kelime, tamamen aynı anlamı taşımaz ve kullanıldıkları bağlam ve cümleler farklılık gösterebilir.

2. Eş Sesli (Sesteş) Sözcükler
Bu tip sözcüklerin hem yazılışı hem de okunuşu aynı olsa bile aslında farklı anlamdadırlar,. Sadece sesleri aynı olduğu için eş sesli denmiştir.

Eş Sesli Sözcük Örnekleri
Eş sesli sözcükler, okunuşları aynı, ancak anlamları farklı olan kelimelerdir. Türkçe’de birçok eş sesli kelime bulunmaktadır. Bazı örnekler şunlardır:

Daire: Hem bir geometrik şekil hem de bir kurumun ofisi anlamına gelir.
Kalem: Hem yazma aracı hem de maden cevheri olarak kullanılan bir kelime.
Demir: Hem bir metal elementi hem de “dayanıklı” anlamında kullanılan bir kelime.
Yaz: Hem bir mevsim hem de yazma işi anlamında kullanılan bir kelime.
Fırça: Hem resim yapmak için kullanılan bir araç hem de saçların düzleştirilmesi için kullanılan bir alet.
Yol: Hem bir ulaşım yolu hem de bir seyahat anlamına gelir.
Top: Hem bir spor aracı hem de bir şekil anlamına gelir.
Diken: Hem bir bitki parçası hem de batıcı bir nesne anlamına gelir.
Anahtar: Hem bir kilit açma aracı hem de bir şeyin ana ve önemli parçası anlamına gelir.
3. Zıt Anlamlı Sözcükler
Zıt anlam, bir kelimenin veya ifadenin anlamıyla tamamen ters olan bir kelimenin veya ifadenin kullanımıdır. Örneğin, “sıcak” kelimesinin zıt anlamlısı “soğuk” veya “yakın” kelimesinin zıt anlamlısı “uzak” olabilir. Zıt anlamlı kelimeler, bir karşıtlık veya tezat oluşturarak anlatımı daha etkili hale getirebilir. Bununla birlikte, zıt anlamlı kelimeler arasında tam bir karşıtlık olmayabilir ve kelime kullanımı, cümlenin veya metnin bağlamına bağlı olarak değişebilir.

Zıt Anlamlı Sözcük Örnekleri
Zıt anlamlı sözcükler aşağıdaki gibi sıralanabilir:

Sıcak – Soğuk
Büyük – Küçük
Hızlı – Yavaş
İyi – Kötü
Açık – Kapalı
Siyah – Beyaz
Genç – Yaşlı
Zengin – Fakir
Güzel – Çirkin
Doğru – Yanlış
Acı – Tatlı
Kuru – Islak
Kolay – Zor
Ön – Arka
Dış – İç
Tabii ki, bu sadece birkaç örnek. Türkçe’de sayısız zıt anlamlı kelime vardır. Ancak, belirtmek gerekir ki, her zıt anlamlı kelime tam bir karşıtlık oluşturmayabilir ve kelime kullanımı, cümlenin veya metnin bağlamına bağlı olarak değişebilir.

4. Yakın Anlamlı Sözcükler
Yakın anlamlı sözcükler ilk başta kafanı karıştırabilir ama biraz düşününce hemen anlayacağını düşünüyoruz. Yakın anlamlı sözcükler tıpkı eş anlamlı sözcükler gibi gözükürler yani yazılışları farklıdır. Eş anlamlı sözcüklerin anlamı bire birken yakın anlamlı sözcüklerin anlamlarında birbirinden farklılık vardır.

Yani her zaman birbirlerinin yerine kullanılamazlar!

Yakın Anlamlı Sözcük Örnekleri
Mutlu: Neşeli, keyifli, sevinçli
Hüzünlü: Üzgün, kederli, gamlı
Büyük: Devasa, iri, kocaman
Küçük: Minik, ufak, çocukça
Güzel: Şık, hoş, estetik
Zayıf: Cılız, ince, narin
Güçlü: Kuvvetli, sağlam, dayanıklı
Temiz: Sağlam, hijyenik, steril
Kirli: Pis, lekeli, paslı
Kolay: Basit, sade, rahat
Zor: Güç, meşakkatli, müşkül
Sevgi: Aşk, muhabbet, bağlılık
Saygı: İtibar, hürmet, onur
Doğru: Yanlışsız, gerçek, dürüst
Yanlış: Hatalı, yanıltıcı, yanılgılı
Tabii ki, bu sadece birkaç örnek. Türkçe’de sayısız yakın anlamlı kelime vardır. Ancak, belirtmek gerekir ki, her yakın anlamlı kelime, tamamen aynı anlamı taşımaz ve kullanıldıkları bağlam ve cümleler farklılık gösterebilir.

5. Genel ve Özel Anlamlı Sözcükler
Genel anlam, bir kelimenin veya ifadenin en yaygın veya standart anlamıdır. Sözlük anlamı olarak da düşünülebilir. Bu anlam, kelimenin veya ifadenin kullanıldığı bağlamdan bağımsız olarak genel kabul gören anlamdır.

Özel anlam, bir kelimenin veya ifadenin genel kabul gören anlamından farklı olarak, belirli bir bağlam veya durumda özelleşmiş anlamdır. Bu anlam, belirli bir grup insan veya belirli bir alanda kullanılan jargon veya argo terimleri gibi durumlarda ortaya çıkabilir.

6. Ad Aktarması (Mecazımürsel)
Ad aktarması bir sözcüğün başka sözcük yerine benzetme amacı olmadan doğrudan kullanılmasıdır.

Ad Aktarması Örnekleri
“Beni evden yemeğe bekliyorlar.” cümlesinde ev sözcüğü benzetme olmaksızın doğrudan aile sözcüğü yerine kullanılmıştır.
“Milyonlar tek yürek bu anı bekliyordu.” cümlesinde milyonlar sözcüğü yine benzetme amacı olmadan halk sözcüğü yerine kullanılmıştır.

Söz Öbekleri
1. Yansıma Sözcükler
Doğadaki seslerin taklit edilmesiyle oluşan sözcüklerdir.

pat

gurul

vızır

hışırtı

cıvıltı

2. İkilemeler
İkileme bir kelimenin veya sözcüğün aynı veya benzer anlamdaki kelimelerle bir araya getirilerek tekrar edilmesiyle oluşan söz sanatıdır. İkilemeler, dilde vurgu ve anlam güçlendirmesi amacıyla kullanılır ve genellikle şiirlerde, deyimlerde, atasözlerinde ve günlük konuşmalarda sıkça görülür.

İkilemeler, anlamını pekiştirirken ritmik ve hoş bir söyleyiş sağlar. Türkçe’de sıkça kullanılan ikilemelerden bazıları şunlardır:

sağ sol
gürültü patırtı
yol yordam
iç içe
yavaş yavaş
kara kara
usul usul
İkilemeler, dilin zenginliğini artıran ve anlatımı güçlendiren unsurlardır. Ayrıca, bazı ikilemeler Türkçede atasözü ve deyimlerin içinde de yer alabilir ve bu deyimlerin anlamına derinlik katarlar.

3. Deyimler
Deyim, dilin figüratif veya mecazi anlamları kullanarak oluşturduğu sabit ifadelerdir. Bir deyim, kelime kelime alındığında tam anlamıyla anlaşılmayabilir ve birebir çeviriyle açıklanamaz. Genellikle özel bir anlam taşıyan bu tür ifadeler, dilin renk ve zenginliğini artırır ve iletişimde daha etkili ve çarpıcı ifadeler kullanmamızı sağlar.

Deyimler, bir toplumun veya dilin özelliklerine özgü olabilir ve belli bir bölgede veya toplulukta yaygın olarak kullanılırlar. Ayrıca, deyimler zaman içinde ortaya çıkabilir, değişebilir ve yeni deyimler dilimize kazandırılabilir. Dilin kullanıldığı edebiyat, günlük konuşmalar, hikayeler ve yazılı metinlerde sıkça rastlanan deyimler, dilin renkli ve etkileyici bir şekilde kullanılmasını sağlar.

Deyim Örnekleri
Yaka silkmek: Bir kişi ya da durumdan sıkılmak.

Ateş püskürmek: Aşırı derecede sinirlenmek, kızmak.

Göze girmek: İlgi ve değer kazanmak.

Pabucu dama atılmak: Önemini kaybetmek

Dolap çevirmek: Birilerinden habersiz gizlice iş çevirenler için kullanılır.

Yelkenleri suya indirmek: Israrından vazgeçip karşı tarafın isteklerini kabul etmek, kabullenmek

Zıvanadan çıkmak: Çok öfkelenmek, sinirlenmek, delirmek anlamlarında kullanılır.

Ok yaydan çıkmak: Geri dönülemeyecek bir adım atmak, iş yapmak

Öpüp başına koymak: Bir şeyi memnuniyetle karşılamak, severek kabul etmek

Ağzı laf yapmak: Güzel ve ikna edici konuşmak

Ağızdan düşürmemek: Sürekli bir şeyden bahsetmek

Kafadan atmak: Bir konuda bilgi sahibi olmadan konuşmak

Kara gün dostu: Sıkıntılı ve kötü günlerde yanında olan dost

Kesenin ağzını açmak: Fazladan para harcamaya başlamak

Yüzünü gören cennetlik: Uzun bir süre ortalıkta gözükmeyen kişi

Beş parasız: Zengin olmamak, varlıklı olmayan kişi

Biçilmiş kaftan: Bir iş ya da durum için en uygunu olmak

Bir köşeye çekilmek: Tüm işleri bırakıp olanlara karışmamak

Borusu ötmek: Sözü geçmek, korkulan kişi olmak

4. Atasözleri
Atasözü, halk arasında yaygın olarak kullanılan, deneyim ve bilgelik içeren kısa ve özlü cümlelerdir. Bu cümleler, nesilden nesle aktarılarak birçok kişi tarafından benimsenmiş ve kullanılmıştır. Atasözleri, genellikle toplumun değerleri, ahlaki öğütler, doğru davranış biçimleri, yaşamın gerçekleri ve deneyimlerle ilgili bilgileri içerir. Türkçede de yaygın olan atasözleri, dilimize özgü ve zengin bir kültürel mirasa sahiptir. Bu atasözleri sayesinde birçok insan, günlük yaşamlarında karşılaştıkları durumlara yönelik bilgelik dolu tavsiyeler alır ve bu sözleri paylaşarak iletişim kurar.

Atasözü Örnekleri
“Damlaya damlaya göl olur.” Anlamı: Küçük görünen bir etki, zamanla birikerek büyük sonuçlara yol açabilir.
“Akıllı oğlan evde oturmaz.” Anlamı: Zeki ve becerikli insanlar, işlerini yerine getirmek için sürekli aktif olmalıdır.
“El eli yıkar, yüz yüzü.” Anlamı: Birlikte hareket ederek, işler daha hızlı ve verimli bir şekilde tamamlanabilir.
“Dost kara günde belli olur.” Anlamı: Zor zamanlarda gerçek dostlarınızı ve destekçilerinizi tanırsınız.
“Her taşın altından kurbağa çıkmaz.” Anlamı: Her sıkıntılı durumun altında büyük bir sorun veya tehlike yatmaz.
“İyi dost kara günde belli olur.” Anlamı: Zor durumlarda, gerçek dostlarınızın kim olduğunu anlarsınız.
“Yavaş yavaş dağlar bile delinir.” Anlamı: Sabırla ve azimle, zorlu ve büyük işler dahi başarılabilecektir.
“İşleyen demir pas tutmaz.” Anlamı: Sürekli çalışan ve üretken olan kişiler, yeteneklerini kaybetmezler.
“Bana arkadaşını söyle, sana kim olduğunu söyleyeyim.” Anlamı: Bir kişinin arkadaşları, o kişi hakkında ipuçları verir ve kişiliğini yansıtır.
“Herkes kendi gölgesinin peşinden koşar.” Anlamı: İnsanlar genellikle kişisel çıkarlarını düşünür ve kendi hedeflerini takip ederler.
“Akıl akıldan üstündür.” Anlamı: Bir insanın bilgisi ve zekası, diğer insanların bilgisine ve zekasına üstünlük sağlar.
“Acele işe şeytan karışır.” Anlamı: İşleri aceleye getirmek, hatalara ve sorunlara neden olabilir.
5. Özdeyişler (Vecizeler)
Özdeyiş, ahlaki, sosyal veya pratik bilgileri içeren, halk arasında yaygın olarak kullanılan kısa ve özlü cümlelerdir. Aynı zamanda “vecize” olarak da adlandırılır. Özdeyişler, toplumun deneyimleri ve bilgeliği üzerine temellendirilmiş, derin anlamlara sahip sözlerdir. Bu nedenle atasözleriyle benzerlik gösterirler, ancak genellikle daha bireysel veya pratik bilgiler içerirler.

Özdeyişler, genellikle bir kişinin yaşamını yönlendiren, doğru davranış biçimleri veya hayatın gerçekleri hakkında öğütler veren cümlelerdir. Söylenen bir olaydan veya bir kişinin yaşantısından alınmış olabileceği gibi, anonim de olabilir. Dilimizde ve diğer dillerde, halk arasında bilgelik ve deneyim paylaşımında yaygın olarak kullanılırlar.

Özdeyiş Örnekleri
Adalet evrenin ruhudur. (Ömer Hayyam)

Bilimsiz şiir, temelsiz duvara benzer. (Fuzuli)

Cahil kimsenin yanında kitap gibi sessiz ol. (Mevlana)

Aile hayatının güzelliği gibi hiç bir şey yoktur. (Oscar Wilde)

Akıllı olmak da bir şey değil, mühim olan o aklı yerinde kullanmaktır. (Descartes)

Aşılmasına imkan olmayan hiçbir duvar yoktur. (Çehov)

Aşk, güzelliğin aracılığıyla çoğalma arzusudur. (Sokrates)

Dedikodu, basit ruhlu insanların eğlencesidir. (Jorneille)

Kitapsız yaşamak, kör sağır, dilsiz yaşamaktır. (Seneca)

Bilim ve sanat bütün dünyanın malıdır, milletlerin sınırlarını tanımaz. (Goethe)

Camdan evde oturanlar başkalarına taş atmamalıdırlar. (G. Nerbert)

Sanat, doğaya eklenmiş insandır. (Bacon)

Saygı olmayan yerde aşk da olmaz. (E. Zola)

Eğitim öğrencilere saygıyla başlar. (Emerson)

Tilki, kümesi iyi tanıyor diye bekçi yapılır mı? (Truman)

Hayatta en hakiki mürşit ilimdir. (Mustafa Kemal Atatürk)

Yurtta barış cihanda barış. (Mustafa Kemal Atatürk)

6. Dolaylama
Tek kelimeyle ifade edilebilen bir kavramı birden fazla kelimeyle ifade etmeye denir.

meşin yuvarlark: top

yedinci sanat: sinema

file bekçisi: kaleci

bacasız sanayi: turizm

beyaz perde: sinema

kızıl gezegen: mars

7. Güzel Adlandırma
Söylendiğinde insana rahatsızlık verici bazı duygularla kötü çağrışımlar uyandıran kimi kavramların yerine daha hoş bir kavramın kullanılmasına denir.

kör: görme engelli

sağır: işitme engelli

tuvalet: ayak yolu

hastalanmak: şifayı kapmak

cin: üç harfli

ölmek: melek olmak
"""


resp = generate_question("META (llama3.1)", promt)
print(resp)