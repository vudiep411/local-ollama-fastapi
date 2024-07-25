import { useChatStore } from '@/store/store';
import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { AiFillRobot } from "react-icons/ai";


const ChatWindow: React.FC = () => {
  const messages = useChatStore((state: any) => state.conversations)
  const endOfMessagesRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    // Scroll to the bottom whenever messages change
    if (endOfMessagesRef.current) {
      endOfMessagesRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className='overflow-auto leading-relaxed'>
      <div className="flex flex-col p-4 space-y-4 h-screen max-w-screen-lg mx-auto px-4 sm:px-6 lg:px-8 ">
        {messages.map((message: any, index: number) => (
          <div key={index} className={`p-3 rounded-2xl ${message.role === 'human' && 'bg-primary-foreground self-end'}`}>
            {message.role === 'AIMessageChunk' ? (
              <div className="prose prose-lg mx-auto">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeRaw]}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            ) : (
              <p>{message.content}</p>
            )}
          </div>
        ))}
        <div ref={endOfMessagesRef}/>
      </div>
    </div>
  );
};

export default ChatWindow;
