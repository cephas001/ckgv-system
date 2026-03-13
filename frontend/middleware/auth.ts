export default defineNuxtRouteMiddleware((to, from) => {
  // Check if the user has a valid login token stored in their browser cookies
  const token = useCookie("auth_token");

  // If there is no token, redirect them to the login page immediately
  if (!token.value) {
    return navigateTo("/admin/login");
  }
});
