import { Link, useLocation } from 'react-router-dom';

export const Header = () => {
  const location = useLocation();

  const navItems = [
    { label: 'Practice', path: '/' },
    { label: 'Polyatomic Ions', path: '/polyatomic' },
    { label: 'Curriculum', path: '/table-of-contents' },
    { label: 'Settings', path: '/settings' },
  ];

  return (
    <header className="w-full bg-slate-900 border-b border-slate-800 px-6 py-3 sticky top-0 z-30">
      <div className="max-w-6xl w-full mx-auto flex items-center justify-between">
        <Link to="/" className="flex items-center gap-1.5 font-bold tracking-tight text-slate-100 hover:text-cyan-400 transition-colors text-base">
          <span className="text-cyan-400">CHEM</span>GEN
        </Link>
        <nav className="flex items-center gap-1 sm:gap-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`px-3 py-1.5 text-sm transition-colors ${
                  isActive
                    ? 'bg-slate-800 text-cyan-400 font-medium'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
};
