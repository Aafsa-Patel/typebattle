import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Practice from './pages/Practice';
import Battle from './pages/Battle';
import Leaderboard from './pages/Leaderboard';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Register from './pages/Register';
import './App.css';

function Shell({ darkMode, setDarkMode }) {
  const location = useLocation();
  const authPage = location.pathname === '/login' || location.pathname === '/register';
  return <div className="app-shell">
    {!authPage && <Navbar darkMode={darkMode} setDarkMode={setDarkMode} />}
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/practice" element={<Practice />} />
      <Route path="/battle" element={<Battle />} />
      <Route path="/leaderboard" element={<Leaderboard />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  </div>;
}

export default function App() {
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('typebattle-theme') !== 'light');
  useEffect(() => {
    document.body.classList.toggle('dark-mode', darkMode);
    document.body.classList.toggle('light-mode', !darkMode);
    localStorage.setItem('typebattle-theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);
  return <BrowserRouter><Shell darkMode={darkMode} setDarkMode={setDarkMode} /></BrowserRouter>;
}
