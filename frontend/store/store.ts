import { create } from 'zustand'

interface Message {
  text: string;
  role: string;
}

interface Conversation {
  title: string;
  messages: Message[];
}

interface ChatState {
  conversations: Conversation[];
  selectedConversationIndex: number;
  selectConversation: (index: number) => void;
  sendMessage: (message: string) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  conversations: [
    { title: 'Conversation 1', messages: [{ text: 'Hello!', role: 'user' }] },
    { title: 'Conversation 2', messages: [{ text: 'How can I help you?', role: 'assistant' }] },
  ],
  selectedConversationIndex: 0,
  selectConversation: (index) => set({ selectedConversationIndex: index }),
  sendMessage: (message) => set((state) => {
    const newConversations = [...state.conversations];
    newConversations[state.selectedConversationIndex].messages.push({ text: message, role: "user" });
    return { conversations: newConversations };
  }),
}));