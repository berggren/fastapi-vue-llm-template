<template>
  <v-app-bar flat>
    <v-app-bar-title>
      <span> {{ appName }} </span>
    </v-app-bar-title>
    <template v-slot:prepend>
      <v-btn icon @click="navigate('/')">
        <v-icon>mdi-atom-variant</v-icon>
      </v-btn>
    </template>
    <template v-slot:append>
      <v-btn
        v-if="systemConfig && systemConfig.active_llms.length"
        to="prompt"
        variant="outlined"
        prepend-icon="mdi-console-line"
        class="text-none mr-4"
      >
        Prompt
      </v-btn>
      <toggle-llm v-if="systemConfig && systemConfig.active_llms.length" />
      <toggle-theme />
      <user-avatar />
    </template>
  </v-app-bar>
</template>

<script>
import { useAppStore } from "@/stores/app";
import settings from "@/settings";
import UserAvatar from "@/components/UserAvatar.vue";
import ToggleLlm from "@/components/ToggleLLM.vue";
import ToggleTheme from "@/components/ToggleTheme.vue";

export default {
  components: {
    UserAvatar,
    ToggleLlm,
    ToggleTheme,
  },
  data() {
    return {
      appStore: useAppStore(),
      appName: settings.appName,
    };
  },
  computed: {
    systemConfig() {
      return this.appStore.systemConfig;
    },
  },
  methods: {
    navigate(path) {
      this.$router.push(path);
    },
  },
};
</script>
