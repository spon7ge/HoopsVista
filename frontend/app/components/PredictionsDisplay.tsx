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
                <div key={index} className="bg-gray-800 p-4 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
                    <h3 className="text-lg font-bold mb-2 text-white-400 text-center">{prop.name}</h3>
                    <div className="space-y-2">
                        <div className="flex justify-center items-center space-x-4">
                            <p className="text-sm"><span className="text-gray-400">Type:</span> <span className="text-white">{prop.type}</span></p>
                            <p className="text-sm"><span className="text-gray-400">Odds:</span> <span className="text-white-400">{prop.odds}</span></p>
                        </div>
                        <p className="text-center text-3xl font-bold text-white-400">{prop.line}</p>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default PredictionsDisplay;