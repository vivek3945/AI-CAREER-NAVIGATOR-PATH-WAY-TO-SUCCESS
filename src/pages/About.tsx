import { BookOpen, Brain, GraduationCap, Search } from 'lucide-react';

export default function About() {
  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Dynamic Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 animate-gradient-x">
        {/* Animated Overlay */}
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1510519138101-570d1dca3d66?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2400&q=80')] bg-cover bg-center opacity-5"></div>
        
        {/* Geometric Patterns */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-grid opacity-10"></div>
          <div className="absolute inset-0 bg-gradient-to-t from-transparent via-purple-500/10 to-transparent animate-pulse-slow"></div>
        </div>
      </div>
      
      <div className="relative max-w-6xl mx-auto px-4 py-20">
        <h1 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-purple-200 mb-12 text-center">
          About Educational Pathfinder
        </h1>
        
        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: <BookOpen className="w-12 h-12" />,
              title: "AI-Powered Recommendations",
              description: "Our advanced AI algorithms analyze your academic profile to suggest the most suitable educational paths."
            },
            {
              icon: <Brain className="w-12 h-12" />,
              title: "Machine Learning Insights",
              description: "Benefit from our ML models trained on extensive educational data to make informed decisions."
            },
            {
              icon: <GraduationCap className="w-12 h-12" />,
              title: "Expert Guidance",
              description: "Get personalized advice through our AI chatbot to help you navigate your educational journey."
            },
            {
              icon: <Search className="w-12 h-12" />,
              title: "Skill Gap Analysis",
              description: "Identify the skills required for your desired career path and receive tailored recommendations to bridge the gap."
            }
          ].map((feature, index) => (
            <div
              key={index}
              className="glass-morphism rounded-xl p-6 text-white hover:transform hover:scale-105 transition-all duration-300"
            >
              <div className="mb-4 text-indigo-300 relative">
                <div className="absolute inset-0 blur-xl bg-indigo-500/20 rounded-full"></div>
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
              <p className="opacity-80">{feature.description}</p>
            </div>
          ))}
        </div>

        <div className="mt-20 glass-morphism rounded-xl p-8 text-white">
          <h2 className="text-3xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-white to-purple-200">
            How It Works
          </h2>
          <div className="space-y-6">
            {[
              {
                step: "1",
                title: "Enter Your Details",
                description: "Provide your educational background and academic performance."
              },
              {
                step: "2",
                title: "AI Analysis",
                description: "Our AI system analyzes your profile using advanced algorithms."
              },
              {
                step: "3",
                title: "Get Recommendations",
                description: "Receive personalized educational pathway suggestions and career options."
              },
              {
                step: "4",
                title: "Skill Gap Analysis",
                description: "Compare your current skills with industry requirements and get suggestions for courses and training."
              },
              {
                step: "5",
                title: "Expert Support",
                description: "Chat with our AI advisor for detailed guidance and answers to your questions."
              }
            ].map((step, index) => (
              <div key={index} className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-gradient-to-br from-indigo-400 to-purple-400 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg shadow-indigo-500/30">
                  {step.step}
                </div>
                <div>
                  <h3 className="font-semibold text-xl mb-2">{step.title}</h3>
                  <p className="opacity-80">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
