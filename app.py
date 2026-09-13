import datetime
import urllib.parse
import streamlit as st

# -----------------------------------------------------------------------------
# 1. 全局頁面配置與黑金時尚 UI 風格
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SIS Fitness Club | 運動空間",
    page_icon="💎",
    layout="wide"
)

st.markdown("""
    <style>
    /* 全局背景與字體 */
    .stApp {
        background: linear-gradient(135deg, #07070c 0%, #110d21 50%, #07070c 100%);
        color: #f1f1f6;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 頂部炫彩標題 */
    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #facc15 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 10px 0 20px 0;
    }

    /* VIP 資訊列 */
    .vip-bar {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 14px;
        padding: 12px 20px;
        margin-bottom: 20px;
    }

    /* 按鈕樣式 */
    .stButton>button {
        background: linear-gradient(135deg, #2e1065 0%, #3b0764 100%) !important;
        color: #f3e8ff !important;
        border: 1px solid rgba(168, 85, 247, 0.4) !important;
        border-radius: 10px !important;
        padding: 8px 12px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.25s ease-in-out !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%) !important;
        color: #ffffff !important;
        border-color: transparent !important;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4) !important;
    }

    /* 通用卡片 */
    .luxury-card {
        background: rgba(23, 15, 38, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* 設施與教練資歷卡片 */
    .facility-card, .coach-card {
        background: rgba(30, 20, 50, 0.65);
        border: 1px solid rgba(168, 85, 247, 0.25);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .coach-avatar {
        width: 100%;
        height: 220px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 14px;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }

    .badge-gold {
        background: rgba(234, 179, 8, 0.2);
        color: #fef08a;
        border: 1px solid rgba(234, 179, 8, 0.5);
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }

    .badge-purple {
        background: rgba(168, 85, 247, 0.2);
        color: #e9d5ff;
        border: 1px solid rgba(168, 85, 247, 0.5);
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 4px;
        margin-bottom: 6px;
    }

    .action-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px 14px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        text-decoration: none !important;
        background: linear-gradient(135deg, #4285F4 0%, #1a73e8 100%);
        color: #ffffff !important;
        width: 100%;
        text-align: center;
        margin-top: 10px;
    }

    .ig-btn {
        background: linear-gradient(135deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%) !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 雙語字典
# -----------------------------------------------------------------------------
I18N = {
    "zh": {
        "app_title": "✦ SIS FITNESS CLUB ✦",
        "menu_venue": "🏛️ 場館介紹",
        "menu_booking": "📅 課程預約",
        "menu_mylist": "📋 我的行程",
        "menu_equip": "🏋️ 器材圖鑑",
        "menu_ai": "🤖 AI 健身菜單",
        "menu_coaches": "👥 明星師資",
        "menu_inbox": "💬 預約私訊箱",
        "menu_join": "🏫 入會指引",
        "lang_select": "🌐 語言選擇 / Language",
        "role_test": "👤 身分切換測試",
        "member_login": "切換為【會員登入】狀態",
        "vip_welcome": "✨ 歡迎來到 SIS Fitness Club，VIP 會員 <b>{name}</b>！",
        "fit_coins": "💎 點數: ",
        "sim_title": "⏱️ 測試專用：系統時間模擬器",
        "sim_hour": "模擬當前小時",
        "sim_min": "模擬當前分鐘",
        "status_ended": "⌛ 已結束",
        "status_ongoing": "🔥 進行中",
        "status_open": "🟢 開放預約",
        "btn_ended": "已結束",
        "btn_full": "已滿班",
        "btn_cancel": "取消預約",
        "btn_book": "預約",
        "btn_checkin": "💎 完成今日簽到 (+50 PTS)",
        "checkin_success": "簽到成功！點數已增加 50 PTS！",
        "book_success": "成功預約 {name}，已扣除 {cost} PTS！",
        "cancel_success": "已成功取消 {name}，退還 {cost} PTS！",
        "coins_not_enough": "點數不足！",
        "my_bookings_title": "🗓️ 我已預約的課程行程",
        "no_bookings": "💡 您目前尚未預約任何課程！",
        "add_gcal": "📅 加入 Google 行事曆",
        "teacher": "指導老師",
        "room": "教室",
        "booked_count": "報名人數：",
        "pts_cost": "扣點：",
        "lock_msg": "🔒 此功能為會員專屬！請先切換至會員登入狀態。",
        "equip_title": "📖 30項健身器材完整圖鑑指南",
        "target_label": "🎯 核心訓練部位：",
        "tips_label": "⚠️ 注意事項：",
        "coach_title": "👥 明星教練團隊 & 資歷卡片",
        "inbox_title": "💬 預約私訊箱",
        "select_cat_label": "選擇類別：",
        "all_cat": "全部",
        "send_msg_title": "✉️ 發送私訊給教練或客服",
        "msg_receiver": "接收對象",
        "msg_input": "請輸入訊息內容...",
        "btn_send": "發送訊息",
        "msg_sent_success": "訊息已成功發送！"
    },
    "en": {
        "app_title": "✦ SIS FITNESS CLUB ✦",
        "menu_venue": "🏛️ Facilities",
        "menu_booking": "📅 Class Booking",
        "menu_mylist": "📋 Schedule",
        "menu_equip": "🏋️ Equipment",
        "menu_ai": "🤖 AI Workout Plan",
        "menu_coaches": "👥 Trainers",
        "menu_inbox": "💬 Inbox",
        "menu_join": "🏫 Join Us",
        "lang_select": "🌐 Language",
        "role_test": "👤 Role Switcher",
        "member_login": "Member Mode",
        "vip_welcome": "✨ Welcome to SIS Fitness Club, VIP <b>{name}</b>!",
        "fit_coins": "💎 Points: ",
        "sim_title": "⏱️ Time Simulator",
        "sim_hour": "Hour",
        "sim_min": "Minute",
        "status_ended": "⌛ Ended",
        "status_ongoing": "🔥 Ongoing",
        "status_open": "🟢 Open",
        "btn_ended": "Ended",
        "btn_full": "Full",
        "btn_cancel": "Cancel",
        "btn_book": "Book",
        "btn_checkin": "💎 Check-in (+50 PTS)",
        "checkin_success": "+50 PTS added!",
        "book_success": "Booked {name}! -{cost} PTS",
        "cancel_success": "Cancelled {name}. +{cost} PTS",
        "coins_not_enough": "Not enough points!",
        "my_bookings_title": "🗓️ My Booked Classes",
        "no_bookings": "💡 No active bookings.",
        "add_gcal": "📅 Google Calendar",
        "teacher": "Instructor",
        "room": "Studio",
        "booked_count": "Booked: ",
        "pts_cost": "Cost: ",
        "lock_msg": "🔒 Member exclusive!",
        "equip_title": "📖 Equipment Guide (30 Items)",
        "target_label": "🎯 Target: ",
        "tips_label": "⚠️ Caution: ",
        "coach_title": "👥 Star Trainers",
        "inbox_title": "💬 Inbox",
        "select_cat_label": "Category: ",
        "all_cat": "All",
        "send_msg_title": "✉️ Send Message to Coach or Support",
        "msg_receiver": "Recipient",
        "msg_input": "Enter your message here...",
        "btn_send": "Send Message",
        "msg_sent_success": "Message sent successfully!"
    }
}

def create_gcal_link(title, date_str, time_str, location, teacher):
    raw_date = date_str.split(' ')[0].replace('/', '')
    start_t_str, end_t_str = time_str.split('~')
    start_h, start_m = start_t_str.split(':')
    end_h, end_m = end_t_str.split(':')
    dates_param = f"{raw_date}T{start_h}{start_m}00/{raw_date}T{end_h}{end_m}00"
    params = {
        "action": "TEMPLATE",
        "text": f"🏋️ {title}",
        "dates": dates_param,
        "details": f"Fitness Class - Instructor: {teacher}",
        "location": location,
        "ctz": "Asia/Taipei"
    }
    return f"https://calendar.google.com/calendar/render?{urllib.parse.urlencode(params)}"

# -----------------------------------------------------------------------------
# 3. Session State 初始化
# -----------------------------------------------------------------------------
if 'lang' not in st.session_state:
    st.session_state.lang = "zh"
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = True
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Alex"
if 'fit_coins' not in st.session_state:
    st.session_state.fit_coins = 320
if 'selected_cat' not in st.session_state:
    st.session_state.selected_cat = I18N[st.session_state.lang]["menu_venue"]
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = "2026/09/14"
if 'my_bookings' not in st.session_state:
    st.session_state.my_bookings = {101}
if 'inbox_messages' not in st.session_state:
    st.session_state.inbox_messages = [
        {"sender": "系統通知", "time": "2026/09/14 10:00", "text": "歡迎來到 SIS Fitness Club！首次登入已獲得 320 點數。"},
        {"sender": "Chloe 教練", "time": "2026/09/14 11:30", "text": "Alex 您好！期待下週一的 TRX 課程，記得帶毛巾與水壺喔！"}
    ]

# -----------------------------------------------------------------------------
# 4. 資料庫 (課表、器材、教練、8大場館設施)
# -----------------------------------------------------------------------------
WEEK_DATES = [
    {"date_key": "2026/09/13", "day": "日", "num": "09/13"},
    {"date_key": "2026/09/14", "day": "一", "num": "09/14"},
    {"date_key": "2026/09/15", "day": "二", "num": "09/15"},
    {"date_key": "2026/09/16", "day": "三", "num": "09/16"},
    {"date_key": "2026/09/17", "day": "四", "num": "09/17"},
    {"date_key": "2026/09/18", "day": "五", "num": "09/18"},
    {"date_key": "2026/09/19", "day": "六", "num": "09/19"},
]

COURSES_WEEK_DATA = [
    {"id": 101, "date_key": "2026/09/14", "cat": "瑜珈/提斯", "name": {"zh": "瑜珈提斯", "en": "Yogalates"}, "time": "17:50~18:50", "date": "2026/09/14 (一)", "teacher": "Umi", "room": {"zh": "瑜珈教室", "en": "Yoga Studio"}, "booked": 5, "max": 18, "cost": 50},
    {"id": 102, "date_key": "2026/09/14", "cat": "瑜珈/提斯", "name": {"zh": "哈達瑜珈", "en": "Hatha Yoga"}, "time": "19:00~20:00", "date": "2026/09/14 (一)", "teacher": "Umi", "room": {"zh": "瑜珈教室", "en": "Yoga Studio"}, "booked": 7, "max": 18, "cost": 50},
    {"id": 103, "date_key": "2026/09/14", "cat": "心肺/有氧/拳擊", "name": {"zh": "互動拳擊", "en": "Interactive Boxing"}, "time": "19:15~20:00", "date": "2026/09/14 (一)", "teacher": "James", "room": {"zh": "自由訓練空間", "en": "Functional Area"}, "booked": 0, "max": 8, "cost": 50},
    {"id": 104, "date_key": "2026/09/14", "cat": "肌力訓練", "name": {"zh": "TRX懸吊訓練", "en": "TRX Training"}, "time": "20:15~21:15", "date": "2026/09/14 (一)", "teacher": "Chloe", "room": {"zh": "自由訓練空間", "en": "Functional Area"}, "booked": 12, "max": 12, "cost": 60},
    {"id": 105, "date_key": "2026/09/15", "cat": "舞蹈", "name": {"zh": "K-POP 流行舞蹈", "en": "K-POP Dance"}, "time": "18:30~19:30", "date": "2026/09/15 (二)", "teacher": "Lisa", "room": {"zh": "舞蹈教室", "en": "Dance Studio"}, "booked": 10, "max": 20, "cost": 50},
]

VENUE_FACILITIES = [
    {"name": "🧘‍♀️ 瑜珈教室", "desc": "溫潤木質地板與柔和光影設計，專為瑜珈、皮拉提斯與深層伸展打造的平靜空間。"},
    {"name": "💃 舞蹈教室", "desc": "高規格環繞音響與全面鏡牆，釋放體能與韻律節奏的專屬熱力舞台。"},
    {"name": "🏃 自由訓練空間", "desc": "寬敞無障礙草皮與多功能功能訓練架，適合 TRX、壺鈴及敏捷度訓練。"},
    {"name": "🏋️ 重訓區", "desc": "引進頂級固定式器材與豐富自由重量，滿足從新手到專業者的訓練需求。"},
    {"name": "💧 飲水機", "desc": "全時段提供冷熱極淨過濾水，陪伴您隨時補充運動過程中所需的水分。"},
    {"name": "🛎️ 服務櫃檯", "desc": "親切專員提供諮詢、報到與貼心服務，帶來如家人般溫暖的招呼與接待。"},
    {"name": "🚹 男廁區", "desc": "獨立乾淨的男廁與衛浴空間，提供運動後舒適清爽的盥洗體驗。"},
    {"name": "🚺 女廁區", "desc": "優雅明亮且注重隱私的女性專屬空間，配置貼心備品與梳妝區域。"}
]

EQUIPMENT_DATA = [
    {"id": 1, "name": {"zh": "01. 坐姿胸推機", "en": "Chest Press Machine"}, "target": {"zh": "胸大肌、三頭肌、三角肌前束", "en": "Pectoralis Major, Triceps"}, "tips": {"zh": "手肘勿過度張開，推起時切勿鎖死手肘關節。", "en": "Keep elbows at 45 degrees."}},
    {"id": 2, "name": {"zh": "02. 蝴蝶牌夾胸機", "en": "Pec Deck Fly"}, "target": {"zh": "胸大肌內側、前鋸肌", "en": "Inner Chest"}, "tips": {"zh": "背部緊貼靠墊，沉肩不聳肩。", "en": "Keep back flat."}},
    {"id": 3, "name": {"zh": "03. 高位下拉機", "en": "Lat Pulldown"}, "target": {"zh": "背括肌、大圓肌、二頭肌", "en": "Latissimus Dorsi"}, "tips": {"zh": "下拉時微胸，向胸前上方拉拉至鎖骨位置。", "en": "Pull down to upper chest."}},
    {"id": 4, "name": {"zh": "04. 史密斯架", "en": "Smith Machine"}, "target": {"zh": "全身複合肌群（深蹲、臥推）", "en": "Full Body Compound"}, "tips": {"zh": "確認安全鎖扣位置正確後方可進行訓練。", "en": "Check safety locks."}},
]

COACHES_DETAIL_DATA = [
    {
        "name": "Umi 老師",
        "role": "瑜珈與皮拉提斯專任導師",
        "exp": "8 年教學經驗",
        "img": "https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=500&auto=format&fit=crop",
        "tags": ["哈達瑜珈", "瑜珈提斯", "體態矯正", "產後修復"],
        "certs": ["美國瑜珈聯盟 RYT-200 國際認證", "Polestar Pilates 墊上皮拉提斯認證", "KT TAPE 肌貼運動防護認證"],
        "bio": "溫柔且注重細節的教學風格，擅長透過呼吸與覺察帶領學員釋放壓力並打造優雅體態。"
    },
    {
        "name": "Chloe 教練",
        "role": "TRX & 女性體態雕塑總監",
        "exp": "6 年專業指導經驗",
        "img": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&auto=format&fit=crop",
        "tags": ["TRX 懸吊", "臀腿雕塑", "肌力強化", "飲食指導"],
        "certs": ["NASM-CPT 美國國家運動醫學會私人教練", "TRX STC 懸吊訓練師專業認證", "ACE-SNS 運動營養專家認證"],
        "bio": "陪伴數百位女性學員成功實現體態蛻變，主打精準動作控制與不給壓力的陪伴式帶領。"
    },
    {
        "name": "James 教練",
        "role": "自由搏擊 & 高強度燃脂總教練",
        "exp": "10 年體能培訓經驗",
        "img": "https://images.unsplash.com/photo-1567013127542-490d757e51fc?w=500&auto=format&fit=crop",
        "tags": ["互動拳擊", "HIIT燃脂", "自由重量", "爆發力訓練"],
        "certs": ["NSCA-CSCS 體能訓練專家認證", "WBC 拳擊高級教練認證", "紅十字會高級急救員證照"],
        "bio": "前職業運動員背景，課堂充滿高昂能量！善於根據每位學員的體能極限調整訓練強度。"
    }
]

t = I18N[st.session_state.lang]

# -----------------------------------------------------------------------------
# 5. 側邊欄控制
# -----------------------------------------------------------------------------
with st.sidebar:
    lang_choice = st.selectbox(
        t["lang_select"],
        options=["繁體中文", "English"],
        index=0 if st.session_state.lang == "zh" else 1
    )
    new_lang = "zh" if lang_choice == "繁體中文" else "en"
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.session_state.selected_cat = t["menu_venue"]
        st.rerun()

    st.markdown("---")
    st.title(t["role_test"])
    login_toggle = st.toggle(t["member_login"], value=st.session_state.is_logged_in)
    
    if login_toggle != st.session_state.is_logged_in:
        st.session_state.is_logged_in = login_toggle
        st.session_state.selected_cat = t["menu_booking"] if st.session_state.is_logged_in else t["menu_venue"]
        st.rerun()

    st.markdown("---")
    st.markdown("### 📱 會員專屬 QR Code")
    if st.session_state.is_logged_in:
        st.success(f"VIP Member: {st.session_state.user_name}")
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=SIS_VIP_{st.session_state.user_name}"
        st.image(qr_url, width=180)
        st.caption(f"{t['fit_coins']} {st.session_state.fit_coins} PTS")
    else:
        st.info("Visitor Mode")
        qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=https://www.instagram.com/sisfitnessclub/"
        st.image(qr_url, width=180)

# -----------------------------------------------------------------------------
# 6. 頁頭 Banner 與 VIP 資訊
# -----------------------------------------------------------------------------
st.markdown(f"<div class='hero-title'>{t['app_title']}</div>", unsafe_allow_html=True)

if st.session_state.is_logged_in:
    welcome_str = t["vip_welcome"].format(name=st.session_state.user_name)
    st.markdown(f"""
    <div class='vip-bar'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='color: #cbd5e1; font-size: 0.9rem;'>{welcome_str}</span>
            <span style='color: #fef08a; font-weight: 700; font-size: 0.95rem;'>{t['fit_coins']}<span style='font-size: 1.1rem;'>{st.session_state.fit_coins}</span> PTS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. 主選單 Tab 切換
# -----------------------------------------------------------------------------
if st.session_state.is_logged_in:
    menu_items = [t["menu_venue"], t["menu_booking"], t["menu_mylist"], t["menu_equip"], t["menu_ai"], t["menu_coaches"], t["menu_inbox"]]
else:
    menu_items = [t["menu_venue"], t["menu_coaches"], t["menu_equip"], t["menu_inbox"], t["menu_join"]]

cols = st.columns(len(menu_items))
for idx, item in enumerate(menu_items):
    with cols[idx]:
        if st.button(item):
            st.session_state.selected_cat = item
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 8. 模組：🏛️ 場館介紹
# -----------------------------------------------------------------------------
if st.session_state.selected_cat in [I18N["zh"]["menu_venue"], I18N["en"]["menu_venue"]]:
    st.markdown("""
    <div class='luxury-card'>
        <span class='badge-gold'>BRAND STORY</span>
        <div style='font-size: 1.6rem; font-weight: 800; color: #facc15; margin-top: 4px;'>有溫度的空間 • 有溫度的人群</div>
        <p style='color: #cbd5e1; font-size: 0.95rem; line-height: 1.8; margin-top: 10px;'>
            我們相信，運動不僅僅是汗水與數據的堆疊，更是生活溫度的傳達。在 SIS Fitness Club，我們打造了一個兼具專業與親和力的體能空間，用最真誠的心迎接每一位走進來的夥伴。<br>
            不論你是運動新手或健體高手，這裡始終有最溫暖的笑容、最專業的指導與充滿支持的社群氛圍。來這裡，感受有溫度的空間，遇見有溫度的人群。
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏢 場館八大特色設施")
    v_cols1 = st.columns(4)
    for idx, fac in enumerate(VENUE_FACILITIES[:4]):
        with v_cols1[idx]:
            st.markdown(f"""
            <div class='facility-card'>
                <div style='font-weight: 700; font-size: 1.05rem; color: #ffffff; margin-bottom: 8px;'>{fac['name']}</div>
                <div style='font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;'>{fac['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    v_cols2 = st.columns(4)
    for idx, fac in enumerate(VENUE_FACILITIES[4:]):
        with v_cols2[idx]:
            st.markdown(f"""
            <div class='facility-card'>
                <div style='font-weight: 700; font-size: 1.05rem; color: #ffffff; margin-bottom: 8px;'>{fac['name']}</div>
                <div style='font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;'>{fac['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📍 社群與地圖導覽")
    map_col1, map_col2 = st.columns(2)
    
    with map_col1:
        st.markdown("""
        <div class='luxury-card' style='text-align: center;'>
            <div style='font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 6px;'>📸 官方 Instagram</div>
            <div style='color: #cbd5e1; font-size: 0.85rem;'>追蹤最新課程動態與運動日常</div>
            <a href='https://www.instagram.com/sisfitnessclub/' target='_blank' class='action-btn ig-btn'>👉 追蹤 @sisfitnessclub</a>
        </div>
        """, unsafe_allow_html=True)
        
    with map_col2:
        google_map_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote('SIS Fitness Club')}"
        st.markdown(f"""
        <div class='luxury-card' style='text-align: center;'>
            <div style='font-size: 1.2rem; font-weight: 700; color: #fff; margin-bottom: 6px;'>🗺️ Google 地圖導航</div>
            <div style='color: #cbd5e1; font-size: 0.85rem;'>一鍵開啟地圖，快速導航前往場館</div>
            <a href='{google_map_url}' target='_blank' class='action-btn'>📍 開啟 Google Map 導航</a>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. 模組：📅 課程預約
# -----------------------------------------------------------------------------
elif st.session_state.selected_cat in [I18N["zh"]["menu_booking"], I18N["en"]["menu_booking"]]:
    if not st.session_state.is_logged_in:
        st.warning(t["lock_msg"])
    else:
        c_col1, c_col2 = st.columns([3, 1])
        with c_col1:
            st.markdown("### 📅 團體課程預約")
        with c_col2:
            if st.button(t["btn_checkin"]):
                st.session_state.fit_coins += 50
                st.success(t["checkin_success"])
                st.rerun()

        now = datetime.datetime.now()
        with st.expander(t["sim_title"]):
            simulated_hour = st.slider(t["sim_hour"], 0, 23, value=18)
            simulated_minute = st.slider(t["sim_min"], 0, 59, value=30)
            current_time = now.replace(hour=simulated_hour, minute=simulated_minute, second=0)

        categories = [t["all_cat"], "瑜珈/提斯", "心肺/有氧/拳擊", "肌力訓練", "舞蹈"]
        selected_category = st.selectbox(t["select_cat_label"], options=categories, index=0)

        date_cols = st.columns(7)
        for idx, wdate in enumerate(WEEK_DATES):
            with date_cols[idx]:
                if wdate["date_key"] == st.session_state.selected_date:
                    st.button(f"👉 {wdate['num']}", key=f"wdate_{wdate['date_key']}", type="primary")
                else:
                    if st.button(f"{wdate['day']} {wdate['num']}", key=f"wdate_{wdate['date_key']}"):
                        st.session_state.selected_date = wdate["date_key"]
                        st.rerun()

        filtered_courses = [
            c for c in COURSES_WEEK_DATA 
            if c["date_key"] == st.session_state.selected_date and 
            (selected_category == t["all_cat"] or c["cat"] == selected_category)
        ]

        if not filtered_courses:
            st.info("💡 當天此類別暫無安排課程。")
        else:
            for c in filtered_courses:
                course_name = c['name'][st.session_state.lang]
                room_name = c['room'][st.session_state.lang]
                is_booked = c['id'] in st.session_state.my_bookings
                current_booked = c['booked'] + (1 if is_booked else 0)
                
                start_str, end_str = c['time'].split('~')
                sh, sm = map(int, start_str.split(':'))
                eh, em = map(int, end_str.split(':'))
                course_start = current_time.replace(hour=sh, minute=sm)
                course_end = current_time.replace(hour=eh, minute=em)

                if current_time > course_end:
                    status_badge = f"<span style='color:#94a3b8;'>{t['status_ended']}</span>"
                    can_book = False
                elif course_start <= current_time <= course_end:
                    status_badge = f"<span style='color:#f59e0b;'>{t['status_ongoing']}</span>"
                    can_book = False
                else:
                    status_badge = f"<span style='color:#10b981;'>{t['status_open']}</span>"
                    can_book = True

                with st.container():
                    st.markdown(f"""
                    <div class='luxury-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div>
                                <span class='badge-purple'>{c['cat']}</span> {status_badge}
                                <div style='font-size:1.3rem; font-weight:700; color:#fff; margin-top:4px;'>{course_name}</div>
                                <div style='font-size:0.85rem; color:#cbd5e1;'>🕒 {c['time']} | 🚪 {room_name} | 👤 {t['teacher']}: {c['teacher']}</div>
                                <div style='font-size:0.85rem; color:#fef08a; margin-top:4px;'>{t['booked_count']} {current_booked}/{c['max']} | {t['pts_cost']} {c['cost']} PTS</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    btn_col1, btn_col2 = st.columns([1, 4])
                    with btn_col1:
                        if is_booked:
                            if st.button(t["btn_cancel"], key=f"bk_{c['id']}"):
                                st.session_state.my_bookings.remove(c['id'])
                                st.session_state.fit_coins += c['cost']
                                st.success(t["cancel_success"].format(name=course_name, cost=c['cost']))
                                st.rerun()
                        else:
                            if not can_book:
                                st.button(t["btn_ended"], key=f"bk_{c['id']}", disabled=True)
                            elif current_booked >= c['max']:
                                st.button(t["btn_full"], key=f"bk_{c['id']}", disabled=True)
                            else:
                                if st.button(t["btn_book"], key=f"bk_{c['id']}"):
                                    if st.session_state.fit_coins >= c['cost']:
                                        st.session_state.my_bookings.add(c['id'])
                                        st.session_state.fit_coins -= c['cost']
                                        st.success(t["book_success"].format(name=course_name, cost=c['cost']))
                                        st.rerun()
                                    else:
                                        st.error(t["coins_not_enough"])

# -----------------------------------------------------------------------------
# 10. 模組：📋 我的行程
# -----------------------------------------------------------------------------
elif st.session_state.selected_cat in [I18N["zh"]["menu_mylist"], I18N["en"]["menu_mylist"]]:
    if not st.session_state.is_logged_in:
        st.warning(t["lock_msg"])
    else:
        st.markdown(f"### {t['my_bookings_title']}")
        if not st.session_state.my_bookings:
            st.info(t["no_bookings"])
        else:
            for c in COURSES_WEEK_DATA:
                if c['id'] in st.session_state.my_bookings:
                    course_name = c['name'][st.session_state.lang]
                    room_name = c['room'][st.session_state.lang]
                    gcal_url = create_gcal_link(course_name, c['date_key'], c['time'], room_name, c['teacher'])
                    
                    st.markdown(f"""
                    <div class='luxury-card'>
                        <div style='font-size: 1.2rem; font-weight: 700; color: #fff;'>{course_name}</div>
                        <div style='font-size: 0.85rem; color: #cbd5e1;'>📅 {c['date']} | 🕒 {c['time']} | 🚪 {room_name}</div>
                        <div style='margin-top: 10px;'>
                            <a href='{gcal_url}' target='_blank' class='action-btn' style='display:inline-block; width:auto;'>{t['add_gcal']}</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"{t['btn_cancel']} {course_name}", key=f"my_cancel_{c['id']}"):
                        st.session_state.my_bookings.remove(c['id'])
                        st.session_state.fit_coins += c['cost']
                        st.rerun()

# -----------------------------------------------------------------------------
# 11. 模組：🏋️ 器材圖鑑
# -----------------------------------------------------------------------------
elif st.session_state.selected_cat in [I18N["zh"]["menu_equip"], I18N["en"]["menu_equip"]]:
    st.markdown(f"### {t['equip_title']}")
    e_cols = st.columns(2)
    for idx, eq in enumerate(EQUIPMENT_DATA):
        with e_cols[idx % 2]:
            st.markdown(f"""
            <div class='facility-card'>
                <div style='font-weight: 700; font-size: 1.1rem; color: #facc15;'>{eq['name'][st.session_state.lang]}</div>
                <div style='font-size: 0.85rem; color: #cbd5e1; margin-top: 6px;'><b>{t['target_label']}</b>{eq['target'][st.session_state.lang]}</div>
                <div style='font-size: 0.85rem; color: #ec4899; margin-top: 4px;'><b>{t['tips_label']}</b>{eq['tips'][st.session_state.lang]}</div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 12. 模組：🤖 AI 健身菜單
# -----------------------------------------------------------------------------
elif st.session_state.selected_cat in [I18N["zh"]["menu_ai"], I18N["en"]["menu_ai"]]:
    if not st.session_state.is_logged_in:
        st.warning(t["lock_msg"])
    else:
        st.markdown("### 🤖 AI 個人化健身菜單生成器")
        goal = st.selectbox("🎯 您的訓練目標", ["減脂雕塑", "增肌增重", "心肺耐力提升", "體態矯正與伸展"])
        days = st.slider("📅 每週預計運動天數", 1, 7, 3)
        level = st.radio("🏋️ 健身經驗強度", ["初學者", "中級階段", "進階愛好者"], horizontal=True)

        if st.button("✨ 生成專屬 AI 健身菜單"):
            st.success(f"🎉 已成功為您規劃【{goal}】專屬菜單（每週 {days} 天 • {level}）")
            st.markdown(f"""
            <div class='luxury-card'>
                <div style='font-weight:700; color:#facc15; font-size:1.1rem;'>Day 1: 主核心與下肢穩定</div>
                <p style='color:#cbd5e1; font-size:0.85rem;'>• 熱身：動態伸展 10 分鐘<br>• 主訓練：徒手深蹲 4 組 x 15 次<br>• TRX 懸吊輔助划船 3 組 x 12 次<br>• 收尾：瑜珈墊緩和拉筋 10 分鐘</p>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 13. 模組：👥 明星師資
# -----------------------------------------------------------------------------
elif st.session_state.selected_cat in [I18N["zh"]["menu_coaches"], I18N["en"]["menu_coaches"]]:
    st.markdown("### 👥 明星師資團隊與資歷卡片")
    st.markdown("<div style='color: #cbd5e1; margin-bottom: 20px; font-size: 0.95rem;'>SIS Fitness Club 擁有頂尖且具備溫度的教練團隊，專業陪伴您的體態轉變歷程。</div>", unsafe_allow_html=True)

    coach_cols = st.columns(3)
    for idx, coach in enumerate(COACHES_DETAIL_DATA):
        with coach_cols[idx]:
            tags_html = "".join([f"<span class='badge-purple'>{tag}</span>" for tag in coach["tags"]])
            certs_html = "".join([f"<li style='margin-bottom: 4px;'>{cert}</li>" for cert in coach["certs"]])

            st.markdown(f"""
            <div class='coach-card'>
                <div>
                    <img src='{coach["img"]}' class='coach-avatar'>
                    <div style='font-size: 1.3rem; font-weight: 800; color: #ffffff;'>{coach["name"]}</div>
                    <div style='font-size: 0.85rem; color: #facc15; font-weight: 600; margin-bottom: 4px;'>{coach["role"]} • {coach["exp"]}</div>
                    <div style='margin-bottom: 10px;'>{tags_html}</div>
                    <p style='font-size: 0.85rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 12px;'>{coach["bio"]}</p>
                    <hr style='border-color: rgba(255,255,255,0.1); margin: 10px 0;'>
                    <div style='font-size: 0.85rem; font-weight: 700; color: #f3e8ff; margin-bottom: 6px;'>🏆 專業認證與資歷：</div>
                    <ul style='font-size: 0.8rem; color: #94a3b8; padding-left: 18px; margin-bottom: 10px;'>
                        {certs_html}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📅 預約 {coach['name']} 一對一體驗", key=f"btn_coach_{idx}"):
                st.success(f"已收到您對 {coach['name']} 的體驗預約申請！客服專員將儘快與您聯繫安排。")

# -----------------------------------------------------------------------------
# 14. 模組：💬 預約私訊箱
# -----------------------------------------------------------------------------
elif st.session_state.selected_cat in [I18N["zh"]["menu_inbox"], I18N["en"]["menu_inbox"]]:
    st.markdown(f"### {t['inbox_title']}")
    for msg in st.session_state.inbox_messages:
        st.markdown(f"""
        <div class='luxury-card'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;'>
                <span style='font-weight: 700; color: #facc15;'>🗣️ {msg['sender']}</span>
                <span style='font-size: 0.8rem; color: #94a3b8;'>{msg['time']}</span>
            </div>
            <div style='color: #f1f1f6; font-size: 0.95rem; line-height: 1.6;'>{msg['text']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"### {t['send_msg_title']}")
    recipient = st.selectbox(t["msg_receiver"], ["客服中心", "Umi 老師", "Chloe 教練", "James 教練"])
    msg_text = st.text_area(t["msg_input"], height=100)
    
    if st.button(t["btn_send"]):
        if msg_text.strip():
            now_str = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
            st.session_state.inbox_messages.append({
                "sender": f"我 ➔ {recipient}",
                "time": now_str,
                "text": msg_text
            })
            st.success(t["msg_sent_success"])
            st.rerun()

# -----------------------------------------------------------------------------
# 15. 模組：🏫 入會指引
# -----------------------------------------------------------------------------
elif st.session_state.selected_cat in [I18N["zh"]["menu_join"], I18N["en"]["menu_join"]]:
    st.markdown("### 🏫 入會與體驗課指引")
    st.markdown("""
    <div class='luxury-card'>
        <div style='font-size: 1.2rem; font-weight: 700; color: #facc15; margin-bottom: 10px;'>🌟 簡單 3 步驟開啟您的健身之旅</div>
        <ol style='color: #cbd5e1; line-height: 2;'>
            <li><b>第一步：線上預約體驗</b> — 選擇您感興趣的單堂團體課程或 1 對 1 教練體驗。</li>
            <li><b>第二步：專員諮詢評估</b> — 到場體驗，由專業團隊為您測量 InBody 並進行動作評估。</li>
            <li><b>第三步：彈性入會方案</b> — 選擇最適合您生活節奏的會籍與點數方案，即刻開展運動生活。</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)