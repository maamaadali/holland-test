import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os
import base64
import time

# تنظیمات اصلی صفحه
st.set_page_config(
    page_title="آزمون رغبت‌سنجی تحصیلی-شغلی | گروه مشاوره خیلی سبز لنجان",
    page_icon="🍏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# استایل اختصاصی برند خیلی سبز (سبز #00A859، قرمز #E31E24)
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');

    html, body, [class*="css"], .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, label, button, input {
        font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }

    :root {
        --ks-green: #00A859;
        --ks-green-dark: #007A3D;
        --ks-red: #E31E24;
        --ks-yellow: #FFD200;
        --ks-bg: #F8FAF8;
    }

    /* کادرهای ورودی */
    .stTextInput>div>div>input {
        border-radius: 10px !important;
        border: 2px solid #D5E8D5 !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #1B365D !important;
        background-color: #FAFCFA !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #00A859 !important;
        box-shadow: 0 0 0 2px rgba(0, 168, 89, 0.25) !important;
    }

    /* دکمه‌های اصلی خیلی سبز */
    .stButton>button, .stDownloadButton>button {
        background: linear-gradient(135deg, #00A859 0%, #008F4C 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(0, 168, 89, 0.35) !important;
        padding: 0.65rem 2rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 168, 89, 0.5) !important;
        background: linear-gradient(135deg, #E31E24 0%, #C41217 100%) !important;
    }

    /* سربرگ اختصاصی */
    .brand-header {
        background: white;
        border-radius: 20px;
        padding: 20px 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 2px solid #EAF5EA;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* کارت‌های سؤالات با وضوح و کنتراست کامل در تم تیره و روشن */
    .question-card {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        margin-bottom: 14px !important;
        border: 1.5px solid #D1E7DD !important;
        border-right: 7px solid #00A859 !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08) !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
    .question-card * {
        color: #111827 !important;
        font-weight: 700 !important;
    }

    /* گزینه‌های رادیویی با کنتراست کامل، کادر مشخص و متن مشکی کاملاً خوانا */
    div[data-testid="stRadio"] [role="radiogroup"] label {
        background-color: #FFFFFF !important;
        border: 1.5px solid #00A859 !important;
        border-radius: 10px !important;
        padding: 6px 16px !important;
        margin-left: 10px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label:hover {
        background-color: #EAF5EA !important;
        border-color: #E31E24 !important;
    }
    /* اعمال رنگ مشکی پررنگ بر روی تمام اجزای متنی داخل گزینه‌ها */
    div[data-testid="stRadio"] [role="radiogroup"] label p,
    div[data-testid="stRadio"] [role="radiogroup"] label span,
    div[data-testid="stRadio"] [role="radiogroup"] label div,
    div[data-testid="stRadio"] [role="radiogroup"] label div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stRadio"] [role="radiogroup"] label * {
        color: #111827 !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
    }

    /* تب‌های استریم‌لیت */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0 !important;
        font-weight: 700 !important;
        padding: 10px 18px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #EAF5EA !important;
        color: #00A859 !important;
    }

    /* پاورقی اختصاصی */
    .brand-footer {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        margin-top: 50px;
        border-top: 3px solid #00A859;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.03);
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# بانک ۳۶ سؤال استاندارد هالند (RIASEC) - هر بعد ۶ سؤال
QUESTIONS = {
    "R": [
        "تعمیر کردن وسایل برقی، مکانیکی یا قطعات سیستم‌های کامپیوتری.",
        "کار با ابزارهای فنی، وسایل آزمایشگاهی، یا ساخت ماکت و کارهای دستی.",
        "فعالیت‌های عملیاتی در فضای باز، طبیعت، زمین‌شناسی یا کشاورزی.",
        "یادگیری نحوه کار با یک دستگاه جدید، ابزار تخصصی یا ماشین‌آلات صنعتی.",
        "سرهم کردن و مونتاژ قطعات و دیدن نتیجه عینی و فیزیکی کارم.",
        "کارهای مهارتی دقیق و دست‌ورزی ظریف (مانند مهارت‌های جراحی، دندان‌سازی یا طراحی صنعتی)."
    ],
    "I": [
        "کشف علت و ریشه علمی بیماری‌ها، پدیده‌های طبیعی یا مسائل اجتماعی.",
        "حل مسائل ریاضی پیچیده، معماهای منطقی یا کشف الگوریتم‌ها.",
        "خواندن مقالات علمی، کتاب‌های فلسفی یا آشنایی با فناوری‌های روز دنیا.",
        "کار روی پروژه‌های تحقیقاتی عمیق و آزمودن فرضیه‌های مختلف.",
        "تحلیل داده‌ها، آمارها و پیدا کردن ارتباط‌های پنهان میان آن‌ها.",
        "مطالعه درباره سازوکار ژن‌ها، سلول‌های زنده یا ساختار کیهان و فیزیک مدرن."
    ],
    "A": [
        "طراحی، نقاشی، عکاسی یا کارهای گرافیکی و ویرایش تصویر.",
        "نوشتن متن‌های ادبی، داستان، شعر، مقاله، یا سناریونویسی.",
        "چیدمان و طراحی دکوراسیون، زیبایی‌شناسی فضاها یا طراحی ظاهر یک محصول.",
        "فعالیت‌های مرتبط با موسیقی، نقد فیلم، تئاتر و هنرهای نمایشی.",
        "انجام کارها با روش‌های نوآورانه و خارج از چارچوب‌های خشک اداری.",
        "به تصویر کشیدن و ابراز آزادانه احساسات و افکار از طریق هنر و خلاقیت."
    ],
    "S": [
        "آموزش دادن یک مبحث درسی به دیگران و لذت بردن از فهمیدن آن‌ها.",
        "گوش دادن به درد دل و دغدغه‌های دوستان و کمک به آرامش روحی آن‌ها.",
        "مراقبت، پرستاری و درمان بیماران یا امدادرسانی در شرایط بحرانی.",
        "مشارکت در فعالیت‌های خیرخواهانه، عام‌المنفعه و خدمات مددکاری.",
        "گفتگو، ارتباط‌گیری نزدیک و درک عمیق رفتارها و عواطف انسان‌ها.",
        "میانجی‌گری برای رفع کدورت‌ها و حل اختلافات میان هم‌کلاسی‌ها یا اعضای گروه."
    ],
    "E": [
        "مدیریت یک گروه یا تیم و تقسیم وظایف میان اعضا برای رسیدن به هدف.",
        "شرکت در بحث‌ها و مناظره‌ها و دفاع قوی از دیدگاهم برای متقاعد کردن دیگران.",
        "راه‌اندازی یک پروژه کاری، خرید و فروش، تجارت یا ایده‌پردازی برای کسب درآمد.",
        "سخنرانی در جمع و معرفی یک ایده یا برنامه با اعتمادبه‌نفس بالا.",
        "پذیرفتن چالش‌های بزرگ کاری و موقعیت‌های پرریسک در ازای موفقیت و رشد بالا.",
        "ترغیب، انگیزه دادن و همراه‌سازی دیگران برای پیوستن به یک هدف مشترک."
    ],
    "C": [
        "ثبت منظم حساب‌وکتاب، دخل‌وخرج، و تنظیم دقیق گزارش‌های مالی.",
        "مرتب‌سازی فایل‌ها، پوشه‌ها و مدارک بر اساس ساختار و دسته‌بندی مشخص.",
        "انجام کارها طبق دستورالعمل‌های رسمی، قوانین مکتوب و استانداردهای تعیین‌شده.",
        "بازبینی دقیق اطلاعات و متون برای یافتن خطاها، اشتباهات تایپی یا مغایرت‌های آماری.",
        "کار با نرم‌افزارهای سازمان‌دهی داده‌ها، فرم‌های مالی و جداول اکسل.",
        "فعالیت در یک محیط شغلی با شرح وظایف بسیار شفاف، مشخص و بدون غافلگیری."
    ]
}

TYPE_TITLES = {
    "R": "واقع‌گرا (Realistic - عمل‌گرا و مهارتی)",
    "I": "کاوشگر (Investigative - اندیشمند و تحلیلی)",
    "A": "هنری (Artistic - خلاق و آفریننده)",
    "S": "اجتماعی (Social - همدل و انسان‌محور)",
    "E": "جسور / متهور (Enterprising - راهبر و ارزش‌آفرین)",
    "C": "قراردادی (Conventional - سازمان‌یافته و دقیق)"
}

TYPE_SHORT = {
    "R": "واقع‌گرا",
    "I": "کاوشگر",
    "A": "هنری",
    "S": "اجتماعی",
    "E": "متهور",
    "C": "قراردادی"
}

# متن تحلیل نیم‌صفحه‌ای اختصاصی برای هر یک از ۶ تیپ
ANALYSES = {
    "R": """شخصیت شما بر پایه عمل‌گرایی، تماس مستقیم با واقعیت‌های ملموس و کار با ابزارها، تجهیزات و پدیده‌های فیزیکی شکل گرفته است. شما از غرق شدن در تئوری‌های انتزاعیِ بدون کاربرد عینی زود خسته می‌شوید؛ یادگیری واقعی شما زمانی اتفاق می‌افتد که بتوانید دست به کار شوید، مکانیزم‌ها را از نزدیک بررسی کنید، عیب‌یابی انجام دهید و نتیجه تلاشتان را در دنیای واقعی لمس نمایید. هوش فضایی و مکانیکی بالا، ثبات قدم در پروژه‌های مهارتی و تمرکز روی خروجی‌های عینی از بزرگ‌ترین نقاط قوت شماست. محیط آرمانی شما فضایی سرشار از تحرک، کارگاه‌ها، آزمایشگاه‌های عینی، محیط‌های بالینی درمانی و فضاهای آزاد میدانی است. در مقابل، بزرگ‌ترین آسیب روحی شما پشت‌میزنشینی مداوم و انجام امور دفتری تکراری و بی‌تحرک است. توصیه مشاور این است که مسیری را انتخاب کنید که در آن کار مهارتی و دست‌ورزی ارزش شمرده شود و تئوری‌ها بلافاصله به عمل فیزیکی تبدیل شوند.""",
    
    "I": """جهان در ذهن شما مجموعه‌ای از مسائل حل‌نشده، ارتباطات پنهان میان داده‌ها و پرسش‌های عمیق پیرامون «چرایی» پدیده‌هاست. شما فردی مستقل، تحلیل‌گر و تشنه کشف حقایق هستید که از تصمیم‌گیری‌های سطحی یا شتاب‌زده بیزارید و از غرق شدن در مباحث منطقی، علمی، پزشکی یا فلسفی لذت می‌برید. قدرت بالای تمرکز طولانی‌مدت، تفکر نقادانه و میل به پژوهش در ریشه مسائل، شما را به یک حلال مسائل پیچیده تبدیل کرده است. بستر شکوفایی شما مراکز تحقیق و توسعه (R&D)، آزمایشگاه‌های عمیق، اتاق‌های فکر آکادمیک و شرکت‌های دانش‌بنیان است؛ جایی که استقلال فکری شما محترم شمرده شود. با این حال، مهم‌ترین نقطه کور شما خطر گرفتاری در «کمال‌گرایی و وسواس تحلیلی» است؛ جایی که بیش از حد در فرضیات غرق می‌شوید و اقدام عملی را عقب می‌اندازید. توصیه مشاور این است که همیشه در کنار تفکر تئوریک، روحیه عمل‌گرایی و جسارت در تصمیم‌گیری را نیز در خود پرورش دهید.""",
    
    "A": """شما جهان را از دریچه فرم، رنگ، واژه‌ها، زیبایی‌شناسی و تفکر واگرا تجربه می‌کنید. چارچوب‌های تکراری، بخشنامه‌های خشک اداری و فرمول‌های غیرمنعطف انگیزه شما را خاموش می‌کنند؛ چرا که نیاز حیاتی روان شما در نوآوری، خلق آثار و ابراز اصیل فردیت نهفته است. شما درک شهودی قدرتمندی دارید و ترجیح می‌دهید به جای مسیرهای از پیش تعیین‌شده، راه‌هایی بکر برای بازآفرینی مفاهیم پیدا کنید. محیط رشد شما آتلیه‌ها، استودیوهای طراحی، دفاتر تولید محتوا و رسانه، و اکوسیستم‌های منعطفی با کار پروژه‌محور و شناور است. بزرگ‌ترین هشدار مشاور برای شما، پرهیز از فضاهای شدیداً بروکراتیک، نظامی یا مشاغلی با آیین‌نامه‌های صلب است؛ ورود به چنین فضاهایی روحیه شما را به شدت فرسوده می‌کند. مسیر آینده شما حتماً باید فضایی باز برای دیده شدن سلیقه شخصی، امضای منحصربه‌فرد و آفرینشگری شما داشته باشد.""",
    
    "S": """هسته اصلی رضایت درونی شما در ارتباط زنده با انسان‌ها، شنیدن دغدغه‌هایشان، آموزش دادن و ایجاد دگرگونی مثبت در زندگی دیگران شکل گرفته است. شما دارای هوش هیجانی و بین‌فردی بالا، صبر ستودنی و روحیه‌ای حمایت‌گر هستید. در گروه‌ها به سرعت پیوند و صمیمیت می‌آفرینید و زبان بدن و عواطف دیگران را عمیقاً درک می‌کنید. پاداش درونی شما ارتقای سلامت و آگاهی انسان‌هاست، نه سر و کله زدن با ماشین‌آلات یا ارقام بی‌روح. محیط دانشگاهی و شغلی آرمانی شما، مراکز درمانی، آموزشی، توان‌بخشی، مشاوره‌ای و سازمان‌های تعاملی است. انزوای کاری (تنها نشستن پای سیستم و کار با اشیاء بی‌جان) انرژی روانی شما را تخلیه می‌کند. هشدار مهم مشاور برای شما، مراقبت در برابر «فرسودگی ناشی از دلسوزی افراطی» است؛ شما باید یاد بگیرید بین همدلی مؤثر و غرق شدن در غصه‌های دیگران مرز سالمی بگذارید تا خودتان دچار خستگی عاطفی نشوید.""",
    
    "E": """شما فردی کنش‌گرا، پرانرژی، فرصت‌شناس و شیفته اثربخشی، هدایت و مدیریت هستید. اعتمادبه‌نفس بالا، قدرت اقناع کلامی و شجاعت در پذیرش ریسک‌های حساب‌شده به شما این امکان را می‌دهد که دیگران را با اشتیاق برای رسیدن به اهداف مشترک بسیج کنید. شما به جای توقف طولانی در تئوری‌ها، به دنبال نتایج ملموس، توسعه اقتصادی و جایگاه‌های اثرگذار هستید و از رقابت سالم و حل چالش‌های بزرگ انگیزه می‌گیرید. محیط ایده‌آل شما بازارهای پویا، اتاق‌های مذاکره و مدیریت قراردادها، سازمان‌های رو به رشد و فضاهای کارآفرینی است. نقطه کور شما کم‌طاقتی در برابر کارهای تحقیقاتی طولانی‌مدت یا جزئیات خسته‌کننده اداری است که پاداش زودهنگام ندارند. توصیه مشاور این است که فضاهایی را هدف بگیرید که مسیر ارتقا، آزادی عمل در تصمیم‌گیری و مدیریت پروژه داشته باشند و در عین حال صبوری لازم برای یادگیری مهارت‌های پایه را از دست ندهید.""",
    
    "C": """شما معمار نظم، انضباط و ساختارمندی هستید. ذهن شما در سازماندهی داده‌ها، استخراج الگوها، حفظ چارچوب‌های استاندارد، انطباق با قوانین و یافتن ریزترین خطاهای محاسباتی و اسنادی با بالاترین دقت عمل می‌کند. شما به قابلیت پیش‌بینی، وفاداری به تعهدات و شفافیت رویه‌های کاری باور دارید و در جایی که بی‌نظمی و فقدان برنامه حاکم باشد، آرامش خود را از دست می‌دهید. بستر دانشگاهی و کاری ایده‌آل شما، سازمان‌های مالی، نهادهای پایش و کنترل کیفیت، موسسات حسابرسی و محیط‌هایی با شرح وظایف بسیار شفاف و مدون است. نقطه کور اصلی شما استرس در برابر شرایط غیرقابل پیش‌بینی یا مشاغلی با دستورالعمل‌های مبهم و تغییرات مکرر است. توصیه مشاور این است که در مسیرهایی گام بردارید که پایداری، اعتبار رسمی و ساختار محکم داشته باشند؛ جایی که دقت وسواس‌گونه و نظم خلل‌ناپذیر شما بالاترین ارزش را پیدا کند."""
}

# سمت‌وسو و حوزه‌های کلان تحصیلی-شغلی (بدون ذکر نام رشته)
DOMAINS = {
    "R": "حوزه‌های مهندسی و ساخت فیزیکی، کار با تجهیزات و ادوات فناورانه، مداخله‌های درمانی مهارتی و دست‌ورزی بالینی، و پروژه‌های عملیاتی میدانی و منابع محیطی.",
    "I": "حوزه‌های پژوهش‌های بنیادین، حل مسائل پیچیده الگوریتمی و نظری، علوم آزمایشگاهی عمیق، کشف سازوکارهای حیات، و تحلیل نظام‌های فکری و داده‌محور.",
    "A": "حوزه‌های آفرینش بصری و فضایی، تولید محتوای رسانه‌ای و متنی، زیبایی‌شناسی مفهومی، و طراحی تجربیات نوآورانه بدون قیدوبندهای کلیشه‌ای.",
    "S": "حوزه‌های توان‌بخشی و رشد انسانی، مراقبت و سلامت بالینی، آموزش و یاددهی، التیام بحران‌های فردی و روانی، و توسعه ارتباطات عمومی و اجتماعی.",
    "E": "حوزه‌های هدایت استراتژیک سازمانی، توسعه بازار و تجارت، متقاعدسازی و حقوق مذاکراتی، کارآفرینی اجرایی، و مدیریت پروژه‌های اقتصادی پرتحرک.",
    "C": "حوزه‌های ساختاردهی به کلان‌داده‌ها و اسناد، انضباط و شفافیت مالی و محاسباتی، کنترل کیفیت فرآیندها، و انطباق با مقررات و استانداردهای مدون."
}

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_candidates = ["logo.jpg", "logo.png", "image_2f36ae.jpg", "kheilisabz_logo.jpg"]
logo_base64 = None
for candidate in logo_candidates:
    b64 = get_base64_image(candidate)
    if b64:
        logo_base64 = b64
        break

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "student_info" not in st.session_state:
    st.session_state.student_info = {}
if "step" not in st.session_state:
    st.session_state.step = "login"

# ۱. سربرگ اختصاصی برند خیلی سبز لنجان
logo_html = ""
if logo_base64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" style="height: 80px; width: auto; border-radius: 12px; object-fit: contain;">'
else:
    logo_html = '<div style="font-size: 3rem;">🍏❤️</div>'

st.markdown(f"""
<div class="brand-header">
    <div style="flex: 1; text-align: right;">
        <h2 style="color: #00A859; margin: 0; font-weight: 800; font-size: 1.65rem;">گروه مشاوره خیلی سبز لنجان</h2>
        <p style="color: #555; margin: 5px 0 0 0; font-size: 0.98rem; font-weight: 500;">
            سامانه تخصصی رغبت‌سنجی تحصیلی-شغلی (مبتنی بر مدل استاندارد RIASEC جان هالند)
        </p>
    </div>
    <div style="text-align: left; padding-left: 10px;">
        {logo_html}
    </div>
</div>
""", unsafe_allow_html=True)

# ۲. صفحه لاگین با کد فعال‌سازی ۸۵۰۰
if not st.session_state.authenticated:
    st.markdown("### 🔐 ورود به پنل رغبت‌سنجی تحصیلی-شغلی داوطلب")
    st.info("برای شرکت در آزمون روان‌شناختی ترجیحات شغلی و شخصیتی، مشخصات خود و کد اختصاصی را وارد نمایید.")

    col1, col2 = st.columns(2)
    with col1:
        st_name = st.text_input("👤 نام و نام خانوادگی داوطلب (اجباری):", placeholder="مثال: محمدعلی ایزدی")
        st_phone = st.text_input("📱 شماره تماس همراه (اجباری):", placeholder="مثال: 09130660326")
    with col2:
        st_school = st.text_input("🏫 نام مدرسه / شعبه آموزشگاه:", placeholder="مثال: خیلی سبز لنجان")
        st_code = st.text_input("🔑 کد فعال‌سازی اختصاصی:", type="password", placeholder="کد ۴ رقمی مشاور")

    st_track = st.radio(
        "🎯 شاخه تحصیلی داوطلب:",
        ["ریاضی فیزیک", "علوم تجربی", "علوم انسانی"],
        horizontal=True
    )

    if st.button("🚀 ورود به سامانه و شروع آزمون رغبت‌سنجی"):
        if not st_name.strip():
            st.error("⚠️ لطفاً نام و نام خانوادگی خود را وارد کنید.")
        elif not st_phone.strip():
            st.error("⚠️ لطفاً شماره تماس همراه را وارد کنید.")
        elif st_code.strip() != "8500":
            st.error("⛔ کد فعال‌سازی وارد شده صحیح نمی‌باشد! لطفاً با گروه مشاوره خیلی سبز لنجان (09130660326) تماس بگیرید.")
        else:
            st.session_state.authenticated = True
            st.session_state.student_info = {
                "name": st_name.strip(),
                "phone": st_phone.strip(),
                "school": st_school.strip() if st_school.strip() else "خیلی سبز لنجان",
                "track": st_track
            }
            st.session_state.step = "test"
            st.rerun()

# ۳. صفحه سؤالات آزمون رغبت‌سنجی (۳۶ سؤال)
elif st.session_state.step == "test":
    info = st.session_state.student_info
    st.markdown(f"#### داوطلب گرامی، {info['name']} عزیز! 👋")
    st.markdown(f"""
    به آزمون رغبت‌سنجی تحصیلی-شغلی خوش آمدید. شاخه انتخابی شما: **{info['track']}**.  
    برای هر یک از فعالیت‌های زیر، حسی که به انجام آن دارید را مشخص کنید:
    * **علاقه‌مندم (۲ امتیاز)** | **نظری ندارم / ممتنع (۱ امتیاز)** | **علاقه‌مند نیستم (۰ امتیاز)**
    """)

    scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    
    q_counter = 1
    for dim_key, q_list in QUESTIONS.items():
        st.markdown(f"##### بعد {TYPE_SHORT[dim_key]}:")
        for q_text in q_list:
            st.markdown(f"<div class='question-card'><b>{q_counter}. {q_text}</b></div>", unsafe_allow_html=True)
            choice = st.radio(
                f"نظر شما برای سؤال {q_counter}:",
                ["علاقه‌مندم", "نظری ندارم / ممتنع", "علاقه‌مند نیستم"],
                index=1,
                key=f"q_{q_counter}",
                horizontal=True,
                label_visibility="collapsed"
            )
            
            if choice == "علاقه‌مندم":
                scores[dim_key] += 2
            elif choice == "نظری ندارم / ممتنع":
                scores[dim_key] += 1
            else:
                scores[dim_key] += 0
                
            q_counter += 1
        st.markdown("---")

    if st.button("🔍 تحلیل روان‌شناختی و صدور کارنامه رغبت‌سنجی"):
        status_box = st.empty()
        progress_bar = st.progress(0)
        
        steps = [
            (20, "📥 دریافت و ثبت پاسخ‌های داوطلب در ۶ بعد شخصیت تحصیلی...", 1.2),
            (45, "🧠 محاسبه مقیاس‌های استاندارد RIASEC بر پایه مدل جان هالند...", 1.5),
            (70, "🔍 استخراج کدهای غالب و مکمل و تحلیل تمایلات حرفه‌ای...", 1.8),
            (90, "🎯 تدوین تحلیل نیم‌صفحه‌ای اختصاصی و ترسیم حوزه‌های کلان...", 1.5),
            (100, "✨ تحلیل نهایی با موفقیت تکمیل شد! در حال صدور کارنامه تک‌صفحه‌ای...", 1.0)
        ]
        
        for pct, msg, sleep_dur in steps:
            status_box.info(f"**{msg}**")
            progress_bar.progress(pct)
            time.sleep(sleep_dur)
            
        status_box.empty()
        progress_bar.empty()
        
        st.session_state.scores = scores
        st.session_state.step = "results"
        st.rerun()

# ۴. داشبورد نتایج، نمودار و کارنامه رسمی
elif st.session_state.step == "results":
    info = st.session_state.student_info
    scores = st.session_state.scores
    
    # رتبه‌بندی ابعاد بر اساس بیشترین امتیاز
    sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary_code = sorted_dims[0][0]
    secondary_code = sorted_dims[1][0]
    holland_code = f"{primary_code}{secondary_code}"

    primary_title = TYPE_TITLES[primary_code]
    secondary_title = TYPE_TITLES[secondary_code]
    analysis_text = ANALYSES[primary_code]
    domain_text = DOMAINS[primary_code]

    st.success(f"🎉 تحلیل رغبت‌سنجی داوطلب محترم **{info['name']}** با موفقیت استخراج شد.")

    tab_overview, tab_printable = st.tabs([
        "📊 مشاهده تحلیل ابعاد و نمودار رغبت‌سنجی",
        "📄 مشاهده و چاپ مستقیم کارنامه تک‌صفحه‌ای رسمی"
    ])

    with tab_overview:
        col_res, col_chart = st.columns([3, 2])
        
        with col_res:
            st.markdown(f"""
            <div style="background:#FFFFFF; border-radius:16px; padding:20px; border-right:6px solid #00A859; box-shadow:0 4px 15px rgba(0,0,0,0.05); margin-bottom:20px;">
                <h3 style="color:#00A859; margin-top:0;">کد رغبت‌سنجی شما: <span style="color:#E31E24; letter-spacing:3px;">{holland_code}</span></h3>
                <p><b>تیپ غالب (رتبه ۱):</b> {primary_title}</p>
                <p><b>تیپ مکمل (رتبه ۲):</b> {secondary_title}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📝 تحلیل نیم‌صفحه‌ای شخصیت و مدل ذهنی شما:")
            st.info(analysis_text)
            
            st.markdown("#### 🧭 سمت‌وسو و حوزه‌های راهبردی تحصیلی-شغلی شما:")
            st.markdown(f"""
            <div style="background:#EAF5EA; border-radius:12px; padding:15px; border:1px solid #C3E6C3; color:#1B365D; font-weight:600; line-height:1.8;">
                {domain_text}
            </div>
            """, unsafe_allow_html=True)

        with col_chart:
            st.markdown("#### 📈 نمودار مقایسه‌ای ۶ بعد رغبت‌سنجی:")
            chart_data = pd.DataFrame({
                "بعد": [TYPE_SHORT[k] for k, _ in sorted_dims][::-1],
                "امتیاز (از ۱۲)": [v for _, v in sorted_dims][::-1]
            })
            st.bar_chart(chart_data.set_index("بعد"), color="#00A859")

            st.markdown("---")
            if st.button("🔄 آزمون مجدد برای داوطلب دیگر"):
                st.session_state.authenticated = False
                st.session_state.step = "login"
                st.rerun()

    with tab_printable:
        logo_img_report = f'<img src="data:image/jpeg;base64,{logo_base64}" style="height: 50px; width: auto; object-fit: contain;">' if logo_base64 else '🍏'

        scores_table_rows = ""
        for code, val in sorted_dims:
            pct = round((val / 12) * 100)
            scores_table_rows += f"""
            <tr>
                <td style="padding:2.5px 6px; border:1px solid #ddd; font-weight:bold;">{TYPE_TITLES[code]}</td>
                <td style="padding:2.5px 6px; border:1px solid #ddd; text-align:center;">{val} از ۱۲</td>
                <td style="padding:2.5px 6px; border:1px solid #ddd; text-align:center; color:#00A859; font-weight:bold;">{pct}٪</td>
            </tr>
            """

        report_html = f"""<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="utf-8">
    <title>کارنامه رغبت‌سنجی - {info['name']}</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
        @page {{
            size: A4 portrait;
            margin: 5mm 8mm 5mm 8mm !important;
        }}
        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}
        body {{
            font-family: 'Vazirmatn', Tahoma, sans-serif;
            direction: rtl;
            margin: 0;
            padding: 5px;
            background: #ffffff;
            color: #222;
        }}
        .report-box {{
            border: 2px solid #00A859;
            border-radius: 12px;
            padding: 8px 14px;
            margin: 0 auto;
            max-width: 820px;
            page-break-inside: avoid !important;
        }}
        .btn-print {{
            background: #00A859;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
            font-family: inherit;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .btn-print:hover {{
            background: #E31E24;
        }}
        @media print {{
            .btn-print, .no-print {{ display: none !important; }}
            body {{ padding: 0 !important; margin: 0 !important; }}
            .report-box {{ border: 2px solid #00A859 !important; padding: 6px 10px !important; }}
        }}
    </style>
</head>
<body>
    <center class="no-print">
        <button class="btn-print" onclick="window.print()">🖨️ چاپ مستقیم کارنامه تک‌صفحه‌ای یا ذخیره به عنوان PDF</button>
    </center>
    
    <div class="report-box" id="printable-report">
        <!-- سربرگ -->
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #E31E24; padding-bottom:5px; margin-bottom:6px;">
            <div>
                <h2 style="color:#00A859; margin:0; font-size:16px; font-weight:800;">کارنامه رسمی رغبت‌سنجی تحصیلی-شغلی (مدل هالند)</h2>
                <h4 style="color:#444; margin:3px 0 0 0; font-size:12px; font-weight:600;">گروه مشاوره و برنامه‌ریزی خیلی سبز لنجان</h4>
            </div>
            <div>
                {logo_img_report}
            </div>
        </div>
        
        <!-- نوار مشخصات -->
        <table style="width:100%; margin-bottom:6px; background:#F8FAF8; border:1px solid #E2EFE2; border-radius:6px; padding:3px; font-size:11px;">
            <tr>
                <td style="padding:2px 4px;"><b>نام داوطلب:</b> {info['name']}</td>
                <td style="padding:2px 4px;"><b>شاخه تحصیلی:</b> {info['track']}</td>
                <td style="padding:2px 4px;"><b>شماره تماس:</b> <span style="direction:ltr; display:inline-block;">{info['phone']}</span></td>
                <td style="padding:2px 4px;"><b>مرکز مشاوره:</b> {info['school']}</td>
                <td style="padding:2px 4px; text-align:left;"><b>کد هالند:</b> <span style="color:#E31E24; font-weight:800; font-size:12px;">{holland_code}</span></td>
            </tr>
        </table>

        <!-- جدول نتایج ۶ بعد -->
        <table style="width:100%; border-collapse:collapse; text-align:right; font-size:10px; margin-bottom:6px;">
            <thead>
                <tr style="background:#00A859; color:white;">
                    <th style="padding:3px 6px; border:1px solid #ccc;">ابعاد شش‌گانه رغبت‌سنجی تحصیلی-شغلی</th>
                    <th style="padding:3px 6px; border:1px solid #ccc; text-align:center; width:20%;">امتیاز کسب‌شده</th>
                    <th style="padding:3px 6px; border:1px solid #ccc; text-align:center; width:20%;">درصد تطابق</th>
                </tr>
            </thead>
            <tbody>
                {scores_table_rows}
            </tbody>
        </table>

        <!-- بخش تحلیل نیم‌صفحه‌ای اختصاصی -->
        <div style="background:#FAFDFC; border:1px solid #D5EBD5; border-radius:6px; padding:6px 10px; margin-bottom:6px;">
            <div style="color:#00A859; font-weight:800; font-size:11px; margin-bottom:3px;">
                💡 تحلیل روان‌شناختی تیپ غالب شما: {primary_title}
            </div>
            <div style="font-size:9.5px; line-height:1.5; text-align:justify; color:#333;">
                {analysis_text}
            </div>
        </div>

        <!-- سمت‌وسوها و حوزه‌های کلان تحصیلی-شغلی -->
        <div style="background:#FFFDFD; border:1px solid #F5D3D5; border-radius:6px; padding:6px 10px; margin-bottom:6px;">
            <div style="color:#E31E24; font-weight:800; font-size:11px; margin-bottom:3px;">
                🧭 سمت‌وسو و حوزه‌های راهبردی تحصیلی-شغلی متناسب با شخصیت شما:
            </div>
            <div style="font-size:10px; line-height:1.45; color:#1B365D; font-weight:600;">
                {domain_text}
            </div>
        </div>

        <!-- پاورقی و امضا -->
        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #eee; padding-top:5px; font-size:10px;">
            <div>
                <b>مهر و تاییدیه مشاور ارشد:</b> ............................................
            </div>
            <div style="text-align:left;">
                📞 تماس: <b>09130660326</b> | اینستاگرام: <b>@kheilisabze_lenjan</b>
            </div>
        </div>
    </div>
</body>
</html>"""

        col_b1, col_b2 = st.columns([1, 1])
        with col_b1:
            st.download_button(
                label="📥 دانلود فایل کارنامه رسمی (HTML آماده چاپ تک‌صفحه‌ای)",
                data=report_html,
                file_name=f"کارنامه_رغبت‌سنجی_{info['name']}.html",
                mime="text/html"
            )
        with col_b2:
            st.info("💡 برای چاپ فوری، دکمه سبز رنگ بالای پیش‌نمایش زیر را بزنید یا کلیدهای Ctrl + P را فشار دهید.")

        components.html(report_html, height=720, scrolling=True)

# ۵. پاورقی ثابت برند خیلی سبز لنجان
st.markdown(f"""
<div class="brand-footer">
    <div style="font-size: 1.15rem; font-weight: 800; color: #00A859; margin-bottom: 8px;">
        🍏 گروه مشاوره و برنامه‌ریزی خیلی سبز لنجان
    </div>
    <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; font-size: 0.98rem; color: #333;">
        <div>📞 <b>شماره تماس:</b> <a href="tel:09130660326" style="color:#00A859; text-decoration:none;">09130660326</a></div>
        <div>📸 <b>اینستاگرام:</b> <a href="https://instagram.com/kheilisabze_lenjan" target="_blank" style="color:#E31E24; text-decoration:none; font-weight:bold;">@kheilisabze_lenjan</a></div>
        <div>✈️ <b>طراح و توسعه‌دهنده:</b> <a href="https://t.me/mmd1ali1" target="_blank" style="color:#0088cc; text-decoration:none; font-weight:bold;">@mmd1ali1</a></div>
    </div>
    <div style="font-size: 0.85rem; color: #888; margin-top: 10px;">
        تمامی حقوق مادی و معنوی این سامانه متعلق به «گروه مشاوره خیلی سبز لنجان» می‌باشد.
    </div>
</div>
""", unsafe_allow_html=True)
