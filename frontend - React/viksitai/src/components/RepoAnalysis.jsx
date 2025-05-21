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
  
  const [queryType, setQueryType] = useState('repository'); // 'repository' or 'code'
  const [queryText, setQueryText] = useState('');
  const [queryResponse, setQueryResponse] = useState('');
  const [isQuerying, setIsQuerying] = useState(false);
  const [queryError, setQueryError] = useState(null);
  
  // State for file selection (for code queries)
  const [selectedFilePath, setSelectedFilePath] = useState('');
  const [fileContent, setFileContent] = useState('');
  const [isLoadingFile, setIsLoadingFile] = useState(false);
  const [fileError, setFileError] = useState(null);
  
  // State for repository structure (for file selection)
  const [repoStructure, setRepoStructure] = useState([]);
  const [isLoadingStructure, setIsLoadingStructure] = useState(false);
  const [structureError, setStructureError] = useState(null);
  
  // API Base URL
  const API_BASE_URL = 'https://viksit.onrender.com/api';
  
  // Fetch repository info on component mount or when username/repoName changes
  useEffect(() => {
    if (username && repoName) {
      fetchRepoInfo();
      fetchRepoStructure();
    }
  }, [username, repoName]);
  
  // Function to fetch repository info
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
  
  // Function to fetch repository structure
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
  
  // Function to fetch directory contents
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
  
  // Function to fetch file content
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
  
  // Function to generate documentation
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
      setDocumentation(data.documentation);
    } catch (err) {
      setDocsError(`Error generating documentation: ${err.message}`);
    } finally {
      setIsGeneratingDocs(false);
    }
  };
  
  // Function to submit a query
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
      setQueryResponse(data.response);
    } catch (err) {
      setQueryError(`Error processing query: ${err.message}`);
      setQueryResponse('');
    } finally {
      setIsQuerying(false);
    }
  };
  
  // Function to handle file selection
  const handleFileSelect = async (item) => {
    if (item.type === 'file') {
      setSelectedFilePath(item.path);
      await fetchFileContent(item.download_url);
    }
  };
  
  // Function to handle directory click (expand/collapse)
  const handleDirectoryClick = async (item, e) => {
    e.stopPropagation();
    
    // Toggle expanded state
    const isExpanded = item.expanded;
    
    // If not yet expanded, fetch contents
    if (!isExpanded && (!item.children || item.children.length === 0)) {
      const contents = await fetchDirectoryContents(item.path);
      
      // Update repo structure with new contents
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
      // Just toggle expanded state
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
  
  // Recursive function to render file tree
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
  
  // Helper function to determine file syntax highlighting
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
            <button
              onClick={generateDocumentation}
              disabled={isGeneratingDocs || !username || !repoName}
              className="bg-blue-600 px-4 py-2 rounded-lg text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
            >
              {isGeneratingDocs ? 'Generating...' : 'Generate Documentation'}
            </button>
          </div>
          
          {docsError && (
            <div className="mb-4 bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
              {docsError}
            </div>
          )}
          
          <div className="prose prose-invert max-w-none mt-4 bg-gray-900 p-6 rounded-lg max-h-[600px] overflow-y-auto">
            {isGeneratingDocs ? (
              <div className="flex flex-col items-center justify-center py-10">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
                <p className="mt-4 text-gray-400">Generating comprehensive documentation...</p>
                <p className="mt-2 text-gray-500 text-sm">This may take a moment as we analyze the repository.</p>
              </div>
            ) : documentation ? (
              <div dangerouslySetInnerHTML={{ __html: marked.parse(documentation) }} />
            ) : (
              <div className="text-center py-10 text-gray-400">
                <svg className="mx-auto h-12 w-12 text-gray-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <p>Click "Generate Documentation" to create a comprehensive analysis of this repository</p>
              </div>
            )}
          </div>
        </div>
        
        {/* Right Column: Query Interface */}
        <div className="lg:col-span-4 bg-gray-800 rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-bold text-gray-100 mb-4">Ask about the Repository</h2>
          
          {/* Query Type Selector */}
          <div className="mb-4 flex bg-gray-750 rounded-lg p-1">
            <button
              className={`px-4 py-2 text-sm font-medium rounded-md transition-colors flex-1 ${queryType === 'repository' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'}`}
              onClick={() => setQueryType('repository')}
            >
              Repository Query
            </button>
            <button
              className={`px-4 py-2 text-sm font-medium rounded-md transition-colors flex-1 ${queryType === 'code' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'}`}
              onClick={() => setQueryType('code')}
            >
              Code Query
            </button>
          </div>
          
          {/* Query Form */}
          <form onSubmit={submitQuery} className="mb-4">
            <div className="mb-4">
              <label htmlFor="query" className="block text-sm font-medium text-gray-400 mb-2">
                {queryType === 'repository' 
                  ? 'Ask anything about this repository' 
                  : 'Ask about the selected file code'}
              </label>
              <textarea
                id="query"
                value={queryText}
                onChange={(e) => setQueryText(e.target.value)}
                placeholder={queryType === 'repository' 
                  ? 'E.g., Explain the main purpose of this repository' 
                  : 'E.g., Explain what this code does'}
                className="w-full h-32 rounded-lg bg-gray-700 border-gray-600 text-white px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            
            {queryType === 'code' && (
              <div className="mb-4 p-4 bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-300 mb-2">
                  {selectedFilePath 
                    ? `Selected file: ${selectedFilePath}` 
                    : 'Please select a file from the file explorer'}
                </p>
                {selectedFilePath && (
                  <div className="text-xs text-gray-400 truncate">
                    {isLoadingFile 
                      ? 'Loading file content...' 
                      : `File loaded (${fileContent.length} characters)`}
                  </div>
                )}
              </div>
            )}
            
            <button
              type="submit"
              disabled={isQuerying || (queryType === 'code' && !fileContent)}
              className="w-full rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isQuerying ? 'Processing...' : 'Submit Query'}
            </button>
          </form>
          
          {/* Query Error */}
          {queryError && (
            <div className="mb-4 bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg text-sm">
              {queryError}
            </div>
          )}
          
          {/* Query Response */}
          {!isQuerying && queryResponse && (
            <div className="bg-gray-900 p-4 rounded-lg mt-4 max-h-[300px] overflow-y-auto">
              <h3 className="text-sm font-medium text-gray-400 mb-2">Response:</h3>
              <div className="prose prose-invert max-w-none text-sm">
                <p className="text-gray-300">{queryResponse}</p>
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Code Viewer (appears when a file is selected) */}
      {selectedFilePath && (
        <div className="mt-8 bg-gray-800 rounded-xl shadow-lg overflow-hidden">
          <div className="bg-gray-750 px-6 py-4 flex justify-between items-center border-b border-gray-700">
            <div className="flex items-center">
              <svg className="h-5 w-5 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              <h3 className="font-medium text-gray-200 truncate">
                {selectedFilePath}
              </h3>
            </div>
          </div>
          
          <div className="overflow-auto p-4 bg-gray-900 max-h-[500px]">
            {isLoadingFile ? (
              <div className="flex items-center justify-center h-32">
                <div className="flex flex-col items-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
                  <p className="mt-4 text-gray-400">Loading file content...</p>
                </div>
              </div>
            ) : fileError ? (
              <div className="bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
                {fileError}
              </div>
            ) : (
              <pre className="text-sm font-mono text-gray-300 whitespace-pre-wrap">
                <code className={`language-${getLanguageFromFilename(selectedFilePath)}`}>
                  {fileContent}
                </code>
              </pre>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Add marked library for Markdown parsing
const marked = {
  parse: (markdown) => {
    if (!markdown) return '';
    
    // Very basic markdown parsing - in a real app, use a proper markdown library
    return markdown
      // Headers
      .replace(/^### (.*$)/gim, '<h3 class="text-xl font-bold my-3 text-gray-200">$1</h3>')
      .replace(/^## (.*$)/gim, '<h2 class="text-2xl font-bold my-4 text-gray-100">$1</h2>')
      .replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold my-5 text-white">$1</h1>')
      // Bold
      .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
      // Italic
      .replace(/\*(.*)\*/gim, '<em>$1</em>')
      // Lists
      .replace(/^\- (.*$)/gim, '<li class="ml-4">$1</li>')
      // Line breaks
      .replace(/\n/gim, '<br>');
  }
};

export default RepoAnalysis;