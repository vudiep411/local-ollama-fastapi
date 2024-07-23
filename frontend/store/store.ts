import { create } from 'zustand'
import axios from 'axios';

const URL = "http://127.0.0.1:8000"
export const useChatStore = create((set) => ({
  sessions: [],
  conversations: [],
  sessionId: "",
  userId: "vudiep411",
  fetchSessions: async (user_id: any) => {
    console.log("fetch session...")
    try {
      const response = await axios.get(`${URL}/sessions/${user_id}`)
      const data = response.data
      const sessionsData : any = []
      for(const key in data) {
        sessionsData.push({key: key, value: data[key]})
      }

      set((state: any) => ({
        sessions: sessionsData
      }))
    } catch (error) {
      console.log(error)
    }
  },
  fetchMessages: async (session_id: any) => {
    try {
      console.log("fetch messages...")
      const response = await axios.get(`${URL}/messages/${session_id}`)
      set((state: any) => ({
        conversations: response.data
      }))
    } catch (error) {
      console.log(error)
    }
  },
  sendMessage: async(message: string, session_id: string, user_id: string) => {
    try {
      const response = await fetch(`${URL}/stream_chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: message,
          session_id: session_id,
          user_id: user_id,
        }),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8');
      set((state: any) => ({
        conversations: [...state.conversations, 
          {role: "human", content: message},
          {role: "AIMessageChunk", content: ""}
        ]
      }))

      let done = false
      let accumulatedChunks = '';
      while(!done) {
        const { value, done: streamDone } = await reader?.read()!;
        done = streamDone;
        accumulatedChunks += decoder.decode(value);
        set((state: any) => ({
          conversations: [...state.conversations.slice(0, -1), 
            { role: "AIMessageChunk", content: accumulatedChunks}
          ]
        }))

      }
      set((state: any) => ({
        conversations: [...state.conversations.slice(0, -1), 
          { role: "AIMessageChunk", content: accumulatedChunks}
        ]
      }))
      
    } catch (error) {
      console.log(error)
    }
  },

  setSession: async (sessionId: string) => {
    try {
      const response = await axios.get(`${URL}/messages/${sessionId}`)

      set((state: any) => ({
        sessionId: sessionId
      }))
      set((state: any) => ({
        conversations: response.data
      }))
    } catch (error) {
      console.log(error)
    }
  },

  addSession: (sessionId: string) => {
    set((state: any) => ({
      sessions: [...state.sessions, {key: sessionId, value: sessionId}]
    }))
  }
}));