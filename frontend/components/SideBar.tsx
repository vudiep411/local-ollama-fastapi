import { useChatStore } from '@/store/store';
import React, { useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';

const SideBar: React.FC = () => {
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
    <div className="w-1/6 h-full p-2 border-r-2 border-slate-300">
      <h2 className="text-lg font-bold mb-4 text-center">Conversations</h2>
      <div className='cursor-pointer hover:bg-gray-700 p-2 rounded' onClick={() => {addSession(uuidv4())}}>
        New convo
      </div>
        <ul>
          {sessions.map((session: any, i: number) => (
            <li
              key={i}
              className={`cursor-pointer hover:bg-gray-700 p-2 rounded truncate ${session.key === sessionId ? "bg-gray-700" : ""}`}
              onClick={() => {
                setSession(session.key)
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