import { useState } from 'react';

export default function SkillGapAnalysis() {
  const [level, setLevel] = useState('');
  const [skills, setSkills] = useState('');
  const [career, setCareer] = useState('');
  const [result, setResult] = useState<{ gaps: string[]; recommendations: string[] } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyzeSkillGap = async () => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/skill-gap', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ level, skills, career }),
      });

      if (!response.ok) throw new Error('Failed to fetch skill gap data');

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Error fetching data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-indigo-600 mb-6">Skill Gap Analysis</h1>

      <div className="bg-white shadow-lg rounded-lg p-6 w-full max-w-lg">
        <label className="block font-semibold mb-2">Education Level:</label>
        <input
          type="text"
          value={level}
          onChange={(e) => setLevel(e.target.value)}
          className="w-full p-2 border rounded mb-4"
          placeholder="e.g., Bachelor's"
        />

        <label className="block font-semibold mb-2">Current Skills (comma separated):</label>
        <input
          type="text"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          className="w-full p-2 border rounded mb-4"
          placeholder="e.g., Python, Data Analysis"
        />

        <label className="block font-semibold mb-2">Desired Career Path:</label>
        <input
          type="text"
          value={career}
          onChange={(e) => setCareer(e.target.value)}
          className="w-full p-2 border rounded mb-4"
          placeholder="e.g., Data Scientist"
        />

        <button
          onClick={analyzeSkillGap}
          className="w-full bg-indigo-600 text-white font-semibold p-2 rounded hover:bg-indigo-700 transition"
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Analyze Skill Gap'}
        </button>
      </div>

      {error && <p className="text-red-600 mt-4">{error}</p>}

      {result && (
        <div className="mt-6 bg-white shadow-lg rounded-lg p-6 w-full max-w-lg">
          <h2 className="text-xl font-semibold text-indigo-600 mb-2">Results</h2>
          <p className="font-semibold">Missing Skills:</p>
          <ul className="list-disc pl-6 mb-4">
            {result.gaps.map((gap, index) => (
              <li key={index} className="text-red-500">{gap}</li>
            ))}
          </ul>

          <p className="font-semibold">Recommended Resources:</p>
          <ul className="list-disc pl-6">
            {result.recommendations.map((rec, index) => (
              <li key={index} className="text-green-600">{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
