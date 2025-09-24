const Account = () => {
	const userFirstName = sessionStorage.getItem("userFirstName") || "User";
	const userEmailAddress = sessionStorage.getItem("userEmailAddress") || "";

	return (
		<div className="container">
			<h1 className="mb-3">Account</h1>
			<div className="card">
				<div className="card-body">
					<h5 className="card-title">{userFirstName}</h5>
					<p className="card-text">{userEmailAddress}</p>
				</div>
			</div>
		</div>
	);
};

export default Account;
