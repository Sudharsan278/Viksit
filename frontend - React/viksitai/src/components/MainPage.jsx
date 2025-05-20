import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const MainPage = ({ username }) => {
  const [selectedRepo, setSelectedRepo] = useState(null);
  
  const recentRepos = [
    { id: 1, name: 'viksit-dashboard', language: 'JavaScript', lastUpdated: '2 hours ago', stars: 4 },
    { id: 2, name: 'ml-model-deployment', language: 'Python', lastUpdated: '1 day ago', stars: 12 },
    { id: 3, name: 'mobile-app-api', language: 'TypeScript', lastUpdated: '3 days ago', stars: 7 }
  ];
  
  const statsCards = [
    { title: 'Code Analyzed', value: '24.5K', icon: 'code', color: 'from-blue-500 to-blue-700', increase: '+12%' },
    { title: 'Docs Generated', value: '156', icon: 'document', color: 'from-purple-500 to-purple-700', increase: '+8%' },
    { title: 'Repos Connected', value: '7', icon: 'repo', color: 'from-green-500 to-green-700', increase: '+2' }
  ];
  
  const languageColors = {
    JavaScript: 'bg-yellow-500',
    Python: 'bg-blue-600',
    TypeScript: 'bg-blue-400',
    Ruby: 'bg-red-600',
    Go: 'bg-blue-300',
    Java: 'bg-orange-600'
  };
  
  const handleRepoClick = (repo) => {
    setSelectedRepo(repo);
  };

  return (
    <div className="pt-20 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-100">Welcome back, {username.split('@')[0]}</h1>
        <p className="text-gray-400">Here's what's happening with your projects</p>
      </div>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-6 mb-10 md:grid-cols-3">
        {statsCards.map((stat, index) => (
          <div key={index} className="relative overflow-hidden rounded-xl bg-gray-800 p-6 shadow-lg">
            <div className={`absolute -right-4 -top-4 h-24 w-24 rounded-full bg-gradient-to-br ${stat.color} opacity-20 blur-xl`}></div>
            <div className="flex justify-between">
              <div>
                <p className="text-sm font-medium text-gray-400">{stat.title}</p>
                <p className="mt-2 text-3xl font-bold text-white">{stat.value}</p>
                <p className="mt-1 text-sm font-medium text-green-400">{stat.increase}</p>
              </div>
              <div className={`rounded-lg bg-gradient-to-br ${stat.color} p-3 shadow-lg`}>
                {stat.icon === 'code' && (
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                  </svg>
                )}
                {stat.icon === 'document' && (
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                )}
                {stat.icon === 'repo' && (
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path>
                  </svg>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
        {/* Recent Repositories */}
        <div className="lg:col-span-2">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-100">Recent Repositories</h2>
            <button className="rounded-lg bg-gray-800 px-4 py-2 text-sm font-medium text-gray-300 transition-colors hover:bg-gray-700">
              View all
            </button>
          </div>
          
          <div className="space-y-4">
            {recentRepos.map(repo => (
              <div 
                key={repo.id} 
                className={`group cursor-pointer rounded-xl bg-gray-800 p-5 transition-all hover:bg-gray-750 ${selectedRepo?.id === repo.id ? 'ring-2 ring-blue-500' : ''}`}
                onClick={() => handleRepoClick(repo)}
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
                        <span className={`mr-2 h-3 w-3 rounded-full ${languageColors[repo.language]}`}></span>
                        <span className="text-xs text-gray-400">{repo.language}</span>
                        <span className="mx-2 text-gray-600">•</span>
                        <span className="text-xs text-gray-400">Updated {repo.lastUpdated}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <div className="flex items-center mr-4">
                      <svg className="mr-1 h-4 w-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                      </svg>
                      <span className="text-xs font-medium text-gray-400">{repo.stars}</span>
                    </div>
                    <Link 
                      to="/repo-structure"
                      className="rounded-full bg-gray-700 p-1.5 text-gray-400 transition-colors hover:bg-gray-600 hover:text-white"
                    >
                      <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
                      </svg>
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-8">
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-100">Recent Activities</h2>
            </div>
            
            <div className="relative">
              <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-700"></div>
              
              <div className="space-y-8">
                <div className="relative pl-10">
                  <div className="absolute left-0 mt-1.5 h-8 w-8 rounded-full bg-blue-900 text-blue-500 flex items-center justify-center">
                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                  </div>
                  <div className="rounded-lg bg-gray-800 p-4">
                    <p className="text-sm text-gray-300">
                      Generated documentation for <span className="font-medium text-blue-400">api-service</span>
                    </p>
                    <p className="mt-1 text-xs text-gray-500">Today, 11:32 AM</p>
                  </div>
                </div>
                
                <div className="relative pl-10">
                  <div className="absolute left-0 mt-1.5 h-8 w-8 rounded-full bg-purple-900 text-purple-500 flex items-center justify-center">
                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                    </svg>
                  </div>
                  <div className="rounded-lg bg-gray-800 p-4">
                    <p className="text-sm text-gray-300">
                      Code analyzed for <span className="font-medium text-blue-400">ml-model-deployment</span>
                    </p>
                    <p className="mt-1 text-xs text-gray-500">Yesterday, 3:15 PM</p>
                  </div>
                </div>
                
                <div className="relative pl-10">
                  <div className="absolute left-0 mt-1.5 h-8 w-8 rounded-full bg-green-900 text-green-500 flex items-center justify-center">
                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                    </svg>
                  </div>
                  <div className="rounded-lg bg-gray-800 p-4">
                    <p className="text-sm text-gray-300">
                      Added new repository <span className="font-medium text-blue-400">mobile-app-api</span>
                    </p>
                    <p className="mt-1 text-xs text-gray-500">3 days ago</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Quick Actions */}
        <div>
          <div className="mb-6">
            <h2 className="text-xl font-bold text-gray-100">Quick Actions</h2>
          </div>
          
          <div className="space-y-4">
            <div className="group cursor-pointer rounded-xl bg-gradient-to-br from-blue-500 to-blue-700 p-5 shadow-lg transition-all hover:shadow-blue-500/20">
              <div className="flex items-center">
                <div className="mr-4 rounded-lg bg-white bg-opacity-20 p-3">
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-white">Add Repository</h3>
                  <p className="text-sm text-blue-100">Connect a new GitHub repository</p>
                </div>
              </div>
            </div>
            
            <div className="group cursor-pointer rounded-xl bg-gradient-to-br from-purple-500 to-purple-700 p-5 shadow-lg transition-all hover:shadow-purple-500/20">
              <div className="flex items-center">
                <div className="mr-4 rounded-lg bg-white bg-opacity-20 p-3">
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-white">Generate Documentation</h3>
                  <p className="text-sm text-purple-100">Create docs for your code</p>
                </div>
              </div>
            </div>
            
            <div className="group cursor-pointer rounded-xl bg-gradient-to-br from-green-500 to-green-700 p-5 shadow-lg transition-all hover:shadow-green-500/20">
              <div className="flex items-center">
                <div className="mr-4 rounded-lg bg-white bg-opacity-20 p-3">
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-white">Explain Code</h3>
                  <p className="text-sm text-green-100">Get insights into your code</p>
                </div>
              </div>
            </div>
          </div>
          
          {/* Pro Features */}
          <div className="mt-8 rounded-xl bg-gradient-to-br from-gray-800 to-gray-900 p-6">
            <div className="mb-4 flex justify-between">
              <h3 className="font-bold text-gray-100">Pro Features</h3>
              <span className="rounded-full bg-gray-700 px-2 py-0.5 text-xs font-medium text-gray-300">Free Trial</span>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <span className="text-sm text-gray-300">Advanced code analysis</span>
              </div>
              <div className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <span className="text-sm text-gray-300">Team collaboration</span>
              </div>
              <div className="flex items-center">
                <svg className="mr-2 h-5 w-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <span className="text-sm text-gray-300">Custom integrations</span>
              </div>
            </div>
            
            <button className="mt-6 w-full rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 py-2 text-sm font-medium text-white transition-colors hover:from-blue-600 hover:to-purple-700">
              Upgrade Now
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;