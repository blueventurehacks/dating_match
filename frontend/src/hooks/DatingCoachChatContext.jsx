import { createContext, useContext, useState, useEffect } from "react";

const DatingCoachChatContext = createContext();

const initialMessage = {
	id: 1,
	text: "Welcome! I'm your personal dating coach. How can I help you improve your dating life today? You can ask me about profile tips, messaging, or anything else on your mind.",
	sender: "bot",
	timestamp: new Date(),
};

export const DatingCoachChatProvider = ({ children }) => {
	const [messages, setMessages] = useState(() => {
		const savedMessages = sessionStorage.getItem("datingCoachMessages");
		return savedMessages ? JSON.parse(savedMessages) : [initialMessage];
	});

	useEffect(() => {
		sessionStorage.setItem("datingCoachMessages", JSON.stringify(messages));
	}, [messages]);

	const resetChat = () => {
		sessionStorage.removeItem("datingCoachMessages");
		setMessages([initialMessage]);
	};

	return (
		<DatingCoachChatContext.Provider
			value={{ messages, setMessages, resetChat }}
		>
			{children}
		</DatingCoachChatContext.Provider>
	);
};

export const useDatingCoachChat = () => useContext(DatingCoachChatContext);
