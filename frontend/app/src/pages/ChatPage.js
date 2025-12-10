import { useState, useEffect, useRef } from 'react';
import ChatBubble from '../components/ChatBubble';
import LoadingDots from '../components/LoadingDots';
import ChatInput from '../components/ChatInput';
import { sendMessage } from '../api';

export default function ChatPage({ username, onLogout }) {
  const [messages, setMessages] = useState([
    { role: 'bot', content: 'Xin chào! Tôi là hướng dẫn viên du lịch Huế, rất sẵn lòng hỗ trợ bạn.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    const text = input;
    setInput('');
    setIsLoading(true);

    try {
      const res = await sendMessage(text);
      setMessages(prev => [...prev, { role: 'bot', content: res.data.reply }]);
    } catch {
      setMessages(prev => [...prev, { role: 'bot', content: 'Không kết nối được server' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 shadow-lg">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Hướng Dẫn Viên Du Lịch Huế</h1>
          <div className="flex items-center gap-4">
            <span>Xin chào, <strong>{username}</strong></span>
            <button
              onClick={onLogout}
              className="px-4 py-2 bg-white/20 rounded-lg hover:bg-white/30 transition"
            >
              Đăng xuất
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-4xl mx-auto w-full p-4 pb-32 overflow-y-auto">
        {messages.map((msg, i) => (
          <ChatBubble key={i} message={msg} />
        ))}
        {isLoading && <LoadingDots />}
        <div ref={messagesEndRef} />
      </main>

      <ChatInput
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onSubmit={handleSend}
        disabled={isLoading}
      />
    </div>
  );
}