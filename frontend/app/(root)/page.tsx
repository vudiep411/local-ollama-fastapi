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

    return (
        <div className="h-screen flex">
            <SideBar/>
            {/* <Darkmode/> */}
            <div className="flex-grow flex flex-col max-w-screen-lg mx-auto px-4 sm:px-6 lg:px-8">
                <ChatWindow />
                <InputField/>
            </div>
        </div>
    );
}