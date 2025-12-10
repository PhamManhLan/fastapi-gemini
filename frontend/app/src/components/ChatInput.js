export default function ChatInput({ value, onChange, onSubmit, disabled }) {
  return (
    <form onSubmit={onSubmit} className="fixed bottom-0 left-0 right-0 bg-white border-t p-4 shadow-lg">
      <div className="max-w-4xl mx-auto flex gap-3">
        <input
          type="text"
          value={value}
          onChange={onChange}
          placeholder="Hỏi gì về Huế nào..."
          className="flex-1 px-6 py-4 border rounded-full text-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={disabled}
        />
        <button
          type="submit"
          disabled={disabled || !value.trim()}
          className="px-8 py-4 bg-indigo-600 text-white rounded-full font-bold hover:bg-indigo-700 disabled:opacity-50 transition"
        >
          Gửi
        </button>
      </div>
    </form>
  );
}