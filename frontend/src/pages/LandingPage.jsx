import ChatBox from "../components/ChatBox";

const LandingPage = () => {
	const starting_text = "Hey there! I'm your self-discovery assistant. Please talk to me about your interests, personality traits, and relationship goals. I'm here to help you explore and understand yourself better!"

	return (
		<div className="min-vh-100 d-flex align-items-center">
			<div className="container">
				<div className="row justify-content-center">
					<div className="col-12 col-md-10 col-lg-8 col-xl-7">
						<div
							className="card shadow-sm border-0 rounded-4"
							style={{ minHeight: "70vh" }}
						>
							<div className="card-body p-0">
								<ChatBox starting_text={starting_text} />
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default LandingPage;
