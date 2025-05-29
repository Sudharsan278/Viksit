import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const RepoAnalysis = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  
  const [username, setUsername] = useState(queryParams.get('username') || '');
  const [repoName, setRepoName] = useState(queryParams.get('repo_name') || '');
  const [repoInfo, setRepoInfo] = useState(null);
  
  const [documentation, setDocumentation] = useState('');
  const [isGeneratingDocs, setIsGeneratingDocs] = useState(false);
  const [docsError, setDocsError] = useState(null);
  
  const [selectedLanguage, setSelectedLanguage] = useState('en-IN');
  const [translatedDocumentation, setTranslatedDocumentation] = useState('');
  const [isTranslating, setIsTranslating] = useState(false);
  const [translationError, setTranslationError] = useState(null);
  const [isPlayingTTS, setIsPlayingTTS] = useState(false);
  const [isPausedTTS, setIsPausedTTS] = useState(false);
  const [ttsError, setTtsError] = useState(null);
  const audioRef = useRef(null);
  
  const [queryType, setQueryType] = useState('repository'); 
  const [queryText, setQueryText] = useState('');
  const [queryResponse, setQueryResponse] = useState('');
  const [isQuerying, setIsQuerying] = useState(false);
  const [queryError, setQueryError] = useState(null);
  
  const [selectedFilePath, setSelectedFilePath] = useState('');
  const [fileContent, setFileContent] = useState('');
  const [isLoadingFile, setIsLoadingFile] = useState(false);
  const [fileError, setFileError] = useState(null);
  
  const [repoStructure, setRepoStructure] = useState([]);
  const [isLoadingStructure, setIsLoadingStructure] = useState(false);
  const [structureError, setStructureError] = useState(null);
  
  const API_BASE_URL = 'https://viksit.onrender.com/api';
  const SARVAM_API_KEY = import.meta.env.VITE_APP_SARVAM_API_KEY;
  
  const languages = [
    { code: 'en-IN', name: 'English', flag: '🇺🇸', speaker: 'anushka' },
    { code: 'hi-IN', name: 'Hindi', flag: '🇮🇳', speaker: 'anushka' },
    { code: 'bn-IN', name: 'Bengali', flag: '🇧🇩', speaker: 'anushka' },
    { code: 'ta-IN', name: 'Tamil', flag: '🇮🇳', speaker: 'anushka' },
    { code: 'te-IN', name: 'Telugu', flag: '🇮🇳', speaker: 'anushka' },
    { code: 'ml-IN', name: 'Malayalam', flag: '🇮🇳', speaker: 'anushka' },
    { code: 'kn-IN', name: 'Kannada', flag: '🇮🇳', speaker: 'anushka' },
    { code: 'gu-IN', name: 'Gujarati', flag: '🇮🇳', speaker: 'anushka' },
    { code: 'pa-IN', name: 'Punjabi', flag: '🇮🇳', speaker: 'anushka' },
    { code: 'or-IN', name: 'Odia', flag: '🇮🇳', speaker: 'anushka' }
  ];
  
  const stripMarkdown = (text) => {
    if (!text) return '';
    
    return text
        // Remove headers (# ## ### etc.)
        .replace(/^#{1,6}\s+/gm, '')
        // Remove bold/italic (**text** *text* __text__ _text_)
        .replace(/(\*\*|__)(.*?)\1/g, '$2')
        .replace(/(\*|_)(.*?)\1/g, '$2')
        // Remove inline code (`code`)
        .replace(/`([^`]+)`/g, '$1')
        // Remove code blocks (```code```)
        .replace(/```[\s\S]*?```/g, '')
        // Remove links [text](url)
        .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1')
        // Remove images ![alt](url)
        .replace(/!\[([^\]]*)\]\([^\)]+\)/g, '$1')
        // Remove horizontal rules (--- or ***)
        .replace(/^(-{3,}|\*{3,})$/gm, '')
        // Remove blockquotes (> text)
        .replace(/^>\s+/gm, '')
        // Remove list markers (- * + and numbers)
        .replace(/^[\s]*[-\*\+]\s+/gm, '• ')
        .replace(/^[\s]*\d+\.\s+/gm, '')
        // Remove strikethrough (~~text~~)
        .replace(/~~(.*?)~~/g, '$1')
        // Remove = and ?
        .replace(/[=?]/g, '')
        // Clean up extra whitespace
        .replace(/\n{3,}/g, '\n\n')
        .trim();
  };
  
  useEffect(() => {
    if (username && repoName) {
      fetchRepoInfo();
      fetchRepoStructure();
    }
  }, [username, repoName]);
  
  useEffect(() => {
    setTranslatedDocumentation('');
    setSelectedLanguage('en-IN');
  }, [documentation]);
  
  const fetchRepoInfo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/repo-info/${username}/${repoName}/`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch repository info: ${response.status}`);
      }
      
      const data = await response.json();
      setRepoInfo(data);
    } catch (err) {
      console.error('Error fetching repository info:', err.message);
    }
  };
  
  const fetchRepoStructure = async () => {
    setIsLoadingStructure(true);
    setStructureError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/repo-structure/${username}/${repoName}/`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch repository structure: ${response.status}`);
      }
      
      const data = await response.json();
      setRepoStructure(data.structure || []);
    } catch (err) {
      setStructureError(`Error fetching repository structure: ${err.message}`);
    } finally {
      setIsLoadingStructure(false);
    }
  };
  
  const fetchDirectoryContents = async (path) => {
    try {
      const response = await fetch(`${API_BASE_URL}/repo-structure/${username}/${repoName}/?path=${encodeURIComponent(path)}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch directory contents: ${response.status}`);
      }
      
      const data = await response.json();
      return data.structure || [];
    } catch (err) {
      console.error(`Error fetching directory contents for ${path}:`, err.message);
      return [];
    }
  };
  
 
  const fetchFileContent = async (fileUrl) => {
    setIsLoadingFile(true);
    setFileError(null);
    
    try {
      const response = await fetch(fileUrl);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch file content: ${response.status}`);
      }
      
      const content = await response.text();
      setFileContent(content);
    } catch (err) {
      setFileError(`Error fetching file content: ${err.message}`);
      setFileContent('');
    } finally {
      setIsLoadingFile(false);
    }
  };
  
  const generateDocumentation = async () => {
    if (!username || !repoName) return;
    
    setIsGeneratingDocs(true);
    setDocsError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/generate-documentation/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          repo_name: repoName,
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Failed to generate documentation: ${response.status}`);
      }
      
      const data = await response.json();
      
      setDocumentation(stripMarkdown(data.documentation));
    } catch (err) {
      setDocsError(`Error generating documentation: ${err.message}`);
    } finally {
      setIsGeneratingDocs(false);
    }
  };
  
  const translateDocumentation = async (targetLanguage) => {
    if (!documentation || targetLanguage === 'en-IN') {
      setTranslatedDocumentation('');
      return;
    }
    
    setIsTranslating(true);
    setTranslationError(null);
    
    try {
      const response = await fetch('https://api.sarvam.ai/translate', {
        method: 'POST',
        headers: {
          'api-subscription-key': SARVAM_API_KEY,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input: documentation.slice(0,900),
          source_language_code: 'en-IN',
          target_language_code: targetLanguage,
          speaker_gender: 'Female',
          mode: 'formal',
          model: 'mayura:v1',
          enable_preprocessing: true
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Translation failed: ${response.status}`);
      }
      
      const data = await response.json();
      setTranslatedDocumentation(data.translated_text);
    } catch (err) {
      setTranslationError(`Translation error: ${err.message}`);
      setTranslatedDocumentation('');
    } finally {
      setIsTranslating(false);
    }
  };
  
  const convertToSpeech = async (text, languageCode) => {

    if (!text) return;
    
    setIsPlayingTTS(true);
    setIsPausedTTS(false);
    setTtsError(null);
    
    try {
      const selectedLang = languages.find(lang => lang.code === languageCode);
      const speaker = selectedLang ? selectedLang.speaker : 'meera';
      
      const maxLength = 900;
      let textToConvert = text.length > maxLength ? text.substring(0, maxLength) + '...' : text;


      let originalText = textToConvert.trim();
      let lowerNoSpace = originalText.replace(/\s+/g, '').toLowerCase();

      let cleanedText = originalText;

      if (lowerNoSpace.startsWith("samplepythonprograms")) {
        const index = cleanedText.toLowerCase().indexOf("sample python programs");
        if (index !== -1) {
          cleanedText = cleanedText.slice(index + "sample python programs".length).trim();
        }
      }

      lowerNoSpace = cleanedText.replace(/\s+/g, '').toLowerCase();

      if (lowerNoSpace.startsWith("overview")) {
        const index = cleanedText.toLowerCase().indexOf("overview");
        if (index !== -1) {
          cleanedText = cleanedText.slice(index + "overview".length).trim();
        }
      }

      textToConvert = cleanedText.length > maxLength
        ? cleanedText.substring(0, maxLength) + '...'
        : cleanedText;

      console.log(languageCode)
      console.log(textToConvert)
      
      const response = await fetch('https://api.sarvam.ai/text-to-speech', {
        method: 'POST',
        headers: {
          'api-subscription-key': SARVAM_API_KEY,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: textToConvert,
          target_language_code: languageCode,
          speaker: speaker
        }),
      });
      
      if (!response.ok) {
        throw new Error(`TTS failed: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.audios && data.audios.length > 0) {
  
        const audioBase64 = data.audios[0];
        const binaryString = atob(audioBase64);
        const bytes = new Uint8Array(binaryString.length);
        
        for (let i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }
        
        const audioBlob = new Blob([bytes], { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        
        if (audioRef.current) {
          audioRef.current.src = audioUrl;
          audioRef.current.play();
        }
      }
    } catch (err) {
      setTtsError(`TTS error: ${err.message}`);
      setIsPlayingTTS(false);
    }
  };
  
  const toggleAudioPlayback = () => {
    if (audioRef.current) {
      if (isPausedTTS) {
        audioRef.current.play();
        setIsPausedTTS(false);
      } else {
        audioRef.current.pause();
        setIsPausedTTS(true);
      }
    }
  };
  
  const stopAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlayingTTS(false);
      setIsPausedTTS(false);
    }
  };
  
  const handleAudioEnded = () => {
    setIsPlayingTTS(false);
    setIsPausedTTS(false);
  };
  
  const handleLanguageChange = (languageCode) => {
    setSelectedLanguage(languageCode);
    translateDocumentation(languageCode);
  };
  
  const submitQuery = async (e) => {
    e.preventDefault();
    
    if (!queryText) return;
    
    setIsQuerying(true);
    setQueryError(null);
    
    try {
      let endpoint = '';
      let requestBody = {};
      
      if (queryType === 'repository') {
        endpoint = `${API_BASE_URL}/query-repository/`;
        requestBody = {
          username,
          repo_name: repoName,
          query: queryText,
        };
      } else if (queryType === 'code') {
        endpoint = `${API_BASE_URL}/query-code/`;
        requestBody = {
          query: queryText,
          file_content: fileContent,
        };
        
        if (!fileContent) {
          throw new Error('Please select a file first');
        }
      }
      
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });
      
      if (!response.ok) {
        throw new Error(`Failed to process query: ${response.status}`);
      }
      
      const data = await response.json();
      setQueryResponse(stripMarkdown(data.response));
    } catch (err) {
      setQueryError(`Error processing query: ${err.message}`);
      setQueryResponse('');
    } finally {
      setIsQuerying(false);
    }
  };
  
  const handleFileSelect = async (item) => {
    if (item.type === 'file') {
      setSelectedFilePath(item.path);
      await fetchFileContent(item.download_url);
    }
  };
  
  const handleDirectoryClick = async (item, e) => {
    e.stopPropagation();
    
    const isExpanded = item.expanded;
    
    if (!isExpanded && (!item.children || item.children.length === 0)) {
      const contents = await fetchDirectoryContents(item.path);
      
      setRepoStructure(prevStructure => {
        const updateStructure = (items) => {
          return items.map(structureItem => {
            if (structureItem.path === item.path) {
              return {
                ...structureItem,
                children: contents,
                expanded: true,
              };
            } else if (structureItem.children && structureItem.children.length > 0) {
              return {
                ...structureItem,
                children: updateStructure(structureItem.children),
              };
            }
            return structureItem;
          });
        };
        
        return updateStructure(prevStructure);
      });
    } else {
  
      setRepoStructure(prevStructure => {
        const updateStructure = (items) => {
          return items.map(structureItem => {
            if (structureItem.path === item.path) {
              return {
                ...structureItem,
                expanded: !isExpanded,
              };
            } else if (structureItem.children && structureItem.children.length > 0) {
              return {
                ...structureItem,
                children: updateStructure(structureItem.children),
              };
            }
            return structureItem;
          });
        };
        
        return updateStructure(prevStructure);
      });
    }
  };
  
  const renderFileTree = (items, level = 0) => {
    if (!items || items.length === 0) return null;
    
    return (
      <ul className="pl-4">
        {items.map((item) => (
          <li key={item.path} className="py-1">
            {item.type === 'dir' ? (
              <div 
                className="flex items-center cursor-pointer hover:text-blue-400"
                onClick={(e) => handleDirectoryClick(item, e)}
              >
                <span className="mr-2">
                  {item.expanded ? (
                    <svg className="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  ) : (
                    <svg className="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                    </svg>
                  )}
                </span>
                <svg className="h-5 w-5 text-blue-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
                <span className="text-gray-300 font-medium">{item.name}</span>
              </div>
            ) : (
              <div 
                className={`flex items-center cursor-pointer hover:text-blue-400 pl-6 ${selectedFilePath === item.path ? 'text-blue-400 font-medium' : 'text-gray-400'}`}
                onClick={() => handleFileSelect(item)}
              >
                <svg className="h-5 w-5 text-gray-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                {item.name}
              </div>
            )}
            {item.expanded && item.children && renderFileTree(item.children, level + 1)}
          </li>
        ))}
      </ul>
    );
  };
  
  const getLanguageFromFilename = (filename) => {
    if (!filename) return 'text';
    
    const ext = filename.split('.').pop().toLowerCase();
    
    const languageMap = {
      'js': 'javascript',
      'jsx': 'javascript',
      'ts': 'typescript',
      'tsx': 'typescript',
      'py': 'python',
      'java': 'java',
      'html': 'html',
      'css': 'css',
      'json': 'json',
      'md': 'markdown',
      'txt': 'text',
      'xml': 'xml',
      'yml': 'yaml',
      'yaml': 'yaml',
      'sh': 'bash',
      'php': 'php',
      'rb': 'ruby',
      'c': 'c',
      'cpp': 'cpp',
      'cs': 'csharp',
      'go': 'go',
      'rs': 'rust',
      'swift': 'swift',
      'kt': 'kotlin'
    };
    
    return languageMap[ext] || 'text';
  };
  
  return (
    <div className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 min-h-screen bg-gray-900 text-gray-100">
      {/* Hidden audio element for TTS */}
      <audio ref={audioRef} onEnded={handleAudioEnded} />
      
      {/* Back button */}
      <button 
        onClick={() => navigate(-1)}
        className="mb-8 flex items-center text-gray-400 hover:text-white transition-colors"
      >
        <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path>
        </svg>
        Back
      </button>
      
      {/* Repository Information Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-100">
          Repository Analysis: {username}/{repoName}
        </h1>
        {repoInfo && (
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-sm font-medium text-gray-400">Description</h3>
              <p className="mt-1 text-white">{repoInfo.description || 'No description available'}</p>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-sm font-medium text-gray-400">Primary Language</h3>
              <p className="mt-1 text-white">{repoInfo.language || 'Not specified'}</p>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-sm font-medium text-gray-400">Stars</h3>
              <p className="mt-1 text-white">{repoInfo.stars}</p>
            </div>
            <div className="bg-gray-800 p-4 rounded-lg">
              <h3 className="text-sm font-medium text-gray-400">Forks</h3>
              <p className="mt-1 text-white">{repoInfo.forks}</p>
            </div>
          </div>
        )}
      </div>
      
      {/* Main Content - Three Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: File Explorer */}
        <div className="lg:col-span-3 bg-gray-800 p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-bold text-gray-100 mb-4">File Explorer</h2>
          
          {isLoadingStructure ? (
            <div className="flex justify-center py-10">
              <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
            </div>
          ) : structureError ? (
            <div className="bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
              {structureError}
            </div>
          ) : repoStructure.length > 0 ? (
            <div className="mt-4 max-h-[600px] overflow-y-auto text-sm">
              {renderFileTree(repoStructure)}
            </div>
          ) : (
            <div className="text-center py-10 text-gray-400">
              No files available
            </div>
          )}
        </div>
        
        {/* Middle Column: Documentation Generator */}
        <div className="lg:col-span-5 bg-gray-800 rounded-xl p-6 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-gray-100">Repository Documentation</h2>
            <div className="flex gap-2">
              <button
                onClick={generateDocumentation}
                disabled={isGeneratingDocs || !username || !repoName}
                className="bg-blue-600 px-4 py-2 rounded-lg text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
              >
                {isGeneratingDocs ? 'Generating...' : 'Generate Documentation'}
              </button>
            </div>
          </div>
          
          {/* Language and TTS Controls */}
          {documentation && (
            <div className="mb-4 flex flex-wrap gap-2 items-center p-4 bg-gray-750 rounded-lg">
              <select
                value={selectedLanguage}
                onChange={(e) => handleLanguageChange(e.target.value)}
                className="bg-gray-700 text-white px-3 py-2 rounded-lg text-sm border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isTranslating}
              >
                {languages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
              
              {/* Audio control buttons */}
              <div className="flex gap-1">
                {!isPlayingTTS ? (
                  <button
                    onClick={() => convertToSpeech(
                      selectedLanguage === 'en-IN' ? documentation : translatedDocumentation || documentation,
                      selectedLanguage
                    )}
                    disabled={!documentation && !translatedDocumentation}
                    className="bg-green-600 px-3 py-2 rounded-lg text-white hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm flex items-center gap-1"
                  >
                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h8m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Listen
                  </button>
                ) : (
                  <>
                    <button
                      onClick={toggleAudioPlayback}
                      className="bg-yellow-600 px-3 py-2 rounded-lg text-white hover:bg-yellow-700 transition-colors text-sm flex items-center gap-1"
                    >
                      {isPausedTTS ? (
                        <>
                          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h8m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                          Resume
                        </>
                      ) : (
                        <>
                          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          Pause
                        </>
                      )}
                    </button>
                    
                    <button
                      onClick={stopAudio}
                      className="bg-red-600 px-3 py-2 rounded-lg text-white hover:bg-red-700 transition-colors text-sm flex items-center gap-1"
                    >
                      <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 10h6v4H9z" />
                      </svg>
                      Stop
                    </button>
                  </>
                )}
              </div>
              
              {(isTranslating || isPlayingTTS) && (
                <div className="text-sm text-blue-400">
                  {isTranslating && 'Translating...'}
                  {isPlayingTTS && !isPausedTTS && 'Playing audio...'}
                  {isPlayingTTS && isPausedTTS && 'Audio paused'}
                </div>
              )}
            </div>
          )}
          
          {/* Documentation Display */}
          <div className="bg-gray-750 rounded-lg p-4 min-h-[400px] max-h-[600px] overflow-y-auto">
            {docsError && (
              <div className="bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg mb-4">
                {docsError}
              </div>
            )}
            
            {translationError && (
              <div className="bg-yellow-900/30 border border-yellow-700 text-yellow-300 px-4 py-3 rounded-lg mb-4">
                {translationError}
              </div>
            )}
            
            {ttsError && (
              <div className="bg-orange-900/30 border border-orange-700 text-orange-300 px-4 py-3 rounded-lg mb-4">
                {ttsError}
              </div>
            )}
            
            {isGeneratingDocs ? (
              <div className="flex flex-col items-center justify-center py-20">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
                <p className="text-gray-400">Generating documentation...</p>
              </div>
            ) : documentation ? (
              <div className="prose prose-invert max-w-none">
                <div className="whitespace-pre-wrap text-gray-200 leading-relaxed">
                  {selectedLanguage === 'en-IN' ? documentation : (
                    <>
                      {isTranslating ? (
                        <div className="flex items-center justify-center py-10">
                          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500 mr-3"></div>
                          <span className="text-gray-400">Translating to {languages.find(l => l.code === selectedLanguage)?.name}...</span>
                        </div>
                      ) : translatedDocumentation ? (
                        translatedDocumentation
                      ) : (
                        documentation
                      )}
                    </>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center py-20 text-gray-400">
                <svg className="mx-auto h-12 w-12 text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p>No documentation generated yet.</p>
                <p className="text-sm mt-2">Click "Generate Documentation" to get started.</p>
              </div>
            )}
          </div>
        </div>
        
        <div className="lg:col-span-4 bg-gray-800 rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-bold text-gray-100 mb-4">Ask Questions</h2>
          
          {/* Query Type Selection */}
          <div className="mb-4">
            <div className="flex gap-2">
              <button
                onClick={() => setQueryType('repository')}
                className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                  queryType === 'repository'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                Repository Query
              </button>
              <button
                onClick={() => setQueryType('code')}
                className={`px-4 py-2 rounded-lg text-sm transition-colors ${
                  queryType === 'code'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                Code Query
              </button>
            </div>
          </div>
          
          {/* File Selection for Code Query */}
          {queryType === 'code' && (
            <div className="mb-4 p-4 bg-gray-750 rounded-lg">
              <h3 className="text-sm font-medium text-gray-300 mb-2">Selected File:</h3>
              {selectedFilePath ? (
                <div className="text-sm text-blue-400 mb-2">{selectedFilePath}</div>
              ) : (
                <div className="text-sm text-gray-500 mb-2">No file selected</div>
              )}
              
              {isLoadingFile && (
                <div className="flex items-center text-sm text-gray-400">
                  <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-blue-500 mr-2"></div>
                  Loading file content...
                </div>
              )}
              
              {fileError && (
                <div className="bg-red-900/30 border border-red-700 text-red-300 px-3 py-2 rounded text-sm">
                  {fileError}
                </div>
              )}
            </div>
          )}
          
          {/* Query Form */}
          <form onSubmit={submitQuery} className="mb-4">
            <textarea
              value={queryText}
              onChange={(e) => setQueryText(e.target.value)}
              placeholder={
                queryType === 'repository'
                  ? 'Ask anything about this repository...'
                  : 'Ask about the selected file or code...'
              }
              className="w-full h-24 p-3 bg-gray-700 text-white rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              disabled={isQuerying || (queryType === 'code' && !fileContent)}
            />
            <button
              type="submit"
              disabled={isQuerying || !queryText || (queryType === 'code' && !fileContent)}
              className="mt-3 w-full bg-green-600 px-4 py-2 rounded-lg text-white hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isQuerying ? 'Processing...' : 'Submit Query'}
            </button>
          </form>
          
          {/* Query Response */}
          <div className="bg-gray-750 rounded-lg p-4 min-h-[300px] max-h-[400px] overflow-y-auto">
            {queryError && (
              <div className="bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg mb-4">
                {queryError}
              </div>
            )}
            
            {isQuerying ? (
              <div className="flex flex-col items-center justify-center py-16">
                <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-green-500 mb-4"></div>
                <p className="text-gray-400">Processing your query...</p>
              </div>
            ) : queryResponse ? (
              <div className="prose prose-invert max-w-none">
                <div className="whitespace-pre-wrap text-gray-200 leading-relaxed">
                  {queryResponse}
                </div>
              </div>
            ) : (
              <div className="text-center py-16 text-gray-400">
                <svg className="mx-auto h-10 w-10 text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p>No response yet.</p>
                <p className="text-sm mt-2">
                  {queryType === 'repository' 
                    ? 'Ask questions about the repository structure, dependencies, or functionality.'
                    : 'Select a file from the explorer and ask questions about the code.'
                  }
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* File Content Modal/Viewer (Optional Enhancement) */}
      {selectedFilePath && fileContent && (
        <div className="mt-8 bg-gray-800 rounded-xl p-6 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold text-gray-100">
              File Content: {selectedFilePath}
            </h3>
            <button
              onClick={() => {
                setSelectedFilePath('');
                setFileContent('');
              }}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div className="bg-gray-900 rounded-lg p-4 max-h-96 overflow-auto">
            <pre className="text-sm text-gray-300 whitespace-pre-wrap font-mono">
              <code className={`language-${getLanguageFromFilename(selectedFilePath)}`}>
                {fileContent}
              </code>
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default RepoAnalysis;