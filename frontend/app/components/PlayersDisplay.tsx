import React from 'react';

interface Prop {
    name: string;
    type: string;
    line: number;
    odds: number;
}

interface PlayerProp {
    name: string;
    line: number;
    overOdds: number;
    underOdds: number;
}

interface PlayersDisplayProps {
    players: Prop[];
}

const PlayersDisplay: React.FC<PlayersDisplayProps> = ({ players }) => {
    if (players.length === 0) {
        return <p className="text-center text-gray-400 mt-8">No predictions available for this category.</p>;
    }

    // Group players by name and combine over/under odds
    const groupedPlayers: PlayerProp[] = players.reduce((acc, prop) => {
        const existingPlayer = acc.find(p => p.name === prop.name && p.line === prop.line);
        if (existingPlayer) {
            if (prop.type === 'Over') {
                existingPlayer.overOdds = prop.odds;
            } else {
                existingPlayer.underOdds = prop.odds;
            }
        } else {
            acc.push({
                name: prop.name,
                line: prop.line,
                overOdds: prop.type === 'Over' ? prop.odds : 0,
                underOdds: prop.type === 'Under' ? prop.odds : 0,
            });
        }
        return acc;
    }, [] as PlayerProp[]);

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {groupedPlayers.map((player, index) => (
                <div key={index} className="bg-gray-800 p-3 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
                    <h3 className="text-lg font-bold mb-2 text-white-400 text-center">{player.name}</h3>
                    <div className="space-y-2 border-2 border-gray-300 p-4 rounded-lg">
                        <p className="text-center text-3xl font-bold text-white-400">{player.line}</p>
                        <p className="text-center text-sm">
                            <span className="text-gray-400">O: </span>
                            <span className="text-white">{player.overOdds}</span>
                            <span className="text-gray-400 font-bold"> | </span>
                            <span className="text-gray-400">U: </span>
                            <span className="text-white">{player.underOdds}</span>
                        </p>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default PlayersDisplay;
