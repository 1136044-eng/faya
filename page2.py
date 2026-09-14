import React, { useState } from 'react';

// 模擬精緻美食餐廳資料庫
const RESTAURANTS = [
  { id: 1, name: "極光 AURA 私廚酒吧", category: "氛圍餐酒", price: 1800, rating: 4.9, tags: ["約會首選", "調酒強", "極致精緻"], mapUrl: "https://maps.google.com", igUrl: "https://instagram.com", image: "🍸" },
  { id: 2, name: "赤焰川味麻辣火鍋", category: "重口解壓", price: 650, rating: 4.8, tags: ["麻辣燙", "深夜食堂", "爽快解壓"], mapUrl: "https://maps.google.com", igUrl: "https://instagram.com", image: "🔥" },
  { id: 3, name: "雲端陽明山夜景餐廳", category: "浪漫夜景", price: 1200, rating: 4.7, tags: ["陽明山夜景", "約會首選", "飯店餐廳"], mapUrl: "https://maps.google.com", igUrl: "https://instagram.com", image: "🌙" },
  { id: 4, name: "黑金和牛炭火燒肉", category: "頂級和牛", price: 2500, rating: 4.9, tags: ["頂級私廚", "精緻高質感", "極致精緻"], mapUrl: "https://maps.google.com", igUrl: "https://instagram.com", image: "🥩" },
];

