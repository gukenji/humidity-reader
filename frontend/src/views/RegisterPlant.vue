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

<script>
  import { createPlant } from "@/services/plantService/plantService";
  import Input from "@/components/molecules/create-plant-form.vue";

  export default {
    components: {
      Input,
    },
    data() {
      return {
        form: {
          name: "",
          moisture_threshold: null,
          check_interval: null,
        },
        loading: false,
        error: null,
        success: false,
      };
    },
    methods: {
      async submitForm() {
        this.loading = true;
        this.error = null;
        this.success = false;

        try {
          const response = await createPlant(this.form);
          console.log(response);

          this.success = true;
        } catch (err) {
          console.error(err);
          this.error = "There was an error while registering the plant.";
        } finally {
          this.loading = false;
        }
      },
    },
  };
</script>

<style scoped></style>
