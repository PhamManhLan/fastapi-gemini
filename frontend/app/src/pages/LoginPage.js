import { useState } from 'react';
import { login, register } from '../api';

export default function LoginPage({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!username.trim() || !password.trim()) {
      setError('Vui lòng nhập đầy đủ thông tin');
      return;
    }

    try {
      if (!isLogin) {
        await register(username, password);
      }

      const res = await login(username, password);
      localStorage.setItem('token', res.data.access_token);
      onLoginSuccess(username);

    } catch (err) {
      setError(err.response?.data?.detail || 'Sai tài khoản hoặc mật khẩu');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl shadow-2xl p-10 w-full max-w-md">
        <h1 className="text-4xl font-bold text-center mb-8 text-indigo-700">
          Huế Chat
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            type="text"
            placeholder="Tên tài khoản (vd: hue123)"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full px-5 py-4 border rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-lg"
            autoFocus
          />

          <input
            type="password"
            placeholder="Mật khẩu"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-5 py-4 border rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 text-lg"
          />

          {error && <p className="text-red-500 text-center font-medium">{error}</p>}

          <button
            type="submit"
            className="w-full py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition"
          >
            {isLogin ? 'Đăng nhập' : 'Đăng ký'}
          </button>
        </form>

        <p className="text-center mt-6 text-gray-600">
          {isLogin ? 'Chưa có tài khoản? ' : 'Đã có tài khoản? '}
          <button
            type="button"
            onClick={() => {
              setIsLogin(!isLogin);
              setError('');
            }}
            className="text-indigo-600 font-bold hover:underline"
          >
            {isLogin ? 'Đăng ký ngay' : 'Đăng nhập'}
          </button>
        </p>

        <p className="text-center text-xs text-gray-500 mt-6">
          Test nhanh: <strong>admin</strong> / <strong>123456</strong>
        </p>
      </div>
    </div>
  );
}