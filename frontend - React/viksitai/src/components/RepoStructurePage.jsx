import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import RepoAnalysis from './RepoAnalysis';
import * as d3 from 'd3';

const RepoStructurePage = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [searchedUsername, setSearchedUsername] = useState('');
  const [repositories, setRepositories] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState(null);
  const [repoStructure, setRepoStructure] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [visualizationType, setVisualizationType] = useState('tree');
  
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState('');
  const [fileLoading, setFileLoading] = useState(false);
  const [fileError, setFileError] = useState(null);
  
  const [expandedDirs, setExpandedDirs] = useState(new Set());
  
  const svgRef = useRef(null);
  const tooltipRef = useRef(null);
  
  const API_BASE_URL = 'https://viksit.onrender.com/api';
  
  const fetchRepositories = async (username) => {
    if (!username) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/repositories/${username}/`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch repositories: ${response.status}`);
      }
      
      const data = await response.json();
      setRepositories(data.repos || []);
      setSearchedUsername(username);
    } catch (err) {
      setError(`Error fetching repositories: ${err.message}`);
      setRepositories([]);
    } finally {
      setLoading(false);
    }
  };
  
  const fetchDirectoryContents = async (dirPath) => {
    if (!searchedUsername || !selectedRepo || !dirPath) return [];
    
    try {
      const response = await fetch(`${API_BASE_URL}/repo-structure/${searchedUsername}/${selectedRepo.name}/?path=${encodeURIComponent(dirPath)}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch directory contents: ${response.status}`);
      }
      
      const data = await response.json();
      return data.structure || [];
    } catch (err) {
      console.error(`Error fetching directory contents for ${dirPath}:`, err.message);
      return [];
    }
  };
  
  const expandAllDirectories = async (node) => {
    if (!node || node.type !== 'dir') return node;
    
    if (!node.children || node.children.length === 0) {
      const contents = await fetchDirectoryContents(node.path);
      
      node.children = contents.map(item => ({
        name: item.name,
        path: item.path,
        type: item.type,
        size: item.size || 0,
        url: item.url,
        download_url: item.download_url,
        children: item.type === 'dir' ? [] : null
      }));
      
      setExpandedDirs(prev => new Set([...prev, node.path]));
    }
    
    if (node.children && node.children.length > 0) {
      for (const child of node.children) {
        if (child.type === 'dir') {
          await expandAllDirectories(child);
        }
      }
    }
    
    return node;
  };
  
  const fetchRepoStructure = async (repo) => {
    if (!repo) return;
    
    setLoading(true);
    setError(null);
    setExpandedDirs(new Set());
    
    try {
      const response = await fetch(`${API_BASE_URL}/repo-structure/${searchedUsername}/${repo.name}/`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch repository structure: ${response.status}`);
      }
      
      const data = await response.json();
      const fileList = data.structure || [];
      
      const rootNode = {
        name: repo.name,
        path: '',
        type: 'dir',
        children: []
      };
      
      rootNode.children = fileList.map(item => ({
        name: item.name,
        path: item.path,
        type: item.type,
        size: item.size || 0, 
        url: item.url,
        download_url: item.download_url,
        children: item.type === 'dir' ? [] : null
      }));
      
      const expandedRootNode = { ...rootNode };
      
      for (const child of expandedRootNode.children) {
        if (child.type === 'dir') {
          await expandAllDirectories(child);
        }
      }
      
      setRepoStructure(expandedRootNode);
    } catch (err) {
      setError(`Error fetching repository structure: ${err.message}`);
      setRepoStructure(null);
    } finally {
      setLoading(false);
    }
  };
  
  const fetchFileContent = async (fileUrl, fileName) => {
    if (!fileUrl) return;
    
    setFileLoading(true);
    setFileError(null);
    
    try {
      const response = await fetch(fileUrl);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch file content: ${response.status}`);
      }
      
      const content = await response.text();
      
      setSelectedFile({
        name: fileName,
        url: fileUrl
      });
      setFileContent(content);
    } catch (err) {
      setFileError(`Error fetching file content: ${err.message}`);
      setFileContent('');
    } finally {
      setFileLoading(false);
    }
  };
  
  const handleNodeClick = async (d) => {
    if (d.data.type === 'dir') {
      if (!expandedDirs.has(d.data.path) && d.data.children && d.data.children.length === 0) {
        const contents = await fetchDirectoryContents(d.data.path);
        
        d.data.children = contents.map(item => ({
          name: item.name,
          path: item.path,
          type: item.type,
          size: item.size || 0,
          url: item.url,
          download_url: item.download_url,
          children: item.type === 'dir' ? [] : null
        }));
        
        setExpandedDirs(prev => new Set([...prev, d.data.path]));
        
        if (visualizationType === 'tree') {
          renderTreeVisualization();
        } else if (visualizationType === 'sunburst') {
          renderSunburstVisualization();
        }
      }
    } else if (d.data.type === 'file') {
      fetchFileContent(d.data.download_url, d.data.name);
    }
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    fetchRepositories(username);
    
    setSelectedFile(null);
    setFileContent('');
  };
  
  const handleRepoSelect = (repo) => {
    setSelectedRepo(repo);
    fetchRepoStructure(repo);
    
    setSelectedFile(null);
    setFileContent('');
  };
  
  const handleDownloadFile = () => {
    if (!selectedFile || !fileContent) return;
    
    const blob = new Blob([fileContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = selectedFile.name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };
  
  useEffect(() => {
    if (!repoStructure || !svgRef.current) return;
    
    d3.select(svgRef.current).selectAll("*").remove();
    
    if (visualizationType === 'tree') {
      renderTreeVisualization();
    } else if (visualizationType === 'sunburst') {
      renderSunburstVisualization();
    }
  }, [repoStructure, visualizationType]);
  
  const getLanguageFromFilename = (filename) => {
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
  
  const renderTreeVisualization = () => {
    const svg = d3.select(svgRef.current);
    const width = 960;
    const height = 800;
    const margin = { top: 20, right: 120, bottom: 20, left: 120 };
    
    svg.attr("width", width)
       .attr("height", height);
    
    const g = svg.append("g")
                 .attr("transform", `translate(${margin.left},${margin.top})`);
    
    const treeLayout = d3.tree()
                          .size([height - margin.top - margin.bottom, width - margin.left - margin.right]);
    
    const root = d3.hierarchy(repoStructure);
    
    const treeData = treeLayout(root);
    
    const links = g.selectAll(".link")
                    .data(treeData.links())
                    .enter()
                    .append("path")
                    .attr("class", "link")
                    .attr("d", d3.linkHorizontal()
                              .x(d => d.y)
                              .y(d => d.x))
                    .attr("fill", "none")
                    .attr("stroke", "#64748b")
                    .attr("stroke-width", 1.5)
                    .attr("opacity", 0)
                    .transition()
                    .duration(800)
                    .delay((d, i) => i * 5) 
                    .attr("opacity", 0.6);
  
                    
    const nodes = g.selectAll(".node")
                    .data(treeData.descendants())
                    .enter()
                    .append("g")
                    .attr("class", d => `node ${d.data.type}`)
                    .attr("transform", d => `translate(${d.y},${d.x})`)
                    .attr("opacity", 0)
                    .transition()
                    .duration(800)
                    .delay((d, i) => i * 10) 
                    .attr("opacity", 1);
    
    g.selectAll(".node")
      .append("circle")
      .attr("r", d => d.data.type === 'dir' ? 7 : 5)
      .attr("fill", d => d.data.type === 'dir' ? "#3B82F6" : "#10B981")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .style("cursor", "pointer")
      .on("mouseover", function(event, d) {
        const tooltip = d3.select(tooltipRef.current);
        tooltip.style("opacity", 1)
               .html(`
                 <div class="p-2">
                   <div class="font-bold">${d.data.name}</div>
                   <div class="text-xs text-gray-300">${d.data.path}</div>
                   <div class="text-xs text-gray-400">${d.data.type}</div>
                   ${d.data.size ? `<div class="text-xs">Size: ${formatFileSize(d.data.size)}</div>` : ''}
                 </div>
               `)
               .style("left", (event.pageX + 10) + "px")
               .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseout", function() {
        d3.select(tooltipRef.current).style("opacity", 0);
      })
      .on("click", function(event, d) {
        handleNodeClick(d);
      });
    
    g.selectAll(".node")
      .append("text")
      .attr("dy", d => d.children ? -10 : 3)
      .attr("x", d => d.children ? -8 : 8)
      .attr("text-anchor", d => d.children ? "end" : "start")
      .text(d => d.data.name.length > 20 ? d.data.name.slice(0, 20) + "..." : d.data.name)
      .attr("fill", "#e2e8f0")
      .attr("font-size", "0.75rem")
      .style("cursor", "pointer")
      .on("click", function(event, d) {
        handleNodeClick(d);
      });
  };
  
  const renderSunburstVisualization = () => {
    const svg = d3.select(svgRef.current);
    const width = 800;
    const height = 800;
    const radius = Math.min(width, height) / 2;
    
    svg.attr("width", width)
       .attr("height", height);
       
    const g = svg.append("g")
                 .attr("transform", `translate(${width / 2},${height / 2})`);
    
    const root = d3.hierarchy(repoStructure)
                   .sum(d => d.type === 'file' ? (d.size || 1) : 0);
    
    const colorScale = d3.scaleOrdinal()
                          .domain(["file", "dir"])
                          .range(["#10B981", "#3B82F6"]);
    
    const partition = d3.partition()
                         .size([2 * Math.PI, radius]);
    
    partition(root);
    
    const arc = d3.arc()
                   .startAngle(d => d.x0)
                   .endAngle(d => d.x1)
                   .innerRadius(d => d.y0)
                   .outerRadius(d => d.y1);
    
    const arcs = g.selectAll("path")
                   .data(root.descendants().filter(d => d.depth))
                   .enter()
                   .append("path")
                   .attr("d", arc)
                   .style("fill", d => colorScale(d.data.type))
                   .style("stroke", "#1e293b")
                   .style("stroke-width", "1px")
                   .style("opacity", 0)
                   .style("cursor", "pointer")
                   .on("mouseover", function(event, d) {
                     d3.select(this).style("opacity", 1);
                     
                     const tooltip = d3.select(tooltipRef.current);
                     tooltip.style("opacity", 1)
                            .html(`
                              <div class="p-2">
                                <div class="font-bold">${d.data.name}</div>
                                <div class="text-xs text-gray-300">${d.data.path}</div>
                                <div class="text-xs text-gray-400">${d.data.type}</div>
                                ${d.data.size ? `<div class="text-xs">Size: ${formatFileSize(d.data.size)}</div>` : ''}
                              </div>
                            `)
                            .style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 28) + "px");
                   })
                   .on("mouseout", function() {
                     d3.select(this).style("opacity", 0.8);
                     d3.select(tooltipRef.current).style("opacity", 0);
                   })
                   .on("click", function(event, d) {
                     handleNodeClick(d);
                   })
                   .transition()
                   .duration(1000)
                   .delay((d, i) => i * 2)
                   .style("opacity", 0.8);
  };
  
  // Helper function to format file size
  const formatFileSize = (size) => {
    if (size < 1024) return `${size} B`;
    else if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    else if (size < 1024 * 1024 * 1024) return `${(size / (1024 * 1024)).toFixed(1)} MB`;
    else return `${(size / (1024 * 1024 * 1024)).toFixed(1)} GB`;
  };
  
  return (
    <div className="pt-20 pb-12 px-4 sm:px-6 lg:px-8 min-h-screen bg-gray-900 text-gray-100">
      {/* Back button */}
      <button 
        onClick={() => navigate('/')}
        className="mb-8 flex items-center text-gray-400 hover:text-white transition-colors"
      >
        <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path>
        </svg>
        Back to Dashboard
      </button>
      
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-100">Repository Structure Visualization</h1>
        <p className="text-gray-400">Explore GitHub repository structures and view file contents interactively</p>
      </div>
      
      {/* GitHub Username Form */}
      <div className="mb-8 bg-gray-800 rounded-xl p-6 shadow-lg">
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4">
          <div className="flex-grow">
            <label htmlFor="username" className="block text-sm font-medium text-gray-400 mb-2">GitHub Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter GitHub username"
              className="w-full rounded-lg bg-gray-700 border-gray-600 text-white px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div className="flex items-end">
            <button
              type="submit"
              className="rounded-lg bg-blue-600 px-6 py-2 font-medium text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900"
              disabled={loading}
            >
              {loading ? 'Loading...' : 'Search'}
            </button>
          </div>
        </form>
      </div>
      
      {/* Loading indicator for initial repository structure loading */}
      {loading && !error && (
        <div className="mb-8 bg-gray-800 rounded-xl p-6 shadow-lg flex justify-center">
          <div className="flex flex-col items-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            <p className="mt-4 text-gray-400">
              {selectedRepo 
                ? 'Loading full repository structure...' 
                : 'Loading repositories...'}
            </p>
            <p className="mt-2 text-gray-500 text-sm">
              {selectedRepo && 'This may take a moment as we expand all directories.'}
            </p>
          </div>
        </div>
      )}
      
      {/* Error message */}
      {error && (
        <div className="mb-8 bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}
      
      {/* Repositories Grid */}
      {repositories.length > 0 && !loading && (
        <div className="mb-8">
          <h2 className="text-xl font-bold text-gray-100 mb-4">
            Repositories for {searchedUsername}
          </h2>
          
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {repositories.map(repo => (
              <div
                key={repo.id}
                className={`group cursor-pointer rounded-xl bg-gray-800 p-5 transition-all hover:bg-gray-750 ${selectedRepo?.id === repo.id ? 'ring-2 ring-blue-500' : ''}`}
                onClick={() => handleRepoSelect(repo)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="mr-4 rounded-lg bg-gray-700 p-3">
                      <svg className="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path>
                      </svg>
                    </div>
                    <div>
                      <h3 className="font-medium text-gray-100 group-hover:text-white">{repo.name}</h3>
                      <div className="mt-1 flex items-center">
                        <span className="text-xs text-gray-400">Updated {repo.id}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Main Content Section */}
      {selectedRepo && !loading && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Visualization Section - 2 columns on large screens */}
          <div className="lg:col-span-2">
            {/* Visualization Controls */}
            <div className="mb-8">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                <h2 className="text-xl font-bold text-gray-100">
                  Structure for {selectedRepo.name}
                </h2>
                <div className="flex bg-gray-800 rounded-lg p-1">
                  <button
                    className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${visualizationType === 'tree' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'}`}
                    onClick={() => setVisualizationType('tree')}
                  >
                    Tree View
                  </button>
                  <button
                    className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${visualizationType === 'sunburst' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'}`}
                    onClick={() => setVisualizationType('sunburst')}
                  >
                    Sunburst View
                  </button>
                </div>
              </div>
              
              {/* Legend */}
              <div className="mb-6 flex gap-6 bg-gray-800 rounded-lg p-4">
                <div className="flex items-center">
                  <div className="h-3 w-3 rounded-full bg-blue-500 mr-2"></div>
                  <span className="text-sm text-gray-300">Directories</span>
                </div>
                <div className="flex items-center">
                  <div className="h-3 w-3 rounded-full bg-green-500 mr-2"></div>
                  <span className="text-sm text-gray-300">Files</span>
                </div>
              </div>
              
              {/* Visualization container */}
              <div className="bg-gray-800 rounded-xl p-6 shadow-lg overflow-auto relative min-h-[600px]">
                {repoStructure ? (
                  <div className="relative">
                    <svg ref={svgRef} className="mx-auto" style={{ overflow: 'visible' }}></svg>
                    <div 
                      ref={tooltipRef} 
                      className="absolute opacity-0 pointer-events-none bg-gray-900 text-white p-2 rounded-lg shadow-lg z-10 border border-gray-700"
                      style={{ transition: 'opacity 0.2s ease-in-out' }}
                    ></div>
                  </div>
                ) : (
                  <div className="text-center py-12 text-gray-400">
                    {selectedRepo ? 'No structure data available' : 'Select a repository to visualize its structure'}
                  </div>
                )}
              </div>
            </div>
          </div>
          
          {/* File Content Viewer - 1 column on large screens */}
          <div className="lg:col-span-1">
            <div className="bg-gray-800 rounded-xl shadow-lg overflow-hidden h-full">
              <div className="bg-gray-750 px-6 py-4 flex justify-between items-center border-b border-gray-700">
                <div className="flex items-center">
                  <svg className="h-5 w-5 text-gray-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  <h3 className="font-medium text-gray-200 truncate">
                    {selectedFile ? selectedFile.name : 'File Viewer'}
                  </h3>
                </div>
                {selectedFile && (
                  <button 
                    onClick={handleDownloadFile}
                    className="text-blue-400 hover:text-blue-300 focus:outline-none flex items-center"
                    title="Download file"
                  >
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                    </svg>
                  </button>
                )}
              </div>
              
              <div className="h-[600px] overflow-auto p-4 bg-gray-900">
                {fileLoading ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="flex flex-col items-center">
                      <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
                      <p className="mt-4 text-gray-400">Loading file content...</p>
                    </div>
                  </div>
                ) : fileError ? (
                  <div className="bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
                    {fileError}
                  </div>
                ) : selectedFile ? (
                  <pre className="text-sm font-mono text-gray-300 whitespace-pre-wrap">
                    <code className={`language-${getLanguageFromFilename(selectedFile.name)}`}>
                      {fileContent}
                    </code>
                  </pre>
                ) : (
                  <div className="flex flex-col items-center justify-center h-full text-center">
                    <svg className="h-16 w-16 text-gray-700 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    <p className="text-gray-500">Click on a file in the visualization to view its content</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
      <button 
        onClick={() => navigate(`/repo-analysis?username=${searchedUsername}&repo_name=${selectedRepo.name}`)}
        className="bg-blue-600 px-4 py-2 rounded-lg text-white hover:bg-blue-700"
      >
        Analyze Repository
      </button>
    </div>
  )
}

export default RepoStructurePage;