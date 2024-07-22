import { useChatStore } from '@/store/store';
import React from 'react';
import ReactMarkdown from 'react-markdown';

const ChatWindow: React.FC = () => {
  const messages = useChatStore((state: any) => state.conversations)

  return (
    <div className="flex flex-col p-4 space-y-4 h-screen">
      {messages.map((message: any, index: number) => (
        <div key={index} className={`p-4 rounded-xl ${message.role === 'human' && 'bg-gray-800 self-end'}`}>
          {message.role === 'AIMessageChunk' ? (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          ) : (
            <p>{message.content}</p>
          )}
        </div>
      ))}
    </div>
  );
};

export default ChatWindow;
