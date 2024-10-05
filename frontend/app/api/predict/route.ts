import { NextResponse } from 'next/server';

export async function GET(
  request: Request,
  { params }: { params: { prop: string } }
) {
  const prop = params.prop;
  
  // TODO: Replace this with actual API call to your backend
  const mockPredictions = [
    {
      id: '1',
      playerName: 'LeBron James',
      prop: prop,
      propLine: 25.5,
      predictedProbability: 0.65,
    },
    {
      id: '2',
      playerName: 'Stephen Curry',
      prop: prop,
      propLine: 28.5,
      predictedProbability: 0.58,
    },
    // Add more mock predictions...
  ];

  return NextResponse.json(mockPredictions);
}
