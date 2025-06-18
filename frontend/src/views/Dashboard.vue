<script setup>
  import PlantsTable from "@/components/organisms/PlantsTable.vue";

  const selectedPlant = {
    id: 4,
    name: "ae",
    moisture_threshold: 1.0,
    check_interval: 1,
  };
</script>

<template lang="">
  <div>
    <h2>MY PLANTS</h2>
    <PlantsTable :plant="selectedPlant" />
  </div>
</template>

<style lang=""></style>
