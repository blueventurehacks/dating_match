import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
	const [user, setUser] = useState(() =>
		JSON.parse(sessionStorage.getItem("user"))
	);

	const login = (userData) => {
		sessionStorage.setItem("user", JSON.stringify(userData));
		setUser(userData);
	};

	const logout = () => {
		sessionStorage.removeItem("user");
		setUser(null);
	};

	const isAuthenticated = !!user;

	return (
		<AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
			{children}
		</AuthContext.Provider>
	);
};

export const useAuth = () => useContext(AuthContext);
