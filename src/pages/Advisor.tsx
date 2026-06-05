import { useState } from 'react';
import EducationForm from '../components/EducationForm';
import RecommendationCard from '../components/RecommendationCard';
import Chatbot from '../components/Chatbot';
import { EducationLevel, MarksInput, Recommendation } from '../types';

export default function Advisor() {
  const [recommendations, setRecommendations] = useState<{ ai: Recommendation; ml: Recommendation } | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (data: { level: EducationLevel; marks: MarksInput }) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      
      if (!response.ok) {
        throw new Error('Failed to get recommendations');
      }
      
      const fetchedRecommendations = await response.json();
      setRecommendations(fetchedRecommendations);
      setErrorMessage('');
    } catch (error) {
      console.error('Error getting recommendations:', error);
      setErrorMessage('Unable to fetch recommendations. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 animate-gradient-x">
        <div className="absolute inset-0 bg-grid opacity-30"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-purple-100/20 to-transparent animate-pulse-slow"></div>
      </div>

      <div className="relative max-w-6xl mx-auto px-4 py-12 flex flex-col items-center justify-center">
        <div className="grid gap-12 w-full max-w-2xl">
          <div className="glass-morphism rounded-2xl shadow-xl p-6 md:p-8">
            <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 mb-6 text-center">
              Enter Your Educational Details
            </h2>
            <EducationForm onSubmit={handleSubmit} />
          </div>

          {loading && (
            <div className="text-indigo-600 font-medium text-center animate-pulse">
              Processing your recommendations...
            </div>
          )}

          {errorMessage && (
            <div className="text-red-600 font-medium text-center">
              {errorMessage}
            </div>
          )}

          {recommendations && (
            <div className="space-y-8 animate-fadeIn">
              <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 text-center">
                Your Personalized Recommendations
              </h2>
              <RecommendationCard 
                recommendations={recommendations}
                isLoading={false} 
              />
            </div>
          )}
        </div>
      </div>
      <Chatbot />
    </div>
  );
}
