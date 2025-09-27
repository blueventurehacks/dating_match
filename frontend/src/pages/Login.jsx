import { useState } from "react";
import { useAuth } from "../hooks/AuthContext";
import { useNavigate } from "react-router-dom";

const LOGIN_API = (import.meta.env.VITE_API_URL || "") + "/auth/login";

const Login = () => {
	const { login } = useAuth();
	const navigate = useNavigate();

	const initialValues = {
		emailAddress: "",
		password: "",
	};
	const [formValues, setFormValues] = useState(initialValues);
	const [isLoading, setIsLoading] = useState(false);
	const [errorMsg, setErrorMsg] = useState("");

	const handleChange = (event) => {
		const { name, value } = event.target;
		setFormValues({ ...formValues, [name]: value });
	};

	const handleLogin = async (event) => {
		event.preventDefault();
		setErrorMsg("");

		if (formValues.password.length > 72) {
			setErrorMsg("Password cannot be longer than 72 characters.");
			return;
		}
		setIsLoading(true);

		try {
			const response = await fetch(LOGIN_API, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: "include",
				body: JSON.stringify({
					emailAddress: formValues.emailAddress,
					password: formValues.password,
				}),
			});

			if (!response.ok) {
				const err = await response.json().catch(() => ({}));
				throw new Error(err.message || "Login failed");
			}

			const jsonResponse = await response.json();

			// The login function from AuthContext will handle storage
			login(jsonResponse);
			navigate("/overview");
		} catch (error) {
			setErrorMsg(error.message);
		} finally {
			setIsLoading(false);
		}
	};

	const navToCreateAcc = () => {
		navigate("/create-account");
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
							<h1 className="pb-3">Login</h1>

							<div className="col-md-12">
								<label
									htmlFor="emailAddress"
									className="form-label"
								>
									Email Address
								</label>
								<input
									type="email"
									className="form-control"
									name="emailAddress"
									id="emailAddress"
									onChange={handleChange}
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
									id="password"
									onChange={handleChange}
								/>
							</div>

							{errorMsg && (
								<div className="col-12 text-danger small">
									{errorMsg}
								</div>
							)}

							<div className="d-grid col-md-2">
								<button
									type="submit"
									className="btn btn-primary btn mt-1"
									onClick={handleLogin}
									disabled={isLoading}
								>
									{isLoading ? "Logging in..." : "Login"}
								</button>
							</div>
							<div className="col-md-5">
								<button
									type="button"
									className="btn btn-link mt-1"
									onClick={navToCreateAcc}
								>
									Create Account
								</button>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Login;
