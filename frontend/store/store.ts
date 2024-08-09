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
  setState: (message: string, type: string) => {
    set((state: any) => ({
      conversations: [...state.conversations, 
        { role: type, content: message },
      ]
    }))
  },
  sendMessage: async(message: string, session_id: string, user_id: string, context: string) => {
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
          context: context
        }),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8');
      set((state: any) => ({
        conversations: [...state.conversations, 
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
      sessions: [...state.sessions, { key: sessionId, value: sessionId }]
    }))
    set((state: any) => ({
      sessionId: sessionId
    }))
    set((state: any) => ({
      conversations: []
    }))
  },

  deleteSession: async (sessionId: string, user_id: string) => {
    try {
      await axios.delete(`${URL}/session`, {
        data: {
          user_id: user_id,
          session_id: sessionId
        }
      })
      set((state: any) => ({
        sessions: state.sessions.filter((session: any) => session.key != sessionId)
      }))

      set((state: any) => ({
        sessionId: ""
      }))
      
    } catch (error) {
      console.log(error)
    }
  },

  getWebContext: async (message: string, session_id: string, user_id: string) => {
    try {
      const response = await axios.post(`${URL}/web_search`, {
        content: message,
        session_id: session_id,
        user_id: user_id
      })
      return response.data
    } catch (error) {
      console.log(error)
    }
  }
}));