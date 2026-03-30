import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();

  const menuItems = [
    { label: 'Polyatomic Ions', path: '/polyatomic' },
    { label: 'Settings', path: '/settings' },
    { label: 'Home', path: '/' },
  ];

  const handleMenuClick = (path: string) => {
    navigate(path);
    setIsMenuOpen(false);
  };

  return (
    <header className="w-full bg-bg-secondary border-b-2 border-text-secondary px-6 py-4 relative">
      <div className="flex justify-end items-center">
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="w-10 h-10 flex flex-col justify-center items-center gap-1.5 hover:opacity-70 transition-opacity"
          aria-label="Toggle menu"
        >
          <span className={`block w-6 h-0.5 bg-text-primary transition-transform ${isMenuOpen ? 'rotate-45 translate-y-2' : ''}`}></span>
          <span className={`block w-6 h-0.5 bg-text-primary transition-opacity ${isMenuOpen ? 'opacity-0' : ''}`}></span>
          <span className={`block w-6 h-0.5 bg-text-primary transition-transform ${isMenuOpen ? '-rotate-45 -translate-y-2' : ''}`}></span>
        </button>
      </div>

      {isMenuOpen && (
        <nav className="absolute top-full right-0 bg-bg-secondary border-l-2 border-b-2 border-text-secondary shadow-lg">
          <ul className="flex">
            {menuItems.map((item) => (
              <li key={item.path}>
                <button
                  onClick={() => handleMenuClick(item.path)}
                  className="px-6 py-4 text-text-primary hover:bg-highlight transition-colors whitespace-nowrap border-r-2 border-text-secondary last:border-r-0"
                >
                  {item.label}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </header>
  );
};
