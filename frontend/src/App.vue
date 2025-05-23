<script>
  export default {
    data() {
      return {
        humidity: null,
        intervalId: null,
      };
    },
    methods: {
      getBackendUrl() {
        const host = window.location.hostname;
        const port = 8000;

        // Senão, usa o host atual
        return `http://${host}:${port}/humidity/`;
      },

      async fetchHumidity() {
        try {
          const apiUrl = this.getBackendUrl();
          const response = await fetch(apiUrl);
          const data = await response.json();

          if (data.length > 0) {
            const last = data[data.length - 1];
            this.humidity = last.value;
          } else {
            this.humidity = "Sem dados";
          }
        } catch (error) {
          console.error("Erro ao buscar umidade:", error);
          this.humidity = "Erro";
        }
      },
    },
    mounted() {
      this.fetchHumidity(); // chamada inicial
      this.intervalId = setInterval(this.fetchHumidity, 5000); // atualiza a cada 5s
    },
    beforeUnmount() {
      clearInterval(this.intervalId);
    },
  };
</script>

<template>
  <div>
    <h1>Umidade: {{ humidity }}%</h1>
  </div>
</template>
