import React, { useState, useEffect, useRef } from 'react';
import { collection, addDoc, onSnapshot, query, orderBy, serverTimestamp } from 'firebase/firestore';
import { db } from '../../utils/firebase.js';

const CommunityPage = ({ userName }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [translationStates, setTranslationStates] = useState({});
  const [showLanguageDropdown, setShowLanguageDropdown] = useState({});
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);


  const SARVAM_API_KEY = import.meta.env.VITE_APP_SARVAM_API_KEY;

  
  const languages = [
    { code: 'hi-IN', name: 'Hindi', native: 'हिंदी' },
    { code: 'bn-IN', name: 'Bengali', native: 'বাংলা' },
    { code: 'gu-IN', name: 'Gujarati', native: 'ગુજરાતી' },
    { code: 'kn-IN', name: 'Kannada', native: 'ಕನ್ನಡ' },
    { code: 'ml-IN', name: 'Malayalam', native: 'മലയാളം' },
    { code: 'mr-IN', name: 'Marathi', native: 'मराठी' },
    { code: 'ne-IN', name: 'Nepali', native: 'नेपाली' },
    { code: 'or-IN', name: 'Odia', native: 'ଓଡ଼ିଆ' },
    { code: 'pa-IN', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
    { code: 'sa-IN', name: 'Sanskrit', native: 'संस्कृत' },
    { code: 'ta-IN', name: 'Tamil', native: 'தமிழ்' },
    { code: 'te-IN', name: 'Telugu', native: 'తెలుగు' },
    { code: 'ur-IN', name: 'Urdu', native: 'اردو' },
    { code: 'en-IN', name: 'English', native: 'English' }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const messagesRef = collection(db, 'communityMessages');
    const q = query(messagesRef, orderBy('timestamp', 'asc'));

    const unsubscribe = onSnapshot(q, (snapshot) => {
      const messagesList = [];
      snapshot.forEach((doc) => {
        messagesList.push({
          id: doc.id,
          ...doc.data()
        });
      });
      setMessages(messagesList);
      setLoading(false);
    }, (error) => {
      console.error('Error fetching messages:', error);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const translateMessage = async (messageId, text, targetLanguage) => {
    setTranslationStates(prev => ({
      ...prev,
      [messageId]: { ...prev[messageId], translating: true }
    }));

    try {
      const response = await fetch("https://api.sarvam.ai/translate", {
        method: "POST",
        headers: {
          "api-subscription-key": SARVAM_API_KEY,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "input": text,
          "source_language_code": "auto",
          "target_language_code": targetLanguage
        }),
      });

      const data = await response.json();

      if (response.ok && data.translated_text) {
        setTranslationStates(prev => ({
          ...prev,
          [messageId]: {
            ...prev[messageId],
            translating: false,
            translation: data.translated_text,
            targetLanguage: targetLanguage,
            sourceLanguage: data.source_language_code
          }
        }));
      } else {
        throw new Error(data.message || 'Translation failed');
      }
    } catch (error) {
      console.error('Translation error:', error);
      setTranslationStates(prev => ({
        ...prev,
        [messageId]: {
          ...prev[messageId],
          translating: false,
          error: 'Translation failed. Please try again.'
        }
      }));
    }

    setShowLanguageDropdown(prev => ({ ...prev, [messageId]: false }));
  };

  const toggleTranslation = (messageId) => {
    setTranslationStates(prev => ({
      ...prev,
      [messageId]: {
        ...prev[messageId],
        showTranslation: !prev[messageId]?.showTranslation
      }
    }));
  };

  const clearTranslation = (messageId) => {
    setTranslationStates(prev => {
      const newState = { ...prev };
      delete newState[messageId];
      return newState;
    });
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim() || sending) return;

    setSending(true);
    
    try {
      const messagesRef = collection(db, 'communityMessages');
      await addDoc(messagesRef, {
        text: newMessage.trim(),
        sender: userName,
        senderName: userName.split('@')[0], 
        timestamp: serverTimestamp(),
        createdAt: new Date().toISOString()
      });
      
      setNewMessage('');
      inputRef.current?.focus();
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Failed to send message. Please try again.');
    } finally {
      setSending(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    
    const date = timestamp.toDate ? timestamp.toDate() : new Date(timestamp);
    const now = new Date();
    const diffInMs = now - date;
    const diffInHours = diffInMs / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else {
      return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    }
  };

  const isOwnMessage = (message) => {
    return message.sender === userName;
  };

  const getLanguageName = (code) => {
    const lang = languages.find(l => l.code === code);
    return lang ? lang.native : code;
  };

  const currentUserName = userName.split('@')[0];

  return (
    <div className="pt-20 pb-4 px-4 sm:px-6 lg:px-8 h-screen flex flex-col bg-gray-900">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-100">Community Chat</h1>
        <p className="text-gray-400">Connect with other developers in the community</p>
      </div>

      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="h-3 w-3 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-sm text-gray-400">Community Chat</span>
        </div>
        <div className="text-sm text-gray-400">
          Welcome, <span className="text-blue-400 font-medium">{currentUserName}</span>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 bg-gray-800 rounded-xl overflow-hidden flex flex-col">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
          ) : messages.length === 0 ? (
            <div className="flex items-center justify-center h-full text-gray-400">
              <div className="text-center">
                <svg className="mx-auto h-12 w-12 text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
                <p>No messages yet. Start the conversation!</p>
              </div>
            </div>
          ) : (
            messages.map((message) => {
              const messageState = translationStates[message.id] || {};
              const showingTranslation = messageState.showTranslation && messageState.translation;
              
              return (
                <div
                  key={message.id}
                  className={`flex ${isOwnMessage(message) ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-xs lg:max-w-md ${isOwnMessage(message) ? 'order-1' : 'order-2'}`}>
                    <div
                      className={`px-4 py-2 rounded-2xl relative ${
                        isOwnMessage(message)
                          ? 'bg-blue-600 text-white rounded-br-md'
                          : 'bg-gray-700 text-gray-100 rounded-bl-md'
                      }`}
                    >
                      {!isOwnMessage(message) && (
                        <p className="text-xs font-medium text-blue-400 mb-1">
                          {message.senderName}
                        </p>
                      )}
                      
                      <div className="flex items-start justify-between">
                        <div className="flex-1 pr-2">
                          <p className="text-sm whitespace-pre-wrap break-words">
                            {showingTranslation ? messageState.translation : message.text}
                          </p>
                          
                          {/* Translation info */}
                          {showingTranslation && (
                            <div className="mt-1 text-xs opacity-75">
                              <span>Translated to {getLanguageName(messageState.targetLanguage)}</span>
                              <button
                                onClick={() => toggleTranslation(message.id)}
                                className="ml-2 underline hover:no-underline"
                              >
                                Show original
                              </button>
                            </div>
                          )}
                          
                          {messageState.translation && !showingTranslation && (
                            <div className="mt-1 text-xs opacity-75">
                              <button
                                onClick={() => toggleTranslation(message.id)}
                                className="underline hover:no-underline"
                              >
                                Show translation
                              </button>
                            </div>
                          )}
                          
                          {messageState.error && (
                            <div className="mt-1 text-xs text-red-400">
                              {messageState.error}
                            </div>
                          )}
                        </div>
                        
                        {/* Translation controls */}
                        <div className="relative flex items-center space-x-1">
                          {messageState.translating ? (
                            <div className="animate-spin rounded-full h-4 w-4 border-b border-current"></div>
                          ) : (
                            <>
                              <button
                                onClick={() => setShowLanguageDropdown(prev => ({
                                  ...prev,
                                  [message.id]: !prev[message.id]
                                }))}
                                className="p-1 rounded hover:bg-black hover:bg-opacity-20 transition-colors"
                                title="Translate message"
                              >
                                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path>
                                </svg>
                              </button>
                              
                              {messageState.translation && (
                                <button
                                  onClick={() => clearTranslation(message.id)}
                                  className="p-1 rounded hover:bg-black hover:bg-opacity-20 transition-colors"
                                  title="Clear translation"
                                >
                                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                                  </svg>
                                </button>
                              )}
                            </>
                          )}
                          
                          {/* Language dropdown */}
                          {showLanguageDropdown[message.id] && (
                            <div className={`absolute top-8 z-50 bg-gray-800 border border-gray-600 rounded-lg shadow-lg py-2 w-48 max-h-60 overflow-y-auto ${
                              isOwnMessage(message) ? 'right-0' : 'left-0'
                            }`}>
                              {languages.map((lang) => (
                                <button
                                  key={lang.code}
                                  onClick={() => translateMessage(message.id, message.text, lang.code)}
                                  className="w-full text-left px-3 py-2 text-sm text-gray-200 hover:bg-gray-700 transition-colors"
                                >
                                  <div className="flex justify-between items-center">
                                    <span>{lang.name}</span>
                                    <span className="text-gray-400 text-xs">{lang.native}</span>
                                  </div>
                                </button>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                      
                      <p className={`text-xs mt-1 ${
                        isOwnMessage(message) ? 'text-blue-200' : 'text-gray-400'
                      }`}>
                        {formatTime(message.timestamp)}
                      </p>
                    </div>
                  </div>
                  
                  {/* Avatar */}
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium ml-2 mr-2 ${
                    isOwnMessage(message) ? 'order-2 bg-blue-500 text-white' : 'order-1 bg-gray-600 text-gray-200'
                  }`}>
                    {(message.senderName || 'U').charAt(0).toUpperCase()}
                  </div>
                </div>
              );
            })
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Message Input */}
        <div className="border-t border-gray-700 p-4">
          <div className="flex items-end space-x-3">
            <div className="flex-1">
              <textarea
                ref={inputRef}
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type your message..."
                className="w-full px-4 py-3 bg-gray-700 text-gray-100 rounded-xl resize-none border-0 focus:ring-2 focus:ring-blue-500 focus:outline-none placeholder-gray-400"
                rows="1"
                style={{ minHeight: '48px', maxHeight: '120px' }}
                disabled={sending}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!newMessage.trim() || sending}
              className={`px-4 py-3 rounded-xl font-medium transition-all duration-200 ${
                newMessage.trim() && !sending
                  ? 'bg-blue-600 text-white hover:bg-blue-700 transform hover:scale-105'
                  : 'bg-gray-600 text-gray-400 cursor-not-allowed'
              }`}
            >
              {sending ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Click outside to close dropdowns */}
      {Object.values(showLanguageDropdown).some(Boolean) && (
        <div 
          className="fixed inset-0 z-40"
          onClick={() => setShowLanguageDropdown({})}
        />
      )}
    </div>
  );
};

export default CommunityPage;