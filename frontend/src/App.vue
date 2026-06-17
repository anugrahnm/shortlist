<script setup lang="ts">
import { ref } from 'vue';

const jd_text = ref("")
const jd_url = ref("")
const results = ref(null)


const onSubmit = async() => {

  const body = jd_text.value ? { text: jd_text.value } : { url: jd_url.value }

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  }

  const response = await fetch("http://localhost:8000/analyze/", requestOptions)
  results.value = await response.json()
}

</script>

<template>
  <div>
    <input v-model="jd_text" placeholder="Paste the JD Text Here">
    <input v-model="jd_url" placeholder="Paste the JD URL Here">
    <button @click="onSubmit">Submit</button>
    <div v-if="results">
      <div >
          {{ results }}
      </div>
    </div>
    <div v-else>TEST</div>
  </div>
</template>
