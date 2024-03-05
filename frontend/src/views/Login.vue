<template>
  <v-container fluid style="margin-top: 12vh">
    <v-card flat class="mx-auto" max-width="700">
      <template v-slot:title>
        <h2>Login</h2>
      </template>
      <template v-slot:text>
        <code>
          Greetings and welcome to this web application development template.
          Designed for swift and efficient creation of web applications, it
          offers a Python-based backend API and a frontend built using Vue, all
          integrated with the Material design framework.
        </code>
        <br /><br />
        <v-btn variant="outlined" prepend-icon="mdi-google" :href="loginUrl">
          Login with Google
        </v-btn>
      </template>
    </v-card>
  </v-container>
</template>

<script>
import settings from "@/settings";

export default {
  name: "Login",
  computed: {
    loginUrl() {
      return settings.apiServerUrl + "/login";
    },
  },
};
</script>
