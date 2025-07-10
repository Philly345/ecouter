import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './dashboard.css';
import {
  FaUser,
  FaMicrophoneAlt,
  FaFileAlt,
  FaFolderOpen,
  FaSignOutAlt,
  FaBars,
} from 'react-icons/fa';

const Sidebar = ({ isOpen, toggleSidebar }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigation = (path) => {
    navigate(path);
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const menuItems = [
    { path: '/profile', label: 'Profile', icon: <FaUser /> },
    { path: '/transcribe', label: 'Transcribe File', icon: <FaMicrophoneAlt /> },
    { path: '/history', label: 'Transcribed Files', icon: <FaFileAlt /> },
    { path: '/projects', label: 'Projects', icon: <FaFolderOpen /> }, // ✅ NEW PROJECTS LINK
  ];

  return (
    <div className={`sidebar ${isOpen ? '' : 'collapsed'}`}>
      <div className="toggle-btn" onClick={toggleSidebar}>
        <FaBars />
      </div>

      <ul>
        {menuItems.map(({ path, label, icon }) => (
          <li
            key={path}
            className={location.pathname === path ? 'active' : ''}
            onClick={() => handleNavigation(path)}
          >
            <span className="icon">{icon}</span>
            {isOpen && <span>{label}</span>}
          </li>
        ))}

        <li onClick={handleLogout}>
          <span className="icon">
            <FaSignOutAlt />
          </span>
          {isOpen && <span>Logout</span>}
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
