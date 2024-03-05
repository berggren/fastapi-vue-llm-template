/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from "@/plugins";

// Components
import App from "./App.vue";

// Composables
import { createApp } from "vue";

// EventBus
import eventBus from "./plugins/eventbus";

const app = createApp(App);

registerPlugins(app);

app.use(eventBus);
app.mount("#app");
