"use client"
 
import React, { useState } from "react"
import SideBar from "@/components/SideBar";
import ChatWindow from "@/components/ChatWindow";
import InputField from "@/components/InputField";
import Darkmode from "@/components/DarkMode";
import { useChatStore } from "@/store/store";


export default function Home() {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const sessionId = useChatStore((state: any) => state.sessionId)
    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };
    return (
        <div className="h-screen flex">
            <SideBar 
                isOpen={sidebarOpen}
                toggleSidebar={toggleSidebar}
            />
            <div className="flex-grow flex flex-col">
                <div className="flex justify-between">
                    <button
                        className="lg:hidden p-2 rounded"
                        onClick={toggleSidebar}
                    >
                        &#9776;
                    </button>
                    <Darkmode/>
                </div>
                <ChatWindow/>
                { sessionId.length > 0 && <InputField/> }
            </div>
        </div>
    );
}