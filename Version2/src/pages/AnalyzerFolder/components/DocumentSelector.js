import React from 'react';

const OccupationSelector = ({ occupations, selectedOccupation, onSelectOccupation }) => {
  return (
    <select
      className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
      onChange={(e) => onSelectOccupation(occupations[parseInt(e.target.value)])}
      value={selectedOccupation ? occupations.indexOf(selectedOccupation) : ''}
    >
      <option value="">Select an occupation</option>
      {occupations.map((occupation, index) => (
        <option key={index} value={index}>
          {occupation['Occupation Name']}
        </option>
      ))}
    </select>
  );
};

export default OccupationSelector;