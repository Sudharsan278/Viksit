import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import SubscriptionPlans from './SubscriptionPlans';
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';

const LandingPage = () => {
  const [showSubscription, setShowSubscription] = useState(false);
  const [currentLanguageIndex, setCurrentLanguageIndex] = useState(0);

  const languages = [
    "INDIA",      
    "भारत",       
    "ভাৰত",       
    "ଭାରତ",       
    "భారత్",      
    "ભારત",       
    "ಭಾರತ",       
    "भारत",       
    "ভারত",       
    "ਭਾਰਤ",       
    "தமிழ்நாடு", 
    "കേരളം",      
    "ଓଡ଼ିଶା"       
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentLanguageIndex((prevIndex) => (prevIndex + 1) % languages.length);
    }, 2000); 

    return () => clearInterval(interval);
  }, [languages.length]);

  const handleGoogleSignIn = async () => {
    try {
      const provider = new firebase.auth.GoogleAuthProvider();
      await firebase.auth().signInWithPopup(provider);
      navigate('/main');
    } catch (error) {
      console.error('Google sign in error:', error);
    }
  };

  const handleCloseSubscription = () => {
    setShowSubscription(false);
  };

  // Animation for floating code snippets
  const floatingCodeStyles = [
    "animate-bounce opacity-50 absolute font-mono text-xs md:text-sm text-blue-300 whitespace-pre rounded-lg bg-opacity-10 bg-blue-900 p-3",
    "animate-pulse opacity-50 absolute font-mono text-xs md:text-sm text-green-300 whitespace-pre rounded-lg bg-opacity-10 bg-green-900 p-3",
    "animate-bounce opacity-50 absolute font-mono text-xs md:text-sm text-purple-300 whitespace-pre rounded-lg bg-opacity-10 bg-purple-900 p-3",
    "animate-pulse opacity-50 absolute font-mono text-xs md:text-sm text-yellow-300 whitespace-pre rounded-lg bg-opacity-10 bg-yellow-900 p-3",
    "animate-bounce opacity-50 absolute font-mono text-xs md:text-sm text-red-300 whitespace-pre rounded-lg bg-opacity-10 bg-red-900 p-3",
    "animate-pulse opacity-50 absolute font-mono text-xs md:text-sm text-pink-300 whitespace-pre rounded-lg bg-opacity-10 bg-pink-900 p-3"
  ];

  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-b from-gray-900 via-gray-800 to-black px-4 py-16 text-white">
      {/* Animated background glow */}
      <div className="absolute -top-40 left-1/4 h-96 w-96 animate-pulse rounded-full bg-blue-500 opacity-10 blur-3xl"></div>
      <div className="absolute -bottom-20 right-1/4 h-64 w-64 animate-pulse rounded-full bg-purple-500 opacity-10 blur-3xl"></div>
      
      <header className="relative mx-auto mb-12 flex max-w-6xl items-center justify-between">
        <div className="relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 rounded-lg blur opacity-30 group-hover:opacity-50 animate-pulse"></div>
          <div className="relative text-xl font-bold tracking-tight">
            <span 
              className="bg-gradient-to-r from-blue-400 via-purple-500 to-cyan-400 bg-clip-text text-transparent font-black tracking-wider"
              style={{
                backgroundSize: '200% 200%',
                animation: 'gradient-x 3s ease infinite, shimmer 2s linear infinite',
                textShadow: '0 0 20px rgba(59, 130, 246, 0.5)',
                filter: 'drop-shadow(0 0 10px rgba(147, 51, 234, 0.3))'
              }}
            >
              VIKSIT.AI
            </span>
          </div>
        </div>
        <button 
          onClick={handleGoogleSignIn}
          className="hidden rounded-lg bg-gray-800 px-4 py-2 text-sm font-medium text-gray-200 transition-all hover:bg-gray-700 sm:block"
        >
          Sign In
        </button>
      </header>
      
      <div className="relative mx-auto max-w-4xl">
        <div className="mb-12 flex flex-col items-center text-center">
          <div className="relative mb-4">
            <div className="absolute -inset-2 bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 rounded-lg blur-lg opacity-20 animate-pulse"></div>
            <h1 className="relative text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl">
              <span 
                className="bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 bg-clip-text text-transparent font-black tracking-wider"
                style={{
                  backgroundSize: '200% 100%',
                  animation: 'shimmer 2s linear infinite, glow-pulse 3s ease-in-out infinite',
                  filter: 'drop-shadow(0 4px 20px rgba(59, 130, 246, 0.4))',
                  textShadow: '0 0 30px rgba(99, 102, 241, 0.6)'
                }}
              >
                VIKSIT.AI
              </span>
            </h1>
          </div>
          
          <p className="mb-6 text-lg font-medium">
            Built in <span className="inline-block min-w-[80px] text-center">
              <span 
                key={currentLanguageIndex}
                className="inline-block animate-pulse text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-500 font-semibold"
              >
                {languages[currentLanguageIndex]}
              </span>
            </span>, for the World!
          </p>
          
          <p className="mb-8 max-w-2xl text-xl text-gray-300">
            Your AI coding guru that explains code and generates documentation for your codebase.
          </p>
          
          <button 
            className="group relative overflow-hidden rounded-lg bg-gradient-to-br from-blue-600 to-purple-600 px-6 py-3 font-medium text-white shadow-lg transition-all hover:shadow-blue-500/30"
            onClick={() => setShowSubscription(true)}
          >
            <span className="relative z-10">Explore Plans</span>
            <span className="absolute inset-0 h-full w-full bg-gradient-to-br from-blue-700 to-purple-700 opacity-0 transition-opacity group-hover:opacity-100"></span>
          </button>
        </div>
        
        {/* Feature highlight */}
        <div className="grid gap-8 md:grid-cols-3">
          <div className="rounded-xl bg-gray-800 bg-opacity-50 p-6 backdrop-blur-sm transition-all duration-300 hover:bg-opacity-70">
            <div className="mb-4 rounded-full bg-blue-900 bg-opacity-50 p-3 inline-block">
              <svg className="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
              </svg>
            </div>
            <h3 className="mb-2 text-lg font-medium">Code Explanation</h3>
            <p className="text-sm text-gray-400">Get detailed explanations for any code snippet or repository structure.</p>
          </div>
          
          <div className="rounded-xl bg-gray-800 bg-opacity-50 p-6 backdrop-blur-sm transition-all duration-300 hover:bg-opacity-70">
            <div className="mb-4 rounded-full bg-purple-900 bg-opacity-50 p-3 inline-block">
              <svg className="h-6 w-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <h3 className="mb-2 text-lg font-medium">Documentation</h3>
            <p className="text-sm text-gray-400">Automatically generate professional documentation for your projects.</p>
          </div>
          
          <div className="rounded-xl bg-gray-800 bg-opacity-50 p-6 backdrop-blur-sm transition-all duration-300 hover:bg-opacity-70">
            <div className="mb-4 rounded-full bg-indigo-900 bg-opacity-50 p-3 inline-block">
              <svg className="h-6 w-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <h3 className="mb-2 text-lg font-medium">Community</h3>
            <p className="text-sm text-gray-400">Join our community of developers to share insights and best practices.</p>
          </div>
        </div>
      </div>
      
      {/* Floating code snippets */}
      <div className={`${floatingCodeStyles[0]} top-1/4 left-10`}>
        {`function analyze(code) {\n  return AI.explain(code);\n}`}
      </div>
      <div className={`${floatingCodeStyles[1]} top-1/3 right-10`}>
        {`import torch\nmodel = torch.load('nlp_model.pt')`}
      </div>
      <div className={`${floatingCodeStyles[2]} bottom-1/4 left-5`}>
        {`def process_repo(path):\n  files = scan_dir(path)\n  return analyze_all(files)`}
      </div>
      <div className={`${floatingCodeStyles[3]} top-1/2 right-5`}>
        {`class CodeParser {\n  constructor() {\n    this.ast = null;\n  }\n}`}
      </div>
      <div className={`${floatingCodeStyles[4]} bottom-1/7 right-12`}>
        {`SELECT repo_name, COUNT(*)\nFROM code_analysis\nGROUP BY repo_name;`}
      </div>
      <div className={`${floatingCodeStyles[5]} bottom-10 left-1/3`}>
        {`async function fetchDocs() {\n  const response = await api.get('/docs');\n}`}
      </div>

      {showSubscription && (
        <SubscriptionPlans 
          onGoogleSignIn={handleGoogleSignIn} 
          onClose={handleCloseSubscription}
        />
      )}
      
      <style jsx>{`
        @keyframes gradient-x {
          0%, 100% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
        }
        
        @keyframes shimmer {
          0% {
            background-position: -200% center;
          }
          100% {
            background-position: 200% center;
          }
        }
        
        @keyframes glow-pulse {
          0%, 100% {
            filter: drop-shadow(0 4px 20px rgba(59, 130, 246, 0.4)) brightness(1);
          }
          50% {
            filter: drop-shadow(0 8px 40px rgba(99, 102, 241, 0.8)) brightness(1.2);
          }
        }
        
        @keyframes tilt {
          0%, 50%, 100% {
            transform: rotate(0deg);
          }
          25% {
            transform: rotate(1deg);
          }
          75% {
            transform: rotate(-1deg);
          }
        }
      `}</style>
    </div>
  );
};

export default LandingPage;