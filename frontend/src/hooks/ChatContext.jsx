import { createContext, useContext, useState } from "react";

const ChatContext = createContext();

const initialMessage = {
	id: 1,
	text: "Hey there! I'm your self-discovery assistant. Please talk to me about your interests, personality traits, and relationship goals. I'm here to help you explore and understand yourself better!",
	sender: "bot",
	timestamp: new Date(),
};

export const ChatProvider = ({ children }) => {
	const [messages, setMessages] = useState([initialMessage]);

	const resetChat = () => {
		setMessages([initialMessage]);
	};

	return (
		<ChatContext.Provider value={{ messages, setMessages, resetChat }}>
			{children}
		</ChatContext.Provider>
	);
};

export const useChat = () => useContext(ChatContext);
