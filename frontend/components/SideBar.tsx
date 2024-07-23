import { useChatStore } from '@/store/store';
import React, { useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { AiFillFileAdd } from "react-icons/ai";

interface SideBarProps {
  isOpen: boolean;
  toggleSidebar: any
}

const SideBar: React.FC<SideBarProps> = ({ isOpen, toggleSidebar }) => {
  const sessions = useChatStore((state: any) => state.sessions)
  const fetchSessions = useChatStore((state: any) => state.fetchSessions)
  const sessionId = useChatStore((state: any) => state.sessionId)
  const setSession = useChatStore((state: any) => state.setSession)
  const addSession = useChatStore((state: any) => state.addSession)
  const userId = useChatStore((state: any) => state.userId)

  useEffect(() => {
    fetchSessions(userId)
  }, [fetchSessions])
  
  
  return (
    <div className={`fixed top-0 left-0 h-full w-72 bg-sidebar overflow-auto p-4 drop-shadow-md lg:relative lg:w-1/6 ${isOpen ? 'block' : 'hidden lg:block'}`}>
      <h2 className="text-lg font-bold mb-4 text-center">Conversations</h2>
      <div className='cursor-pointer hover:bg-secondary p-2 rounded flex mb-2' onClick={() => {addSession(uuidv4())}}>
        <AiFillFileAdd className='mt-2'/>
        <p>&nbsp; New Convo</p>
      </div>
        <ul>
          {sessions.map((session: any, i: number) => (
            <li
              key={i}
              className={`cursor-pointer hover:bg-secondary p-2 rounded truncate ${session.key === sessionId ? "bg-secondary" : ""}`}
              onClick={() => {
                setSession(session.key)
                toggleSidebar()
              }}
            >
              {session.value}
            </li>
          ))}
        </ul>
    </div>
  );
};

export default SideBar;