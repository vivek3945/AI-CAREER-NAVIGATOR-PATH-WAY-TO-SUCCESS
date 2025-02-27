import React, { useState } from 'react';
import { EducationLevel, MarksInput } from '../types';
import { School2, GraduationCap, BookOpen, Calculator, BrainCircuit } from 'lucide-react';

const educationLevels: EducationLevel[] = ['SSLC', 'PU', 'Diploma', 'ITI', 'Bachelors', 'Masters'];

export default function EducationForm({ onSubmit }: { onSubmit: (data: { level: EducationLevel; marks: MarksInput }) => void }) {
  const [level, setLevel] = useState<EducationLevel>('SSLC');
  const [marks, setMarks] = useState<MarksInput>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ level, marks });
  };

  const renderFields = () => {
    switch (level) {
      case 'SSLC':
        return (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input
              type="number"
              placeholder="Science marks"
              className="input-field"
              onChange={(e) => setMarks({ ...marks, science_marks: Number(e.target.value) })}
            />
            <input
              type="number"
              placeholder="Maths marks"
              className="input-field"
              onChange={(e) => setMarks({ ...marks, maths_marks: Number(e.target.value) })}
            />
            <input
              type="number"
              placeholder="English marks"
              className="input-field"
              onChange={(e) => setMarks({ ...marks, english_marks: Number(e.target.value) })}
            />
          </div>
        );
      case 'PU':
      case 'Diploma':
      case 'ITI':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Specialization"
              className="input-field"
              onChange={(e) => setMarks({ ...marks, specialization: e.target.value })}
            />
            <input
              type="number"
              placeholder="Percentage"
              className="input-field"
              onChange={(e) => setMarks({ ...marks, percentage: Number(e.target.value) })}
            />
          </div>
        );
      case 'Bachelors':
      case 'Masters':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Specialization"
              className="input-field"
              onChange={(e) => setMarks({ ...marks, specialization: e.target.value })}
            />
            <input
              type="number"
              step="0.01"
              placeholder="CGPA"
              className="input-field"
              onChange={(e) => setMarks({ ...marks, cgpa: Number(e.target.value) })}
            />
          </div>
        );
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {educationLevels.map((edu) => (
          <button
            key={edu}
            type="button"
            onClick={() => setLevel(edu)}
            className={`p-4 rounded-lg transition-all duration-300 ${
              level === edu ? 'bg-indigo-600 text-white shadow-lg scale-105' : 'bg-white text-gray-600 hover:bg-indigo-50'
            }`}
          >
            <div className="flex flex-col items-center space-y-2">
              {edu === 'SSLC' && <School2 className="w-6 h-6" />}
              {edu === 'PU' && <BookOpen className="w-6 h-6" />}
              {edu === 'Diploma' && <Calculator className="w-6 h-6" />}
              {edu === 'ITI' && <BrainCircuit className="w-6 h-6" />}
              {edu === 'Bachelors' && <GraduationCap className="w-6 h-6" />}
              {edu === 'Masters' && <School2 className="w-6 h-6" />}
              <span className="text-sm font-medium">{edu}</span>
            </div>
          </button>
        ))}
      </div>

      <div className="bg-white p-6 rounded-lg shadow-lg space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">Enter your details</h3>
        {renderFields()}
      </div>

      <button
        type="submit"
        className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-300"
      >
        Get Recommendations
      </button>
    </form>
  );
}
