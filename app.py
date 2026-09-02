import streamlit as st
import pandas as pd
import random

# 網頁基本設定
st.set_page_config(page_title="Z世代餐廳地圖", page_icon="🍔", layout="wide")
st.title("🍔 Z世代餐廳地圖 App 原型測試")
st.caption("公開透明、整合 Google/IG 資訊、AI 情境穿搭推薦")

# 模擬資料庫
restaurants = [
    {"名稱": "網美風：微光森林 Cafe", "分類": "網美餐廳", "均消": 450, "評價": "4.8 ★ (IG熱門)", "月業績": 950000},
    {"名稱": "老牌：金牌張排骨大王", "分類": "老牌餐廳", "均消": 150, "評價": "4.5 ★ (Google千評)", "月業績": 880000},
    {"名稱": "精緻：Aether 法式現代料理", "分類": "精緻餐廳", "均消": 2500, "評價": "4.9 ★ (頂級私廚)", "月業績": 1200000},
    {"名稱": "平價：九零後麻辣燙", "分類": "平價餐廳", "均消": 180, "評價": "4.3 ★ (學生最愛)", "月業績": 520000},
    {"名稱": "網美風：粉紅泡泡餐酒館", "分類": "網美餐廳", "均消": 600, "評價": "4.7 ★ (拍照聖地)", "月業績": 710000},
]

# 側邊欄：商家與平台機制展示
st.sidebar.header("🏪 商家與平台專區")
st.sidebar.subheader("💰 餐廳加入平台會費")
st.sidebar.code("月費方案：$1,500 / 月\n季費方案：$1,200 / 月 (省20%)\n年費方案：$900 / 月 (省40%)\n💡 買越久越便宜！")

st.sidebar.subheader("🏆 年度業績大賽")
st.sidebar.info("🥇 第一名：獎金 $100,000\n🥈 第二名：獎金 $50,000\n🥉 第三名：獎金 $30,000")

# 主頁面：功能標籤頁
tab1, tab2, tab3 = st.tabs(["🗺️ 餐廳地圖瀏覽", "🤖 AI 穿搭與情境推薦", "👑 每月排行榜"])

with tab1:
    st.header("探索全新世代餐廳")
    cate = st.multiselect("選擇你想找的餐廳種類：", ["網美餐廳", "老牌餐廳", "精緻餐廳", "平價餐廳"], default=["網美餐廳", "老牌餐廳", "精緻餐廳", "平價餐廳"])
    
    st.write("---")
    for r in restaurants:
        if r["分類"] in cate:
            # 模擬前三名皇冠
            crown = "👑 " if r["月業績"] >= 880000 else ""
            st.subheader(f"{crown}{r['名稱']}")
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 價格公開透明 (均消)", f"${r['均消']}")
            col2.write(f"🌟 **社群整合數據**\n\n{r['評價']}")
            col3.button("查看 Google / IG 詳細串聯資料", key=r["名稱"])
            st.write("---")

with tab2:
    st.header("🤖 AI 穿搭與目的地智能推薦")
    st.caption("付費用戶可解鎖更多推薦")
    
    style = st.text_input("今天的穿搭風格是？（例如：美式復古、韓系街頭、正式西裝）")
    purpose = st.selectbox("今天的聚會目的是？", ["談生意", "浪漫約會", "生日慶祝", "單純跟朋友聚餐"])
    
    if st.button("啟動 AI 推薦餐廳"):
        st.success(f"AI 根據您的【{style}】穿搭與【{purpose}】目的，為您精選以下餐廳：")
        
        st.subheader("🔓 基本款推薦（免費瀏覽 2 個）")
        st.info("1. 微光森林 Cafe - 氣氛極佳，完美契合您的穿搭")
        st.info("2. Aether 法式現代料理 - 隱密性高，最適合您的聚會目的")
        
        st.write("---")
        st.subheader("💎 Prime 會員專屬（解鎖額外 3 個推薦）")
        st.warning("⚠️ 需每月支付訂閱費以解鎖 Prime 款進階推薦餐廳功能！")
        if st.button("立即付費解鎖額外 3 個推薦"):
            st.balloons()

with tab3:
    st.header("👑 本月業績排行榜 (自動標示皇冠)")
    df = pd.DataFrame(restaurants).sort_values(by="月業績", ascending=False)
    st.dataframe(df)
