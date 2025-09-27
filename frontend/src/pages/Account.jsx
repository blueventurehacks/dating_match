import { useEffect, useState } from "react";
import { useAuth } from "../hooks/AuthContext";

const USER_API = (import.meta.env.VITE_API_URL || "") + "/auth/user";

const Account = () => {
	// Get the authenticated user from context to access the token
	const { user: authUser } = useAuth();
	const [userDetails, setUserDetails] = useState(null);
	const [isLoading, setIsLoading] = useState(true);

	useEffect(() => {
		// Ensure we are in a loading state whenever this effect runs.
		setIsLoading(true);

		const fetchUserDetails = async () => {
			// Don't do anything if the authUser hasn't been loaded from context yet.

			try {
				const url = `${USER_API}?userId=${authUser.id}`;
				const response = await fetch(url);
				if (response.ok) {
					const data = await response.json();
					setUserDetails(data);
				}
			} catch (error) {
				console.error("Failed to fetch user details:", error);
			} finally {
				setIsLoading(false);
			}
		};

		// Only attempt to fetch if we have a user from the context.
		// Otherwise, we are not logged in, so we can stop loading.
		if (authUser?.id) {
			fetchUserDetails();
		} else {
			// If there's no user or token, we're done loading and can show the login message.
			setIsLoading(false);
		}

	}, [authUser]); // Re-run the effect if the authUser object from context changes.

	if (isLoading) {
		return (
			<div className="container text-center">
				<p>Loading account details...</p>
			</div>
		);
	}

	return (
		<div className="container py-5">
			<div className="text-center mb-5">
				{!userDetails && (
					<div className="alert alert-warning">
						Please log in to view your account details.
					</div>
				)}

				{userDetails && (
					<>
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
							{userDetails.firstName} {userDetails.lastName}
				</h2>
						<p className="text-muted">{userDetails.emailAddress}</p>
					</>
				)}
			</div>

			<div className="card shadow-sm mb-4">
				<div className="card-header bg-light fw-bold fs-4">
					Profile Details
				</div>
				<div className="card-body p-0">
					{userDetails && (
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
										{userDetails[key] || "Not set"}
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
									{userDetails.hobbies ||
									"No hobbies listed yet. Tell me about them in the chat!"}
							</p>
						</li>
					</ul>
					)}
				</div>
			</div>
		</div>
	);
};

export default Account;
