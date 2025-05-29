import React, { useState, useRef } from 'react';

const CodeEditor = () => {
  const [code, setCode] = useState('print("Hello, World!")');
  const [language, setLanguage] = useState('python3');
  const [stdin, setStdin] = useState('');
  const [output, setOutput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [error, setError] = useState('');

  
  const [githubUsername, setGithubUsername] = useState('');
  const [repositories, setRepositories] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState(null);
  const [repoContents, setRepoContents] = useState([]);
  const [currentPath, setCurrentPath] = useState('');
  const [isLoadingRepos, setIsLoadingRepos] = useState(false);
  const [isLoadingContents, setIsLoadingContents] = useState(false);
  const [showGithubPanel, setShowGithubPanel] = useState(false);

  
  const [showAiPanel, setShowAiPanel] = useState(false);
  const [aiQuery, setAiQuery] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [isAiLoading, setIsAiLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const fileInputRef = useRef(null);

  const BASE_URL = 'https://viksit.onrender.com/api';

  const languages = [
    { value: 'python3', label: 'Python 3', version: '3', extensions: ['.py'] },
    { value: 'java', label: 'Java', version: '3', extensions: ['.java'] },
    { value: 'cpp', label: 'C++', version: '5', extensions: ['.cpp', '.cc', '.cxx'] },
    { value: 'c', label: 'C', version: '4', extensions: ['.c'] },
    { value: 'nodejs', label: 'JavaScript', version: '3', extensions: ['.js', '.mjs'] },
    { value: 'go', label: 'Go', version: '3', extensions: ['.go'] },
    { value: 'rust', label: 'Rust', version: '0', extensions: ['.rs'] },
    { value: 'php', label: 'PHP', version: '3', extensions: ['.php'] },
    { value: 'ruby', label: 'Ruby', version: '3', extensions: ['.rb'] },
    { value: 'csharp', label: 'C#', version: '3', extensions: ['.cs'] }
  ];

  const getLanguageFromExtension = (filename) => {
    const ext = '.' + filename.split('.').pop().toLowerCase();
    const lang = languages.find(l => l.extensions.includes(ext));
    return lang ? lang.value : 'python3';
  };

  const encodeImage = async (imageFile) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const dataUrl = reader.result;
        const base64String = dataUrl.split(',')[1];
        
        resolve(base64String);
      };
      reader.onerror = reject;
      reader.readAsDataURL(imageFile);
    });
  };

  const fetchRepositories = async () => {
    if (!githubUsername.trim()) return;
    
    setIsLoadingRepos(true);
    setError('');
    
    try {
      const response = await fetch(`${BASE_URL}/repositories/${githubUsername}/`);
      
      if (!response.ok) {
        throw new Error(`Backend API error: ${response.status}`);
      }
      
      const data = await response.json();
      setRepositories(data.repos || []);
      setSelectedRepo(null);
      setRepoContents([]);
      setCurrentPath('');
    } catch (err) {
      setError(`Failed to fetch repositories: ${err.message}`);
    } finally {
      setIsLoadingRepos(false);
    }
  };

  const fetchRepoContents = async (repo, path = '') => {
    setIsLoadingContents(true);
    setError('');
    
    try {
      const url = `${BASE_URL}/repo-structure/${githubUsername}/${repo.name}/`;
      const queryParams = path ? `?path=${encodeURIComponent(path)}` : '';
      const response = await fetch(url + queryParams);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch contents: ${response.status}`);
      }
      
      const data = await response.json();
      setRepoContents(data.structure || []);
      setCurrentPath(path);
      setSelectedRepo(repo);
    } catch (err) {
      setError(`Failed to fetch repository contents: ${err.message}`);
    } finally {
      setIsLoadingContents(false);
    }
  };

  const fetchFileContent = async (file) => {
    try {
      if (!file.download_url) {
        setError('File download URL not available');
        return;
      }

      const response = await fetch(file.download_url);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch file: ${response.status}`);
      }
      
      const content = await response.text();
      setCode(content);
      setSelectedFile(file);
      
      const detectedLang = getLanguageFromExtension(file.name);
      setLanguage(detectedLang);
      
    } catch (err) {
      setError(`Failed to fetch file content: ${err.message}`);
    }
  };

  const navigateToDirectory = (item) => {
    if (item.type === 'dir') {
      fetchRepoContents(selectedRepo, item.path);
    } else {
      fetchFileContent(item);
    }
  };

  const navigateBack = () => {
    if (currentPath) {
      const parentPath = currentPath.split('/').slice(0, -1).join('/');
      fetchRepoContents(selectedRepo, parentPath);
    }
  };

  const executeCode = async () => {
    setIsExecuting(true);
    setError('');
    setOutput('');

    const selectedLang = languages.find(lang => lang.value === language);
    
    try {
      const response = await fetch(`${BASE_URL}/execute-code/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          script: code,
          language: language,
          stdin: stdin,
          versionIndex: selectedLang?.version || '0',
          compileOnly: false
        })
      });

      const result = await response.json();
      
      if (!response.ok) {
        setError(result.error || 'Failed to execute code');
      } else {
        setOutput(result.output || '');
        if (result.error) {
          setError(result.error);
        }
      }
    } catch (err) {
      setError('Network error: Failed to connect to server');
    } finally {
      setIsExecuting(false);
    }
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type.startsWith('image/')) {
        setSelectedImage(file);
        const reader = new FileReader();
        reader.onload = (e) => {
          setImagePreview(e.target.result);
        };
        reader.readAsDataURL(file);
      } else {
        setError('Please select a valid image file');
      }
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const queryAI = async () => {
    if (!aiQuery.trim() && !selectedImage) {
      setError('Please provide a query or upload an image');
      return;
    }

    setIsAiLoading(true);
    setError('');

    try {
      const payload = {};
      
      if (selectedFile && selectedRepo) {
        payload.file_url = selectedFile.download_url;
        payload.query = aiQuery;
      } else {
        payload.file_content = code;
        payload.query = aiQuery || 'Please analyze this code and provide insights, potential issues, or improvements.';
      }

      if (selectedImage) {
        const base64Image = await encodeImage(selectedImage);
        payload.image = base64Image;
        console.log('Image size:', selectedImage.size, 'bytes');
        console.log('Base64 length:', base64Image.length);
        console.log('Base64 preview:', base64Image.substring(0, 50) + '...');
      }

      console.log('Sending payload to /query-code/', {
        ...payload,
        image: payload.image ? `[BASE64_IMAGE_${payload.image.length}_CHARS]` : undefined
      });

      const response = await fetch(`${BASE_URL}/query-code/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();
      
      if (!response.ok) {
        setError(result.error || 'Failed to get AI response');
      } else {
        setAiResponse(result.response || '');
      }
    } catch (err) {
      setError(`Network error: Failed to connect to AI service - ${err.message}`);
    } finally {
      setIsAiLoading(false);
    }
  };

  const queryRepository = async () => {
    if (!selectedRepo || (!aiQuery.trim() && !selectedImage)) {
      setError('Please select a repository and provide a query or image');
      return;
    }

    setIsAiLoading(true);
    setError('');

    try {
      const payload = {
        username: githubUsername,
        repo_name: selectedRepo.name,
        query: aiQuery
      };

      if (selectedImage) {
        const base64Image = await encodeImage(selectedImage);
        payload.image = base64Image;
        console.log('Repository query - Image size:', selectedImage.size, 'bytes');
        console.log('Repository query - Base64 length:', base64Image.length);
        console.log('Repository query - Base64 preview:', base64Image.substring(0, 50) + '...');
      }

      console.log('Sending payload to /query-repository/', {
        ...payload,
        image: payload.image ? `[BASE64_IMAGE_${payload.image.length}_CHARS]` : undefined
      });

      const response = await fetch(`${BASE_URL}/query-repository/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();
      
      if (!response.ok) {
        setError(result.error || 'Failed to get AI response');
      } else {
        setAiResponse(result.response || '');
      }
    } catch (err) {
      setError(`Network error: Failed to connect to AI service - ${err.message}`);
    } finally {
      setIsAiLoading(false);
    }
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
    
    if (!selectedRepo) {
      const defaultCode = {
        python3: 'print("Hello, World!")',
        java: 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
        cpp: '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, World!" << endl;\n    return 0;\n}',
        c: '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
        nodejs: 'console.log("Hello, World!");',
        go: 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}',
        rust: 'fn main() {\n    println!("Hello, World!");\n}',
        php: '<?php\necho "Hello, World!\\n";\n?>',
        ruby: 'puts "Hello, World!"',
        csharp: 'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}'
      };
      
      setCode(defaultCode[newLanguage] || 'print("Hello, World!")');
    }
  };

  const getFileIcon = (item) => {
    if (item.type === 'dir') {
      return (
        <svg className="h-5 w-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path>
        </svg>
      );
    }
    
    const ext = item.name.split('.').pop().toLowerCase();
    const iconColor = {
      py: 'text-blue-500',
      js: 'text-yellow-500',
      java: 'text-orange-500',
      cpp: 'text-blue-400',
      c: 'text-blue-400',
      go: 'text-blue-300',
      rs: 'text-orange-600',
      php: 'text-purple-500',
      rb: 'text-red-500',
      cs: 'text-green-500'
    };
    
    return (
      <svg className={`h-5 w-5 ${iconColor[ext] || 'text-gray-400'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
      </svg>
    );
  };

  return (
    <div className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 bg-gray-900 min-h-screen">
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-100">AI-Powered Code Editor</h1>
            <p className="text-gray-400">Write, debug, and execute code with AI assistance</p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setShowAiPanel(!showAiPanel)}
              className="flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            >
              <svg className="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
              </svg>
              AI Assistant
            </button>
            <button
              onClick={() => setShowGithubPanel(!showGithubPanel)}
              className="flex items-center px-4 py-2 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700 transition-colors"
            >
              <svg className="mr-2 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z" clipRule="evenodd"></path>
              </svg>
              GitHub
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-4">
        {/* GitHub Panel */}
        {showGithubPanel && (
          <div className="lg:col-span-1 space-y-6">
            {/* GitHub Username Input */}
            <div className="rounded-xl bg-gray-800 p-4">
              <label className="block text-sm font-medium text-gray-300 mb-3">
                GitHub Username
              </label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={githubUsername}
                  onChange={(e) => setGithubUsername(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && fetchRepositories()}
                  className="flex-1 px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter GitHub username"
                />
                <button
                  onClick={fetchRepositories}
                  disabled={isLoadingRepos || !githubUsername.trim()}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoadingRepos ? '...' : 'Fetch'}
                </button>
              </div>
            </div>

            {/* Repositories List */}
            {repositories.length > 0 && (
              <div className="rounded-xl bg-gray-800 p-4">
                <h3 className="text-sm font-medium text-gray-300 mb-3">Repositories</h3>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {repositories.map((repo) => (
                    <button
                      key={repo.id}
                      onClick={() => fetchRepoContents(repo)}
                      className={`w-full text-left p-3 rounded-lg transition-colors ${
                        selectedRepo?.id === repo.id
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="font-medium">{repo.name}</p>
                          <p className="text-xs opacity-75">Repository</p>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Repository Contents */}
            {selectedRepo && (
              <div className="rounded-xl bg-gray-800 p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-sm font-medium text-gray-300">Contents</h3>
                  {currentPath && (
                    <button
                      onClick={navigateBack}
                      className="text-blue-400 hover:text-blue-300 transition-colors"
                    >
                      <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                      </svg>
                    </button>
                  )}
                </div>
                
                {currentPath && (
                  <p className="text-xs text-gray-500 mb-2">/{currentPath}</p>
                )}
                
                <div className="space-y-1 max-h-60 overflow-y-auto">
                  {isLoadingContents ? (
                    <div className="flex items-center justify-center py-8">
                      <svg className="animate-spin h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    </div>
                  ) : (
                    repoContents.map((item, index) => (
                      <button
                        key={`${item.path}-${index}`}
                        onClick={() => navigateToDirectory(item)}
                        className="w-full text-left p-2 rounded hover:bg-gray-700 transition-colors group"
                      >
                        <div className="flex items-center">
                          {getFileIcon(item)}
                          <span className="ml-2 text-sm text-gray-300 group-hover:text-white">
                            {item.name}
                          </span>
                        </div>
                      </button>
                    ))
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* AI Assistant Panel */}
        {showAiPanel && (
          <div className="lg:col-span-1 space-y-6">
            <div className="rounded-xl bg-gray-800 p-4">
              <h3 className="text-sm font-medium text-gray-300 mb-3 flex items-center">
                <svg className="mr-2 h-5 w-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
                AI Debug Assistant
              </h3>
              
              {/* Query Input */}
              <textarea
                value={aiQuery}
                onChange={(e) => setAiQuery(e.target.value)}
                className="w-full h-24 px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none mb-3"
                placeholder="Ask AI to debug, explain, or improve your code..."
              />

              {/* Image Upload */}
              <div className="mb-3">
                <label className="block text-xs font-medium text-gray-400 mb-2">
                  Upload Image (Optional)
                </label>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="hidden"
                />
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="w-full px-3 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 transition-colors text-sm flex items-center justify-center"
                >
                  <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  Upload Image
                </button>
              </div>

              {/* Image Preview */}
              {imagePreview && (
                <div className="mb-3 relative">
                  <img
                    src={imagePreview}
                    alt="Uploaded"
                    className="w-full h-32 object-cover rounded-lg"
                  />
                  <button
                    onClick={removeImage}
                    className="absolute top-2 right-2 bg-red-600 text-white rounded-full p-1 hover:bg-red-700 transition-colors"
                  >
                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </div>
              )}

              {/* Action Buttons */}
              <div className="space-y-2">
                <button
                  onClick={queryAI}
                  disabled={isAiLoading || (!aiQuery.trim() && !selectedImage)}
                  className="w-full py-2 px-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors text-sm"
                >
                  {isAiLoading ? 'Analyzing...' : 'Analyze Code'}
                </button>
                
                {selectedRepo && (
                  <button
                    onClick={queryRepository}
                    disabled={isAiLoading || (!aiQuery.trim() && !selectedImage)}
                    className="w-full py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors text-sm"
                  >
                    {isAiLoading ? 'Analyzing...' : 'Ask About Repository'}
                  </button>
                )}
              </div>

              {/* AI Response */}
              {aiResponse && (
                <div className="mt-4 p-3 bg-gray-900 border border-gray-700 rounded-lg max-h-64 overflow-y-auto">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-xs font-medium text-purple-300">AI Response</h4>
                    <button
                      onClick={() => setAiResponse('')}
                      className="text-gray-400 hover:text-gray-300 transition-colors"
                    >
                      <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                      </svg>
                    </button>
                  </div>
                  <div className="text-xs text-gray-200 whitespace-pre-wrap">
                    {aiResponse}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Code Editor Section */}
        <div className={`space-y-6 ${(showGithubPanel && showAiPanel) ? 'lg:col-span-2' : (showGithubPanel || showAiPanel) ? 'lg:col-span-3' : 'lg:col-span-4'}`}>
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {/* Left Column - Editor */}
            <div className="space-y-6">
              {/* Language Selector */}
              <div className="rounded-xl bg-gray-800 p-4">
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Select Language
                </label>
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                  {languages.map((lang) => (
                    <button
                      key={lang.value}
                      onClick={() => handleLanguageChange(lang.value)}
                      className={`px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                        language === lang.value
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                      }`}
                    >
                      {lang.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Code Input */}
              <div className="rounded-xl bg-gray-800 p-4">
                <div className="flex items-center justify-between mb-3">
                  <label className="block text-sm font-medium text-gray-300">
                    Code Editor
                    {selectedFile && (
                      <span className="ml-2 text-xs text-blue-400">
                        ({selectedFile.name})
                      </span>
                    )}
                  </label>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-gray-400">
                      Lines: {code.split('\n').length}
                    </span>
                  </div>
                </div>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  className="w-full h-96 px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-gray-100 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  placeholder="Write your code here..."
                  spellCheck="false"
                />
              </div>

              {/* Standard Input */}
              <div className="rounded-xl bg-gray-800 p-4">
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Standard Input (Optional)
                </label>
                <textarea
                  value={stdin}
                  onChange={(e) => setStdin(e.target.value)}
                  className="w-full h-24 px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-gray-100 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  placeholder="Enter input data for your program..."
                />
              </div>

              {/* Execute Button */}
              <div className="rounded-xl bg-gray-800 p-4">
                <button
                  onClick={executeCode}
                  disabled={isExecuting || !code.trim()}
                  className="w-full flex items-center justify-center px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors"
                >
                  {isExecuting ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Executing...
                    </>
                  ) : (
                    <>
                      <svg className="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M19 10a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      Run Code
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Right Column - Output */}
            <div className="space-y-6">
              {/* Output */}
              <div className="rounded-xl bg-gray-800 p-4">
                <div className="flex items-center justify-between mb-3">
                  <label className="block text-sm font-medium text-gray-300">
                    Output
                  </label>
                  {output && (
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(output);
                        // You could add a toast notification here
                      }}
                      className="text-gray-400 hover:text-gray-300 transition-colors"
                      title="Copy output"
                    >
                      <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                      </svg>
                    </button>
                  )}
                </div>
                <div className="bg-gray-900 border border-gray-700 rounded-lg p-4 h-96 overflow-y-auto">
                  {isExecuting ? (
                    <div className="flex items-center justify-center h-full">
                      <div className="text-center">
                        <svg className="animate-spin h-8 w-8 text-blue-500 mx-auto mb-2" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <p className="text-gray-400 text-sm">Executing code...</p>
                      </div>
                    </div>
                  ) : output ? (
                    <pre className="text-green-400 text-sm font-mono whitespace-pre-wrap">
                      {output}
                    </pre>
                  ) : (
                    <div className="flex items-center justify-center h-full">
                      <div className="text-center">
                        <svg className="h-12 w-12 text-gray-600 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                        <p className="text-gray-500 text-sm">Output will appear here</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Error Display */}
              {error && (
                <div className="rounded-xl bg-red-900/20 border border-red-700/50 p-4">
                  <div className="flex items-start">
                    <svg className="h-5 w-5 text-red-400 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <div className="flex-1">
                      <h3 className="text-sm font-medium text-red-400 mb-1">Error</h3>
                      <p className="text-sm text-red-300 whitespace-pre-wrap font-mono">
                        {error}
                      </p>
                    </div>
                    <button
                      onClick={() => setError('')}
                      className="text-red-400 hover:text-red-300 transition-colors ml-2"
                    >
                      <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              )}

              {/* Code Statistics */}
              <div className="rounded-xl bg-gray-800 p-4">
                <h3 className="text-sm font-medium text-gray-300 mb-3">Statistics</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <p className="text-lg font-bold text-blue-400">{code.split('\n').length}</p>
                    <p className="text-xs text-gray-400">Lines</p>
                  </div>
                  <div className="text-center">
                    <p className="text-lg font-bold text-green-400">{code.length}</p>
                    <p className="text-xs text-gray-400">Characters</p>
                  </div>
                  <div className="text-center">
                    <p className="text-lg font-bold text-purple-400">{code.split(/\s+/).filter(word => word.length > 0).length}</p>
                    <p className="text-xs text-gray-400">Words</p>
                  </div>
                  <div className="text-center">
                    <p className="text-lg font-bold text-orange-400">{languages.find(l => l.value === language)?.label || 'Unknown'}</p>
                    <p className="text-xs text-gray-400">Language</p>
                  </div>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="rounded-xl bg-gray-800 p-4">
                <h3 className="text-sm font-medium text-gray-300 mb-3">Quick Actions</h3>
                <div className="space-y-2">
                  <button
                    onClick={() => setCode('')}
                    className="w-full px-3 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 transition-colors text-sm flex items-center justify-center"
                  >
                    <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                    Clear Code
                  </button>
                  <button
                    onClick={() => {
                      const defaultCode = {
                        python3: 'print("Hello, World!")',
                        java: 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
                        cpp: '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, World!" << endl;\n    return 0;\n}',
                        c: '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
                        nodejs: 'console.log("Hello, World!");',
                        go: 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}',
                        rust: 'fn main() {\n    println!("Hello, World!");\n}',
                        php: '<?php\necho "Hello, World!\\n";\n?>',
                        ruby: 'puts "Hello, World!"',
                        csharp: 'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}'
                      };
                      setCode(defaultCode[language] || 'print("Hello, World!")');
                    }}
                    className="w-full px-3 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 transition-colors text-sm flex items-center justify-center"
                  >
                    <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                    </svg>
                    Reset to Template
                  </button>
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(code);
                    }}
                    className="w-full px-3 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 transition-colors text-sm flex items-center justify-center"
                  >
                    <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                    Copy Code
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodeEditor;