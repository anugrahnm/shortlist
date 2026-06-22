<script setup lang="ts">
import {
  Binary,
  Link,
  Loader,
  Moon,
  Sparkles,
  Sun,
  Type,
} from "lucide-vue-next";
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
const isLoading = ref(false);
const cache = ref(
  new Map<
    string,
    {
      matched: string[][];
      missing: string[][];
      score: number;
      review: string;
    }
  >(),
);

const onSubmit = async () => {
  if (jd_text.value === "" && jd_url.value === "") {
    alert("Please enter the JD Text/URL before Submitting!");
    return;
  }
  isLoading.value = true;
  const key = `${isUseAi.value ? "gemini" : "tfidf"}_${jd_text.value || jd_url.value}`;
  if (cache.value.has(key)) {
    results.value = cache.value.get(key) as typeof results.value;
    isLoading.value = false;
    return;
  } else {
    const body = jd_text.value
      ? { text: jd_text.value }
      : { url: jd_url.value };

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    };

    const response = await fetch(
      isUseAi.value
        ? `${import.meta.env.VITE_API_URL}/analyze/gemini/`
        : `${import.meta.env.VITE_API_URL}/analyze/`,
      requestOptions,
    );
    results.value = await response.json();

    if (results.value) {
      cache.value.set(key, results.value);
      isLoading.value = false;
    }
  }
};

const onSwitchInput = () => {
  isUrl.value = !isUrl.value;
};

const onSwitchMode = () => {
  isUseAi.value = !isUseAi.value;
};

const hasHovered = ref(false);
const hasHoveredInput = ref(false);
const hasPinged = ref(false);
const hasPingedInput = ref(false);

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

const onHover = () => {
  hasHovered.value = !hasHovered.value;
};
const onHoverInput = () => {
  hasHoveredInput.value = !hasHoveredInput.value;
};

const bounceLoop = () => {
  (async () => {
    while (!hasHovered.value) {
      await delay(1000);
    }
    hasPinged.value = true;
  })();

  (async () => {
    while (!hasHoveredInput.value) {
      await delay(1000);
    }
    hasPingedInput.value = true;
  })();
};
bounceLoop();

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
        <div
          class="flex flex-col justify-center items-start sm:flex-row sm:justify-start sm:items-center gap-1 sm:gap-2"
        >
          <div
            class="has-tooltip border rounded-lg w-16 sm:w-20 h-6 sm:h-8 bg-gray-100 dark:bg-gray-800"
          >
            <div
              @mouseover="onHoverInput"
              @click="onSwitchInput"
              v-if="isUrl"
              :class="!hasPingedInput ? 'animate-bounce' : 'animate-none '"
              class="cursor-pointer border-2 shadow-2xl rounded-md w-12/20 sm:w-12 h-full flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-900"
            >
              <Link class="w-3.5 h-3.5 sm:w-4.5 sm:h-4.5" />
            </div>
            <div
              @click="onSwitchInput"
              v-else
              class="cursor-pointer border-2 shadow-2xl rounded-md w-12/20 sm:w-12 h-full ml-[25.3px] sm:ml-7.5 flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-900"
              dark:hover:bg-gray-950
            >
              <Type class="w-3.5 h-3.5 sm:w-4.5 sm:h-4.5" />
            </div>
            <span
              class="tooltip text-xs rounded shadow-lg p-1 bg-gray-100 text-gray-700 w-50"
              >Click to change input type (Text/URL)</span
            >
          </div>
          <div
            class="has-tooltip border rounded-lg w-16 sm:w-20 h-6 sm:h-8 bg-gray-100 dark:bg-gray-800"
          >
            <div
              @mouseover="onHover"
              @click="onSwitchMode"
              v-if="isUseAi"
              :class="!hasPinged ? 'animate-bounce' : 'animate-none '"
              class="cursor-pointer border-2 shadow-2xl rounded-md w-12/20 sm:w-12 h-full flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-800 dark:hover:bg-gray-900"
            >
              <Sparkles class="w-3.5 h-3.5 sm:w-4.5 sm:h-4.5" />
            </div>
            <div
              @click="onSwitchMode"
              v-else
              class="cursor-pointer border-2 shadow-2xl rounded-md w-12/20 sm:w-12 h-full ml-[25.3px] sm:ml-7.5 flex items-center justify-center bg-gray-200 hover:bg-gray-300 dark:bg-gray-900 dark:hover:bg-gray-900"
            >
              <Binary class="w-3.5 h-3.5 sm:w-4.5 sm:h-4.5" />
            </div>
            <span
              class="tooltip text-xs rounded shadow-lg p-1 bg-gray-100 text-gray-700 w-50"
              >Click to change mode (Gemini/TD-IDF)</span
            >
          </div>
        </div>
        <div class="justify-center items-center">
          <p class="text-center flex-1 text-lg sm:text-2xl">Shortlist</p>
          <p class="text-center flex-1 text-[10px] sm:text-xs">
            Match your CV to any job.
          </p>
        </div>
        <div class="flex items-center justify-end cursor-pointer">
          <Sun
            class="w-6 h-6 sm:w-7.5 sm:h-7.5"
            v-if="isDark"
            @click="isDark = false"
          ></Sun>
          <Moon
            :size="26"
            v-else
            @click="isDark = true"
            class="w-6 h-6 sm:w-7.5 sm:h-7.5 cursor-pointer"
          ></Moon>
        </div>
      </div>

      <div class="flex flex-col gap-2">
        <input
          required
          v-if="isUrl && isUseAi"
          class="border rounded-md p-2 text-xs sm:text-md outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
          v-model="jd_url"
          placeholder="Paste the JD URL Here"
        />
        <textarea
          required
          v-else-if="!isUrl || isUseAi"
          class="border field-sizing-content resize-none rounded-md text-xs sm:text-md p-2 min-h-8 max-h-80"
          v-model="jd_text"
          placeholder="Paste the JD Text Here."
        />
        <input
          required
          v-if="isUrl && !isUseAi"
          class="border rounded-md text-xs sm:text-md p-2 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100"
          v-model="jd_url"
          placeholder="URL mode on TD-IDF mode wont work well for JS-heavy sites. Use text mode for best results or switch to the AI Mode."
        />
      </div>
      <button
        type="button"
        class="border cursor-pointer text-xs sm:text-md font-mono bg-gray-100 dark:bg-gray-900 hover:bg-gray-300 dark:hover:bg-gray-950 rounded-md p-2"
        @click="onClear"
      >
        CLEAR
      </button>
      <div class="flex justify-center items-center">
        <Loader v-if="isLoading" class="animate-spin" />
        <button
          v-else
          type="button"
          class="border-2 cursor-pointer text-xs sm:text-md w-full font-mono bg-gray-200 dark:bg-gray-900 hover:bg-gray-300 dark:hover:bg-gray-950 rounded-md p-2"
          @click="onSubmit"
        >
          SUBMIT
        </button>
      </div>

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
        <a
          href="https://github.com/anugrahnm/shortlist"
          target="/blank"
          class="dark: fill-current has-tooltip"
        >
          <svg width="24" height="24" aria-hidden="true" class="">
            <use href="/icons.svg#github-icon" />
          </svg>
          <span
            class="tooltip-bottom text-[10px] rounded shadow-lg p-1 bg-gray-100 text-gray-700 w-fit"
          >
            Repo: https://www.github.com/anugrahnm/shortlist
          </span>
        </a>
      </div>
    </div>
  </div>
</template>
