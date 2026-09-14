import streamlit as st
import streamlit.components.v1 as components

# 設定頁面滿版與標題
st.set_page_config(layout="wide", page_title="Z-Gen 奢華美食地圖")

html_code = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    body { background-color: #0b0f19; color: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; }
    ::-webkit-scrollbar { height: 6px; width: 6px; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    const { useState } = React;

    const RESTAURANTS = [
      { id: 1, name: "頂級頂樓微醺酒吧", category: "奢華酒吧", price: 1500, rating: 4.8, tags: ["高空夜景", "約會首選", "微醺"], mapUrl: "https://maps.google.com", igUrl: "https://instagram.com", image: "🍷" },
      { id: 2, name: "極上黑毛和牛燒肉", category: "極緻燒肉", price: 2500, rating: 4.9, tags: ["和牛專賣", "極致口感", "聚餐包廂"], mapUrl: "https://maps.google.com", igUrl: "https://instagram.com", image: "🥩" },
      { id: 3, name: "雲端陽明山夜景餐廳", category: "浪漫夜景", price: 1200, rating: 4.7, tags: ["陽明山夜景", "約會首選", "飯店餐廳"], mapUrl: "https://maps.google.com", igUrl: "https://instagram.com", image: "🌙" }
    ];

    const allTags = ['All', '高空夜景', '約會首選', '微醺', '和牛專賣', '極致口感', '聚餐包廂', '陽明山夜景', '飯店餐廳'];

    function App() {
      const [activeTab, setActiveTab] = useState('explore');
      const [selectedTag, setSelectedTag] = useState('All');
      const [search, setSearch] = useState('');
      const [aiRecommendation, setAiRecommendation] = useState('');
      const [password, setPassword] = useState('');
      const [isUnlocked, setIsUnlocked] = useState(false);

      const filtered = RESTAURANTS.filter(r => {
        const matchesTag = selectedTag === 'All' || r.tags.includes(selectedTag);
        const matchesSearch = r.name.includes(search) || r.category.includes(search);
        return matchesTag && matchesSearch;
      });

      const handleAiRecommend = () => {
        const randomRes = RESTAURANTS[Math.floor(Math.random() * RESTAURANTS.length)];
        setAiRecommendation(randomRes.name);
      };

      const handleUnlock = () => {
        if (password === '8888') {
          setIsUnlocked(true);
        } else {
          alert('授權密碼錯誤！');
        }
      };

      return (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          {/* 頁面標頭 Header */}
          <div style={{ textAlign: 'center', padding: '20px 0', borderBottom: '1px solid #1e293b' }}>
            <span style={{ background: 'linear-gradient(45deg, #f59e0b, #ec4899)', color: '#fff', padding: '4px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 'bold' }}>
              FOODIE EXPLORER
            </span>
            <h1 style={{ fontSize: '28px', margin: '10px 0 5px', color: '#fff' }}>Z-Gen 奢華美食地圖 🍷</h1>
            <p style={{ color: '#94a3b8', fontSize: '14px' }}>探索 Z 世代最具質感的品味餐廳與限定獎勵</p>
          </div>

          {/* 頁籤選單 Tabs */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', margin: '20px 0' }}>
            {[
              { id: 'explore', label: '🎴 分類探索' },
              { id: 'ai', label: '✨ AI 今日靈感' },
              { id: 'rewards', label: '🏆 競賽與獎金' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  padding: '10px 18px',
                  borderRadius: '12px',
                  border: 'none',
                  backgroundColor: activeTab === tab.id ? '#f59e0b' : '#1e293b',
                  color: activeTab === tab.id ? '#0f172a' : '#94a3b8',
                  fontWeight: 'bold',
                  cursor: 'pointer'
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* 1. 分類探索 Tab */}
          {activeTab === 'explore' && (
            <div>
              <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '15px' }}>
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
                      fontSize: '13px',
                      whiteSpace: 'nowrap',
                      cursor: 'pointer'
                    }}
                  >
                    {tag}
                  </button>
                ))}
              </div>

              <input
                type="text"
                placeholder="搜尋餐廳名稱或類別..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '10px',
                  border: '1px solid #334155',
                  backgroundColor: '#1e293b',
                  color: '#fff',
                  marginBottom: '20px',
                  boxSizing: 'border-box'
                }}
              />

              <div style={{ display: 'grid', gap: '15px' }}>
                {filtered.map(r => (
                  <div key={r.id} style={{ backgroundColor: '#1e293b', padding: '16px', borderRadius: '12px', border: '1px solid #334155', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <h3 style={{ margin: '0 0 6px', color: '#fff', fontSize: '18px' }}>{r.image} {r.name}</h3>
                      <p style={{ margin: '0 0 8px', color: '#94a3b8', fontSize: '13px' }}>{r.category} • 平均消費 ${r.price} • ★ {r.rating}</p>
                      <div>
                        {r.tags.map(t => (
                          <span key={t} style={{ fontSize: '11px', backgroundColor: '#0f172a', color: '#38bdf8', padding: '2px 8px', borderRadius: '6px', marginRight: '5px' }}>#{t}</span>
                        ))}
                      </div>
                    </div>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <a href={r.mapUrl} target="_blank" style={{ color: '#f59e0b', textDecoration: 'none', fontSize: '13px', padding: '6px 10px', border: '1px solid #f59e0b', borderRadius: '6px' }}>地圖</a>
                      <a href={r.igUrl} target="_blank" style={{ color: '#ec4899', textDecoration: 'none', fontSize: '13px', padding: '6px 10px', border: '1px solid #ec4899', borderRadius: '6px' }}>IG</a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 2. AI 今日靈感 Tab */}
          {activeTab === 'ai' && (
            <div style={{ backgroundColor: '#1e293b', padding: '30px', borderRadius: '16px', textAlign: 'center', border: '1px solid #334155' }}>
              <h2 style={{ color: '#fff', marginTop: 0 }}>✨ 糾結不知道吃什麼？</h2>
              <p style={{ color: '#94a3b8', fontSize: '14px' }}>點擊下方按鈕，讓 AI 為你隨機挑選今日極緻美食！</p>
              <button
                onClick={handleAiRecommend}
                style={{ padding: '12px 24px', backgroundColor: '#ec4899', border: 'none', borderRadius: '10px', color: '#fff', fontWeight: 'bold', fontSize: '16px', cursor: 'pointer', marginTop: '10px' }}
              >
                🎲 幫我選餐廳
              </button>
              {aiRecommendation && (
                <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#0f172a', borderRadius: '10px', border: '1px solid #ec4899' }}>
                  <p style={{ margin: 0, color: '#ec4899', fontWeight: 'bold' }}>🎉 AI 為你推薦：{aiRecommendation}</p>
                </div>
              )}
            </div>
          )}

          {/* 3. 競賽與獎金 Tab */}
          {activeTab === 'rewards' && (
            <div style={{ backgroundColor: '#1e293b', borderRadius: '16px', padding: '20px', border: '1px solid #334155' }}>
              <h3 style={{ color: '#fff', fontSize: '16px', marginTop: 0 }}>🔒 內部同仁開發獎金專區</h3>
              {!isUnlocked ? (
                <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
                  <input
                    type="password"
                    placeholder="請輸入授權密碼 (8888)"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{ flex: 1, padding: '10px', borderRadius: '8px', border: '1px solid #475569', backgroundColor: '#0f172a', color: '#fff' }}
                  />
                  <button 
                    onClick={handleUnlock} 
                    style={{ padding: '10px 20px', backgroundColor: '#f59e0b', border: 'none', borderRadius: '8px', color: '#0f172a', fontWeight: 'bold', cursor: 'pointer' }}
                  >
                    解鎖
                  </button>
                </div>
              ) : (
                <div style={{ marginTop: '15px', backgroundColor: '#0f172a', padding: '15px', borderRadius: '12px', border: '1px solid #10b981' }}>
                  <p style={{ color: '#10b981', fontWeight: 'bold', margin: '0 0 10px' }}>解鎖成功！內部開發獎金明細：</p>
                  <ul style={{ color: '#cbd5e1', fontSize: '14px', paddingLeft: '20px', margin: 0, lineHeight: '1.8' }}>
                    <li>基礎推薦獎金：<strong style={{ color: '#fbbf24' }}>$200 / 店</strong></li>
                    <li>高人氣加碼獎金：<strong style={{ color: '#fbbf24' }}>$500 / 店</strong></li>
                    <li>月度開發王大獎：<strong style={{ color: '#fbbf24' }}>$3,000</strong></li>
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

components.html(html_code, height=900, scrolling=True)
