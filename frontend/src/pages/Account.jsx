import { useAuth } from "../hooks/AuthContext";

const Account = () => {
	const { user } = useAuth();

	if (!user) {
		return (
			<div className="container text-center">
				<p>Please log in to view your account details.</p>
			</div>
		);
	}

	return (
		<div className="container py-5">
			<div className="text-center mb-5">
				<img
					src="..\vite.svg"
					alt="Profile Picture"
					className="rounded-circle mb-3 border border-primary border-3"
					style={{
						width: "150px",
						height: "150px",
						objectFit: "cover",
					}}
				/>
				<h2 className="mb-1">
					{user.firstName} {user.lastName}
				</h2>
				<p className="text-muted">{user.emailAddress}</p>
			</div>

			<div className="card shadow-sm mb-4">
				<div className="card-header bg-light fw-bold fs-4">
					Profile Details
				</div>
				<div className="card-body p-0">
					<ul className="list-group list-group-flush">
						{[
							{ label: "MBTI Personality", key: "mbti" },
							{ label: "Attachment Style",  key: "attachmentStyle" },
							{ label: "Relationship Goal", key: "relationshipGoal" },
						].map(({ label, key }) => (
							<li
								key={key}
								className="list-group-item d-flex justify-content-between align-items-center py-3"
							>
								<span className="fw-medium">{label}</span>
								<span className="badge bg-light text-dark border rounded-pill px-3 py-2">
									{user[key] || "Not set"}
								</span>
							</li>
						))}

						{/* This is filler ----- */}
						<li className="list-group-item d-flex justify-content-between align-items-center py-3">
							<span className="fw-medium">Self-Esteem Level</span>
							<span className="badge bg-light text-dark border rounded-pill px-3 py-2">
								{"Not set"}
							</span>
						</li>
						<li className="list-group-item d-flex justify-content-between align-items-center py-3">
							<span className="fw-medium">
								Communication Style
							</span>
							<span className="badge bg-light text-dark border rounded-pill px-3 py-2">
								{"Not set"}
							</span>
						</li>
						<li className="list-group-item d-flex justify-content-between align-items-center py-3">
							<span className="fw-medium">More later...</span>
							<span className="badge bg-light text-dark border rounded-pill px-3 py-2">
								{"Not set"}
							</span>
						</li>
						{/* ----- End of filler */}
						
						<li className="list-group-item py-3">
							<span className="fw-medium">
								Hobbies & Interests
							</span>
							<p className="text-muted mb-0 mt-1">
								{user.hobbies ||
									"No hobbies listed yet. Tell me about them in the chat!"}
							</p>
						</li>
					</ul>
				</div>
			</div>
		</div>
	);
};

export default Account;
