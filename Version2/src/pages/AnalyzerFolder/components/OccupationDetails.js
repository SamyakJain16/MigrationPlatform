import React from 'react';

const pastelColors = [
  'bg-red-100', 'bg-yellow-100', 'bg-green-100', 'bg-blue-100', 'bg-indigo-100',
  'bg-purple-100', 'bg-pink-100', 'bg-orange-100', 'bg-teal-100', 'bg-cyan-100',
];

const OccupationDetails = ({ occupation }) => {
  return (
    <div className="bg-white shadow-lg rounded-lg overflow-hidden">
      <div className="bg-blue-600 text-white p-6">
        <h3 className="text-2xl font-bold">{occupation['Occupation Name']}</h3>
        <p className="text-sm mt-2">Occupation ID: {occupation['occupation_id']} | ANZSCO Code: {occupation['ANZSCO Code']}</p>
      </div>
      
      <div className="p-6 space-y-6">
        <div>
          <h4 className="text-lg font-semibold text-gray-700 mb-2">Occupation Details</h4>
          <p className="text-gray-600"><span className="font-medium">Caveats:</span> {occupation['Caveats'] || 'None'}</p>
          <p className="text-gray-600"><span className="font-medium">Assessing Authority:</span> {occupation['Assessing Authority']}</p>
        </div>

        <div>
          <h4 className="text-lg font-semibold text-gray-700 mb-2">Australian Government Migration Lists</h4>
          <div className="flex flex-wrap gap-2">
            {Object.entries(occupation['Australian Government Migration Lists'])
              .filter(([_, value]) => value === "1")
              .map(([key, _]) => (
                <span key={key} className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                  {key}
                </span>
              ))}
          </div>
        </div>

        <div>
          <h4 className="text-lg font-semibold text-gray-700 mb-2">Visa Type Availability</h4>
          <div className="flex flex-wrap gap-2">
            {Object.entries(occupation['Visa Type'])
              .filter(([_, value]) => value === "1")
              .map(([key, _]) => (
                <span key={key} className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                  {key}
                </span>
              ))}
          </div>
        </div>

        <div>
          <h4 className="text-lg font-semibold text-gray-700 mb-2">State and Subregion Visa Availability</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(occupation['States']).map(([state, details], index) => (
              <div key={state} className={`${pastelColors[index % pastelColors.length]} p-4 rounded-md`}>
                <h5 className="font-semibold text-gray-700 mb-2">{state}</h5>
                <ul className="space-y-1">
                  {Object.entries(details).map(([key, value]) => {
                    if (typeof value === 'object') {
                      return (
                        <li key={`${state}-${key}`} className="ml-4">
                          <span className="font-medium">{key}</span>
                          <ul className="ml-4 mt-1">
                            {Object.entries(value)
                              .filter(([_, subValue]) => subValue === "1")
                              .map(([subKey, _]) => (
                                <li key={`${state}-${key}-${subKey}`} className="text-sm text-gray-600">
                                  {subKey}
                                </li>
                              ))}
                          </ul>
                        </li>
                      );
                    } else if (value === "1") {
                      return <li key={`${state}-${key}`} className="text-sm text-gray-600">{key}</li>;
                    }
                    return null;
                  })}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OccupationDetails;