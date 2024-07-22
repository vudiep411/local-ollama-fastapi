import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';


const InputField: React.FC = () => {
  const [message, setMessage] = useState('');

  return (
    <div className="w-full p-4 flex">
      <Input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="flex-grow p-4 h-12 rounded-full placeholder-gray-500"
        placeholder="Type your message..."
      />
      <Button
        className="ml-2 px-4 py-2 rounded"
      >
        Send
      </Button>
    </div>
  );
};

export default InputField;