"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";

// Sample data for agents
const agents = [
  {
    id: 1,
    name: "Legal Agent",
    status: "active",
    icon: "/legal-agent.png",
    lastActivity: "Completed risk assessment (2 mins ago)",
    taskCount: 42,
    efficiency: 97,
  },
  {
    id: 2,
    name: "Business Advisor",
    status: "active",
    icon: "/ceo-agent.png",
    lastActivity: "Market analysis for eco-friendly trends (5 mins ago)",
    taskCount: 28,
    efficiency: 94,
  },
  {
    id: 3,
    name: "Design Analysis Agent",
    status: "active",
    icon: "/design-agent.png",
    lastActivity: "Generated design parameters for Acme Corp (1 min ago)",
    taskCount: 67,
    efficiency: 91,
  },
  {
    id: 4,
    name: "Production Planning Agent",
    status: "idle",
    icon: "/production-agent.png",
    lastActivity: "Optimized production workflow for batch #2234 (15 mins ago)",
    taskCount: 53,
    efficiency: 89,
  },
];

// Recent activities
const recentActivities = [
  {
    id: 1,
    agent: "Legal Agent",
    action: "Risk Assessment Completed",
    details: "Identified 2 potential compliance issues with recent marketing materials.",
    timestamp: "Today, 10:23 AM",
    severity: "medium",
  },
  {
    id: 2,
    agent: "Business Advisor",
    action: "Strategy Recommendation",
    details: "Suggested focusing on premium product tier based on market analysis.",
    timestamp: "Today, 9:45 AM",
    severity: "low",
  },
  {
    id: 3,
    agent: "Design Analysis Agent",
    action: "New Design Created",
    details: "Generated 3 concepts for Acme Corp's eco-friendly t-shirt campaign.",
    timestamp: "Today, 9:32 AM",
    severity: "none",
  },
  {
    id: 4,
    agent: "Legal Agent",
    action: "IP Conflict Detected",
    details: "Potential trademark issue identified in design #RT-7829. Suggested modifications provided.",
    timestamp: "Today, 9:17 AM",
    severity: "high",
  },
  {
    id: 5,
    agent: "Production Planning Agent",
    action: "Production Schedule Optimized",
    details: "Rearranged production queue for 15% improvement in throughput.",
    timestamp: "Today, 8:50 AM",
    severity: "none",
  },
];

