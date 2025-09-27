import DatingCoachChatBox from "../components/DatingCoachChatBox";

const DatingCoach = () => {
	return (
		<div className="min-vh-100 d-flex align-items-center py-4">
			<div className="container">
				<div className="row justify-content-center">
					<div className="col-12 col-md-10 col-lg-8 col-xl-7">
						<div
							className="card shadow-sm border-0 rounded-4"
							style={{ height: "80vh" }}
						>
							<div className="card-header bg-light text-center py-3 border-bottom-0">
								<h5 className="mb-0 fw-semibold">
									Dating Coach
								</h5>
							</div>
							<div className="card-body p-0 h-100">
								<DatingCoachChatBox />
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default DatingCoach;
