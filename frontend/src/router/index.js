// Composables
import { createRouter, createWebHistory } from "vue-router";

// Import the default layout that wrapps all other views with an AppBar etc.
import Default from "@/layouts/default/Default.vue";

// Import App views
import Login from "@/views/Login.vue";
import Home from "@/views/Home.vue";
import Prompt from "@/views/Prompt.vue";

// Import Pinia stores
import { useUserStore } from "@/stores/user";

// Routes
const routes = [
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/",
    component: Default,
    children: [
      {
        path: "",
        name: "home",
        component: Home,
        props: true,
      },
      {
        path: "/prompt",
        name: "prompt",
        component: Prompt,
        props: true,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, _from, next) => {
  const userStore = useUserStore();
  if (to.name === "login") {
    next();
  } else if (userStore.user === null) {
    userStore
      .setUser()
      .then(() => {
        if (userStore.user === null) {
          next({ name: "login" });
        } else {
          next();
        }
      })
      .catch((error) => {
        if (error.response.status === 401) {
          next({ name: "login" });
          return;
        }
      });
  } else {
    next();
  }
});

export default router;
