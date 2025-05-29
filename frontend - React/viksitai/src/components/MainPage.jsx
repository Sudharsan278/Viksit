import React, { useState } from 'react';
import { Github, Eye, Play, Brain, Users, Zap, Code2, GitBranch, MessageSquare, Star, TrendingUp, Search, Plus } from 'lucide-react';
import { Link } from 'react-router';

const MainPage = ({ username }) => {
  const [activeTab, setActiveTab] = useState('explore');

  const coreFeatures = [
    {
      icon: <Eye className="w-8 h-8" />,
      title: "Repository Visualization",
      description: "Interactive tree view and dependency graphs to understand code structure at a glance",
      gradient: "from-slate-600 to-slate-700",
      hoverGradient: "hover:from-slate-500 hover:to-slate-600",
      iconBg: "bg-blue-500/20",
      link : 'repo-structure'
    },
    {
      icon: <Play className="w-8 h-8" />,
      title: "Code Compilation",
      description: "Compile and run code directly in the browser with real-time output and error handling",
      gradient: "from-blue-600 to-indigo-700",
      hoverGradient: "hover:from-blue-500 hover:to-indigo-600",
      iconBg: "bg-blue-400/20",
      link : 'code-editor'
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI Code Analysis",
      description: "Powered by Groq AI for intelligent code review, optimization suggestions, and bug detection",
      gradient: "from-indigo-600 to-purple-700",
      hoverGradient: "hover:from-indigo-500 hover:to-purple-600",
      iconBg: "bg-purple-400/20",
      link : 'code-editor'
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Developer Community",
      description: "Connect with developers worldwide, share insights, and get expert guidance on your projects",
      gradient: "from-slate-700 to-gray-700",
      hoverGradient: "hover:from-slate-600 hover:to-gray-600",
      iconBg: "bg-slate-400/20",
      link : 'community'
    }
  ];

  const quickActions = [
    {
      icon: <Github className="w-6 h-6" />,
      title: "Analyze Repository",
      subtitle: "Enter GitHub URL",
      color: "bg-slate-700 hover:bg-slate-600 border-slate-600",
      action: "analyze"
    },
    {
      icon: <Code2 className="w-6 h-6" />,
      title: "Quick Compile",
      subtitle: "Paste & run code",
      color: "bg-blue-700 hover:bg-blue-600 border-blue-600",
      action: "compile"
    },
    {
      icon: <MessageSquare className="w-6 h-6" />,
      title: "Join Community",
      subtitle: "Chat with devs",
      color: "bg-indigo-700 hover:bg-indigo-600 border-indigo-600",
      action: "community"
    },
    {
      icon: <Plus className="w-6 h-6" />,
      title: "New Project",
      subtitle: "Start fresh",
      color: "bg-purple-700 hover:bg-purple-600 border-purple-600",
      action: "create"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-900 mt-20">
      {/* Refined animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-8 animate-pulse"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-8 animate-pulse animation-delay-2000"></div>
        <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-8 animate-pulse animation-delay-4000"></div>
      </div>

      <div className="relative z-10 px-4 sm:px-6 lg:px-8 pt-8 pb-12">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 bg-slate-800 border border-slate-600 rounded-full mb-6">
            <Zap className="w-4 h-4 text-blue-400 mr-2" />
            <span className="text-sm text-slate-100 font-medium">Powered by AI & Community</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Code
            </span>
            <span className="text-white"> meets </span>
            <span className="bg-gradient-to-r from-purple-400 via-indigo-400 to-blue-400 bg-clip-text text-transparent">
              Intelligence
            </span>
          </h1>
          
          <p className="text-xl text-slate-300 max-w-3xl mx-auto mb-8">
            Visualize GitHub repositories, compile code instantly, get AI-powered insights, 
            and connect with a vibrant developer community—all in one powerful platform.
          </p>

        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-16">
          {quickActions.map((action, index) => (
            <button
              key={index}
              className={`${action.color} p-6 rounded-2xl text-white hover:scale-105 transition-all duration-300 group shadow-lg hover:shadow-2xl border`}
            >
              <div className="flex items-center justify-between mb-3">
                {action.icon}
                <div className="w-2 h-2 bg-white/20 rounded-full group-hover:bg-white/40 transition-colors"></div>
              </div>
              <h3 className="font-semibold text-lg mb-1">{action.title}</h3>
              <p className="text-sm opacity-80">{action.subtitle}</p>
            </button>
          ))}
        </div>

        {/* Core Features */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Everything you need to understand code
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              From visualization to compilation, AI analysis to community support—we've got you covered.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {coreFeatures.map((feature, index) => (
              <div
                key={index}
                className={`bg-gradient-to-br ${feature.gradient} ${feature.hoverGradient} p-8 rounded-3xl text-white transition-all duration-500 hover:scale-105 group shadow-2xl border border-slate-600/50`}
              >
                <div className={`${feature.iconBg} w-16 h-16 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-white/20 transition-colors backdrop-blur-sm`}>
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold mb-4">{feature.title}</h3>
                <p className="text-white/90 leading-relaxed">{feature.description}</p>
                <div className="mt-6 flex items-center text-white/70 group-hover:text-white/90 transition-colors">
                  <Link to={`/${feature.link}`} ><span className="text-sm font-medium">Learn more</span></Link>
                    <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                    </svg>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Community Stats */}
        <div className="bg-slate-800/50 border border-slate-700 rounded-3xl p-8 mb-16 backdrop-blur-sm">
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold text-white mb-2">Join Our Growing Community</h3>
            <p className="text-slate-400">Developers helping developers, powered by AI</p>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl mb-4">
                <GitBranch className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-2xl font-bold text-white mb-2">50K+</h4>
              <p className="text-slate-400">Repositories Analyzed</p>
            </div>
            
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-2xl mb-4">
                <Users className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-2xl font-bold text-white mb-2">12K+</h4>
              <p className="text-slate-400">Active Developers</p>
            </div>
            
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl mb-4">
                <MessageSquare className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-2xl font-bold text-white mb-2">100K+</h4>
              <p className="text-slate-400">Community Messages</p>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <div className="bg-slate-800/50 border border-slate-700 rounded-3xl p-12 shadow-2xl backdrop-blur-sm">
            <h3 className="text-3xl font-bold text-white mb-4">Ready to dive deeper into code?</h3>
            <p className="text-slate-300 text-lg mb-8 max-w-2xl mx-auto">
              Start by analyzing your first repository or join our community to connect with fellow developers.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              
              <Link to='/repo-structure'>
                <button className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg hover:shadow-xl">
                  Analyze Your First Repo
                </button>
              </Link>
              
              <Link to='/community'>
                <button className="px-8 py-4 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-xl transition-colors border border-slate-600 shadow-lg hover:shadow-xl">
                  Join Community Chat
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;