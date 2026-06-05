import { Link, useLocation } from 'react-router-dom';
import { Compass } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Compass className="w-8 h-8 text-white" />
            <span className="font-bold text-xl text-white">PathFinder</span>
          </Link>
          
          <div className="flex space-x-8 font-bold text-lg">
            {[{ path: '/', label: 'Home' }, { path: '/advisor', label: 'Advisor' }, { path: '/skill-gap', label: 'Skill Gap' },{ path: '/about', label: 'About' } ].map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`font-medium transition-colors duration-300 px-3 py-2 rounded-md ${
                  location.pathname === link.path
                    ? 'bg-white text-indigo-600 shadow-md'
                    : 'text-white hover:bg-yellow-300 hover:text-indigo-700'
                }`}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}
