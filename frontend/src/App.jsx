import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import InfoSidebar from './components/InfoSidebar';

function App() {
  const [selectedPlan, setSelectedPlan] = useState(null);

  return (
    <div className="app-container">
      <div className="chat-window-wrapper">
        <header className="header">
          <div className="header-left">
            <div className="bot-avatar-pulse">
              <img src="/frontend/public/sana.png" alt="MediByte Logo" style={{ width: '30px', height: '30px', objectFit: 'contain' }} />
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
