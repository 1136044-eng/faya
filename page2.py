import streamlit as st
import streamlit.components.v1 as components

# 設定頁面滿版與標題
st.set_page_config(layout="wide", page_title="Z-Gen 奢華美食地圖", initial_sidebar_state="collapsed")

html_code = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    * { box-sizing: border-box; }
    body { background-color: #0b0f19; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 12px; }
    ::-webkit-scrollbar { height: 6px; width: 6px; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: 11px; margin-right: 5px; margin-bottom: 5px; }
    .card { background-color: #1e293b; padding: 16px; border-radius: 14px; border: 1px solid #334155; margin-bottom: 12px; }
    button { cursor: pointer; transition: opacity 0.2s; }
    button:hover { opacity: 0.9; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    const { useState } = React;

    const RESTAURANTS = [
      { id: 1, name: "頂級頂樓微醺酒吧", category: "奢華酒吧", price: 1500, rating: 4.8, streak: 12, tags: ["高空夜景", "約會首選", "微醺"], mapUrl: "https://maps.google.com", igUrl: "https://instagram.com", image: "🍷" },
      { id: 2, name: "極上黑毛和牛燒肉", category: "極緻燒肉", price: 2500, rating: 4.9, streak: 8, tags: ["和牛專賣", "極致口感", "聚餐包廂"], mapUrl: "https://maps.google.com", igUrl: "https://instagram.com", image: "🥩" },
      { id: 3, name: "雲端陽明山夜景餐廳", category: "浪漫夜景", price: 1200, rating: 4.7, streak: 15, tags: ["陽明山夜景", "約會首選", "飯店餐廳"], mapUrl: "https://maps.google.com", igUrl: "https://instagram.com", image: "🌙" }
    ];

    const allTags = ['All', '高空夜景', '約會首選', '微醺', '和牛專賣', '極致口感', '聚餐包廂', '陽明山夜景'];

    function App() {
      const [activeTab, setActiveTab] = useState('explore');
      const [selectedTag, setSelectedTag] = useState('All');
      const [search, setSearch] = useState('');
      const [aiRecommendation, setAiRecommendation] = useState(null);
      const [password, setPassword] = useState('');
      const [isUnlocked, setIsUnlocked] = useState(false);

      const filtered = RESTAURANTS.filter(r => {
        const matchesTag = selectedTag === 'All' || r.tags.includes(selectedTag);
        const matchesSearch = r.name.toLowerCase().includes(search.toLowerCase()) || r.category.toLowerCase().includes(search.toLowerCase());
        return matchesTag && matchesSearch;
      });

      const handleAiRecommend = () => {
        const randomRes = RESTAURANTS[Math.floor(Math.random() * RESTAURANTS.length)];
        setAiRecommendation(randomRes);
      };

      const handleUnlock = () => {
        if (password === '8888') {
          setIsUnlocked(true);
        } else {
          alert('授權密碼錯誤！請輸入 8888');
        }
      };

      return (
        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
          
          <div style={{ textAlign: 'center', padding: '15px 0', borderBottom: '1px solid #1e293b' }}>
            <span style={{ background: 'linear-gradient(45deg, #f59e0b, #ec4899)', color: '#fff', padding: '4px 12px', borderRadius: '20px', fontSize: '11px', fontWeight: 'bold' }}>
              MIDNIGHT GOURMET
            </span>
            <h1 style={{ fontSize: '24px', margin: '10px 0 4px', color: '#fff' }}>Z-Gen 奢華美食地圖 🍷</h1>
            <p style={{ color: '#94a3b8', fontSize: '13px', margin: 0 }}>探索 Z 世代最具質感的品味餐廳與獨家獎勵</p>
          </div>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', margin: '16px 0' }}>
            {[
              { id: 'explore', label: '🎴 分類探索' },
              { id: 'ai', label: '✨ AI 今日靈感' },
              { id: 'rewards', label: '🏆 競賽與獎金' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  flex: 1,
                  padding: '10px 0',
                  borderRadius: '12px',
                  border: 'none',
                  backgroundColor: activeTab === tab.id ? '#f59e0b' : '#1e293b',
                  color: activeTab === tab.id ? '#0f172a' : '#94a3b8',
                  fontWeight: 'bold',
                  fontSize: '13px'
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {activeTab === 'explore' && (
            <div>
              <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '12px' }}>
                {allTags.map(tag => (
                  <button
                    key={tag}
                    onClick={() => setSelectedTag(tag)}
                    style={{
                      padding: '6px 14px',
                      borderRadius: '20px',
                      border: '1px solid #334155',
                      backgroundColor: selectedTag === tag ? '#3b82f6' : '#0f172a',
                      color: '#fff',
                      fontSize: '12px',
                      whiteSpace: 'nowrap'
                    }}
                  >
                    {tag}
                  </button>
                ))}
              </div>

              <input
                type="text"
                placeholder="🔍 搜尋餐廳名稱或類別..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '10px',
                  border: '1px solid #334155',
                  backgroundColor: '#1e293b',
                  color: '#fff',
                  marginBottom: '16px',
                  fontSize: '14px'
                }}
              />

              <div>
                {filtered.map(r => (
                  <div key={r.id} className="card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div>
                        <h3 style={{ margin: '0 0 6px', color: '#fff', fontSize: '18px' }}>
                          {r.image} {r.name}
                        </h3>
                        <p style={{ margin: '0 0 8px', color: '#94a3b8', fontSize: '13px' }}>
                          {r.category} • 均消 ${r.price} • ★ {r.rating}
                        </p>
                      </div>
                      <span style={{ backgroundColor: '#0f172a', border: '1px solid #f59e0b', color: '#fbbf24', padding: '4px 8px', borderRadius: '8px', fontSize: '11px', fontWeight: 'bold' }}>
                        👑 連續 {r.streak} 週熱榜
                      </span>
                    </div>

                    <div style={{ margin: '8px 0' }}>
                      {r.tags.map(t => (
                        <span key={t} className="badge" style={{ backgroundColor: '#0f172a', color: '#38bdf8' }}>
                          #{t}
                        </span>
                      ))}
                    </div>

                    <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
                      <a href={r.mapUrl} target="_blank" style={{ flex: 1, textAlign: 'center', color: '#f59e0b', textDecoration: 'none', fontSize: '12px', padding: '8px', border: '1px solid #f59e0b', borderRadius: '8px', fontWeight: 'bold' }}>
                        📍 Google 地圖
                      </a>
                      <a href={r.igUrl} target="_blank" style={{ flex: 1, textAlign: 'center', color: '#ec4899', textDecoration: 'none', fontSize: '12px', padding: '8px', border: '1px solid #ec4899', borderRadius: '8px', fontWeight: 'bold' }}>
                        📸 IG 熱門打卡
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'ai' && (
            <div style={{ backgroundColor: '#1e293b', padding: '24px', borderRadius: '16px', textAlign: 'center', border: '1px solid #334155' }}>
              <h2 style={{ color: '#fff', marginTop: 0, fontSize: '20px' }}>✨ 選擇困難症解星人</h2>
              <p style={{ color: '#94a3b8', fontSize: '13px', lineHeight: '1.5' }}>點擊下方按鈕，讓 AI 為你智慧推薦今晚最具質感的美食據點！</p>
              <button
                onClick={handleAiRecommend}
                style={{ width: '100%', padding: '14px', backgroundColor: '#ec4899', border: 'none', borderRadius: '10px', color: '#fff', fontWeight: 'bold', fontSize: '15px', marginTop: '10px' }}
              >
                🎲 幫我選餐廳
              </button>

              {aiRecommendation && (
                <div style={{ marginTop: '20px', padding: '16px', backgroundColor: '#0f172a', borderRadius: '12px', border: '1px solid #ec4899', textAlign: 'left' }}>
                  <span style={{ color: '#ec4899', fontSize: '12px', fontWeight: 'bold' }}>AI 為你挑選了：</span>
                  <h3 style={{ color: '#fff', margin: '6px 0' }}>{aiRecommendation.image} {aiRecommendation.name}</h3>
                  <p style={{ color: '#cbd5e1', fontSize: '13px', margin: 0 }}>類別：{aiRecommendation.category}｜均消：${aiRecommendation.price}</p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'rewards' && (
            <div style={{ backgroundColor: '#1e293b', borderRadius: '16px', padding: '20px', border: '1px solid #334155' }}>
              <h3 style={{ color: '#fff', fontSize: '16px', marginTop: 0 }}>🔒 內部同仁開發獎金專區</h3>
              
              {!isUnlocked ? (
                <div>
                  <p style={{ color: '#94a3b8', fontSize: '13px' }}>請輸入授權密碼以解鎖內部開發獎金與抽成明細：</p>
                  <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
                    <input
                      type="password"
                      placeholder="請輸入密碼 (預設: 8888)"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      style={{ flex: 1, padding: '10px', borderRadius: '8px', border: '1px solid #475569', backgroundColor: '#0f172a', color: '#fff', fontSize: '14px' }}
                    />
                    <button 
                      onClick={handleUnlock} 
                      style={{ padding: '10px 20px', backgroundColor: '#f59e0b', border: 'none', borderRadius: '8px', color: '#0f172a', fontWeight: 'bold', cursor: 'pointer' }}
                    >
                      解鎖
                    </button>
                  </div>
                </div>
              ) : (
                <div style={{ marginTop: '10px', backgroundColor: '#0f172a', padding: '16px', borderRadius: '12px', border: '1px solid #10b981' }}>
                  <p style={{ color: '#10b981', fontWeight: 'bold', margin: '0 0 10px', fontSize: '14px' }}>🔓 驗證成功！專案開發獎金獎勵方案：</p>
                  <ul style={{ color: '#cbd5e1', fontSize: '13px', paddingLeft: '20px', margin: 0, lineHeight: '2' }}>
                    <li>基礎商家上架獎金：<strong style={{ color: '#fbbf24' }}>$200 / 店</strong></li>
                    <li>連爆熱榜（Streak ≥ 10）：<strong style={{ color: '#fbbf24' }}>額外 +$500 / 店</strong></li>
                    <li>月度開發冠軍大獎：<strong style={{ color: '#fbbf24' }}>$3,000 NTD</strong></li>
                  </ul>
                </div>
              )}
            </div>
          )}

        </div>
      );
    }

    ReactDOM.render(<App />, document.getElementById('root'));
  </script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)
