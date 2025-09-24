import { useState } from "react";
import { useNavigate } from "react-router-dom";

const CREATE_ACCOUNT_API =
	(import.meta.env.VITE_API_URL || "") + "/auth/register";

const CreateAccount = () => {
	const initialValues = {
		firstName: "",
		lastName: "",
		emailAddress: "",
		password: "",
		password2: "",
	};
	const [formValues, setFormValues] = useState(initialValues);
	const [isLoading, setIsLoading] = useState(false);
	const [errorMsg, setErrorMsg] = useState("");
	const navigate = useNavigate();

	const handleChange = (event) => {
		const { name, value } = event.target;
		setFormValues({ ...formValues, [name]: value });
	};

	const handleCreateAccount = async (event) => {
		event.preventDefault();
		setErrorMsg("");

		// if (formValues.password.length < 8) {
		// 	setErrorMsg("Password must be at least 8 characters.");
		// 	return;
		// }
		if (formValues.password !== formValues.password2) {
			setErrorMsg("Passwords do not match.");
			return;
		}

		setIsLoading(true);
		try {
			const response = await fetch(CREATE_ACCOUNT_API, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					firstName: formValues.firstName,
					lastName: formValues.lastName,
					emailAddress: formValues.emailAddress,
					password: formValues.password,
				}),
			});

			if (!response.ok) {
				const err = await response.json().catch(() => ({}));
				throw new Error(err.message || "Account creation failed");
			}

			navigate("/login");
		} catch (error) {
			setErrorMsg(error.message);
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<div>
			<div
				className="d-flex justify-content-center align-items-center"
				style={{ height: "90vh" }}
			>
				<div className="shadow p-3 mb-5 bg-white rounded">
					<div className="container">
						<form className="row g-3">
							<h1 className="pb-3">Create Your Account</h1>
							<div className="col-md-6">
								<label
									htmlFor="firstName"
									className="form-label"
								>
									First Name
								</label>
								<input
									type="text"
									className="form-control"
									name="firstName"
									value={formValues.firstName}
									onChange={handleChange}
									style={{ display: "blocked" }}
									required
								/>
							</div>

							<div className="col-md-6">
								<label
									htmlFor="lastName"
									className="form-label"
								>
									Last Name
								</label>
								<input
									type="text"
									className="form-control"
									name="lastName"
									value={formValues.lastName}
									onChange={handleChange}
									required
								/>
							</div>

							<div className="col-md-12">
								<label
									htmlFor="inputEmail"
									className="form-label"
								>
									Email Address
								</label>
								<input
									type="email"
									className="form-control"
									name="emailAddress"
									value={formValues.emailAddress}
									onChange={handleChange}
									required
								/>
							</div>

							<div className="col-md-12">
								<label
									htmlFor="password"
									className="form-label"
								>
									Password
								</label>
								<input
									type="password"
									className="form-control"
									name="password"
									value={formValues.password}
									onChange={handleChange}
									required
								/>
							</div>

							<div className="col-md-12">
								<label
									htmlFor="password2"
									className="form-label"
								>
									Re-type Password
								</label>
								<input
									type="password"
									className="form-control"
									name="password2"
									value={formValues.password2}
									onChange={handleChange}
									required
								/>
							</div>

							{errorMsg && (
								<div className="col-12 text-danger small">
									{errorMsg}
								</div>
							)}

							<div className="d-grid col-md-2 mt-4">
								<button
									type="submit"
									className="btn btn-primary"
									onClick={handleCreateAccount}
									disabled={isLoading}
								>
									{isLoading
										? "Creating..."
										: "Create Account"}
								</button>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
	);
};

export default CreateAccount;
