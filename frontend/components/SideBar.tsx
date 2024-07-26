import { useChatStore } from '@/store/store';
import React, { useEffect, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { AiFillFileAdd, AiOutlineEllipsis , AiOutlineDelete } from "react-icons/ai";

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
  const deleteSession = useChatStore((state: any) => state.deleteSession)

  useEffect(() => {
    fetchSessions(userId)
  }, [fetchSessions])
  

  return (
    <div className={`fixed top-0 left-0 h-full w-72 bg-sidebar p-4 drop-shadow-md lg:relative lg:w-1/6 ${isOpen ? 'block' : 'hidden lg:block'}`}>
      <h2 className="text-lg font-bold mb-4 text-center">Conversations</h2>
      <div className='cursor-pointer hover:bg-secondary p-2 rounded flex mb-2' onClick={() => {addSession(uuidv4())}}>
        <AiFillFileAdd className='mt-2'/>
        <p>&nbsp; New Convo</p>
      </div>
        <ul>
          {sessions.map((session: any, i: number) => (
            <li
              key={i}
              className={`cursor-pointer hover:bg-secondary p-2 rounded truncate flex justify-between ${session.key === sessionId ? "bg-secondary" : ""}`}
              onClick={() => {
                setSession(session.key)
                toggleSidebar()
              }}
            >
              <p className='overflow-hidden'>{session.value}</p>
              <div className="pl-2" onClick={() => {deleteSession(session.key, userId)}}>
                <AiOutlineDelete 
                  className="text-lg mt-2 hover:scale-125 fill-red-600 stroke-2" 
                />
              </div>
            </li>
          ))}
        </ul>
    </div>
  );
};

export default SideBar;