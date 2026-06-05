import { useState } from 'react';
import { Recommendation } from '../types';
import { Sparkles, Clock, Target, Loader2 } from 'lucide-react';

export default function RecommendationCard({ 
  recommendations,
  isLoading 
}: { 
  recommendations: { ai: Recommendation; ml: Recommendation } | null;
  isLoading?: boolean;
}) {
  const [showAI, setShowAI] = useState(true);
  
  const currentRecommendation = recommendations ? (showAI ? recommendations.ai : recommendations.ml) : null;

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 min-h-[400px] flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
          <p className="text-gray-600">Generating recommendations...</p>
        </div>
      </div>
    );
  }

  if (!recommendations || !currentRecommendation) {
    return null;
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 transform transition-all duration-300 hover:scale-105">
      {/* Toggle Switch */}
      <div className="flex justify-end mb-4">
        <div className="flex items-center space-x-3 bg-gray-100 rounded-lg p-1">
          <button
            onClick={() => setShowAI(true)}
            className={`flex items-center space-x-1 px-3 py-1 rounded-md transition-colors ${
              showAI 
                ? 'bg-white text-purple-600 shadow-sm' 
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span className="text-sm font-medium">AI</span>
          </button>
          <button
            onClick={() => setShowAI(false)}
            className={`flex items-center space-x-1 px-3 py-1 rounded-md transition-colors ${
              !showAI 
                ? 'bg-white text-blue-600 shadow-sm' 
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            <Target className="w-4 h-4" />
            <span className="text-sm font-medium">ML</span>
          </button>
        </div>
      </div>

      {/* Card Content */}
      <div className="animate-fadeIn">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            {showAI ? (
              <Sparkles className="w-6 h-6 text-purple-500" />
            ) : (
              <Target className="w-6 h-6 text-blue-500" />
            )}
            <h3 className="text-xl font-bold text-gray-800">
              {currentRecommendation.pathway}
            </h3>
          </div>
          <span className={`px-3 py-1 text-sm rounded-full ${
            showAI 
              ? 'bg-purple-100 text-purple-800' 
              : 'bg-blue-100 text-blue-800'
          }`}>
            {Math.round(currentRecommendation.confidence)}% Match
          </span>
        </div>

        <p className="text-gray-600 mb-4">{currentRecommendation.description}</p>

        <div className="space-y-4">
          <div className="flex items-center space-x-2">
            <Clock className="w-5 h-5 text-gray-400" />
            <span className="text-sm text-gray-600">
              {currentRecommendation.timeframe}
            </span>
          </div>

          {currentRecommendation.requirements && currentRecommendation.requirements.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-2">
                Requirements:
              </h4>
              <ul className="list-disc list-inside space-y-1">
                {currentRecommendation.requirements.map((req, index) => (
                  <li key={index} className="text-sm text-gray-600">
                    {req}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {currentRecommendation.careers && currentRecommendation.careers.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-2">
                Potential Careers:
              </h4>
              <div className="flex flex-wrap gap-2">
                {currentRecommendation.careers.map((career, index) => (
                  <span
                    key={index}
                    className={`px-3 py-1 text-sm rounded-full ${
                      showAI 
                        ? 'bg-purple-50 text-purple-700' 
                        : 'bg-blue-50 text-blue-700'
                    }`}
                  >
                    {career}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}