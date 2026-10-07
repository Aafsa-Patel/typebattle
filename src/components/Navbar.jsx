import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Moon, Sun, LogOut, Zap } from 'lucide-react';
import { getUser, logout } from '../services/api';
import './Navbar.css';

export default function Navbar({ darkMode, setDarkMode }) {
  const location = useLocation(); const navigate = useNavigate(); const user = getUser();
  const active = (p) => location.pathname === p ? 'active' : '';
  const leave = () => { logout(); navigate('/'); window.location.reload(); };
  return <nav className="navbar"><div className="navbar-container">
    <Link to="/" className="brand"><span className="brand-mark"><Zap size={17} fill="currentColor" /></span><span>TYPE<span>BATTLE</span></span></Link>
    <div className="nav-links">
      <Link to="/" className={active('/')}>Home</Link><Link to="/practice" className={active('/practice')}>Practice</Link><Link to="/battle" className={active('/battle')}>Battle</Link><Link to="/leaderboard" className={active('/leaderboard')}>Leaderboard</Link>
      {user && <Link to="/profile" className={active('/profile')}>Profile</Link>}
    </div>
    <div className="nav-actions"><button className="icon-btn" onClick={() => setDarkMode(v => !v)} title="Toggle theme">{darkMode ? <Sun size={18}/> : <Moon size={18}/>}</button>{user ? <button className="logout-btn" onClick={leave}><LogOut size={16}/> Logout</button> : <Link className="nav-login" to="/login">Login</Link>}</div>
  </div></nav>;
}