export default function ZGenFoodMap() {
  const [activeTab, setActiveTab] = useState('explore');
  const [selectedTag, setSelectedTag] = useState('ALL');
  const [aiMood, setAiMood] = useState('');
  const [aiRecommendation, setAiRecommendation] = useState(null);
  const [password, setPassword] = useState('');
  const [isUnlocked, setIsUnlocked] = useState(false);

  const allTags = ['ALL', '約會首選', '麻辣燙', '深夜食堂', '陽明山夜景', '頂級私廚'];

  const filteredRestaurants = selectedTag === 'ALL' 
    ? RESTAURANTS 
    : RESTAURANTS.filter(r => r.tags.includes(selectedTag));

  const handleAiGenerate = () => {
    if (!aiMood) return;
    const randomChoice = RESTAURANTS[Math.floor(Math.random() * RESTAURANTS.length)];
    setAiRecommendation(randomChoice);
  };

  const handleUnlock = () => {
    if (password === '8888') {
      setIsUnlocked(true);
    } else {
      alert('🔒 密碼錯誤！請輸入 8888');
    }
  };

  return (
    <div style={{ backgroundColor: '#0f172a', color: '#f8fafc', minHeight: '100vh', fontFamily: 'sans-serif', padding: '20px' }}>
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
          { id: 'explore', label: '🗄️ 分類探索' },
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
        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
          <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '15px' }}>
            {allTags.map(tag => (
              <button
                key={tag}
                onClick={() => setSelectedTag(tag)}
                style={{
                  padding: '6px 14px',
                  borderRadius: '20px',
                  border: '1px solid #334155',
                  backgroundColor: selectedTag === tag ? '#3b82f6' : '#1e293b',
                  color: '#fff',
                  fontSize: '13px'
                }}
              >
                #{tag}
              </button>
            ))}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            {filteredRestaurants.map(spot => (
              <div key={spot.id} style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '16px', padding: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <h3 style={{ margin: 0, color: '#fbbf24', fontSize: '18px' }}>{spot.image} {spot.name}</h3>
                  <span style={{ color: '#f59e0b', fontWeight: 'bold' }}>★ {spot.rating}</span>
                </div>
                <p style={{ color: '#94a3b8', fontSize: '14px', margin: '8px 0' }}>💰 人均消費：${spot.price}</p>
                <div style={{ display: 'flex', gap: '6px', marginBottom: '12px' }}>
                  {spot.tags.map(t => (
                    <span key={t} style={{ backgroundColor: '#0f172a', color: '#38bdf8', fontSize: '11px', padding: '2px 8px', borderRadius: '6px' }}>#{t}</span>
                  ))}
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <a href={spot.mapUrl} target="_blank" rel="noreferrer" style={{ flex: 1, textAlign: 'center', backgroundColor: '#334155', color: '#fff', padding: '8px', borderRadius: '8px', textDecoration: 'none', fontSize: '13px' }}>📍 Google 地圖</a>
                  <a href={spot.igUrl} target="_blank" rel="noreferrer" style={{ flex: 1, textAlign: 'center', backgroundColor: '#e1306c', color: '#fff', padding: '8px', borderRadius: '8px', textDecoration: 'none', fontSize: '13px' }}>📸 IG 貼文</a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 2. AI 今日靈感 Tab */}
      {activeTab === 'ai' && (
        <div style={{ maxWidth: '500px', margin: '0 auto', textAlign: 'center', backgroundColor: '#1e293b', padding: '25px', borderRadius: '20px', border: '1px solid #334155' }}>
          <h2 style={{ color: '#f59e0b', fontSize: '20px', marginBottom: '10px' }}>🔮 AI 今日美食氛圍指南</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', textAlign: 'left', marginBottom: '20px' }}>
            {['✨ 想要精緻高質感', '🔥 爽快解壓/重口味', '☕ 浪漫約會/放鬆氛圍'].map(mood => (
              <label key={mood} style={{ padding: '12px', backgroundColor: aiMood === mood ? '#334155' : '#0f172a', borderRadius: '10px', border: '1px solid #475569', cursor: 'pointer', display: 'flex', gap: '10px' }}>
                <input type="radio" name="mood" value={mood} onChange={() => setAiMood(mood)} checked={aiMood === mood} />
                <span style={{ color: '#fff', fontSize: '14px' }}>{mood}</span>
              </label>
            ))}
          </div>
          <button onClick={handleAiGenerate} style={{ width: '100%', padding: '12px', borderRadius: '12px', border: 'none', background: 'linear-gradient(90deg, #f59e0b, #d97706)', color: '#0f172a', fontWeight: 'bold', fontSize: '16px', cursor: 'pointer' }}>
            ✨ 生成今日特選美食
          </button>
          {aiRecommendation && (
            <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#0f172a', borderRadius: '12px', border: '1px solid #f59e0b' }}>
              <h3 style={{ color: '#fbbf24', margin: '0 0 5px' }}>🎉 AI 推薦：{aiRecommendation.name}</h3>
              <p style={{ color: '#cbd5e1', fontSize: '13px' }}>💰 預估消費：${aiRecommendation.price} | ⭐ 評分：{aiRecommendation.rating}</p>
            </div>
          )}
        </div>
      )}

      {/* 3. 競賽與獎金 Tab */}
      {activeTab === 'rewards' && (
        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
          <div style={{ backgroundColor: '#1e293b', borderRadius: '16px', padding: '20px', border: '1px solid #334155', marginBottom: '20px' }}>
            <h2 style={{ color: '#fbbf24', fontSize: '18px', marginTop: 0 }}>👑 店家皇冠連勝激勵方案</h2>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px', textAlign: 'center' }}>
              <div style={{ backgroundColor: '#0f172a', padding: '12px', borderRadius: '10px' }}>
                <div style={{ fontSize: '12px', color: '#94a3b8' }}>連勝 2 個月</div>
                <div style={{ color: '#f59e0b', fontWeight: 'bold', fontSize: '16px' }}>+2% 獎金</div>
              </div>
              <div style={{ backgroundColor: '#0f172a', padding: '12px', borderRadius: '10px' }}>
                <div style={{ fontSize: '12px', color: '#94a3b8' }}>連勝 6 個月</div>
                <div style={{ color: '#f59e0b', fontWeight: 'bold', fontSize: '16px' }}>+6% 獎金</div>
              </div>
              <div style={{ backgroundColor: '#0f172a', padding: '12px', borderRadius: '10px' }}>
                <div style={{ fontSize: '12px', color: '#94a3b8' }}>滿 12 個月</div>
                <div style={{ color: '#10b981', fontWeight: 'bold', fontSize: '16px' }}>+12% 獎金</div>
              </div>
            </div>
          </div>

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
                <button onClick={handleUnlock} style={{ padding: '10px 20px', backgroundColor: '#f59e0b', border: 'none', borderRadius: '8px', color: '#0f172a', fontWeight: 'bold', cursor: 'pointer' }}>解鎖</button>
              </div>
            ) : (
              <div style={{ marginTop: '15px', backgroundColor: '#0f172a', padding: '15px', borderRadius: '12px', border: '1px solid #10b981' }}>
                <p style={{ color: '#10b981', fontWeight: 'bold', margin: '0 0 10px' }}>🔓 驗證成功！內部開發獎金明細：</p>
                <ul style={{ color: '#cbd5e1', fontSize: '14px', paddingLeft: '20px', margin: 0, lineHeight: '1.8' }}>
                  <li>基礎推薦獎金：<strong style={{ color: '#fbbf24' }}>$200 / 店</strong></li>
                  <li>高人氣加碼獎金：<strong style={{ color: '#fbbf24' }}>$500 / 店</strong></li>
                  <li>月度開發王大獎：<strong style={{ color: '#fbbf24' }}>$3,000</strong></li>
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
