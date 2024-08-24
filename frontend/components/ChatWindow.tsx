import { useChatStore } from '@/store/store';
import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { AiFillRobot } from "react-icons/ai";
import { useUtilsStore } from '@/store/utils';
import { ThreeDots } from 'react-loader-spinner';

const ChatWindow: React.FC = () => {
  const messages = useChatStore((state: any) => state.conversations)
  const isSearching = useUtilsStore((state: any) => state.isSearching)
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
            {message.role === 'AIMessageChunk' && (
              <div className="prose prose-md mx-auto">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeRaw]}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            )}
            {message.role === 'human' && (
              <div className="prose prose-md mx-auto">
                <p>{message.content}</p>
              </div>
              )
            }
          </div>
        ))}
        <div ref={endOfMessagesRef}/>
        {isSearching && 
          <div className='flex gap-2 mx-auto'>
            <div className='mt-2'>
              <ThreeDots color="gray" height={20} width={20}/>
            </div>
            <p className="text-gray-500">Searching</p>
          </div>
        }
      </div>
    </div>
  );
};

export default ChatWindow;
