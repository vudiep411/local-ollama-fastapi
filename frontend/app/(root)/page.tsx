"use client"
 
import React, { useState } from "react"
import Darkmode from "@/components/darkmode";
import SideBar from "@/components/SideBar";
import ChatWindow from "@/components/ChatWindow";
import InputField from "@/components/InputField";


interface Conversation {
    title: string;
    messages: { text: string; isUser: boolean }[];
}

export default function Home() {
    const [conversations, setConversations] = useState<Conversation[]>([
        { title: 'Conversation 1', messages: [{ text: 'Hello!', isUser: false }] },
        { title: 'Conversation 2', messages: [{ text: 'How can I help you?', isUser: false }] },
      ]);
      const [selectedConversationIndex, setSelectedConversationIndex] = useState(0);
    
      const handleSendMessage = (message: string) => {
        const newConversations = [...conversations];
        newConversations[selectedConversationIndex].messages.push({ text: message, isUser: true });
        setConversations(newConversations);
      };

      const selectedConversation = conversations[selectedConversationIndex];

    return (
        <div className="h-screen flex">
            <SideBar
                conversations={conversations}
                onSelectConversation={setSelectedConversationIndex}
            />
            <Darkmode/>
            <div className="flex-grow flex flex-col">
            <ChatWindow messages={selectedConversation.messages} />
            <InputField onSendMessage={handleSendMessage} />
            </div>
        </div>
    );
}