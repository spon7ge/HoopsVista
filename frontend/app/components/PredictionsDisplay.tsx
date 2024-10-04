import React from 'react';

interface Prediction {
  id: string;
  playerName: string;
  playerImage: string;
  propLine: number;
  predictedProbability: number;
}

interface PredictionsDisplayProps {
  predictions: Prediction[];
}

const PredictionsDisplay: React.FC<PredictionsDisplayProps> = ({ predictions }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {predictions.map((prediction) => (
        <div key={prediction.id} className="bg-white rounded-lg shadow-md overflow-hidden">
          <img
            src={prediction.playerImage}
            alt={prediction.playerName}
            className="w-full h-48 object-cover"
          />
          <div className="p-4">
            <h3 className="text-lg font-semibold mb-2">{prediction.playerName}</h3>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Prop Line: {prediction.propLine}</span>
              <span className="text-blue-600 font-medium">
                {(prediction.predictedProbability * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PredictionsDisplay;