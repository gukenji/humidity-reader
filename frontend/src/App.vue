<script>
  import LineChart from "./components/molecules/LineChart.vue";
  import { formateDateToString } from "./utils/formatDate";
  import { subtractDays } from "./utils/subtractDays";

  export default {
    components: { LineChart },
    data() {
      return {
        humidity: null,
        humidityValues: [],
        humidityTimestamps: [],
        lastTimestamp: null,
        timeSinceLastUpdate: "",
        currentTime: "",
        showStaleAlert: false,
        intervalId: null,
        timeIntervalId: null,
        updateCheckIntervalId: null,
        plantStatus: "Unknown",
        showAlertSeconds: 1200,
        daysDifference: 3,
      };
    },
    methods: {
      updateTime() {
        const now = new Date();
        this.currentTime = now.toLocaleTimeString();
      },
      formatSeconds(seconds) {
        const hrs = Math.floor(seconds / 3600)
          .toString()
          .padStart(2, "0");
        const mins = Math.floor((seconds % 3600) / 60)
          .toString()
          .padStart(2, "0");
        const secs = Math.floor(seconds % 60)
          .toString()
          .padStart(2, "0");
        return `${hrs}:${mins}:${secs}`;
      },
      updateTimeSinceLastUpdate() {
        if (!this.lastTimestamp) {
          this.timeSinceLastUpdate = "N/A";
          this.showStaleAlert = true;
          return;
        }

        const now = new Date();
        const last = new Date(this.lastTimestamp);
        const diffMs = now - last;
        const seconds = Math.floor(diffMs / 1000);

        this.timeSinceLastUpdate = `${this.formatSeconds(seconds)}s ago`;
        this.showStaleAlert = seconds > this.showAlertSeconds;
      },

      getHumidityUrl() {
        const host = window.location.hostname;
        const port = 8000;
        return `http://${host}:${port}/humidity/`;
      },
      getPlantById(id) {
        const host = window.location.hostname;
        const port = 8000;
        return `http://${host}:${port}/plant/${id}`;
      },
      getTodayHumidityUrl() {
        const host = window.location.hostname;
        const port = 8000;

        const startDate = subtractDays(new Date(), this.daysDifference);
        const endDate = new Date();
        return `http://${host}:${port}/humidity/data?start_date=${formateDateToString(
          startDate
        )}&end_date=${formateDateToString(endDate)}`;
      },
      async updateCheckInterval(id) {
        try {
          const response = await fetch(this.getPlantById(id));
          const data = await response.json();
          this.showAlertSeconds = data.check_interval * 60
          return data.check_interval;
        } catch (error) {
          console.error("Error: ", error);
        }
      },
      async fetchHumidity() {
        try {
          const apiUrl = this.getTodayHumidityUrl();
          const response = await fetch(apiUrl);
          const data = await response.json();

          // Order by timestamp
          if (data.length > 0) {
            data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

            const last = data[data.length - 1];
            this.humidity = last.value;
            this.lastTimestamp = last.timestamp;

            this.humidityValues = data.map((d) => d.value);

            this.plantStatus =
              data[data.length - 1].value >= 60
                ? "Your plant is happy! 🌱"
                : "Your plant is thirsty! 💧";

            this.humidityTimestamps = data.map((d) => {
              const date = new Date(d.timestamp);
              return `${String(date.getMonth() + 1).padStart(2, "0")}/${String(
                date.getDate()
              ).padStart(2, "0")} ${date.getHours()}:${date
                .getMinutes()
                .toString()
                .padStart(2, "0")}`;
            });
          } else {
            this.humidity = "No data available";
            this.lastTimestamp = null;
          }
        } catch (error) {
          console.error("Error: ", error);
          this.humidity = "Erro";
          this.lastTimestamp = null;
        }
      },
    },
    mounted() {
      this.updateTime();
      this.timeIntervalId = setInterval(this.updateTime, 1000);
      this.fetchHumidity().then(async () => {
        this.updateTimeSinceLastUpdate();
        this.intervalId = setInterval(() => {
          this.fetchHumidity();
          this.updateCheckInterval(1)
          console.log(this.showAlertSeconds)

        }, 1000);
        this.updateCheckIntervalId = setInterval(
          this.updateTimeSinceLastUpdate,
          1000
        );
      });
    },
    beforeUnmount() {
      clearInterval(this.intervalId);
      clearInterval(this.timeIntervalId);
      clearInterval(this.updateCheckIntervalId);
    },
  };
</script>
<template>
  <div class="container">
    <div v-if="showStaleAlert" class="alert">
      ⚠️ No humidity updates received in the last {{this.showAlertSeconds / 60}} minutes!
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

  .current-time {
    font-size: 2rem;
    font-weight: bold;
    color: white;
  }

  .last-update {
    font-size: 1.2rem;
    color: lightgray;
  }

  .alert {
    background-color: red;
    color: white;
    font-weight: bold;
    padding: 1rem;
    text-align: center;
    font-size: 1.2rem;
    border-radius: 5px;
  }

  .plant-status-container,
  .current-time-container {
    display: flex;
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
    align-items: center;
    margin: 1rem 0 1rem 0;
  }

  .chart-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 1rem;
    gap: 0.5rem;
    width: 100%;
    max-width: 1000px;
  }

  @media (max-width: 600px) {
    .chart-container {
      max-width: 100%;
    }
  }
</style>
