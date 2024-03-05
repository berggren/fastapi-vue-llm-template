<template>
  <v-container v-if="appStore.activeLLM" fluid style="margin-top: 5vh">
    <v-card flat class="mx-auto" width="700" color="transparent">
      <template v-slot:title>
        <h2>Prompt</h2>
      </template>

      <template v-slot:subtitle>
        Connected to
        <strong style="text-decoration: underline">{{
          appStore.activeLLM.display_name
        }}</strong>
        using model
        <strong style="text-decoration: underline">{{
          appStore.activeLLM.model
        }}</strong>
      </template>

      <template v-slot:text>
        <v-textarea
          v-model="prompt"
          placeholder="Enter your prompt here..."
          prepend-inner-icon="mdi-console-line"
          :disabled="disableInput"
          autofocus
          auto-grow
          variant="outlined"
          rows="2"
          @keydown.enter.exact.prevent="submitPrompt"
          @keydown.enter.shift.exact.prevent="prompt += '\n'"
        />

        <v-card flat max-height="300" class="overflow-auto" color="transparent">
          <v-skeleton-loader
            v-if="isGenerating"
            :loading="isGenerating"
            type="paragraph"
          ></v-skeleton-loader>
          <code
            :class="$vuetify.theme.name === 'dark' ? 'code-font-color' : ''"
            v-html="responseText"
          ></code>
        </v-card>
      </template>

      <template v-slot:actions> </template>
    </v-card>
  </v-container>
</template>

<script>
import DOMPurify from "dompurify";
import RestApiClient from "@/RestApiClient";
import { useAppStore } from "@/stores/app";
import { marked } from "marked";

export default {
  name: "Prompt",
  components: {},
  data() {
    return {
      appStore: useAppStore(),
      prompt: "",
      responseText: "",
      isGenerating: false,
      disableInput: false,
    };
  },
  methods: {
    submitPrompt() {
      if (this.prompt === "") {
        return;
      }
      this.disableInput = true;
      this.isGenerating = true;
      this.responseText = "";
      RestApiClient.sendPrompt(this.prompt, this.appStore.activeLLM.name)
        .then((response) => {
          this.responseText = this.toHtml(response.response);
          this.isGenerating = false;
          this.disableInput = false;
        })
        .catch((error) => {
          console.error(error);
          this.disableInput = false;
          this.isGenerating = false;
        });
    },
    toHtml(markdown) {
      return DOMPurify.sanitize(marked(markdown));
    },
  },
  mounted() {
    this.$eventBus.on("llm-changed", (data) => {
      this.submitPrompt();
    });
  },
};
</script>

<style>
.code-font-color {
  color: lightgreen;
}
</style>
