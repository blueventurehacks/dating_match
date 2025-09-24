import { useState, useRef, useEffect } from "react";

const ChatBox = () => {
	const [messages, setMessages] = useState([
		{
			id: 1,
			text: "Welcome! I'm your dating assistant. How can I help you today?",
			sender: "bot",
			timestamp: new Date(),
		},
	]);
	const [inputMessage, setInputMessage] = useState("");
	const [isTyping, setIsTyping] = useState(false);
	const messagesEndRef = useRef(null);

	const scrollToBottom = () => {
		messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
	};

	useEffect(() => {
		scrollToBottom();
	}, [messages]);

	const handleSendMessage = (e) => {
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

		// Simulate bot response (replace with actual API call later)
		setTimeout(() => {
			const botResponse = {
				id: messages.length + 2,
				text: "I understand you're looking for dating advice. I'm here to help! What specific questions do you have?",
				sender: "bot",
				timestamp: new Date(),
			};
			setMessages((prev) => [...prev, botResponse]);
			setIsTyping(false);
		}, 1500);
	};

	const formatTime = (date) => {
		return date.toLocaleTimeString([], {
			hour: "2-digit",
			minute: "2-digit",
		});
	};

	return (
		<div className="chat-container d-flex flex-column h-100">
			{/* Chat Messages Area */}
			<div className="chat-messages flex-grow-1 p-3 overflow-auto">
				<div className="messages-list">
					{messages.map((message) => (
						<div
							key={message.id}
							className={`message-wrapper d-flex mb-3 ${
								message.sender === "user"
									? "justify-content-end"
									: "justify-content-start"
							}`}
						>
							<div
								className={`message-bubble ${
									message.sender === "user"
										? "bg-primary text-white"
										: "bg-light text-dark border"
								}`}
							>
								<div className="message-text">
									{message.text}
								</div>
								<div
									className={`message-time small ${
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

					{/* Typing Indicator */}
					{isTyping && (
						<div className="message-wrapper d-flex justify-content-start mb-3">
							<div className="message-bubble bg-light text-dark border">
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

			{/* Chat Input Area */}
			<div className="chat-input border-top bg-white p-3">
				<form onSubmit={handleSendMessage} className="d-flex gap-2">
					<div className="input-group">
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
					</div>
				</form>
			</div>
		</div>
	);
};

export default ChatBox;
