'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import AIEngine, { AIMessage, AIPersonality } from '@/lib/ai-engine/core';

const Terminal: React.FC = () => {
  const [engine] = useState(() => new AIEngine());
  const [messages, setMessages] = useState<AIMessage[]>([]);
  const [input, setInput] = useState('');
  const [currentPersonality, setCurrentPersonality] = useState<AIPersonality>(engine.getPersonality());
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Welcome message
    const welcome: AIMessage = {
      id: 'welcome',
      role: 'system',
      content: '🚀 AI Agent Terminal v2.0 - Beyond Truth Terminal\nType /help for commands or just chat with me!',
      timestamp: new Date(),
    };
    setMessages([welcome]);
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const userInput = input.trim();
    setInput('');
    setIsProcessing(true);

    try {
      // Check for personality switch command
      if (userInput.startsWith('@')) {
        const personalityId = userInput.slice(1).toLowerCase();
        engine.setPersonality(personalityId);
        setCurrentPersonality(engine.getPersonality());
        setMessages(engine.getHistory());
      } else {
        const response = await engine.processMessage(userInput);
        setMessages([...engine.getHistory()]);
      }
    } catch (error) {
      console.error('Error processing message:', error);
    } finally {
      setIsProcessing(false);
      inputRef.current?.focus();
    }
  };

  const getMessageColor = (role: string) => {
    switch (role) {
      case 'system':
        return 'text-yellow-400';
      case 'user':
        return 'text-cyan-400';
      case 'assistant':
        return 'text-green-400';
      default:
        return 'text-gray-400';
    }
  };

  const getMessagePrefix = (role: string, personality?: string) => {
    switch (role) {
      case 'system':
        return '[SYSTEM]';
      case 'user':
        return '> USER';
      case 'assistant':
        return `[AI:${personality?.toUpperCase() || 'DEFAULT'}]`;
      default:
        return '';
    }
  };

  return (
    <div className="h-screen bg-terminal-bg text-terminal-text font-mono flex flex-col relative overflow-hidden">
      {/* Scanline Effect */}
      <div className="absolute inset-0 pointer-events-none z-10">
        <div className="h-1 bg-gradient-to-r from-transparent via-terminal-text to-transparent opacity-20 animate-scan" />
      </div>

      {/* Circuit Background */}
      <div className="absolute inset-0 opacity-5 pointer-events-none">
        <div className="grid grid-cols-12 grid-rows-12 h-full w-full">
          {Array.from({ length: 144 }).map((_, i) => (
            <div key={i} className="border border-terminal-text/10" />
          ))}
        </div>
      </div>

      {/* Header */}
      <div className="bg-terminal-border border-b-2 border-terminal-text/30 p-4 z-20">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse" />
              <div className="w-3 h-3 rounded-full bg-yellow-500 animate-pulse" />
              <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
            </div>
            <h1 className="text-xl font-bold">
              <span className="text-terminal-accent">AI AGENT</span>{' '}
              <span className="text-terminal-text">TERMINAL</span>
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-terminal-text/60">
              MODE: <span className="text-terminal-accent font-bold">{currentPersonality.name}</span>
            </span>
            <div className="text-xs text-terminal-text/40">
              {new Date().toLocaleTimeString()}
            </div>
          </div>
        </div>
      </div>

      {/* Personality Bar */}
      <div className="bg-terminal-border border-b border-terminal-text/20 p-2 z-20 flex gap-2 overflow-x-auto">
        {engine.getAllPersonalities().map((personality) => (
          <button
            key={personality.id}
            onClick={() => {
              engine.setPersonality(personality.id);
              setCurrentPersonality(personality);
            }}
            className={`px-3 py-1 text-xs rounded transition-all ${
              personality.id === currentPersonality.id
                ? 'bg-terminal-accent text-white'
                : 'bg-terminal-border text-terminal-text/60 hover:bg-terminal-text/10'
            }`}
          >
            {personality.name}
          </button>
        ))}
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2 z-20">
        <AnimatePresence>
          {messages.map((message, index) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className={`${getMessageColor(message.role)} leading-relaxed`}
            >
              <span className="opacity-60">
                {getMessagePrefix(message.role, message.personality)}
              </span>{' '}
              <span className="whitespace-pre-wrap">{message.content}</span>
            </motion.div>
          ))}
        </AnimatePresence>

        {isProcessing && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-terminal-text/60"
          >
            <span className="inline-flex items-center gap-1">
              Processing
              <span className="animate-pulse">.</span>
              <span className="animate-pulse animation-delay-200">.</span>
              <span className="animate-pulse animation-delay-400">.</span>
            </span>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="bg-terminal-border border-t-2 border-terminal-text/30 p-4 z-20">
        <div className="flex items-center gap-2">
          <span className="text-terminal-accent">$</span>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter command or message..."
            className="flex-1 bg-transparent outline-none text-terminal-text placeholder-terminal-text/30"
            disabled={isProcessing}
          />
          <button
            type="submit"
            disabled={isProcessing || !input.trim()}
            className="px-4 py-1 bg-terminal-accent text-white rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-terminal-accent/80 transition-colors"
          >
            SEND
          </button>
        </div>
      </form>

      {/* Status Bar */}
      <div className="bg-terminal-bg border-t border-terminal-text/20 px-4 py-1 text-xs text-terminal-text/40 z-20 flex justify-between">
        <span>AI Agent Terminal v2.0.0 | Enhanced Edition</span>
        <span>Messages: {messages.length} | Mode: {currentPersonality.id}</span>
      </div>
    </div>
  );
};

export default Terminal;
