import React from 'react';

interface ChatWindowProps {
  messages: { text: string; isUser: boolean }[];
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages }) => {
  return (
    <div className="h-full p-4">
      <div className="space-y-4">

      </div>
    </div>
  );
};

export default ChatWindow;
