import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = ({ signOut, username }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { path: '/main', label: 'Dashboard' },
    { path: '/repo-structure', label: 'Repository' },
    { path: '/code-editor', label: 'Code Editor' },
    { path: '/resources', label: 'Resources' },
    { path: '/community', label: 'Community' },
    { path: '/about', label: 'About' }
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className={`fixed top-0 z-40 w-full transition-all duration-300 ${isScrolled ? 'bg-gray-900 shadow-lg' : 'bg-transparent'}`}>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo and brand */}
          <div className="flex items-center">
            <Link to="/main" className="flex items-center">
              <div className="relative mr-2 h-8 w-8 overflow-hidden rounded-md bg-gradient-to-br from-blue-500 to-purple-600">
                <div className="absolute inset-0 flex items-center justify-center text-xs font-bold text-white">V</div>
              </div>
              <span className="text-lg font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">VIKSIT.AI</span>
            </Link>
          </div>

          {/* Desktop navigation links */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-4">
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`relative px-3 py-2 text-sm font-medium transition-colors ${
                    isActive(link.path)
                      ? 'text-white'
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  {link.label}
                  {isActive(link.path) && (
                    <span className="absolute bottom-0 left-0 h-0.5 w-full bg-gradient-to-r from-blue-500 to-purple-600 transform transition-transform"></span>
                  )}
                </Link>
              ))}
            </div>
          </div>

          {/* User profile and signout */}
          <div className="flex items-center">
            <div className="relative ml-3">
              <div className="flex items-center gap-3">
                
                {/* User menu */}
                <div className="flex items-center gap-2">
                  <div className="h-8 w-8 overflow-hidden rounded-full bg-gradient-to-r from-blue-500 to-purple-600">
                    <div className="flex h-full items-center justify-center text-sm font-medium text-white">
                      {username ? username.charAt(0).toUpperCase() : 'U'}
                    </div>
                  </div>
                  
                  <div className="hidden md:block">
                    <div className="text-sm font-medium text-white">{username}</div>
                    <button 
                      onClick={signOut}
                      className="text-xs text-gray-400 hover:text-gray-200"
                    >
                      Sign out
                    </button>
                  </div>
                </div>

                {/* Mobile menu button */}
                <div className="flex md:hidden">
                  <button
                    onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    className="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white"
                  >
                    <span className="sr-only">Open main menu</span>
                    {isMobileMenuOpen ? (
                      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    ) : (
                      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )}

  export default Navbar;