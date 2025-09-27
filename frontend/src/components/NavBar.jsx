import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/AuthContext";

const NavBar = () => {
	const { isAuthenticated, logout } = useAuth();
	const navigate = useNavigate();

	const handleLogout = () => {
		logout();
		navigate("/login");
	};

	return (
		<nav className="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm sticky-top">
			<div className="container">
				<Link className="navbar-brand fw-semibold" to="/">
					<span className="text-primary">Wingbot</span>
				</Link>

				<button
					className="navbar-toggler"
					type="button"
					data-bs-toggle="collapse"
					data-bs-target="#mainNavbar"
					aria-controls="mainNavbar"
					aria-expanded="false"
					aria-label="Toggle navigation"
				>
					<span className="navbar-toggler-icon"></span>
				</button>

				<div className="collapse navbar-collapse" id="mainNavbar">
					<ul className="navbar-nav me-auto mb-2 mb-lg-0">
						{isAuthenticated && (
							<>
								<li className="nav-item">
									<Link className="nav-link" to="/overview">
										Overview
									</Link>
								</li>
								<li className="nav-item">
									<Link
										className="nav-link"
										to="/self-discovery"
									>
										Self-Discovery
									</Link>
								</li>
								<li className="nav-item">
									<Link
										className="nav-link"
										to="/dating-coach"
									>
										Dating Coach
									</Link>
								</li>
								<li className="nav-item">
									<Link className="nav-link" to="/account">
										Account
									</Link>
								</li>
							</>
						)}
					</ul>
					<div className="d-flex align-items-center gap-2">
						{isAuthenticated ? (
							<button
								className="btn btn-outline-secondary"
								onClick={handleLogout}
							>
								Logout
							</button>
						) : (
							<>
								<Link
									className="btn btn-outline-primary"
									to="/login"
								>
									Login
								</Link>
								<Link
									className="btn btn-primary"
									to="/create-account"
								>
									Sign Up
								</Link>
							</>
						)}
					</div>
				</div>
			</div>
		</nav>
	);
};

export default NavBar;
