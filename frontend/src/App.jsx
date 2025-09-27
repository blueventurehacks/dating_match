import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./hooks/AuthContext";
import { ChatProvider } from "./hooks/ChatContext";
import Overview from "./pages/Overview";
import { DatingCoachChatProvider } from "./hooks/DatingCoachChatContext";
import Login from "./pages/Login";
import CreateAccount from "./pages/CreateAccount";
import Account from "./pages/Account";
import SelfDiscovery from "./pages/SelfDiscovery";
import DatingCoach from "./pages/DatingCoach";
import PrivateRoute from "./router/PrivateRoute";
import NavBar from "./components/NavBar";

function App() {
	return (
		<AuthProvider>
			<ChatProvider>
				<DatingCoachChatProvider>
					<Router>
						<NavBar />
						<Routes>
							{/* Public Routes */}
							<Route path="/login" element={<Login />} />
							<Route
								path="/create-account"
								element={<CreateAccount />}
							/>
							<Route path="/" element={<DatingCoach />} />

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
								path="/self-discovery"
								element={
									<PrivateRoute>
										<SelfDiscovery />
									</PrivateRoute>
								}
							/>
							<Route
								path="/dating-coach"
								element={
									<PrivateRoute>
										<DatingCoach />
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
				</DatingCoachChatProvider>
			</ChatProvider>
		</AuthProvider>
	);
}

export default App;
