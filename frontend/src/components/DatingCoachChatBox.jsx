import { useState, useRef, useEffect } from "react";
import { useDatingCoachChat } from "../hooks/DatingCoachChatContext";
import { useAuth } from "../hooks/AuthContext";

const CHAT_API = (import.meta.env.VITE_API_URL || "") + "/dating_coach/message";

const DatingCoachChatBox = () => {
	const { messages, setMessages, resetChat } = useDatingCoachChat();
	const { user } = useAuth(); // Get the full user object
	const [inputMessage, setInputMessage] = useState("");
	const [isTyping, setIsTyping] = useState(false);
	const messagesEndRef = useRef(null);

	const scrollToBottom = () => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
	};

	useEffect(() => {
		scrollToBottom();
	}, [messages]);

	const handleSendMessage = async (e) => {
		e.preventDefault();
		if (!inputMessage.trim()) return;

		const newMessage = {
			id: messages.length + 1,
			text: inputMessage,
			sender: "user",
			timestamp: new Date(),
		};

		setMessages((prev) => [...prev, newMessage]);
		setInputMessage("");
		setIsTyping(true);

		try {
			const payload = {
				message: inputMessage,
				// Only include userId if the user is logged in and has an ID
				...(user && user.id && { userId: parseInt(user.id) }),
			};

			const response = await fetch(CHAT_API, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(payload),
			});

			if (!response.ok) {
				throw new Error("Failed to get a response from the bot.");
			}

			const data = await response.json();

			const botResponse = {
				id: messages.length + 2,
				text: data.reply,
				sender: "bot",
				timestamp: new Date(),
			};
			setMessages((prev) => [...prev, botResponse]);
		} catch (error) {
			console.error("Chat error:", error);
			const errorResponse = {
				id: messages.length + 2,
				text: "Sorry, I'm having trouble connecting. Please try again later.",
				sender: "bot",
				timestamp: new Date(),
			};
			setMessages((prev) => [...prev, errorResponse]);
		} finally {
			setIsTyping(false);
		}
	};

	const formatTime = (date) => {
		return new Date(date).toLocaleTimeString([], {
			hour: "2-digit",
			minute: "2-digit",
		});
	};

	return (
		<div className="chat-container d-flex flex-column h-100">
			<div className="chat-messages flex-grow-1 p-3 overflow-auto">
				<div className="messages-list">
					{messages.map((message) => (
						<div
							key={message.id}
							className={`message-wrapper d-flex mb-3 ${
								message.sender === "user"
									? "justify-content-end me-2"
									: "justify-content-start ms-2"
							}`}
						>
							<div
								className={`message-bubble p-3 rounded-3 shadow-sm ${
									message.sender === "user"
										? "bg-primary text-white"
										: "bg-light text-dark border"
								}`}
							>
								<div className="message-text">
									{message.text}
								</div>
								<div
									className={`message-time small mt-1 text-end ${
										message.sender === "user"
											? "text-white-50"
											: "text-muted"
									}`}
								>
									{formatTime(message.timestamp)}
								</div>
							</div>
						</div>
					))}
					{isTyping && (
						<div className="message-wrapper d-flex justify-content-start ms-2 mb-3">
							<div className="message-bubble p-3 bg-light text-dark border">
								<div className="typing-indicator">
									<span></span>
									<span></span>
									<span></span>
								</div>
							</div>
						</div>
					)}
					<div ref={messagesEndRef} />
				</div>
			</div>
			<div className="chat-input border-top bg-white p-3">
				<div className="d-flex justify-content-end mb-2">
					<button
						className="btn btn-sm btn-outline-secondary"
						onClick={resetChat}
						title="Start a new conversation"
					>
						<i className="bi bi-arrow-clockwise"></i> New Chat
					</button>
				</div>
				<form onSubmit={handleSendMessage} className="d-flex gap-2">
					<input
						type="text"
						className="form-control"
						placeholder="Type your message here..."
						value={inputMessage}
						onChange={(e) => setInputMessage(e.target.value)}
						disabled={isTyping}
					/>
					<button
						type="submit"
						className="btn btn-primary"
						disabled={!inputMessage.trim() || isTyping}
					>
						<i className="bi bi-send"></i>
					</button>
				</form>
			</div>
		</div>
	);
};

export default DatingCoachChatBox;
