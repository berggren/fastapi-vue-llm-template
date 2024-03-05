// Utilities
import { defineStore } from "pinia";
import RestApiClient from "@/RestApiClient";

export const useAppStore = defineStore("app", {
  state: () => ({
    systemConfig: null,
    activeLLM: null,
  }),
  actions: {
    async setSystemConfig() {
      const response = await RestApiClient.getSystemConfig();
      this.systemConfig = await response;
      const llmName =
        localStorage.getItem("llm") || this.systemConfig.active_llms[0].name;
      const llm = this.systemConfig.active_llms.filter(
        (llm) => llm.name === llmName
      )[0];
      this.activeLLM = llm;
    },
    async setActiveLLM(llm) {
      this.activeLLM = llm;
      localStorage.setItem("llm", llm.name);
    },
  },
});
