export default defineNuxtRouteMiddleware((to, from) => {
  const auth = useAuthStore();

  const adminPages = [
    "/dashboard",
    "/form/create",
    "/subject/create",
    "/form/link",
  ];
  const teacherPages = ["/dashboard", "/form/create", "/form/link"];
  const publicPages = ["/login", "/register", "/unauthorized"];

  if (publicPages.includes(to.path)) {
    return;
  }

  if (!auth.accessToken) {
    return navigateTo("/login");
  }

  const role = auth.user?.role;


  const isAdminOnly =
    adminPages.includes(to.path) && !teacherPages.includes(to.path);

  // student cannot access adminpage and teacherpage
  if (role === "Student") {
    if (adminPages.includes(to.path) || teacherPages.includes(to.path)) {
      return navigateTo("/unauthorized");
    }
  }

  // student cannot access adminpage
  if (role === "Teacher") {
    if (isAdminOnly) {
      return navigateTo("/unauthorized");
    }
  }

  // admin can access any page

});
