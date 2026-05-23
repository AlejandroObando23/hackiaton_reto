import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Mic, Square, Volume2 } from 'lucide-react';

const API_BASE = '/sana-bot';
const SESSION_ID = 'demo-session';
const USER_ID = 'demo-user';

const ChatWindow = ({ selectedPlan, setSelectedPlan }) => {
  const [messages, setMessages] = useState([
    { type: 'bot', content: 'Hola, soy Sana, tu agente de MediByte. ¿Qué síntomas tienes hoy o en qué te puedo ayudar?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const playAudio = async (text) => {
    try {
      const response = await axios.post(`${API_BASE}/tts`, { text }, { responseType: 'blob' });
      const audioUrl = URL.createObjectURL(response.data);
      const audio = new Audio(audioUrl);
      audio.play();
    } catch (error) {
      console.error('Error playing TTS:', error);
    }
  };

  const handleSend = async (textOverride) => {
    const text = textOverride || input;
    if (!text.trim()) return;

    setMessages(prev => [...prev, { type: 'user', content: text }]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/chat/${SESSION_ID}`, {
        message: text,
        user_id: USER_ID,
        insurance_plan: selectedPlan
      });
      const botResponse = res.data.bot_response;
      setMessages(prev => [...prev, { type: 'bot', content: botResponse }]);
      playAudio(botResponse);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { type: 'bot', content: 'Lo siento, hubo un error de conexión.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('file', audioBlob, 'audio.wav');
        
        setIsLoading(true);
        try {
          const res = await axios.post(`${API_BASE}/stt`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          const transcribedText = res.data.text;
          if (transcribedText) {
            handleSend(transcribedText);
          }
        } catch (error) {
          console.error('STT error:', error);
        } finally {
          setIsLoading(false);
        }
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  return (
    <>
      <div className="chat-header">
        <div className="plan-selector">
          <label>Tu Seguro Activo</label>
          <div className="plan-tabs">
            <button 
              className={`plan-tab ${selectedPlan === 'Plan Base' ? 'active' : ''}`}
              onClick={() => setSelectedPlan('Plan Base')}
            >
              Plan Base
            </button>
            <button 
              className={`plan-tab ${selectedPlan === 'Plan Premium' ? 'active' : ''}`}
              onClick={() => setSelectedPlan('Plan Premium')}
            >
              Plan Premium
            </button>
            <button 
              className={`plan-tab ${selectedPlan === 'Plan Platino' ? 'active' : ''}`}
              onClick={() => setSelectedPlan('Plan Platino')}
            >
              Plan Platino
            </button>
          </div>
        </div>
      </div>

      <div className="chat-container" ref={chatRef}>
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            <div className="message-content">{msg.content}</div>
            {msg.type === 'bot' && (
              <button 
                className="play-audio-btn" 
                onClick={() => playAudio(msg.content)}
                title="Escuchar mensaje"
              >
                <Volume2 size={16} />
              </button>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <div className="typing-indicator">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        )}
      </div>

      <div className="input-container">
        <input
          type="text"
          className="text-input"
          placeholder="Escribe tus síntomas aquí..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          disabled={isLoading || isRecording}
        />
        
        <button 
          className={`icon-btn ${isRecording ? 'recording' : ''}`}
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isLoading}
          title={isRecording ? "Detener grabación" : "Hablar por micrófono"}
        >
          {isRecording ? <Square size={20} /> : <Mic size={20} />}
        </button>

        <button 
          className="icon-btn" 
          onClick={() => handleSend()}
          disabled={!input.trim() || isLoading || isRecording}
          title="Enviar mensaje"
        >
          <Send size={20} />
        </button>
      </div>
    </>
  );
};

export default ChatWindow;
