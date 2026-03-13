import { computed } from "vue";

type AuthUser = {
  email: string;
};

export function useAuth() {
  const user = useState<AuthUser | null>("auth:user", () => null);

  const isAuthenticated = computed(() => user.value !== null);

  const login = async (email: string, _password: string) => {
    user.value = { email };
  };

  const logout = () => {
    user.value = null;
  };

  return {
    user,
    isAuthenticated,
    login,
    logout,
  };
}

