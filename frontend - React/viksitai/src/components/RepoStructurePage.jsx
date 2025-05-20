import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
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
  
  const svgRef = useRef(null);
  const tooltipRef = useRef(null);
  
  // Function to fetch repositories for a given username
  const fetchRepositories = async (username) => {
    if (!username) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const token = import.meta.env.VITE_APP_GITHUB_TOKEN;
      const headers = token ? { Authorization: `token ${token}` } : {};
      
      const response = await fetch(`https://api.github.com/users/${username}/repos?per_page=100`, {
        headers
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch repositories: ${response.status}`);
      }
      
      const data = await response.json();
      setRepositories(data);
      setSearchedUsername(username);
    } catch (err) {
      setError(`Error fetching repositories: ${err.message}`);
      setRepositories([]);
    } finally {
      setLoading(false);
    }
  };
  
  const fetchRepoStructure = async (repo) => {
    if (!repo) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const token = import.meta.env.VITE_APP_GITHUB_TOKEN;
      const headers = token ? { Authorization: `token ${token}` } : {};
      
      const response = await fetch(`https://api.github.com/repos/${searchedUsername}/${repo.name}/contents`, {
        headers
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch repository structure: ${response.status}`);
      }
      
      const fileList = await response.json();
      
      // Transform into hierarchical structure
      const rootNode = {
        name: repo.name,
        path: '',
        type: 'dir',
        children: []
      };
      
      // Process first level files/directories
      await Promise.all(fileList.map(async (item) => {
        const node = {
          name: item.name,
          path: item.path,
          type: item.type,
          size: item.size || 0,
          children: []
        };
        
        if (item.type === 'dir') {
          // Fetch subdirectory contents (1 level deep only for performance)
          try {
            const subDirResponse = await fetch(item.url, { headers });
            
            if (subDirResponse.ok) {
              const subDirContents = await subDirResponse.json();
              node.children = subDirContents.map(subItem => ({
                name: subItem.name,
                path: subItem.path,
                type: subItem.type,
                size: subItem.size || 0,
                url: subItem.url,
                children: subItem.type === 'dir' ? [] : null
              }));
            }
          } catch (subdirErr) {
            console.error(`Error fetching subdirectory ${item.path}:`, subdirErr);
          }
        }
        
        rootNode.children.push(node);
      }));
      
      setRepoStructure(rootNode);
    } catch (err) {
      setError(`Error fetching repository structure: ${err.message}`);
      setRepoStructure(null);
    } finally {
      setLoading(false);
    }
  };
  
  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    fetchRepositories(username);
  };
  
  // Handle repository selection
  const handleRepoSelect = (repo) => {
    setSelectedRepo(repo);
    fetchRepoStructure(repo);
  };
  
  // Create D3 visualization when repo structure changes
  useEffect(() => {
    if (!repoStructure || !svgRef.current) return;
    
    // Clear previous visualization
    d3.select(svgRef.current).selectAll("*").remove();
    
    if (visualizationType === 'tree') {
      renderTreeVisualization();
    } else if (visualizationType === 'sunburst') {
      renderSunburstVisualization();
    }
  }, [repoStructure, visualizationType]);
  
  // Tree visualization using D3
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
    
    // Use d3 hierarchy to process our data
    const root = d3.hierarchy(repoStructure);
    
    // Assign positions to nodes
    const treeData = treeLayout(root);
    
    // Add links between nodes
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
                    .delay((d, i) => i * 30)
                    .attr("opacity", 0.6);
    
    // Add nodes
    const nodes = g.selectAll(".node")
                    .data(treeData.descendants())
                    .enter()
                    .append("g")
                    .attr("class", d => `node ${d.data.type}`)
                    .attr("transform", d => `translate(${d.y},${d.x})`)
                    .attr("opacity", 0)
                    .transition()
                    .duration(800)
                    .delay((d, i) => i * 50)
                    .attr("opacity", 1);
    
    // Add circles for nodes
    g.selectAll(".node")
      .append("circle")
      .attr("r", d => d.data.type === 'dir' ? 7 : 5)
      .attr("fill", d => d.data.type === 'dir' ? "#3B82F6" : "#10B981")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
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
      });
    
    // Add labels to nodes
    g.selectAll(".node")
      .append("text")
      .attr("dy", d => d.children ? -10 : 3)
      .attr("x", d => d.children ? -8 : 8)
      .attr("text-anchor", d => d.children ? "end" : "start")
      .text(d => d.data.name.length > 20 ? d.data.name.slice(0, 20) + "..." : d.data.name)
      .attr("fill", "#e2e8f0")
      .attr("font-size", "0.75rem");
  };
  
  // Sunburst visualization using D3
  const renderSunburstVisualization = () => {
    const svg = d3.select(svgRef.current);
    const width = 800;
    const height = 800;
    const radius = Math.min(width, height) / 2;
    
    svg.attr("width", width)
       .attr("height", height);
       
    const g = svg.append("g")
                 .attr("transform", `translate(${width / 2},${height / 2})`);
    
    // Use d3 hierarchy to process our data
    const root = d3.hierarchy(repoStructure)
                   .sum(d => d.type === 'file' ? (d.size || 1) : 0);
    
    // Create a color scale
    const colorScale = d3.scaleOrdinal()
                          .domain(["file", "dir"])
                          .range(["#10B981", "#3B82F6"]);
    
    // Create the sunburst layout
    const partition = d3.partition()
                         .size([2 * Math.PI, radius]);
    
    // Assign positions to nodes
    partition(root);
    
    // Create arc generator
    const arc = d3.arc()
                   .startAngle(d => d.x0)
                   .endAngle(d => d.x1)
                   .innerRadius(d => d.y0)
                   .outerRadius(d => d.y1);
    
    // Add the arcs
    const arcs = g.selectAll("path")
                   .data(root.descendants().filter(d => d.depth))
                   .enter()
                   .append("path")
                   .attr("d", arc)
                   .style("fill", d => colorScale(d.data.type))
                   .style("stroke", "#1e293b")
                   .style("stroke-width", "1px")
                   .style("opacity", 0)
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
                   .transition()
                   .duration(1000)
                   .delay((d, i) => i * 5)
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
        <p className="text-gray-400">Explore GitHub repository structures in an interactive way</p>
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
      
      {/* Error message */}
      {error && (
        <div className="mb-8 bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}
      
      {/* Repositories Grid */}
      {repositories.length > 0 && (
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
                      <div className="mt-1 flex items-center flex-wrap">
                        {repo.language && (
                          <>
                            <span className="mr-2 h-3 w-3 rounded-full" style={{ 
                              backgroundColor: repo.language === 'JavaScript' ? '#f7df1e' : 
                                           repo.language === 'TypeScript' ? '#3178c6' :
                                           repo.language === 'Python' ? '#3572A5' :
                                           repo.language === 'Java' ? '#b07219' :
                                           repo.language === 'HTML' ? '#e34c26' :
                                           repo.language === 'CSS' ? '#563d7c' :
                                           repo.language === 'PHP' ? '#4F5D95' : '#6e7681'
                            }}></span>
                            <span className="text-xs text-gray-400">{repo.language}</span>
                            <span className="mx-2 text-gray-600">•</span>
                          </>
                        )}
                        <span className="text-xs text-gray-400">Updated {new Date(repo.updated_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <div className="flex items-center mr-4">
                      <svg className="mr-1 h-4 w-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                      </svg>
                      <span className="text-xs font-medium text-gray-400">{repo.stargazers_count}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Visualization Controls (displayed when a repo is selected) */}
      {selectedRepo && (
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
          
          {/* Visualization container with loading state */}
          <div className="bg-gray-800 rounded-xl p-6 shadow-lg overflow-auto relative min-h-[600px]">
            {loading ? (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="flex flex-col items-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
                  <p className="mt-4 text-gray-400">Loading repository structure...</p>
                </div>
              </div>
            ) : repoStructure ? (
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
      )}
      
      {/* Information card */}
      <div className="mt-8 bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 shadow-lg">
        <h3 className="font-bold text-gray-100 mb-4">Understanding Repository Structure</h3>
        <p className="text-gray-300 mb-4">
          The visualization above helps you understand the structure of the repository at a glance. 
          Here's how to interpret it:
        </p>
        <ul className="space-y-2 text-gray-400">
          <li className="flex items-start">
            <svg className="h-5 w-5 mr-2 text-blue-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
            </svg>
            <span>Blue nodes represent directories in the repository.</span>
          </li>
          <li className="flex items-start">
            <svg className="h-5 w-5 mr-2 text-green-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
            </svg>
            <span>Green nodes represent individual files.</span>
          </li>
          <li className="flex items-start">
            <svg className="h-5 w-5 mr-2 text-purple-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path>
            </svg>
            <span>Hover over nodes to see more details like file path and size.</span>
          </li>
          <li className="flex items-start">
            <svg className="h-5 w-5 mr-2 text-yellow-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"></path>
            </svg>
            <span>Switch between Tree view and Sunburst view for different perspectives.</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default RepoStructurePage;