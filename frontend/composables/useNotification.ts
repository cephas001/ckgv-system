import { ref } from "vue";

type NotificationType = "success" | "error";

interface Notification {
  show: boolean;
  message: string;
  type: NotificationType;
}

// Define the state OUTSIDE the function so it is shared globally
const notification = ref<Notification>({
  show: false,
  message: "",
  type: "success",
});

export const useNotification = () => {
  const triggerNotification = (
    message: string,
    type: NotificationType = "success",
  ) => {
    notification.value = { show: true, message, type };

    // Auto-hide after 4 seconds
    setTimeout(() => {
      notification.value.show = false;
    }, 4000);
  };

  const closeNotification = () => {
    notification.value.show = false;
  };

  return {
    notification,
    triggerNotification,
    closeNotification,
  };
};
