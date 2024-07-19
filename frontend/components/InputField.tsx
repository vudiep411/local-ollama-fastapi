import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';

interface InputFieldProps {
  onSendMessage: (message: string) => void;
}

const InputField: React.FC<InputFieldProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');

  const handleSendMessage = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <div className="w-full p-4 flex">
      <Input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="flex-grow p-2 border rounded"
        placeholder="Type your message..."
      />
      <Button
        onClick={handleSendMessage}
        className="ml-2 px-4 py-2 rounded"
      >
        Send
      </Button>
    </div>
  );
};

export default InputField;