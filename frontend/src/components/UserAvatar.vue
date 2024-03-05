<template>
  <v-menu>
    <template v-slot:activator="{ props }">
      <v-avatar :size="size" v-bind="props">
        <v-img
          :src="user.picture"
          referrerpolicy="no-referrer"
          alt="Profile Picture"
        ></v-img>
      </v-avatar>
    </template>
    <v-list>
      <v-list-item @click="logout()">
        <v-list-item-title>Logout</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import axios from "axios";
import settings from "@/settings";
import { useUserStore } from "@/stores/user";

export default {
  name: "UserAvatar",
  props: {
    size: String,
  },
  data() {
    return {
      userStore: useUserStore(),
    };
  },
  computed: {
    user() {
      return this.userStore.user;
    },
    logoutUrl() {
      return settings.apiServerUrl + "/logout";
    },
  },
  methods: {
    logout() {
      axios
        .delete(this.logoutUrl, { withCredentials: true })
        .then((response) => {
          window.location.href = "/";
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
