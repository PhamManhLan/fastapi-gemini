export default function ChatBubble({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`
        max-w-[80%] px-5 py-3 rounded-2xl shadow-sm text-sm md:text-base
        ${isUser 
          ? 'bg-blue-600 text-white rounded-tr-none' 
          : 'bg-gray-100 text-gray-800 rounded-tl-none'
        }
      `}>
        <p className="whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  );
}