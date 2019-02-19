<template>
  <section class="container">
    <svg
      :viewBox="viewBox"
      height="100%"
      width="100%"
      class="map"
    >
      <Stop
        v-for="stop in stops"
        :key="stop.id"
        :id="stop.id"
        :name="stop.name"
        :x="stop.x"
        :y="stop.y"
      />
    </svg>
  </section>
</template>

<script>
import axios from 'axios';
import Stop from '~/components/Stop';
import Connection from '~/components/Connection';
import colorMapper from '~/components/ColorMapper';

export default {
  components: {Stop, Connection},
  async data() {
    this.stops = {};
    this.connections = [];
    this.selected = null;
    this.minX = 0;
    this.minY = 0;
    this.maxX = 100;
    this.maxY = 100;

    try {
      // fetch stops
      const stopResponse = await this.$axios.get('stops');
      const stopValues = Object.values(stopResponse.data);

      const x_coordinates = stopValues.map(e => e.x);
      const minX = Math.min(...x_coordinates);
      const maxX = Math.max(...x_coordinates);

      const y_coordinates = stopValues.map(e => e.y);
      const minY = Math.min(...y_coordinates);
      const maxY = Math.max(...y_coordinates);

      const midY = maxY - minY;

      const tmp = {};
      stopValues.forEach(stop => {
        this.stops[stop.id] = {
          ...stop,
          x: stop.x - minX,
          y: ((stop.y - minY) - midY) * -1
        }
      });

      this.maxX = maxX - minX;
      this.maxY = maxY - minY;
      // this.$forceUpdate();
    } catch (e) {
      console.log(e);
    }
  },
  computed: {
    viewBox() {
      return `${this.minX - 1000} ${this.minY - 1000} ${this.maxX + 1000} ${this.maxY + 1000}`
    }
  },
  methods: {
    getConnectionKey(connection) {
      return `${connection.line}-${connection.direction}-${connection.stop1}-${connection.stop2}`;
    },
    handleLineSelect(line) {
      this.selected = (this.selected === line) ? null : line;
    }
  }
}
</script>
