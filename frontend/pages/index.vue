<template>
  <section class="container">
    <svg
      :viewBox="viewBox"
      height="100%"
      width="100%"
    >
      <Stop
        v-for="stop in stops"
        :key="stop.key"
        :name="stop.name"
        :x_coordinate="stop.x_coordinate"
        :y_coordinate="stop.y_coordinate"
      />
    </svg>
  </section>
</template>

<script>
import axios from 'axios';
import Stop from '~/components/Stop';

export default {
  components: {Stop},
  data() {
    return {
      stops: [],
      minX: 0,
      minY: 0,
      maxX: 100,
      maxY: 100
    }
  },
  computed: {
    viewBox() {
      return `${this.minX} ${this.minY} ${this.maxY} ${this.maxX} `
    }
  },
  async created() {
    try {
      const response = await this.$axios.get('stops');

      const x_coordinates = response.data.map(e => e.fields.x_coordinate);
      const minX = Math.min(...x_coordinates);
      const maxX = Math.max(...x_coordinates);

      const y_coordinates = response.data.map(e => e.fields.y_coordinate);
      const minY = Math.min(...y_coordinates);
      const maxY = Math.max(...y_coordinates);

      this.stops = response.data.map(e => {
        return {
          key: e.pk,
          name: e.fields.name,
          x_coordinate: e.fields.x_coordinate - minX,
          y_coordinate: e.fields.y_coordinate - minY
        }
      });

      this.maxX = maxX - minX;
      this.maxY = maxY - minY;
    } catch (e) {
      console.log(e);
    }
  }
}
</script>
