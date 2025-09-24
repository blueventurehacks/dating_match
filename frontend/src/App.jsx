import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./hooks/AuthContext";
import Overview from "./pages/Overview";
import Login from "./pages/Login";
import CreateAccount from "./pages/CreateAccount";
import Account from "./pages/Account";
import LandingPage from "./pages/LandingPage";
import PrivateRoute from "./router/PrivateRoute";
import NavBar from "./components/NavBar";

function App() {
	return (
		<AuthProvider>
			<Router>
				<NavBar />
				<Routes>
					<Route path="/login" element={<Login />} />
					<Route path="/create-account" element={<CreateAccount />} />

					{/* Public landing page: centered chat */}
					<Route path="/" element={<LandingPage />} />

					{/* Private routes */}
					<Route
						path="/overview"
						element={
							<PrivateRoute>
								<Overview />
							</PrivateRoute>
						}
					/>

					<Route
						path="/account"
						element={
							<PrivateRoute>
								<Account />
							</PrivateRoute>
						}
					/>
				</Routes>
			</Router>
		</AuthProvider>
	);
}

export default App;
