import React, { useState, KeyboardEvent } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { useChatStore } from '@/store/store';


const InputField: React.FC = () => {
  const [message, setMessage] = useState('');
  const sendMessage = useChatStore((state: any) => state.sendMessage)
  const sessionId = useChatStore((state: any) => state.sessionId)
  const userId = useChatStore((state: any) => state.userId)

  const handleSendMessage = () => {
    sendMessage(message, sessionId, userId)
    setMessage('')
  }

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter' && message.trim()) {
      event.preventDefault(); // Prevent default Enter key behavior
      handleSendMessage();
    }
  };

  return (
    <div className="w-full p-4 flex max-w-screen-lg mx-auto px-4 sm:px-6 lg:px-8">
      <Input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        className="flex-grow p-4 h-12 rounded-full placeholder-gray-500"
        placeholder="Type your message..."
      />
      <Button
        className="ml-2 px-4 py-2 rounded"
        onClick={handleSendMessage}
        disabled={!message.trim()}
      >
        Send
      </Button>
    </div>
  );
};

export default InputField;