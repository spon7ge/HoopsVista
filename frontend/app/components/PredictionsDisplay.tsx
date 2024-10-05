import React from 'react';

interface Prediction {
    id: string;
    imageUrl: string;
    playerName: string;
    prop: string;
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
        <div key={prediction.id} className="bg-gray-800 rounded-lg overflow-hidden shadow-lg p-4">
          <h3 className="text-lg font-bold text-white mb-2">{prediction.playerName}</h3>
          <hr className="border-gray-600 my-2" />
          <div className="flex justify-between items-center mb-2">
            <div className="text-sm text-gray-400">{prediction.prop}</div>
            <div className="text-2xl font-bold text-white">{prediction.propLine}</div>
          </div>
          <div className="bg-gray-700 px-4 py-2 rounded">
            <div className="text-center text-white font-bold">
              Prediction: {(prediction.predictedProbability > 0.5 ? 'Over' : 'Under')}
              <span className="text-orange-500 ml-2">
                ({(prediction.predictedProbability * 100).toFixed(1)}%)
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PredictionsDisplay;