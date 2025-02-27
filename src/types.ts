export type EducationLevel = 'SSLC' | 'PU' | 'Diploma' | 'ITI' | 'Bachelors' | 'Masters';

export interface MarksInput {
  science_marks?: number;
  maths_marks?: number;
  english_marks?: number;
  specialization?: string;
  cgpa?: number;
  percentage?: number;
}

export interface Recommendation {
  pathway: string;
  confidence: number;
  description: string;
  requirements: string[];
  timeframe: string;
  careers: string[];
}