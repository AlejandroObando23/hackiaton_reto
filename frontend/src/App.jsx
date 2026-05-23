import React from 'react';
import ChatWindow from './components/ChatWindow';

function App() {
  return (
    <div className="app-container">
      <header className="header">
        <div style={{
          width: '40px', height: '40px', borderRadius: '50%', background: 'rgba(255,255,255,0.2)',
          display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}>
          ✨
        </div>
        <div>
          <h1>MediByte</h1>
          <p>Tu asistente médico personal Sana</p>
        </div>
      </header>
      <ChatWindow />
    </div>
  );
}

export default App;
