import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  // Return T-Coin market data
  return NextResponse.json({
    price: Math.random() * 100,
    change24h: (Math.random() - 0.5) * 20,
    volume: Math.random() * 1000000,
    marketCap: Math.random() * 10000000,
    timestamp: new Date().toISOString(),
  });
}

export async function POST(request: NextRequest) {
  try {
    const { action, amount, to } = await request.json();

    let result;

    switch (action) {
      case 'send':
        result = {
          success: true,
          txId: `tx_${Date.now()}`,
          amount,
          to,
          timestamp: new Date().toISOString(),
        };
        break;

      case 'mine':
        result = {
          success: Math.random() > 0.5,
          reward: Math.random() * 10,
          blockHash: `0x${Math.random().toString(16).substr(2)}`,
          timestamp: new Date().toISOString(),
        };
        break;

      case 'stake':
        result = {
          success: true,
          amount,
          apr: 10,
          timestamp: new Date().toISOString(),
        };
        break;

      default:
        return NextResponse.json(
          { error: 'Invalid action' },
          { status: 400 }
        );
    }

    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to process transaction' },
      { status: 500 }
    );
  }
}
