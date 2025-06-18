<script setup>
  import { ref, onMounted, onBeforeUnmount } from "vue";
  import LineChart from "@/components/molecules/LineChart.vue";
  import RegisterPlant from "@/views/RegisterPlant.vue";
  import Dashboard from "@/views/Dashboard.vue";
  import { formatDateToString } from "@/utils/formatDate";
  import { formatSeconds } from "@/utils/formatSeconds";
  import { subtractDays } from "@/utils/subtractDays";
  import { getPlants } from "@/services/plantService/plantService";
  import { getHumidities } from "@/services/humidityService/humidityService";
  defineProps();
  defineEmits();

  const humidity = ref(null);
  const humidityValues = ref([]);
  const humidityTimestamps = ref([]);
  const lastTimestamp = ref(null);
  const timeSinceLastUpdate = ref("");
  const currentTime = ref("");
  const showStaleAlert = ref(false);
  const plantStatus = ref("Unknown");
  const showAlertSeconds = 1200;
  const timeSpan = ref(3);
  const daysDifference = 3;
  const firstPlant = ref(false);

  let intervalId = null;
  let timeIntervalId = null;
  let updateCheckIntervalId = null;

  async function isFirstPlant() {
    const plants = await getPlants();
    firstPlant.value = plants.length === 0;
  }

  function updateTime() {
    const now = new Date();
    currentTime.value = now.toLocaleTimeString();
  }

  function updateTimeSinceLastUpdate() {
    if (!lastTimestamp.value) {
      timeSinceLastUpdate.value = "N/A";
      showStaleAlert.value = true;
      return;
    }

    const now = new Date();
    const last = new Date(lastTimestamp.value);
    const diffMs = now - last;
    const seconds = Math.floor(diffMs / 1000);

    timeSinceLastUpdate.value = `${formatSeconds(seconds)}s ago`;
    showStaleAlert.value = seconds > showAlertSeconds;
  }
  async function fetchHumidity() {
    try {
      const startDate = formatDateToString(
        subtractDays(new Date(), daysDifference)
      );
      const endDate = formatDateToString(new Date());
      const data = await getHumidities(startDate, endDate);

      if (data.length > 0) {
        data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
        const last = data[data.length - 1];

        humidity.value = last.value;
        lastTimestamp.value = last.timestamp;

        humidityValues.value = data.map((d) => d.value);

        plantStatus.value =
          last.value >= 60
            ? "Your plant is happy! 🌱"
            : "Your plant is thirsty! 💧";

        humidityTimestamps.value = data.map((d) => {
          const date = new Date(d.timestamp);
          return `${String(date.getMonth() + 1).padStart(2, "0")}/${String(
            date.getDate()
          ).padStart(2, "0")} ${date.getHours()}:${date
            .getMinutes()
            .toString()
            .padStart(2, "0")}`;
        });
      } else {
        humidity.value = "No data available";
        lastTimestamp.value = null;
      }
    } catch (error) {
      console.error("Error: ", error);
      humidity.value = "Erro";
      lastTimestamp.value = null;
    }
  }

  onMounted(() => {
    updateTime();
    timeIntervalId = setInterval(updateTime, 1000);
    isFirstPlant();
    fetchHumidity().then(() => {
      updateTimeSinceLastUpdate();
      intervalId = setInterval(fetchHumidity, 1000);
      updateCheckIntervalId = setInterval(updateTimeSinceLastUpdate, 1000);
    });
  });

  onBeforeUnmount(() => {
    clearInterval(intervalId);
    clearInterval(timeIntervalId);
    clearInterval(updateCheckIntervalId);
  });
</script>

<template>
  <div class="container">
    <div v-if="firstPlant">
      <RegisterPlant />
    </div>
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<style>
  .container {
    display: flex;
    flex-direction: column;
    height: 100%;
    align-items: center;
    padding-top: 2rem;
  }
</style>
