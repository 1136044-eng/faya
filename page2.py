import streamlit as st
import streamlit.components.v1 as components

# 設定頁面滿版
st.set_page_config(layout="wide", page_title="Z-Gen 美食地圖")

html_code = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    body { background-color: #0b0f19; color: #fff; font-family: sans-serif; margin: 0; padding: 20px; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    const { useState } = React;

    function App() {
      const [isUnlocked, setIsUnlocked] = useState(false);
      const [password, setPassword] = useState('');

      const handleUnlock = () => {
        if (password === '8888') {
          setIsUnlocked(true);
        } else {
          alert('密碼錯誤！');
        }
      };

      return (
        <div>
          <h1 style={{ fontSize: '28px', margin: '10px 0 5px', color: '#fff' }}>Z-Gen 奢華美食地圖 🍷</h1>
          
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
        </div>
      );
    }

    ReactDOM.render(<App />, document.getElementById('root'));
  </script>
</body>
</html>
"""

components.html(html_code, height=800, scrolling=True)
