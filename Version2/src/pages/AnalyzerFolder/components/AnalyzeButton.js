import React from 'react';

const AnalyzeButton = ({ onAnalyze, isDisabled, isAnalyzing }) => {
  return (
    <section className="text-center">
      <button
        onClick={onAnalyze}
        disabled={isDisabled}
        className={`px-8 py-3 rounded-full text-xs font-medium transition-all duration-200 ${
          isDisabled
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-lg transform hover:-translate-y-0.5'
        }`}
      >
        {isAnalyzing ? 'Analyzing...' : 'Analyze Document'}
      </button>
    </section>
  );
};

export default AnalyzeButton;