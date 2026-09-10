import streamlit as st
import random
from supabase import create_client
import google.generativeai as genai

# 1. Supabase 連線設定
SUPABASE_URL = "https://rowtumtnlhpavqokarxp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvd3R1bXRubGhwYXZxb2thcnhwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg5NTM2NzUsImV4cCI6MjEwNDUyOTY3NX0.IoMcwRCFsxD7Y17BK696ONXeBvn_4Q-1nMqwuPqxE78"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Gemini API 設定 (請將 YOUR_GEMINI_API_KEY 替換為你的真實 API Key)
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)

prompt_stylist = (
    "你是頂尖的『AI 時尚穿搭與旅遊顧問』。你的任務是根據用戶輸入的『今天的穿搭風格』和『今天的聚會/聚餐目的』，"
    "給予最精準、幽默且精緻的目的地推薦與配件搭配建議。"
    "回覆請包含：1. 對風格的讚美與點評 2. 推薦 2 個最適合這身穿搭的聚餐地點類型或具體氛圍 3. 建議加上的亮點配件。"
    "請使用繁體中文，字數保持在 150 字以內，語氣要時尚有品味。"
)

stylist_model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=prompt_stylist)

st.set_page_config(page_title="Z-Gen 餐廳地圖", page_icon="🍽️", layout="wide")

# --- 側邊欄：商家與平台專區 ---
with st.sidebar:
    st.header("🏪 商家與平台專區")
    
    st.subheader("💰 餐廳加入平台會費")
    with st.container(border=True):
        st.write("月費方案：`$1,500` / 月")
        st.write("季費方案：`$1,200` / 月 (省 :orange[20%])")
        st.write("年費方案：`$900` / 月 (省 :orange[40%])")
        st.caption("💡 買越久越便宜！")
        
    st.subheader("🏆 年度業績大賽")
    st.info("""
    🥇 **第一名：獎金** `100,000`  
    🥈 **第二名：獎金** `50,000`  
    🥉 **第三名：獎金** `$30,000`
    """)

# --- 主畫面 ---
st.caption("公開透明、整合 Google/IG 資訊、AI 情境穿搭推薦")
st.title("Z-Generation 餐廳地圖 🍽️")

# 3. 從 Supabase 抓取資料
@st.cache_data(ttl=60)
def load_data():
    response = supabase.table("restaurants").select("*").execute()
    return response.data

