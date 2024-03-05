<template>
  <div v-if="systemConfig && activeLLM">
    <v-btn
      v-if="systemConfig.active_llms.length === 1"
      prepend-icon="mdi-shimmer"
      variant="text"
      class="text-none mr-3"
    >
      <template v-slot:prepend>
        <v-icon color="success"></v-icon>
      </template>
      {{ activeLLM.display_name }}
    </v-btn>
    <v-menu v-else>
      <template v-slot:activator="{ props }">
        <v-btn
          prepend-icon="mdi-shimmer"
          append-icon="mdi-chevron-down"
          variant="outlined"
          class="text-none mr-3"
          v-bind="props"
        >
          <template v-slot:prepend>
            <v-icon color="success"></v-icon>
          </template>
          {{ activeLLM.display_name }}
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(llm, index) in systemConfig.active_llms"
          :key="index"
          :value="index"
          @click="setActiveLLM(llm)"
        >
          <v-list-item-title>{{ llm.display_name }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
import { useAppStore } from "@/stores/app";

export default {
  name: "LLMProviderMenu",
  data() {
    return {
      appStore: useAppStore(),
    };
  },
  computed: {
    systemConfig() {
      return this.appStore.systemConfig;
    },
    activeLLM() {
      return this.appStore.activeLLM;
    },
  },
  methods: {
    setActiveLLM(llm) {
      this.appStore.setActiveLLM(llm);
      this.$eventBus.emit("llm-changed");
    },
  },
};
</script>
