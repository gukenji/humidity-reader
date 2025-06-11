<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script setup>
  import { Line } from "vue-chartjs";
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
  } from "chart.js";
  import { computed } from "vue";

  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement
  );

  const props = defineProps({
    labels: {
      type: Array,
      required: true,
    },
    values: {
      type: Array,
      required: true,
    },
  });

  // Computa cores dos pontos com base nos valores
  const pointColors = computed(() =>
    props.values.map((v) => (v < 60 ? "red" : "green"))
  );

  // Define o chartData
  const chartData = computed(() => {
    const points = pointColors.value;
    const lastColor = points.length > 0 ? points[points.length - 1] : "white";
    return {
      labels: props.labels,
      datasets: [
        {
          label: "Humidity (%)",
          data: props.values,
          fill: false,
          borderColor: "white", // Linha branca
          backgroundColor: lastColor, // Cor da legenda
          pointBorderColor: points,
          pointBackgroundColor: points,
          borderWidth: 2,
          tension: 0.4,
        },
      ],
    };
  });

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        labels: {
          color: "white", // legenda branca
        },
      },
      title: {
        display: true,
        text: "Humidity Over Time",
        color: "white",
      },
    },
    scales: {
      x: {
        ticks: { color: "white" },
        grid: { color: "rgba(255,255,255,0.1)" },
      },
      y: {
        ticks: { color: "white" },
        grid: { color: "rgba(255,255,255,0.1)" },
      },
    },
  };
</script>
