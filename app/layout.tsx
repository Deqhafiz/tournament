import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Agent Terminal - Beyond Truth Terminal',
  description: 'Advanced AI Agent Terminal with autonomous capabilities, multi-personality system, and blockchain integration',
  keywords: ['AI', 'Agent', 'Terminal', 'T-Coin', 'Blockchain', 'Autonomous'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  );
}
