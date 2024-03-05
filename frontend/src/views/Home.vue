<template>
  <v-container fluid style="margin-top: 5vh">
    <v-card flat class="mx-auto" max-width="700" color="transparent">
      <template v-slot:title>
        <h2>Hello {{ user.name }}</h2>
      </template>
      <template v-slot:subtitle> Place your content here </template>
      <template v-slot:text>
        <code>
          <p>
            Greetings and welcome to this web application development template.
            Designed for swift and efficient creation of web applications, it
            offers a Python-based backend API and a frontend built using Vue,
            all integrated with the Material design framework.
          </p>
          <br />
          <p v-if="systemConfig && systemConfig.active_llms.length">
            <strong>
              You are connected to {{ systemConfig.active_llms.length }} AI
              system(s):
            </strong>
            <li v-for="llm in systemConfig.active_llms" :key="llm.name">
              {{ llm.display_name }} using model {{ llm.model }}
            </li>
            <br />
            <v-btn
              to="prompt"
              variant="outlined"
              prepend-icon="mdi-console-line"
              class="text-none mr-4"
            >
              Test your prompting skills
            </v-btn>
            <v-btn
              :href="apiServerUrl + '/api/' + apiServerVersion + '/docs'"
              target="_blank"
              variant="text"
              color="primary"
              class="text-none mr-4"
            >
              API documentation
            </v-btn>
          </p>
          <p v-else>
            Please note that at present,
            <strong style="text-decoration: underline"
              >you are not connected to any AI system</strong
            >. To enable this feature, kindly adjust the settings in your
            settings.toml file.
          </p>
        </code>
      </template>
    </v-card>
  </v-container>
</template>

<script>
import { useUserStore } from "@/stores/user";
import { useAppStore } from "@/stores/app";
import settings from "@/settings";

export default {
  name: "Home",
  components: {},
  data() {
    return {
      appStore: useAppStore(),
      userStore: useUserStore(),
      apiServerUrl: settings.apiServerUrl,
      apiServerVersion: settings.apiServerVersion,
    };
  },
  computed: {
    user() {
      return this.userStore.user;
    },
    systemConfig() {
      return this.appStore.systemConfig;
    },
  },
};
</script>
