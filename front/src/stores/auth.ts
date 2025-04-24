import { defineStore } from "pinia";
import type { responseLogin } from "../types/authInterface";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as responseLogin["user"] | null,
    accessToken: useCookie("access_token").value,
    refreshToken: useCookie("refresh_token").value,
    ownProject: useCookie("own_project").value || "",
    ownSubject: useCookie("own_subject").value || "",
  }),

  actions: {
    loadFromCookies() {
      const rawUser = useCookie<string | null>("user").value;
      const accessToken = useCookie("access_token").value;
      const refreshToken = useCookie("refresh_token").value;
      const ownProject = useCookie("own_project").value;
      const ownSubject = useCookie("own_subject").value;

      if (rawUser) {
        try {
          this.user = typeof rawUser === "string" ? JSON.parse(rawUser) : rawUser;
        } catch (error) {
          console.error("Failed to parse user cookie:", error);
          this.user = null;
        }
      } else {
        this.user = null;
      }

      this.accessToken = accessToken ?? null;
      this.refreshToken = refreshToken ?? null;
      this.ownProject = String(ownProject ?? "");
      this.ownSubject = String(ownSubject ?? "");
    },

    setUser(
      user: responseLogin["user"],
      accessToken: string,
      refreshToken: string,
      ownProject: string | number | null,
      ownSubject: string | number | null
    ) {
      this.user = user;
      this.accessToken = accessToken;
      this.refreshToken = refreshToken;
      this.ownProject = String(ownProject ?? "");
      this.ownSubject = String(ownSubject ?? "");

      useCookie("user").value = JSON.stringify(user);
      useCookie("access_token").value = accessToken;
      useCookie("refresh_token").value = refreshToken;
      useCookie("own_project").value = String(ownProject ?? "");
      useCookie("own_subject").value = String(ownSubject ?? "");
    },

    clearUser() {
      this.user = null;
      this.accessToken = null;
      this.refreshToken = null;
      this.ownProject = "";
      this.ownSubject = "";

      useCookie("user").value = null;
      useCookie("access_token").value = null;
      useCookie("refresh_token").value = null;
      useCookie("own_project").value = null;
      useCookie("own_subject").value = null;
    },
  },
});
