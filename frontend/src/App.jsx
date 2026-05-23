import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import InfoSidebar from './components/InfoSidebar';

function App() {
  const [selectedPlan, setSelectedPlan] = useState('Plan Base');

  return (
    <div className="app-container">
      <div className="chat-window-wrapper">
        <header className="header">
          <div className="header-left">
            <div className="bot-avatar-pulse">
              <img src="/sana.png" alt="Sana Logo" style={{ width: '120px', height: '120px', objectFit: 'contain', filter: 'drop-shadow(0 8px 24px rgba(124, 58, 237, 0.4))' }} />
            </div>

            <div>
              <h1>MediByte</h1>
              <p>Tu asistente médico personal Sana</p>
            </div>
          </div>
        </header>

        <ChatWindow selectedPlan={selectedPlan} setSelectedPlan={setSelectedPlan} />
      </div>

      <InfoSidebar selectedPlan={selectedPlan} />
    </div>
  );
}

export default App;
