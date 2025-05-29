import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import LandingPage from './components/LandingPage';
import Navbar from './components/Navbar';
import MainPage from './components/MainPage';
import RepoStructurePage from './components/RepoStructurePage';
import RepoAnalysis from './components/RepoAnalysis';
import ResourcesPage from './components/ResourcesPage';
import CodeEditor from './components/CodeEditor';
import CommunityPage from './components/CommunityPage';
import AboutPage from './components/AboutPage';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_APP_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_APP_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_APP_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_APP_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_APP_FIREBASE_MEASUREMENT_ID
};


if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

const App = () => {
  const [authenticated, setAuthenticated] = useState(false);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = firebase.auth().onAuthStateChanged((user) => {
      if (user) {
        setAuthenticated(true);
        setEmail(user.email);
        setUsername(user.displayName || user.email);
      } else {
        setAuthenticated(false);
        setEmail('');
        setUsername('');
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const signOut = async () => {
    try {
      await firebase.auth().signOut();
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-900">
        <div className="flex flex-col items-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-t-blue-500 border-r-transparent border-b-blue-500 border-l-transparent"></div>
          <p className="mt-4 text-xl font-medium text-gray-200">Loading VIKSIT.AI...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="flex min-h-screen flex-col bg-gray-900 text-gray-100">
        {authenticated && <Navbar signOut={signOut} username={username} />}
        <div className="flex-grow">
          <Routes>
            <Route path="/" element={authenticated ? <Navigate to="/main" /> : <LandingPage />} />
            <Route path="/main" element={authenticated ? <MainPage username={username} /> : <Navigate to="/" />} />
            <Route path="/repo-structure" element={authenticated ? <RepoStructurePage /> : <Navigate to="/" />} />
            <Route path="/repo-analysis" element={<RepoAnalysis />} />
            <Route path="/code-editor" element={authenticated ? <CodeEditor /> : <Navigate to="/" />} />
            <Route path="/resources" element={authenticated ? <ResourcesPage /> : <Navigate to="/" />} />
            <Route path="/community" element={authenticated ? <CommunityPage userName={username}/> : <Navigate to="/" />} />
            <Route path="/about" element={authenticated ? <AboutPage /> : <Navigate to="/" />} /> 
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;