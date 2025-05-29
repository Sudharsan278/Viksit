import React, { useState, useEffect } from 'react';
import { Search, TrendingUp, Code, Globe, Cpu, Smartphone, Database, Cloud, Lock, Zap, BookOpen, ExternalLink, Star, Calendar, Users } from 'lucide-react';

const ResourcesPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchType, setSearchType] = useState('Search');

  const BASE_URL = 'https://viksit.onrender.com/';

 
  const trendingTechnologies = [
    {
      id: 1,
      name: "Artificial Intelligence & Machine Learning",
      icon: <Cpu className="w-6 h-6" />,
      description: "Advanced AI models, neural networks, and machine learning frameworks",
      resources: [
        { title: "TensorFlow Documentation", url: "https://tensorflow.org", type: "Official Docs" },
        { title: "PyTorch Tutorials", url: "https://pytorch.org/tutorials", type: "Tutorial" },
        { title: "OpenAI API Guide", url: "https://openai.com/api", type: "API" },
        { title: "Hugging Face Models", url: "https://huggingface.co/models", type: "Models" }
      ],
      category: "ai",
      popularity: 95,
      growth: "+45%"
    },
    {
      id: 2,
      name: "Cloud Computing & DevOps",
      icon: <Cloud className="w-6 h-6" />,
      description: "Cloud platforms, containerization, and deployment automation",
      resources: [
        { title: "AWS Documentation", url: "https://docs.aws.amazon.com", type: "Official Docs" },
        { title: "Docker Getting Started", url: "https://docker.com/get-started", type: "Tutorial" },
        { title: "Kubernetes Basics", url: "https://kubernetes.io/docs", type: "Documentation" },
        { title: "Terraform Guides", url: "https://terraform.io/guides", type: "Guide" }
      ],
      category: "cloud",
      popularity: 88,
      growth: "+32%"
    },
    {
      id: 3,
      name: "Web Development Frameworks",
      icon: <Globe className="w-6 h-6" />,
      description: "Modern frontend and backend frameworks for web applications",
      resources: [
        { title: "React Documentation", url: "https://react.dev", type: "Official Docs" },
        { title: "Next.js Learn", url: "https://nextjs.org/learn", type: "Tutorial" },
        { title: "Vue.js Guide", url: "https://vuejs.org/guide", type: "Guide" },
        { title: "Django Tutorial", url: "https://djangoproject.com/start", type: "Tutorial" }
      ],
      category: "web",
      popularity: 92,
      growth: "+28%"
    },
    {
      id: 4,
      name: "Mobile Development",
      icon: <Smartphone className="w-6 h-6" />,
      description: "Cross-platform and native mobile app development",
      resources: [
        { title: "React Native Docs", url: "https://reactnative.dev", type: "Official Docs" },
        { title: "Flutter Documentation", url: "https://flutter.dev/docs", type: "Documentation" },
        { title: "Swift Playgrounds", url: "https://developer.apple.com/swift-playgrounds", type: "Learning" },
        { title: "Kotlin for Android", url: "https://kotlinlang.org/docs/android-overview.html", type: "Guide" }
      ],
      category: "mobile",
      popularity: 78,
      growth: "+22%"
    },
    {
      id: 5,
      name: "Database Technologies",
      icon: <Database className="w-6 h-6" />,
      description: "Modern databases, data warehousing, and analytics platforms",
      resources: [
        { title: "PostgreSQL Tutorial", url: "https://postgresql.org/docs", type: "Tutorial" },
        { title: "MongoDB University", url: "https://university.mongodb.com", type: "Course" },
        { title: "Redis Documentation", url: "https://redis.io/documentation", type: "Documentation" },
        { title: "Apache Kafka Guide", url: "https://kafka.apache.org/documentation", type: "Guide" }
      ],
      category: "database",
      popularity: 73,
      growth: "+18%"
    },
    {
      id: 6,
      name: "Cybersecurity & Privacy",
      icon: <Lock className="w-6 h-6" />,
      description: "Security frameworks, encryption, and privacy protection tools",
      resources: [
        { title: "OWASP Top 10", url: "https://owasp.org/www-project-top-ten", type: "Security Guide" },
        { title: "Let's Encrypt Guide", url: "https://letsencrypt.org/getting-started", type: "Tutorial" },
        { title: "OpenSSL Cookbook", url: "https://openssl-cookbook.com", type: "Guide" },
        { title: "Wireshark Documentation", url: "https://wireshark.org/docs", type: "Documentation" }
      ],
      category: "security",
      popularity: 85,
      growth: "+35%"
    }
  ];

  const categories = [
    { id: 'all', name: 'All Technologies', icon: <TrendingUp className="w-4 h-4" /> },
    { id: 'ai', name: 'AI & ML', icon: <Cpu className="w-4 h-4" /> },
    { id: 'cloud', name: 'Cloud & DevOps', icon: <Cloud className="w-4 h-4" /> },
    { id: 'web', name: 'Web Development', icon: <Globe className="w-4 h-4" /> },
    { id: 'mobile', name: 'Mobile', icon: <Smartphone className="w-4 h-4" /> },
    { id: 'database', name: 'Databases', icon: <Database className="w-4 h-4" /> },
    { id: 'security', name: 'Security', icon: <Lock className="w-4 h-4" /> }
  ];

  const filteredTechnologies = selectedCategory === 'all' 
    ? trendingTechnologies 
    : trendingTechnologies.filter(tech => tech.category === selectedCategory);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setIsSearching(true);
    try {
      const response = await fetch(`${BASE_URL}/api/google-search/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery,
          search_type: searchType
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setSearchResults(data.raw_results || []);
      } else {
        // Fallback mock data for demo
        setSearchResults([
          {
            title: `${searchQuery} - Documentation`,
            link: `https://example.com/${searchQuery.toLowerCase()}`,
            snippet: `Comprehensive documentation and tutorials for ${searchQuery}...`,
            displayLink: "example.com"
          },
          {
            title: `${searchQuery} Best Practices`,
            link: `https://example.com/${searchQuery.toLowerCase()}-guide`,
            snippet: `Learn the best practices and common patterns for ${searchQuery} development...`,
            displayLink: "example.com"
          }
        ]);
      }
    } catch (error) {
      console.error('Search error:', error);
      // Mock results for demo
      setSearchResults([
        {
          title: `${searchQuery} - Getting Started`,
          link: `https://example.com/${searchQuery.toLowerCase()}`,
          snippet: `Get started with ${searchQuery} in this comprehensive guide...`,
          displayLink: "example.com"
        }
      ]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white pt-20 pb-12 px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <BookOpen className="w-8 h-8 text-blue-400" />
          <h1 className="text-3xl font-bold text-gray-100">Technology Resources Hub</h1>
        </div>
        <p className="text-lg text-gray-400">Discover trending technologies, comprehensive documentation, and curated learning resources</p>
      </div>

      {/* Search Section */}
      <div className="mb-10">
        <div className="bg-gray-800 rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-bold text-gray-100 mb-6 flex items-center gap-2">
            <Search className="w-6 h-6 text-blue-400" />
            Search
          </h2>
          
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="flex-1">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Search for technologies, tutorials, documentation..."
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20"
              />
            </div>
            <button
              onClick={handleSearch}
              disabled={isSearching || !searchQuery.trim()}
              className="px-8 py-3 bg-gradient-to-r from-blue-500 to-blue-700 rounded-lg font-medium hover:from-blue-600 hover:to-blue-800 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isSearching ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <Search className="w-5 h-5" />
              )}
              {isSearching ? 'Searching...' : 'Search'}
            </button>
          </div>

          {/* Search Results */}
          {searchResults.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-blue-400">Search Results</h3>
              {searchResults.map((result, index) => (
                <div key={index} className="bg-gray-700 rounded-lg p-4">
                  <a
                    href={result.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 font-medium text-lg flex items-center gap-2"
                  >
                    {result.title}
                    <ExternalLink className="w-4 h-4" />
                  </a>
                  <p className="text-green-400 text-sm mt-1">{result.displayLink}</p>
                  <p className="text-gray-300 mt-2">{result.snippet}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Category Filter */}
      <div className="mb-8">
        <div className="flex flex-wrap gap-3">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                selectedCategory === category.id
                  ? 'bg-gradient-to-r from-blue-500 to-blue-700 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
            >
              {category.icon}
              {category.name}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
        {/* Trending Technologies */}
        <div className="lg:col-span-2">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-100 flex items-center gap-2">
              <TrendingUp className="w-6 h-6 text-blue-400" />
              Trending Technologies
            </h2>
          </div>
          
          <div className="space-y-6">
            {filteredTechnologies.map((tech) => (
              <div key={tech.id} className="bg-gray-800 rounded-xl p-6 shadow-lg hover:bg-gray-750 transition-all duration-200">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="p-3 bg-gray-700 rounded-lg">
                      {tech.icon}
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-gray-100">{tech.name}</h3>
                      <div className="flex items-center gap-4 mt-1">
                        <div className="flex items-center gap-1">
                          <Star className="w-4 h-4 text-yellow-400" />
                          <span className="text-sm text-gray-400">{tech.popularity}%</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <TrendingUp className="w-4 h-4 text-green-400" />
                          <span className="text-sm text-green-400">{tech.growth}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <p className="text-gray-400 mb-4">{tech.description}</p>
                
                <div className="space-y-3">
                  <h4 className="font-medium text-blue-400 flex items-center gap-2">
                    <BookOpen className="w-4 h-4" />
                    Key Resources
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {tech.resources.map((resource, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors">
                        <div>
                          <a
                            href={resource.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-400 hover:text-blue-300 font-medium flex items-center gap-2 text-sm"
                          >
                            {resource.title}
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        </div>
                        <span className="text-xs px-2 py-1 bg-gray-600 text-gray-300 rounded">
                          {resource.type}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Access */}
        <div>
          <div className="mb-6">
            <h2 className="text-xl font-bold text-gray-100 flex items-center gap-2">
              <Zap className="w-6 h-6 text-yellow-400" />
              Quick Access
            </h2>
          </div>
          
          <div className="bg-gray-800 rounded-xl p-6">
            
            <div className="space-y-4">
              <div className="bg-gray-700 rounded-lg p-4">
                <h4 className="font-medium text-blue-400 mb-2">Developer Communities</h4>
                <div className="space-y-2">
                  <a href="https://stackoverflow.com" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-300 hover:text-white flex items-center gap-2">
                    <Users className="w-3 h-3" /> Stack Overflow
                  </a>
                  <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-300 hover:text-white flex items-center gap-2">
                    <Code className="w-3 h-3" /> GitHub
                  </a>
                  <a href="https://dev.to" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-300 hover:text-white flex items-center gap-2">
                    <BookOpen className="w-3 h-3" /> Dev.to
                  </a>
                </div>
              </div>
              
              <div className="bg-gray-700 rounded-lg p-4">
                <h4 className="font-medium text-purple-400 mb-2">Learning Platforms</h4>
                <div className="space-y-2">
                  <a href="https://coursera.org" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-300 hover:text-white flex items-center gap-2">
                    <BookOpen className="w-3 h-3" /> Coursera
                  </a>
                  <a href="https://udemy.com" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-300 hover:text-white flex items-center gap-2">
                    <BookOpen className="w-3 h-3" /> Udemy
                  </a>
                  <a href="https://pluralsight.com" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-300 hover:text-white flex items-center gap-2">
                    <BookOpen className="w-3 h-3" /> Pluralsight
                  </a>
                </div>
              </div>
              
              <div className="bg-gray-700 rounded-lg p-4">
                <h4 className="font-medium text-green-400 mb-2">Tech News</h4>
                <div className="space-y-2">
                  <a href="https://techcrunch.com" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-300 hover:text-white flex items-center gap-2">
                    <Calendar className="w-3 h-3" /> TechCrunch
                  </a>
                  <a href="https://hackernews.com" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-300 hover:text-white flex items-center gap-2">
                    <Calendar className="w-3 h-3" /> Hacker News
                  </a>
                  <a href="https://arstechnica.com" target="_blank" rel="noopener noreferrer" className="text-sm text-gray-300 hover:text-white flex items-center gap-2">
                    <Calendar className="w-3 h-3" /> Ars Technica
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResourcesPage;