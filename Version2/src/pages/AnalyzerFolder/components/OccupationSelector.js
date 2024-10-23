import React from 'react';

const OccupationSelector = ({ occupations, selectedOccupation, onSelectOccupation }) => {
  if (!occupations || !Array.isArray(occupations) || occupations.length === 0) {
    return <p>No occupations available.</p>;
  }

  return (
    <select
      className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
      onChange={(e) => {
        const index = parseInt(e.target.value);
        onSelectOccupation(occupations[index]);
      }}
      value={selectedOccupation ? occupations.indexOf(selectedOccupation) : ''}
    >
      <option value="">Select an occupation</option>
      {occupations.map((occupation, index) => (
        <option key={index} value={index}>
          {occupation['Occupation Name'] || `Occupation ${index + 1}`}
        </option>
      ))}
    </select>
  );
};

export default OccupationSelector;