try:
    data = load_data()

    # 建立三個頁籤
    tab1, tab2, tab3 = st.tabs(["📖 餐廳地圖瀏覽", "🤖 AI 穿搭與情境推薦", "👑 業績排行榜 & 獎金制度"])

    # --- 頁籤 1：餐廳地圖瀏覽 ---
    with tab1:
        all_tags = set()
        for item in data:
            if item.get("tags"):
                all_tags.update(item["tags"])

        selected_tag = st.selectbox("選擇分類置物櫃：", ["全部餐廳"] + sorted(list(all_tags)))

        if selected_tag != "全部餐廳":
            filtered_data = [r for r in data if r.get("tags") and selected_tag in r["tags"]]
        else:
            filtered_data = data

        st.write(f"顯示共 **{len(filtered_data)}** 家餐廳：")

        for spot in filtered_data:
            with st.container(border=True):
                st.subheader(spot.get("name", "未命名餐廳"))
                col1, col2 = st.columns(2)
                col1.write(f"💰 平均消費：${spot.get('avg_price', 'N/A')}")
                col2.write(f"⭐ 評分：{spot.get('rating', 'N/A')}")
                
                if spot.get("tags"):
                    st.caption("🏷️ " + " ".join([f"`#{t}`" for t in spot["tags"]]))
                
                btn_col1, btn_col2 = st.columns(2)
                if spot.get("google_map_url"):
                    btn_col1.link_button("📍 Google 地圖", spot["google_map_url"])
                if spot.get("ig_url"):
                    btn_col2.link_button("📸 Instagram", spot["ig_url"])

    # --- 頁籤 2：AI 穿搭與情境推薦 ---
    with tab2:
        st.header("🤖 AI 穿搭與目的地智能推薦")
        st.caption("付費用戶可解鎖更多推薦")

        outfit = st.text_input("今天的穿搭風格是？（例如：美式復古、韓系街頭、正式西裝）", value="美式復古、寬鬆街頭風")
        purpose = st.selectbox("今天的聚會目的是？", ["浪漫約會", "生日慶祝", "單純跟朋友聚餐", "商務宴客 / 談生意"], index=2)

        if st.button("啟動 AI 推薦餐廳", type="primary"):
            st.balloons()
            
            # 呼叫 Gemini AI 進行穿搭顧問點評
            with st.spinner("🤖 AI 時尚顧問正在為您分析穿搭與點評..."):
                try:
                    prompt_input = f"我今天的穿搭風格是：{outfit}。我今天的目的/行程是：{purpose}。請給我智能推薦。"
                    ai_response = stylist_model.generate_content(prompt_input)
                    
                    st.chat_message("assistant").write(f"✨ **【AI 穿搭顧問點評】**\n\n{ai_response.text.strip()}")
                except Exception as ai_err:
                    st.info(f"✨ **【AI 穿搭顧問點評】**\n\n這身「{outfit}」搭配「{purpose}」展現極佳個人品味！建議加上美式復古墨鏡或街頭金屬項鍊，盡情享受美食聚會！")

            st.success(f"✨ 已根據「{outfit}」與「{purpose}」為您篩選最佳餐廳！")
            
            # 隨機抽取餐廳資料庫
            shuffled = random.sample(data, min(len(data), 5))
            free_picks = shuffled[:2]
            prime_picks = shuffled[2:5]

            st.subheader("🆓 基本款推薦（免費瀏覽 2 個）")
            for spot in free_picks:
                with st.container(border=True):
                    st.subheader(f"👉 {spot.get('name')}")
                    st.write(f"💰 預估消費：${spot.get('avg_price')} | ⭐ 評分：{spot.get('rating')}")
                    if spot.get("tags"):
                        st.caption("🏷️ " + " ".join([f"`#{t}`" for t in spot["tags"]]))
                    col1, col2 = st.columns(2)
                    if spot.get("google_map_url"):
                        col1.link_button("📍 Google 地圖", spot["google_map_url"])
                    if spot.get("ig_url"):
                        col2.link_button("📸 Instagram", spot["ig_url"])

            st.markdown("---")
            st.subheader("💎 Prime 會員專屬（解鎖額外 3 個推薦）")
            
            is_prime = st.checkbox("🔑 勾選此項體驗 Prime 會員解鎖權限")

            if is_prime:
                for spot in prime_picks:
                    with st.container(border=True):
                        st.subheader(f"👑 [Prime 獨家] {spot.get('name')}")
                        st.write(f"💰 預估消費：${spot.get('avg_price')} | ⭐ 評分：{spot.get('rating')}")
                        if spot.get("tags"):
                            st.caption("🏷️ " + " ".join([f"`#{t}`" for t in spot["tags"]]))
                        col1, col2 = st.columns(2)
                        if spot.get("google_map_url"):
                            col1.link_button("📍 Google 地圖", spot["google_map_url"])
                        if spot.get("ig_url"):
                            col2.link_button("📸 Instagram", spot["ig_url"])
            else:
                st.warning("⚠️ 需每月支付訂閱費以解鎖 Prime 款進階推薦餐廳功能！")

    # --- 頁籤 3：業績排行榜 & 皇冠連勝獎金制度 ---
    with tab3:
        st.header("👑 餐廳業績排行榜與評比專區")
        
        # 選擇統計週期
        period = st.radio("選擇統計週期：", ["📅 月業績排行榜", "🏆 年業績排行榜"], horizontal=True)
        st.write(f"目前顯示：**{period}**")

        # 排行榜三大分類
        col_rank1, col_rank2, col_rank3 = st.columns(3)

        sorted_by_rating = sorted(data, key=lambda x: x.get('rating', 0), reverse=True)
        
        service_top5 = sorted_by_rating[:5]
        env_top5 = sorted_by_rating[2:7] if len(sorted_by_rating) >= 7 else sorted_by_rating[:5]
        food_top5 = sorted_by_rating[1:6] if len(sorted_by_rating) >= 6 else sorted_by_rating[:5]

        with col_rank1:
            st.subheader("🤝 服務態度極佳 Top 5")
            with st.container(border=True):
                for idx, spot in enumerate(service_top5, 1):
                    # 前三名加上皇冠標誌
                    crown = "👑 " if idx <= 3 else ""
                    st.markdown(f"**Top {idx}. {crown}{spot.get('name')}**")
                    st.caption(f"⭐ 綜合評分：{spot.get('rating')} | 💰 平均消費：${spot.get('avg_price')}")
                    st.divider()

        with col_rank2:
            st.subheader("🌿 環境舒適衛生 Top 5")
            with st.container(border=True):
                for idx, spot in enumerate(env_top5, 1):
                    crown = "👑 " if idx <= 3 else ""
                    st.markdown(f"**Top {idx}. {crown}{spot.get('name')}**")
                    st.caption(f"⭐ 綜合評分：{spot.get('rating')} | 💰 平均消費：${spot.get('avg_price')}")
                    st.divider()

        with col_rank3:
            st.subheader("🍱 餐飲美味 Top 5")
            with st.container(border=True):
                for idx, spot in enumerate(food_top5, 1):
                    crown = "👑 " if idx <= 3 else ""
                    st.markdown(f"**Top {idx}. {crown}{spot.get('name')}**")
                    st.caption(f"⭐ 綜合評分：{spot.get('rating')} | 💰 平均消費：${spot.get('avg_price')}")
                    st.divider()

        st.markdown("---")
        st.subheader("👑 皇冠連勝與累積加碼獎金機制")
        st.write("店家或同仁獲得 **👑 皇冠標章（上榜 Top 3）** 可選擇**每月單次領取**，或**持續累積連勝**解鎖更高加碼與終極福利！")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("連勝 2 個月", "💰 +2% 額外獎金", "獲得 👑 皇冠標章")
        col2.metric("連勝 4 個月", "💰 +6% 額外獎金", "獲得 👑👑 雙皇冠")
        col3.metric("連勝 6 個月", "💰 +8% 額外獎金", "獲得 👑👑👑 三皇冠")
        col4.metric("滿 1 年 (12個月)", "🎁 免費刊登 6 個月", "👑 殿堂級店家專屬")

        st.markdown("---")
        st.subheader("💰 團隊開發與基礎業績獎金制度")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("基礎推薦獎金", "$200 / 店", "成功建立資料並核准")
        m_col2.metric("高人氣店家加碼", "$500 / 店", "獲得 50+ 次收藏/點擊")
        m_col3.metric("月度開發王獎金", "$3,000", "當月新增最多有效店家")

        st.markdown("---")
        st.write("**📋 皇冠機制與獎金核算說明：**")
        st.markdown("""
        * **👑 皇冠標章資格**：凡於月度/年度評比中獲得 `服務態度`、`環境衛生` 或 `餐飲美味` 前 3 名者，即獲得當月 👑 皇冠標章。
        * **領取方式選擇**：
            1. **月領模式**：每月結算基礎獎金發放。
            2. **累積連勝模式**：保持上榜不中斷，將於第 2、4、6 個月自動提高獎金抽成百分比。
        * **滿年終極大獎**：連續 12 個月維持榜單前列（累積 12 👑），平台將直接贈送該店家 **6 個月免費廣告位與優先推薦權**（價值 `$9,000`）！
        """)

except Exception as e:
    st.error(f"連線失敗：{e}")
