export default function LoadingDots() {
  return (
    <div className="flex justify-start mb-4">
      <div className="bg-gray-100 px-5 py-3 rounded-2xl rounded-tl-none shadow-sm">
        <span className="text-gray-600 italic">Đang suy nghĩ</span>
        <span className="dots">...</span>
      </div>
    </div>
  );
}