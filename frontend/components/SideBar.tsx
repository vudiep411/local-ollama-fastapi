import React from 'react';

interface SidebarProps {
    conversations: { title: string }[];
    onSelectConversation: (index: number) => void;
}

const SideBar: React.FC<SidebarProps> = ({ conversations, onSelectConversation }) => {
  return (
    <div className="w-1/6 h-full p-4 border-r-2 border-slate-300">
      <h2 className="text-lg font-bold mb-4">Conversations</h2>

    </div>
  );
};

export default SideBar;