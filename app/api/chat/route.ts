import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { message, personality } = await request.json();

    // In production, integrate with actual AI API (OpenAI, Anthropic, etc.)
    // For now, return simulated response

    const response = {
      message: `[${personality?.toUpperCase() || 'AI'}] Processing: ${message}`,
      personality: personality || 'default',
      timestamp: new Date().toISOString(),
    };

    return NextResponse.json(response);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to process message' },
      { status: 500 }
    );
  }
}
