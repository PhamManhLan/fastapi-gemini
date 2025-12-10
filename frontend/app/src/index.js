import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';           // giữ lại nếu bạn có file index.css
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);