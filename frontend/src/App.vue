<script setup lang="ts">
import { Moon, Sun } from "lucide-vue-next";
import { ref } from "vue";

const jd_text = ref("");
const jd_url = ref("");
const results = ref<{
  matched: string[][];
  missing: string[][];
  score: number;
} | null>(null);
const isDark = ref(false);

const onSubmit = async () => {
  const body = jd_text.value ? { text: jd_text.value } : { url: jd_url.value };

  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  };

  const response = await fetch(
    "http://localhost:8000/analyze/",
    requestOptions,
  );
  results.value = await response.json();
};
</script>

<template>
  <div
    :class="{ dark: isDark }"
    class="flex flex-col w-screen font-mono h-screen sm:m-0 p-4 dark:bg-gray-900 dark:text-white sm:py-4 items-center"
  >
    <div
      class="flex-col flex h-full w-full sm:w-0 sm:min-w-2xl gap-2 border rounded-lg sm:m-0 p-4"
    >
      <div class="flex">
        <p class="text-center flex-1 text-2xl">Shortlist</p>
        <Sun v-if="isDark" @click="isDark = false"></Sun>
        <Moon v-else @click="isDark = true" class="cursor-pointer"></Moon>
      </div>
      <textarea
        class="border rounded-md p-2"
        rows="10"
        v-model="jd_text"
        placeholder="Paste the JD Text Here"
      />
      <input
        class="border rounded-md px-1 sm:p-2"
        v-model="jd_url"
        placeholder="Paste the JD URL Here"
      />
      <button
        type="button"
        class="border-2 cursor-pointer font-mono bg-gray-200 dark:bg-gray-900 hover:bg-gray-300 dark:hover:bg-gray-950 rounded-md p-2"
        @click="onSubmit"
      >
        SUBMIT
      </button>

      <div class="border rounded-lg p-2" v-if="results">
        <ul class="text-center font-mono text-lg" v-if="results.score">
          Score:
          {{
            results.score.toFixed(4)
          }}
        </ul>
        <div
          class="border rounded-lg overflow-y-scroll p-2 h-96 grid grid-cols-2 gap-2"
        >
          <div>
            <p class="text-xl text-center">Matched</p>
            <ul>
              <li v-for="result in results.matched">{{ result[0] }}</li>
            </ul>
          </div>
          <div>
            <p class="text-xl text-center">Missing</p>
            <ul>
              <li v-for="result in results.missing">{{ result[0] }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
