
import { Compass } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Dynamic Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-900 via-purple-800 to-pink-900 animate-gradient-x">
        {/* Aurora Effect */}
        <div className="absolute inset-0 opacity-30">
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 animate-aurora"></div>
        </div>
        
        {/* Stars */}
        <div className="absolute inset-0">
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className="absolute rounded-full bg-white animate-stars"
              style={{
                width: Math.random() * 3 + 'px',
                height: Math.random() * 3 + 'px',
                top: Math.random() * 100 + '%',
                left: Math.random() * 100 + '%',
                animationDelay: Math.random() * 3 + 's'
              }}
            ></div>
          ))}
        </div>

        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-grid opacity-20"></div>
      </div>

      {/* Content */}
      <div className="relative min-h-screen flex flex-col items-center justify-center px-4 text-white text-center">
        <div className="animate-float">
          <div className="relative">
            <div className="absolute inset-0 blur-2xl bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 opacity-30 rounded-full"></div>
            <Compass className="w-24 h-24 mb-8 relative" />
          </div>
        </div>
        <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-fadeIn bg-clip-text text-transparent bg-gradient-to-r from-white to-indigo-200">
          Educational Pathfinder
        </h1>
        <p className="text-xl md:text-2xl mb-12 max-w-2xl animate-fadeIn delay-200 opacity-90 leading-relaxed">
          Discover your perfect educational journey with AI-powered recommendations tailored to your academic profile.
        </p>
        <div className="space-x-4 animate-fadeIn delay-300">
          <Link
            to="/advisor"
            className="bg-white/10 backdrop-blur-lg text-white px-8 py-3 rounded-full font-semibold hover:bg-white hover:text-indigo-600 transition-all duration-300 shadow-[0_0_15px_rgba(255,255,255,0.1)] hover:shadow-[0_0_25px_rgba(255,255,255,0.2)]"
          >
            Get Started
          </Link>
          <Link
            to="/about"
            className="bg-transparent border-2 border-white/30 text-white px-8 py-3 rounded-full font-semibold hover:bg-white/10 hover:border-white transition-all duration-300"
          >
            Learn More
          </Link>
        </div>
      </div>
    </div>
  );
}