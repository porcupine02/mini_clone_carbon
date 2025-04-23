import { useAuthStore } from "@/stores/auth";
import type { responseLogin } from "~/src/types/authInterface";

export const useAuth = () => {
  const login = async (credentials: { username: string; password: string }) => {
    try {
      const response = (await $fetch("http://localhost:8000/auth/login/", {
        method: "POST",
        body: credentials,
      })) as responseLogin;

      const auth = useAuthStore();
      console.log('auth', response)

      auth.setUser(
        response.user,
        response.access,
        response.refresh,
        response.own_project,
        response.own_subject
      );

      return { success: true };
    } catch (error) {
      console.error("Login failed", error);
      return { success: false, error };
    }
  };

  const logout = () => {
    useCookie("access_token").value = null;
    useCookie("refresh_token").value = null;
    useCookie("user").value = null;
    useCookie("own_project").value = null;
    useCookie("own_subject").value = null;
  };

  return {
    login,
    logout,
  };
};
