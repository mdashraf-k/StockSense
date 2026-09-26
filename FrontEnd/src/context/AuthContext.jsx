import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { apiError, authApi, unwrap } from "../lib/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const refreshUser = async () => {
    try {
      const response = await authApi.me();
      const nextUser = unwrap(response);
      setUser(nextUser);
      setError("");
      return nextUser;
    } catch (err) {
      setUser(null);
      if (err?.response?.status !== 401) setError(apiError(err));
      return null;
    }
  };

  useEffect(() => {
    refreshUser().finally(() => setLoading(false));
    const handler = () => {
      setUser(null);
      window.location.href = "/login";
    };
    window.addEventListener("stocksense:unauthorized", handler);
    return () => window.removeEventListener("stocksense:unauthorized", handler);
  }, []);

  const login = async (payload) => {
    setError("");
    try {
      const response = await authApi.login(payload);
      const nextUser = unwrap(response)?.user ?? unwrap(response);
      setUser(nextUser || (await refreshUser()));
      return true;
    } catch (err) {
      const message = apiError(err);
      setError(message);
      throw new Error(message);
    }
  };

  const signup = async (payload) => {
    setError("");
    try {
      await authApi.signup(payload);
      return true;
    } catch (err) {
      const message = apiError(err);
      setError(message);
      throw new Error(message);
    }
  };

  const logout = async () => {
    try { await authApi.logout(); }
    finally {
      setUser(null);
      window.location.href = "/login";
    }
  };

  const updateProfile = async (payload) => {
    const response = await authApi.updateMe(payload);
    const nextUser = unwrap(response);
    setUser(nextUser);
    return nextUser;
  };

  const value = useMemo(() => ({
    user, loading, error, setError, login, signup, logout, refreshUser, updateProfile
  }), [user, loading, error]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);