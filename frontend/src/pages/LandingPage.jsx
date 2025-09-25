import ChatBox from "../components/ChatBox";

const LandingPage = () => {
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
								<ChatBox />
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default LandingPage;
