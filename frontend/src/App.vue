<script setup lang="ts">
import { Binary, Link, Moon, Sparkles, Sun, Type } from "lucide-vue-next";
import { ref } from "vue";

const jd_text = ref("");
const jd_url = ref("");
const results = ref<{
  matched: string[][];
  missing: string[][];
  score: number;
  review: string;
} | null>(null);
const isDark = ref(false);
const isUrl = ref(true);
const isUseAi = ref(true);

const onSubmit = async () => {
  if (jd_text.value === "" && jd_url.value === "") {
    alert("Please enter the JD Text/URL before Submitting!");
  } else {
    const body = jd_text.value
      ? { text: jd_text.value }
      : { url: jd_url.value };

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    };
    console.log("isUseAi:", isUseAi.value);

    const response = await fetch(
      isUseAi.value
        ? `${import.meta.env.VITE_API_URL}/analyze/gemini/`
        : `${import.meta.env.VITE_API_URL}/analyze/`,
      requestOptions,
    );
    results.value = await response.json();
  }
};

const onSwitchInput = () => {
  isUrl.value = !isUrl.value;
};

const onSwitchMode = () => {
  isUseAi.value = !isUseAi.value;
};

const onClear = () => {
  jd_text.value = "";
  jd_url.value = "";
  results.value = null;
};
</script>

<template>
  <div
    :class="{ dark: isDark }"
    class="flex flex-col w-screen font-mono min-w-xs min-h-screen sm:m-0 p-6 dark:bg-gray-900 dark:text-white sm:py-4 items-center justify-center"
  >
    <div
      class="flex-col flex w-full sm:w-0 min-w-xs sm:min-w-2xl gap-2 border rounded-lg sm:m-0 p-4"
    >
      <div class="grid grid-cols-3">
        <div class="flex gap-2">
          <div class="border rounded-lg w-20 h-8 bg-gray-100 dark:bg-gray-800">
            <div
              @click="onSwitchInput"
              v-if="isUrl"
              class="cursor-pointer border-2 shadow-2xl rounded-md w-12 h-full flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-900"
            >
              <Link />
            </div>
            <div
              @click="onSwitchInput"
              v-else
              class="cursor-pointer border-2 shadow-2xl rounded-md w-12 h-full ml-8 flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-900"
              dark:hover:bg-gray-950
            >
              <Type />
            </div>
          </div>
          <div class="border rounded-lg w-20 h-8 bg-gray-100 dark:bg-gray-800">
            <div
              @click="onSwitchMode"
              v-if="isUseAi"
              class="cursor-pointer border-2 shadow-2xl rounded-md w-12 h-full flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-900"
              dark:hover:bg-gray-950
            >
              <Sparkles />
            </div>
            <div
              @click="onSwitchMode"
              v-else
              class="cursor-pointer border-2 shadow-2xl rounded-md w-12 h-full ml-8 flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-900"
            >
              <Binary />
            </div>
          </div>
        </div>
        <div>
          <p class="text-center flex-1 text-2xl">Shortlist</p>
          <p class="text-center flex-1 text-xs">Match your CV to any job.</p>
        </div>
        <div class="flex items-start pt-1 justify-end">
          <Sun :size="26" v-if="isDark" @click="isDark = false"></Sun>
          <Moon
            :size="26"
            v-else
            @click="isDark = true"
            class="cursor-pointer"
          ></Moon>
        </div>
      </div>

      <div class="flex flex-col gap-2">
        <input
          required
          v-if="isUrl && isUseAi"
          class="border rounded-md p-2 sm:p-2 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
          v-model="jd_url"
          placeholder="Paste the JD URL Here"
        />
        <textarea
          required
          v-else-if="!isUrl || isUseAi"
          class="border field-sizing-content resize-none rounded-md p-2 min-h-10 max-h-80"
          rows="1"
          v-model="jd_text"
          placeholder="Paste the JD Text Here."
        />
        <input
          required
          v-if="isUrl && !isUseAi"
          class="border rounded-md p-2 sm:p-2 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
          v-model="jd_url"
          placeholder="URL mode on TD-IDF mode wont work well for JS-heavy sites. Use text mode for best results or switch to the AI Mode."
        />
      </div>
      <button
        type="button"
        class="border cursor-pointer font-mono bg-gray-100 dark:bg-gray-900 hover:bg-gray-300 dark:hover:bg-gray-950 rounded-md p-2"
        @click="onClear"
      >
        CLEAR
      </button>
      <button
        type="button"
        class="border-2 cursor-pointer font-mono bg-gray-200 dark:bg-gray-900 hover:bg-gray-300 dark:hover:bg-gray-950 rounded-md p-2"
        @click="onSubmit"
      >
        SUBMIT
      </button>

      <div class="border rounded-lg p-2 gap-2 flex flex-col" v-if="results">
        <ul class="text-center font-mono text-lg" v-if="results.score">
          Score:
          {{
            results.score.toFixed(2)
          }}
        </ul>
        <div
          class="border rounded-lg overflow-y-scroll p-2 grid grid-cols-2 divide-x-2"
        >
          <div class="flex flex-col divide-y-2">
            <p class="text-xl text-center">Matched</p>
            <ul class="p-2">
              <li v-for="(result, index) in results.matched">
                {{ index + 1 }}:{{ result[0] }}
              </li>
            </ul>
          </div>
          <div class="flex flex-col divide-y-2">
            <p class="text-xl text-center">Missing</p>
            <ul class="p-2">
              <li v-for="(result, index) in results.missing">
                {{ index + 1 }}:{{ result[0] }}
              </li>
            </ul>
          </div>
        </div>
        <div class="border rounded-lg p-2 flex flex-col divide-y-2">
          <p class="text-xl text-center">Review</p>
          <p class="text-lg" v-if="results.review">
            {{ results.review }}
          </p>
        </div>
      </div>
      <div class="flex items-center justify-center pt-1">
        <a href="https://github.com/anugrahnm/shortlist" target="/blank">
          <svg width="24" height="24" aria-hidden="true">
            <use href="/icons.svg#github-icon" />
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>
