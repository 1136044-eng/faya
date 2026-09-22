import streamlit as st
import random
from supabase import create_client

# 1. Supabase 連線設定
SUPABASE_URL = "https://rowtumtnlhpavqokarxp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJvd3R1bXRubGhwYXZxb2thcnhwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg5NTM2NzUsImV4cCI6MjEwNDUyOTY3NX0.IoMcwRCFsxD7Y17BK696ONXeBvn_4Q-1nMqwuPqxE78"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Z-Gen 餐廳地圖", page_icon="🍽️", layout="wide")
st.title("Z-Generation 餐廳地圖 🍽️")

# 2. 從 Supabase 抓取資料
@st.cache_data(ttl=60)
def load_data():
    response = supabase.table("restaurants").select("*").execute()
    return response.data

try:
    data = load_data()

    # 建立三個頁籤：分類探索 vs AI 今日風格 vs 競賽與獎金制度
    tab1, tab2, tab3 = st.tabs(["🗄️ 分類探索", "✨ AI 今日風格氛圍", "🏆 競賽與獎金制度"])

    # --- 頁籤 1：分類探索 ---
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

    # --- 頁籤 2：AI 今日風格氛圍 ---
    with tab2:
        st.subheader("🤖 AI 今日靈感推薦")
        st.write("不確定今天想吃什麼？讓 AI 根據今日氛圍幫你挑選！")
        
        mood = st.radio(
            "你今天的精神狀態/氛圍是？",
            ["✨ 想要精緻高質感", "🔥 爽快解壓/重口味", "☕ 浪漫約會/放鬆氛圍", "🎲 隨便 AI 幫我選"]
        )

        if st.button("🔮 生成今日風格推薦", type="primary"):
            recommendation = None
            
            if mood == "✨ 想要精緻高質感":
                candidates = [r for r in data if r.get("avg_price", 0) and r.get("avg_price", 0) >= 1500]
            elif mood == "🔥 爽快解壓/重口味":
                candidates = [r for r in data if any(t in ["麻辣燙", "湖南湘菜", "川菜", "精釀啤酒"] for t in r.get("tags", []))]
            elif mood == "☕ 浪漫約會/放鬆氛圍":
                candidates = [r for r in data if any(t in ["約會首選", "陽明山夜景", "頂級私廚", "飯店餐廳"] for t in r.get("tags", []))]
            else:
                candidates = data

            if not candidates:
                candidates = data

            recommendation = random.choice(candidates)

            st.balloons()
            st.success("🎉 AI 推薦你今天去這裡：")
            
            with st.container(border=True):
                st.title(f"👉 {recommendation.get('name')}")
                st.write(f"💰 預估消費：${recommendation.get('avg_price')} | ⭐ 評分：{recommendation.get('rating')}")
                if recommendation.get("tags"):
                    st.write("🏷️ " + " ".join([f"`#{t}`" for t in recommendation["tags"]]))
                
                btn1, btn2 = st.columns(2)
                if recommendation.get("google_map_url"):
                    btn1.link_button("📍 前往 Google 地圖", recommendation["google_map_url"])
                if recommendation.get("ig_url"):
                    btn2.link_button("📸 查看 Instagram", recommendation["ig_url"])

    # --- 頁籤 3：競賽與獎金制度 ---
    with tab3:
        # 1. 公開區塊：店家皇冠連勝機制
        st.subheader("👑 合作店家皇冠連勝與累積獎勵機制")
        st.caption("店家獲得 👑 皇冠標章（上榜 Top 3）可選擇每月單次領取，或持續累積連勝解鎖更高加碼與終極福利！")

        streak_col1, streak_col2, streak_col3 = st.columns(3)

        with streak_col1:
            st.caption("連勝 2 個月")
            st.metric(label="獲得 👑 皇冠標章", value="+2% 額外獎金")

        with streak_col2:
            st.caption("連勝 6 個月")
            st.metric(label="獲得 👑👑👑 三皇冠", value="+6% 額外獎金")

        with streak_col3:
            st.caption("滿 1 年 (12 個月)")
            st.metric(label="👑 殿堂級店家專屬", value="+12% 額外獎金", delta="加贈 12 個月免費刊登")

        st.markdown("---")

        # 2. 公開區塊：評選與參賽規範
        st.info("""
📌 **活動參與與評選規範：**
1. **參賽資格門檻**：限當月來客數達 **1,000 人次以上**（或單月營業額達 30 萬元以上）之合作店家參加。
2. **單一獲獎限制**：當月每家店家**限獲頒一個獎項**（若於多個榜單同時上榜，將優先保留名次較高之獎項，其餘順位由後續店家順延）。
3. **同分比序機制**：若店家綜合評分相同，將以**加入簽約會員之時間先後順序**優先決定排名順位。
""")

        st.markdown("---")

        # 3. 隱藏區塊：員工內部開發獎金（需密碼）
        st.subheader("🔒 內部同仁開發獎金專區")
        staff_pwd = st.text_input("請輸入員工授權密碼以查看開發獎金細節：", type="password")

        # 預設密碼設定為：8888 (可自行更改)
        if staff_pwd == "8888":
            st.success("🔓 驗證成功！已解鎖內部同仁獎金制度：")
            col1, col2, col3 = st.columns(3)
            col1.metric("基礎推薦獎金", "$200 / 店", "成功建立資料並核准")
            col2.metric("高人氣店家加碼", "$500 / 店", "獲得 50+ 次收藏/點擊")
            col3.metric("月度開發王獎金", "$3,000", "當月新增最多有效店家")

            st.write("**📋 獎金發放與審核規則：**")
            st.markdown("""
            * **完整欄位要求**：新增店家必須包含 `店家名稱`、`平均消費`、`Google 地圖連結` 及至少 `2 個標籤`。
            * **品質與核實**：由管理團隊審核資料真實性，通過後於次月薪資統一發放。
            * **重複店家判定**：若重複推薦，獎金歸屬於首位提交完整資料之同仁。
            """)
        elif staff_pwd != "":
            st.error("❌ 密碼錯誤，請重新輸入！")

except Exception as e:
    st.error(f"連線失敗：{e}")
