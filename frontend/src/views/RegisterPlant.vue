<template>
  <div class="register-container">
    <h1 class="register-title">Register your plant</h1>

    <form @submit.prevent="submitForm">
      <Input
        id="name"
        label="Plant Name"
        v-model="form.name"
        placeholder="Enter plant name"
        required
      />

      <Input
        id="moisture_threshold"
        label="Moisture Threshold"
        type="number"
        v-model="form.moisture_threshold"
        placeholder="Enter moisture threshold"
        required
      />

      <Input
        id="check_interval"
        label="Check Interval (minutes)"
        type="number"
        v-model="form.check_interval"
        placeholder="Enter check interval"
        required
      />

      <button type="submit">Register Plant</button>
    </form>

    <div v-if="loading">Registering...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="success" class="success">Plant registered successfully!</div>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import { createPlant } from "@/services/plantService/plantService";
  import Input from "@/components/molecules/CreatePlantForm.vue";
  const form = ref({
    name: "",
    moisture_threshold: null,
    check_interval: null,
  });

  const loading = ref(false);
  const error = ref(null);
  const success = ref(false);

  const submitForm = async () => {
    loading.value = true;
    error.value = null;
    success.value = false;

    try {
      await createPlant(form.value);
      success.value = true;
    } catch (err) {
      console.error(err);
      error.value = "There was an error while registering the plant.";
    } finally {
      loading.value = false;
    }
  };
</script>

<style scoped></style>
