import React, { useState, useEffect } from 'react';

const AboutPage = () => {
  const [activeFeature, setActiveFeature] = useState(0);
  const [isVisible, setIsVisible] = useState({});

  
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(prev => ({
              ...prev,
              [entry.target.id]: true
            }));
          }
        });
      },
      { threshold: 0.1 }
    );

    document.querySelectorAll('[data-animate]').forEach((el) => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const features = [
    {
      id: 1,
      title: "AI Help",
      description: "Viksit.AI is like a smart coding buddy that answers your questions about the code.",
      icon: "🤖",
      gradient: "from-blue-500 to-cyan-500"
    },
    {
      id: 2,
      title: "Auto Documentation",
      description: "It makes documentation for your codebase automatically, so it's easier to understand.",
      icon: "📚",
      gradient: "from-purple-500 to-pink-500"
    },
    {
      id: 3,
      title: "Build with Real-time Output",
      description: "Enter a prompt to generate code using AI, then seamlessly integrate and display the output on top of your existing codebase.",
      icon: "⚡",
      gradient: "from-orange-500 to-red-500"
    },
    {
      id: 4,
      title: "Developer Hub",
      description: "Connect with fellow Devs through vibrant community and sharpen your skills.",
      icon: "👥",
      gradient: "from-green-500 to-emerald-500"
    },
    {
      id: 5,
      title: "Developer Resources",
      description: "Provides query specific resources aligning with current trending technologies.",
      icon: "🎯",
      gradient: "from-indigo-500 to-purple-500"
    }
  ];

  const stats = [
    { value: "60%", label: "Time spent reading code", subtext: "Current developer struggle" },
    { value: "10x", label: "Faster code understanding", subtext: "With Viksit.AI" },
    { value: "100%", label: "Automated documentation", subtext: "No manual effort" },
    { value: "24/7", label: "AI assistance", subtext: "Always available" }
  ];

  const targetUsers = [
    { icon: "👨‍💻", title: "Developers", desc: "Professional software developers" },
    { icon: "👷‍♂️", title: "Engineers", desc: "Technical engineers across domains" },
    { icon: "🎓", title: "Students", desc: "Computer science students" },
    { icon: "👨‍🏫", title: "Educators", desc: "Programming instructors" }
  ];

  return (
    <div className="pt-16 bg-gray-900 text-white overflow-hidden">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 to-purple-900/20"></div>
        <div className="relative max-w-7xl mx-auto text-center">
          <div 
            id="hero"
            data-animate
            className={`transition-all duration-1000 ${
              isVisible.hero ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-purple-500 to-cyan-400 bg-clip-text text-transparent">
              VIKSIT.AI
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto leading-relaxed">
              Empowering developers to understand, document, and build with code faster than ever before
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <span className="px-4 py-2 bg-blue-500/20 border border-blue-500/30 rounded-full text-blue-300 text-sm">
                AI-Powered
              </span>
              <span className="px-4 py-2 bg-purple-500/20 border border-purple-500/30 rounded-full text-purple-300 text-sm">
                Real-time
              </span>
              <span className="px-4 py-2 bg-green-500/20 border border-green-500/30 rounded-full text-green-300 text-sm">
                Community-Driven
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-red-900/10 to-orange-900/10">
        <div className="max-w-7xl mx-auto">
          <div 
            id="problem"
            data-animate
            className={`transition-all duration-1000 delay-200 ${
              isVisible.problem ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <h2 className="text-4xl font-bold text-center mb-16 text-red-400">The Problem We Solve</h2>
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <div className="text-6xl font-bold text-red-500 mb-4">60%</div>
                <p className="text-xl text-gray-300 mb-6">
                  Developers spend 60% of their time reading and understanding code
                </p>
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-400">Reading large, complex and undocumented codebases</p>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-400">Understanding other developer's code</p>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-400">New developers struggling with existing codebases</p>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-400">Breaking socio-economic barriers for developers</p>
                  </div>
                </div>
              </div>
              <div className="relative">
                <div className="bg-gray-800 p-6 rounded-xl border border-red-500/30">
                  <div className="text-red-400 mb-4">Current Developer Experience:</div>
                  <div className="space-y-2 text-sm font-mono">
                    <div className="text-gray-500">// Hundreds of lines of undocumented code</div>
                    <div className="text-gray-300">function complexFunction() {`{`}</div>
                    <div className="text-gray-500 ml-4">// What does this do? 🤔</div>
                    <div className="text-gray-300 ml-4">return someComplexLogic;</div>
                    <div className="text-gray-300">{`}`}</div>
                    <div className="text-red-400 mt-4">❌ Time wasted: Hours of confusion</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div 
            id="solution"
            data-animate
            className={`transition-all duration-1000 delay-300 ${
              isVisible.solution ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <h2 className="text-4xl font-bold text-center mb-16 text-green-400">Our Solution</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-gradient-to-br from-blue-900/30 to-blue-800/30 p-6 rounded-xl border border-blue-500/30">
                <div className="text-3xl mb-4">🚀</div>
                <h3 className="text-xl font-bold mb-3 text-blue-400">Build with Real-time Output</h3>
                <p className="text-gray-300">Prompt, Generate and Run. See your code come to life instantly.</p>
              </div>
              <div className="bg-gradient-to-br from-purple-900/30 to-purple-800/30 p-6 rounded-xl border border-purple-500/30">
                <div className="text-3xl mb-4">⚙️</div>
                <h3 className="text-xl font-bold mb-3 text-purple-400">Automated Workflow</h3>
                <p className="text-gray-300">Debugging, optimization and precise code analysis automatically.</p>
              </div>
              <div className="bg-gradient-to-br from-green-900/30 to-green-800/30 p-6 rounded-xl border border-green-500/30">
                <div className="text-3xl mb-4">🤝</div>
                <h3 className="text-xl font-bold mb-3 text-green-400">Comprehensive Support</h3>
                <p className="text-gray-300">Bridging knowledge gaps by linking developers with expert mentors.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-800/50">
        <div className="max-w-7xl mx-auto">
          <div 
            id="stats"
            data-animate
            className={`transition-all duration-1000 delay-400 ${
              isVisible.stats ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <h2 className="text-4xl font-bold text-center mb-16">Impact & Results</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-4xl md:text-5xl font-bold text-transparent bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text mb-2">
                    {stat.value}
                  </div>
                  <div className="text-lg font-semibold text-gray-300 mb-1">{stat.label}</div>
                  <div className="text-sm text-gray-500">{stat.subtext}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div 
            id="features"
            data-animate
            className={`transition-all duration-1000 delay-500 ${
              isVisible.features ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <h2 className="text-4xl font-bold text-center mb-16">Features</h2>
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div className="space-y-4">
                {features.map((feature, index) => (
                  <div
                    key={feature.id}
                    className={`p-6 rounded-xl cursor-pointer transition-all duration-300 ${
                      activeFeature === index
                        ? 'bg-gray-800 border-2 border-blue-500'
                        : 'bg-gray-800/50 border border-gray-700 hover:border-gray-600'
                    }`}
                    onClick={() => setActiveFeature(index)}
                  >
                    <div className="flex items-start space-x-4">
                      <div className={`text-2xl p-3 rounded-lg bg-gradient-to-r ${feature.gradient}`}>
                        {feature.icon}
                      </div>
                      <div>
                        <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                        <p className="text-gray-400">{feature.description}</p>
                      </div>
                    </div>
                    <div className={`text-right text-2xl font-bold bg-gradient-to-r ${feature.gradient} bg-clip-text text-transparent`}>
                      0{feature.id}
                    </div>
                  </div>
                ))}
              </div>
              <div className="relative">
                <div className="bg-gray-800 p-8 rounded-xl border border-gray-700">
                  <div className={`text-6xl mb-6 p-4 rounded-xl bg-gradient-to-r ${features[activeFeature].gradient} bg-opacity-20 text-center`}>
                    {features[activeFeature].icon}
                  </div>
                  <h3 className="text-2xl font-bold mb-4">{features[activeFeature].title}</h3>
                  <p className="text-gray-300 text-lg leading-relaxed">{features[activeFeature].description}</p>
                  <div className="mt-6 p-4 bg-gray-900 rounded-lg">
                    <div className="text-green-400 text-sm font-mono">
                      // {features[activeFeature].title} in action
                    </div>
                    <div className="text-gray-400 text-sm font-mono mt-1">
                      viksit.ai --feature="{features[activeFeature].title.toLowerCase().replace(/\s+/g, '-')}"
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

    
      {/* Target Users Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div 
            id="users"
            data-animate
            className={`transition-all duration-1000 delay-700 ${
              isVisible.users ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <h2 className="text-4xl font-bold text-center mb-16">Who Can Benefit</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {targetUsers.map((user, index) => (
                <div key={index} className="text-center group hover:transform hover:scale-105 transition-all duration-300">
                  <div className="text-6xl mb-4 group-hover:animate-bounce">{user.icon}</div>
                  <h3 className="text-xl font-bold mb-2 text-blue-400">{user.title}</h3>
                  <p className="text-gray-400 text-sm">{user.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-900/20 to-purple-900/20">
        <div className="max-w-4xl mx-auto text-center">
          <div 
            id="cta"
            data-animate
            className={`transition-all duration-1000 delay-800 ${
              isVisible.cta ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
            }`}
          >
            <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Development Experience?</h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of developers who are already building faster and smarter with Viksit.AI
            </p>
            </div>
        </div>
      </section>
    </div>
  );
};

export default AboutPage;