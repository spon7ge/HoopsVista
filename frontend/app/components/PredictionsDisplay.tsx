import React from 'react';

interface Prop {
    name: string;
    type: string;
    line: number;
    odds: number;
}

interface PredictionsDisplayProps {
    predictions: Prop[];
}

const PredictionsDisplay: React.FC<PredictionsDisplayProps> = ({ predictions }) => {
    if (predictions.length === 0) {
        return <p className="text-center text-gray-400 mt-8">No predictions available for this category.</p>;
    }

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {predictions.map((prop, index) => (
                <div key={index} className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
                    <h3 className="text-xl font-bold mb-3 text-blue-400">{prop.name}</h3>
                    <div className="space-y-2">
                        <p><span className="text-gray-400">Type:</span> <span className="text-white">{prop.type}</span></p>
                        <p><span className="text-gray-400">Line:</span> <span className="text-green-400 font-semibold">{prop.line}</span></p>
                        <p><span className="text-gray-400">Odds:</span> <span className="text-yellow-400">{prop.odds}</span></p>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default PredictionsDisplay;