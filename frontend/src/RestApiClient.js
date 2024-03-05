import axios from "axios";
import settings from "./settings.js";

const RestApiClient = axios.create({
  baseURL: settings.apiServerUrl + "/api/" + settings.apiServerVersion + "/",
  withCredentials: true,
});

export default {
  async getUser() {
    return new Promise((resolve, reject) => {
      RestApiClient.get("/users/me")
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  async getSystemConfig() {
    return new Promise((resolve, reject) => {
      RestApiClient.get("/system/config")
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
  async sendPrompt(prompt, provider) {
    const requestBody = {
      prompt: prompt,
      provider: provider,
    };
    return new Promise((resolve, reject) => {
      RestApiClient.post("/prompt/generate", requestBody)
        .then((response) => {
          resolve(response.data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },
};
