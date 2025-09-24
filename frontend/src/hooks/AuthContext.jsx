import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
	const [isAuthenticated, setIsAuthenticated] = useState(() => {
		const storedLoginState = sessionStorage.getItem("storedLoginState");
		return storedLoginState ? JSON.parse(storedLoginState) : false;
	});

	const login = () => {
		setIsAuthenticated(true);
		sessionStorage.setItem("storedLoginState", true);
	};
	const logout = () => {
		setIsAuthenticated(false);
		sessionStorage.setItem("storedLoginState", false);
		sessionStorage.removeItem("userId");
		sessionStorage.removeItem("userFirstName");
		sessionStorage.removeItem("userLastName");
		sessionStorage.removeItem("userEmailAddress");
		sessionStorage.removeItem("accessToken");
	};

	return (
		<AuthContext.Provider value={{ isAuthenticated, login, logout }}>
			{children}
		</AuthContext.Provider>
	);
};

export const useAuth = () => useContext(AuthContext);
