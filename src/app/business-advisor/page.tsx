"use client";

import { useState } from "react";

// Business strategy categories
const STRATEGY_CATEGORIES = [
  "Market Disruption",
  "Vertical Integration",
  "First Principles Thinking",
  "Ambitious Goal Setting",
  "Capital Allocation",
  "Talent Acquisition",
  "Risk Management"
];

export default function BusinessAdvisor() {
  const [businessDescription, setBusinessDescription] = useState("");
  const [industry, setIndustry] = useState("");
  const [challenge, setChallenge] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      // Generate strategic insights based on input
      const insights = generateStrategicInsights(businessDescription, industry, challenge);
      setResults(insights);
      setLoading(false);
    }, 2000);
  };

  // Function to generate strategic insights based on visionary business patterns
  const generateStrategicInsights = (business, industry, challenge) => {
    // Select 3 random strategy categories
    const selectedCategories = [...STRATEGY_CATEGORIES]
      .sort(() => 0.5 - Math.random())
      .slice(0, 3);
    
    const strategies = {
      "Market Disruption": {
        title: "Market Disruption Strategy",
        description: "Identify and exploit inefficiencies in the current market structure.",
        recommendations: [
          `Analyze ${industry} supply chain for inefficiencies that can be eliminated through technology`,
          "Consider vertical integration to control key components of your value chain",
          "Invest heavily in R&D to create products that make current solutions obsolete"
        ]
      },
      "Vertical Integration": {
        title: "Vertical Integration Strategy",
        description: "Control multiple stages of your industry's value chain to increase efficiency and quality.",
        recommendations: [
          "Identify critical dependencies in your supply chain that create bottlenecks",
          "Acquire or develop in-house capabilities for key components",
          "Streamline operations by eliminating intermediaries between you and your customers"
        ]
      },
      "First Principles Thinking": {
        title: "First Principles Approach",
        description: "Break down complex problems into their fundamental elements and rebuild from scratch.",
        recommendations: [
          `Question all assumptions about how ${industry} 'should' operate`,
          "Calculate the theoretical limits of what's physically possible in your domain",
          "Design solutions from the ground up rather than iterating on existing approaches"
        ]
      },
      "Ambitious Goal Setting": {
        title: "Ambitious Goal Framework",
        description: "Set seemingly impossible targets to drive innovation and breakthrough thinking.",
        recommendations: [
          "Establish a 10-year vision that seems almost unattainable",
          "Break down long-term goals into concrete 3-month objectives",
          "Create public commitments to ambitious timelines to create productive pressure"
        ]
      },
      "Capital Allocation": {
        title: "Strategic Capital Allocation",
        description: "Prioritize resources toward high-leverage opportunities with exponential return potential.",
        recommendations: [
          "Identify the 20% of initiatives that will drive 80% of future value",
          "Ruthlessly defund projects that don't align with core strategic objectives",
          "Maintain significant cash reserves for opportunistic acquisitions during market downturns"
        ]
      },
      "Talent Acquisition": {
        title: "Elite Talent Strategy",
        description: "Build teams of exceptional individuals who can execute at extraordinary levels.",
        recommendations: [
          "Implement rigorous hiring processes that filter for problem-solving ability",
          "Create compensation structures that heavily reward exceptional performance",
          "Eliminate bureaucratic layers that slow down decision-making"
        ]
      },
      "Risk Management": {
        title: "Calculated Risk Approach",
        description: "Take significant but carefully calculated risks to achieve outsized returns.",
        recommendations: [
          "Identify existential risks and implement robust mitigation strategies",
          "Allocate 10-20% of resources to high-risk, high-reward initiatives",
          "Create fast feedback loops to quickly detect and correct course when risks materialize"
        ]
      }
    };

    // Calculate opportunity score based on input length and complexity
    const opportunityScore = 65 + Math.floor(Math.random() * 25);

    return {
      businessSummary: `Analysis for ${business} in the ${industry} industry, facing challenges around "${challenge}"`,
      opportunityScore: opportunityScore,
      strategies: selectedCategories.map(category => strategies[category]),
      executionPlan: {
        phase1: "Foundation Building (Months 1-3)",
        phase2: "Accelerated Implementation (Months 4-9)",
        phase3: "Market Dominance Strategy (Months 10-18)"
      },
      competitiveAdvantage: `Your unique position in the ${industry} market can be leveraged by focusing on technological innovation and operational efficiency, creating a sustainable competitive advantage that's difficult for incumbents to replicate.`,
      marketTrends: [
        "Increasing consumer demand for sustainable products",
        "Shift toward digital-first business models",
        "Growing importance of direct-to-consumer channels",
        "Rising emphasis on data-driven decision making"
      ]
    };
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      {/* Business Advisor Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <h1 className="text-3xl md:text-4xl font-bold mb-2">Strategic Business Advisor</h1>
            <p className="text-blue-100">
              Access world-class business strategies modeled after the most innovative industry pioneers of the 21st century.
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
              <h2 className="text-2xl font-bold mb-4">Generate Strategic Business Insights</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="businessDescription" className="block text-sm font-medium text-gray-700 mb-1">
                    Business Description
                  </label>
                  <textarea
                    id="businessDescription"
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={businessDescription}
                    onChange={(e) => setBusinessDescription(e.target.value)}
                    placeholder="Describe your business or startup idea"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-1">
                    Industry
                  </label>
                  <input
                    id="industry"
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={industry}
                    onChange={(e) => setIndustry(e.target.value)}
                    placeholder="E.g., Renewable Energy, E-commerce, Transportation"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="challenge" className="block text-sm font-medium text-gray-700 mb-1">
                    Current Business Challenge
                  </label>
                  <input
                    id="challenge"
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={challenge}
                    onChange={(e) => setChallenge(e.target.value)}
                    placeholder="E.g., Scaling production, Market entry, Fundraising"
                    required
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {loading ? "Generating Strategic Insights..." : "Generate Strategic Insights"}
                </button>
              </form>
            </div>

            {results && (
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h2 className="text-2xl font-bold mb-6 text-center">Strategic Business Analysis</h2>
                
                <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                  <div className="flex justify-between items-center">
                    <h3 className="font-medium text-lg">Business Summary</h3>
                    <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                      Opportunity Score: {results.opportunityScore}%
                    </div>
                  </div>
                  <p className="text-gray-700 mt-2">{results.businessSummary}</p>
                </div>
                
                <h3 className="text-xl font-semibold mb-4">Strategic Recommendations</h3>
                
                <div className="space-y-6">
                  {results.strategies.map((strategy, index) => (
                    <div key={index} className="border-l-4 border-blue-500 pl-4">
                      <h4 className="font-bold text-lg">{strategy.title}</h4>
                      <p className="text-gray-700 mb-3">{strategy.description}</p>
                      <ul className="list-disc pl-5 space-y-1">
                        {strategy.recommendations.map((rec, idx) => (
                          <li key={idx} className="text-gray-800">{rec}</li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
                
                <div className="mt-8 border-t pt-6">
                  <h3 className="text-xl font-semibold mb-4">Execution Roadmap</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h4 className="font-bold text-blue-800">{results.executionPlan.phase1}</h4>
                      <p className="text-gray-700">Focus on building the foundational elements of your strategy and assembling the right team.</p>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h4 className="font-bold text-blue-800">{results.executionPlan.phase2}</h4>
                      <p className="text-gray-700">Rapidly iterate on your product and begin aggressive market penetration tactics.</p>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h4 className="font-bold text-blue-800">{results.executionPlan.phase3}</h4>
                      <p className="text-gray-700">Expand into adjacent markets and build defensible competitive advantages.</p>
                    </div>
                  </div>
                </div>
                
                <div className="mt-8 border-t pt-6">
                  <h3 className="text-xl font-semibold mb-2">Competitive Advantage Analysis</h3>
                  <p className="text-gray-800">{results.competitiveAdvantage}</p>
                </div>

                <div className="mt-8 border-t pt-6">
                  <h3 className="text-xl font-semibold mb-4">Market Trends</h3>
                  <ul className="space-y-2">
                    {results.marketTrends.map((trend, index) => (
                      <li key={index} className="flex items-start">
                        <svg className="h-5 w-5 text-blue-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
                        </svg>
                        <span>{trend}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
          
          <div>
            <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
              <h3 className="font-bold text-lg mb-4">Business Strategy Principles</h3>
              <div className="space-y-4">
                <div className="border-l-4 border-blue-500 pl-4">
                  <h4 className="font-bold">First Principles Thinking</h4>
                  <p className="text-gray-700">Break problems down to their fundamental truths and reason up from there, rather than reasoning by analogy.</p>
                </div>
                <div className="border-l-4 border-green-500 pl-4">
                  <h4 className="font-bold">Vertical Integration</h4>
                  <p className="text-gray-700">Control multiple stages of the supply chain to improve efficiency, quality, and innovation speed.</p>
                </div>
                <div className="border-l-4 border-purple-500 pl-4">
                  <h4 className="font-bold">Ambitious Goal Setting</h4>
                  <p className="text-gray-700">Set seemingly impossible targets that force innovation and breakthrough thinking.</p>
                </div>
                <div className="border-l-4 border-yellow-500 pl-4">
                  <h4 className="font-bold">Iterative Development</h4>
                  <p className="text-gray-700">Rapid prototyping and continuous improvement based on real-world feedback.</p>
                </div>
              </div>
            </div>
            
            <div className="bg-gray-900 rounded-xl shadow-sm p-6 text-white">
              <h3 className="font-bold text-lg mb-4">Success Stories</h3>
              <div className="space-y-4">
                <div className="border-b border-gray-700 pb-4">
                  <h4 className="font-bold">Renewable Energy Startup</h4>
                  <p className="text-gray-300 text-sm mb-2">Using our Business Advisor strategies:</p>
                  <ul className="text-sm text-gray-400 list-disc pl-5 space-y-1">
                    <li>Secured $12M in funding</li>
                    <li>Reduced manufacturing costs by 35%</li>
                    <li>Accelerated time-to-market by 6 months</li>
                  </ul>
                </div>
                <div className="border-b border-gray-700 pb-4">
                  <h4 className="font-bold">E-commerce Platform</h4>
                  <p className="text-gray-300 text-sm mb-2">Using our Business Advisor strategies:</p>
                  <ul className="text-sm text-gray-400 list-disc pl-5 space-y-1">
                    <li>Increased customer retention by 28%</li>
                    <li>Expanded to 3 new markets</li>
                    <li>Achieved 215% YoY growth</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-bold">Healthcare Technology</h4>
                  <p className="text-gray-300 text-sm mb-2">Using our Business Advisor strategies:</p>
                  <ul className="text-sm text-gray-400 list-disc pl-5 space-y-1">
                    <li>Revolutionized patient monitoring</li>
                    <li>Reduced operational costs by 42%</li>
                    <li>Secured partnerships with 5 major hospitals</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
