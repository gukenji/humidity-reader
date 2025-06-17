<template>
  <div class="input-group">
    <label :for="id">{{ label }}</label>
    <input
      v-bind="$attrs"
      v-model="internalValue"
      :type="type"
      :id="id"
      :placeholder="placeholder"
      :required="required"
    />
  </div>
</template>

<script setup>
  import { defineProps, defineEmits, ref, watch } from "vue";

  // Propriedades recebidas pelo componente
  const props = defineProps({
    modelValue: {
      type: [String, Number],
      default: "",
    },
    label: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      default: "text",
    },
    id: {
      type: String,
      required: true,
    },
    placeholder: {
      type: String,
      default: "",
    },
    required: {
      type: Boolean,
      default: false,
    },
  });

  // Evento que emite a alteração do valor
  const emit = defineEmits(["update:modelValue"]);

  // Variável interna para o v-model
  const internalValue = ref(props.modelValue);

  // Watcher para atualizar a `modelValue` quando o valor interno for alterado
  watch(internalValue, (newValue) => {
    emit("update:modelValue", newValue);
  });
</script>

<style scoped>
  .input-group {
    margin-bottom: 1rem;
  }

  label {
    display: block;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }

  input {
    width: 100%;
    padding: 8px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
</style>
