<script setup>
  import { ref, onMounted, onBeforeUnmount } from "vue";

  import LineChart from "@/components/molecules/LineChart.vue";
  const showStaleAlert = ref(false);
  const daysDifference = 3;
  const currentTime = ref("");
  const timeSinceLastUpdate = ref("");
  const humidity = ref(null);
  const humidityValues = ref([]);
  const humidityTimestamps = ref([]);
</script>

<template lang="">
  <div v-if="showStaleAlert" class="alert">
    ⚠️ No humidity updates received in the last 10 minutes!
  </div>
  <div class="days-input-container">
    <label for="days-difference">Enter the number of days:</label>
    <input
      type="number"
      id="days-difference"
      v-model="daysDifference"
      min="1"
      placeholder="Enter days"
    />
  </div>

  <div class="plant-status-container">
    <h1>Is my plant okay?</h1>
    <h2>{{ plantStatus }}</h2>
  </div>
  <div class="current-time-container">
    <p class="current-time">{{ currentTime }}</p>
    <p class="last-update">Last update: {{ timeSinceLastUpdate }}</p>
  </div>

  <div class="chart-container">
    <h2>
      Humidity:
      <span :style="{ color: humidity >= 60 ? 'green' : 'red' }"
        >{{ humidity }}%</span
      >
    </h2>
    <LineChart :labels="humidityTimestamps" :values="humidityValues" />
  </div>
</template>

<style lang=""></style>
