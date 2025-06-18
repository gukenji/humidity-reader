<template>
  <table border="1" cellpadding="8" cellspacing="0">
    <thead>
      <tr>
        <th>ID</th>
        <th>Plant Name</th>
        <th>Moisture Threshold</th>
        <th>Check Interval (min)</th>
        <th>Go to plant</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>{{ plant.id }}</td>
        <td>{{ plant.name }}</td>
        <td>{{ plant.moisture_threshold }}</td>
        <td>{{ plant.check_interval }}</td>
        <td>Check plant</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
  const props = defineProps({
    plant: {
      type: Object,
      required: true,
    },
  });
</script>

<style scoped>
  table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
  }
  th {
    background-color: #000000;
  }
</style>