// Active design projects
const activeProjects = [
  {
    id: "PRJ-2301",
    client: "Acme Corporation",
    title: "Eco-friendly Corporate T-shirts",
    status: "In Production",
    progress: 75,
    thumbnail: "/acme-tshirt-preview.jpg",
    dueDate: "Jun 15, 2025",
  },
  {
    id: "PRJ-2302",
    client: "Green Earth Foundation",
    title: "Ocean Conservation Campaign",
    status: "Design Review",
    progress: 40,
    thumbnail: "/green-earth-preview.jpg",
    dueDate: "Jun 20, 2025",
  },
  {
    id: "PRJ-2303",
    client: "Tech Innovators Inc",
    title: "Annual Conference Merchandise",
    status: "Legal Review",
    progress: 25,
    thumbnail: "/tech-innovators-preview.jpg",
    dueDate: "Jun 30, 2025",
  },
];

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");
  const [isLoading, setIsLoading] = useState(true);
  const [showRiskAssessment, setShowRiskAssessment] = useState(false);
  const [assessmentProgress, setAssessmentProgress] = useState(0);
  const [assessmentResults, setAssessmentResults] = useState(null);
  
  useEffect(() => {
    // Simulate loading data
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1500);
    
    return () => clearTimeout(timer);
  }, []);
  
  const runRiskAssessment = () => {
    setShowRiskAssessment(true);
    setAssessmentProgress(0);
    
    const interval = setInterval(() => {
      setAssessmentProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setAssessmentResults({
            timestamp: new Date().toISOString(),
            riskScore: 78,
            issues: [
              {
                id: "IP-001",
                severity: "high",
                description: "Potential trademark infringement in design #RT-7829",
                recommendation: "Modify wave pattern to increase uniqueness",
                zerobudgetSolution: "Use free alternative design elements from public domain sources"
              },
              {
                id: "DP-002",
                severity: "medium",
                description: "Customer data handling procedures may not comply with GDPR",
                recommendation: "Update privacy policy and data processing workflows",
                zerobudgetSolution: "Implement free GDPR compliance templates"
              },
              {
                id: "SC-003",
                severity: "low",
                description: "Website cookie consent mechanism is outdated",
                recommendation: "Implement new cookie consent UI",
                zerobudgetSolution: "Use open-source cookie consent solution"
              }
            ]
          });
          return 100;
        }
        return prev + 5;
      });
    }, 200);
    
    return () => clearInterval(interval);
  };
  
  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      {/* Dashboard Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold mb-2">AI Agent Dashboard</h1>
              <p className="text-blue-100">Your intelligent team is working 24/7</p>
            </div>
            <div className="mt-4 md:mt-0 flex space-x-3">
              <button 
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md bg-white/20 hover:bg-white/30 focus:outline-none"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                </svg>
                New Design Request
              </button>
              <button 
                onClick={runRiskAssessment}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md bg-white/10 hover:bg-white/20 focus:outline-none"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
                Run Risk Assessment
              </button>
            </div>
          </div>
          
          {/* Dashboard Navigation Tabs */}
          <div className="mt-8 flex space-x-2 overflow-x-auto pb-1">
            <TabButton active={activeTab === "overview"} onClick={() => setActiveTab("overview")}>
              Overview
            </TabButton>
            <TabButton active={activeTab === "agents"} onClick={() => setActiveTab("agents")}>
              AI Agents
            </TabButton>
            <TabButton active={activeTab === "designs"} onClick={() => setActiveTab("designs")}>
              Designs
            </TabButton>
            <TabButton active={activeTab === "legal"} onClick={() => setActiveTab("legal")}>
              Legal Compliance
            </TabButton>
            <TabButton active={activeTab === "analytics"} onClick={() => setActiveTab("analytics")}>
              Analytics
            </TabButton>
          </div>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-12">
            <div className="w-16 h-16 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>
            <p className="mt-4 text-gray-500">Loading dashboard data...</p>
          </div>
        ) : (
          <>
            {/* Risk Assessment Modal */}
            {showRiskAssessment && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-auto">
                  <div className="p-6">
                    <div className="flex justify-between items-center mb-4">
                      <h2 className="text-2xl font-bold">Legal Risk Assessment</h2>
                      <button 
                        onClick={() => setShowRiskAssessment(false)}
                        className="text-gray-400 hover:text-gray-500"
                      >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                    
                    {assessmentProgress < 100 ? (
                      <div>
                        <p className="mb-4">The Legal Agent is analyzing your business operations...</p>
                        <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
                          <div 
                            className="bg-blue-600 h-4 rounded-full transition-all duration-300" 
                            style={{ width: `${assessmentProgress}%` }}
                          ></div>
                        </div>
                        <div className="text-sm text-gray-500 flex justify-between">
                          <span>Analyzing intellectual property...</span>
                          <span>{assessmentProgress}%</span>
                        </div>
                      </div>
                    ) : (
                      <div>
                        <div className="flex items-center mb-6">
                          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                            <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                            </svg>
                          </div>
                          <div>
                            <h3 className="text-xl font-bold">Risk Assessment Complete</h3>
                            <p className="text-gray-500">Your business has a {assessmentResults.riskScore}% compliance score</p>
                          </div>
                        </div>
                        
                        <h4 className="font-bold text-lg mb-3">Identified Issues</h4>
                        <div className="space-y-4 mb-6">
                          {assessmentResults.issues.map(issue => (
                            <div 
                              key={issue.id} 
                              className={`border-l-4 pl-4 py-2 ${
                                issue.severity === 'high' 
                                  ? 'border-red-500 bg-red-50' 
                                  : issue.severity === 'medium'
                                    ? 'border-yellow-500 bg-yellow-50'
                                    : 'border-blue-500 bg-blue-50'
                              }`}
                            >
                              <div className="flex justify-between">
                                <h5 className="font-bold">{issue.id}: {issue.description}</h5>
                                <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                                  issue.severity === 'high' 
                                    ? 'bg-red-100 text-red-800' 
                                    : issue.severity === 'medium'
                                      ? 'bg-yellow-100 text-yellow-800'
                                      : 'bg-blue-100 text-blue-800'
                                }`}>
                                  {issue.severity}
                                </span>
                              </div>
                              <p className="text-gray-700 mt-1">{issue.recommendation}</p>
                              <div className="mt-2 bg-white p-2 rounded border border-gray-200">
                                <p className="text-sm font-medium text-gray-800">Zero-Budget Solution:</p>
                                <p className="text-sm text-gray-600">{issue.zerobudgetSolution}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                        
                        <div className="flex justify-end space-x-3">
                          <button 
                            onClick={() => setShowRiskAssessment(false)}
                            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50"
                          >
                            Close
                          </button>
                          <button className="px-4 py-2 border border-transparent rounded-md text-white bg-blue-600 hover:bg-blue-700">
                            Generate Compliance Report
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          
            {/* Key Metrics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <MetricCard
                title="Active Projects"
                value="3"
                change="+2"
                description="2 in progress, 1 pending review"
                icon="projects"
                color="blue"
              />
              <MetricCard
                title="Compliance Score"
                value="92%"
                change="+5%"
                description="Last updated: Today"
                icon="compliance"
                color="green"
              />
              <MetricCard
                title="Agent Activity"
                value="24"
                change="+8"
                description="Actions in the last 7 days"
                icon="activity"
                color="purple"
              />
              <MetricCard
                title="Designs Created"
                value="18"
                change="+3"
                description="This month"
                icon="designs"
                color="cyan"
              />
            </div>
            
            {/* Main Dashboard Content - Overview Tab */}
            {activeTab === "overview" && (
              <>
                {/* Agent Status Section */}
                <section className="mb-8">
                  <h2 className="text-2xl font-bold mb-4">AI Agent Status</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {agents.map((agent) => (
                      <div key={agent.id} className="bg-white rounded-xl shadow-sm p-4">
                        <div className="flex items-center mb-3">
                          <div className="bg-gray-100 p-2 rounded-lg mr-3">
                            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                              <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                              </svg>
                            </div>
                          </div>
                          <div>
                            <h4 className="font-bold">{agent.name}</h4>
                            <div className="flex items-center">
                              <span className={`inline-block w-2 h-2 rounded-full mr-1 ${
                                agent.status === "active" ? "bg-green-500" : "bg-yellow-500"
                              }`}></span>
                              <span className="text-xs text-gray-500">{agent.status === "active" ? "Active" : "Idle"}</span>
                            </div>
                          </div>
                        </div>
                        <p className="text-sm text-gray-600 line-clamp-2">{agent.lastActivity}</p>
                      </div>
                    ))}
                  </div>
                </section>
                
                {/* Active Projects Section */}
                <section className="mb-8">
                  <h2 className="text-2xl font-bold mb-4">Active Projects</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {activeProjects.map((project) => (
                      <div key={project.id} className="bg-white rounded-xl shadow-sm overflow-hidden">
                        <div className="h-48 w-full bg-gray-200 relative">
                          <div className="absolute inset-0 flex items-center justify-center text-gray-400">
                            <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <span>Design Preview</span>
                          </div>
                        </div>
                        <div className="p-4">
                          <div className="flex justify-between items-start">
                            <div>
                              <span className="text-xs text-gray-500">{project.id}</span>
                              <h3 className="font-bold">{project.title}</h3>
                              <p className="text-sm text-gray-600">{project.client}</p>
                            </div>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              project.status === "In Production" 
                                ? "bg-blue-100 text-blue-800" 
                                : project.status === "Design Review"
                                  ? "bg-purple-100 text-purple-800"
                                  : "bg-amber-100 text-amber-800"
                            }`}>
                              {project.status}
                            </span>
                          </div>
                          <div className="mt-4">
                            <div className="flex justify-between mb-1">
                              <span className="text-xs text-gray-500">Progress</span>
                              <span className="text-xs font-medium">{project.progress}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-blue-600 h-2 rounded-full" 
                                style={{ width: `${project.progress}%` }}
                              ></div>
                            </div>
                          </div>
                          <div className="mt-4 flex justify-between items-center">
                            <span className="text-xs text-gray-500">Due: {project.dueDate}</span>
                            <button className="text-blue-600 text-sm font-medium hover:text-blue-800">
                              View Details
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </section>
                
                {/* Recent Activity Section */}
                <section>
                  <h2 className="text-2xl font-bold mb-4">Recent Activity</h2>
                  <div className="bg-white rounded-xl shadow-sm overflow-hidden">
                    <div className="p-4">
                      <div className="space-y-6">
                        {recentActivities.map((activity) => (
                          <div 
                            key={activity.id} 
                            className={`flex border-l-4 pl-4 ${
                              activity.severity === "high" 
                                ? "border-red-500" 
                                : activity.severity === "medium"
                                  ? "border-yellow-500"
                                  : activity.severity === "low"
                                    ? "border-blue-500"
                                    : "border-gray-200"
                            }`}
                          >
                            <div className="mr-4 flex-shrink-0">
                              <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                                <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                              </div>
                            </div>
                            <div>
                              <div className="flex justify-between">
                                <p className="font-medium">{activity.agent}: {activity.action}</p>
                                <span className="text-sm text-gray-500">{activity.timestamp}</span>
                              </div>
                              <p className="text-gray-600 mt-1">{activity.details}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="border-t border-gray-100 p-4">
                      <button className="text-blue-600 font-medium hover:text-blue-800 flex items-center">
                        View All Activity
                        <svg className="w-5 h-5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </section>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
}

// Tab Button Component
function TabButton({ children, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 font-medium rounded-md whitespace-nowrap transition-colors ${
        active 
          ? "bg-white text-blue-600" 
          : "text-white/80 hover:bg-white/10"
      }`}
    >
      {children}
    </button>
  );
}

// Metric Card Component
function MetricCard({ title, value, change, description, icon, color }) {
  const getColorClass = () => {
    switch (color) {
      case "blue": return "bg-blue-100 text-blue-800";
      case "green": return "bg-green-100 text-green-800";
      case "purple": return "bg-purple-100 text-purple-800";
      case "cyan": return "bg-cyan-100 text-cyan-800";
      default: return "bg-blue-100 text-blue-800";
    }
  };
  
  const getIcon = () => {
    switch (icon) {
      case "projects":
        return (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        );
      case "compliance":
        return (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        );
      case "activity":
        return (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        );
      case "designs":
        return (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        );
      default:
        return null;
    }
  };
  
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-gray-500 text-sm">{title}</p>
          <h3 className="text-3xl font-bold mt-1">{value}</h3>
        </div>
        <div className={`p-3 rounded-lg ${getColorClass()}`}>
          {getIcon()}
        </div>
      </div>
      <div className="mt-4 flex items-center">
        <span className={`text-sm font-medium ${
          change.startsWith("+") ? "text-green-600" : "text-red-600"
        }`}>
          {change}
        </span>
        <span className="ml-2 text-sm text-gray-500">{description}</span>
      </div>
    </div>
  );
}
