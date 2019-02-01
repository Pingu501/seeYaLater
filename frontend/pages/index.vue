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
        :x_coordinate="stop.x"
        :y_coordinate="stop.y"
        :size="stop.size"
      />
      <Connection
        v-for="connection in connections"
        :key="getConnectionKey(connection)"
        :stop1="connection.stop1"
        :x1="connection.x1"
        :y1="connection.y1"

        :stop2="connection.stop2"
        :x2="connection.x2"
        :y2="connection.y2"
        :line="connection.line"

        :selected="selected"
        :onSelectLine="handleLineSelect"
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
  data() {
    return {
      stops: {},
      connections: [],
      selected: null,
      minX: 0,
      minY: 0,
      maxX: 100,
      maxY: 100
    }
  },
  computed: {
    viewBox() {
      return `${this.minX - 1000} ${this.minY - 1000} ${this.maxX + 1000} ${this.maxY + 1000}`
    }
  },
  async created() {
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

      stopValues.forEach(stop => {
        this.stops[stop.id] = {
          ...stop,
          x: stop.x - minX,
          y: ((stop.y - minY) - midY) * -1,
          size: stop.connections.length
        }
      });

      this.maxX = maxX - minX;
      this.maxY = (maxY - minY);

      stopValues.forEach(stop => {
        const numberOfConnections = stop.connections.length;
        const addedLines = [];

        stop.connections.forEach(connection => {
          this.connections.push({
            numberOfConnections: numberOfConnections,

            line: connection.line,
            direction: connection.direction,

            stop1: stop.id,
            x1: this.stops[stop.id].x,
            y1: this.stops[stop.id].y,

            stop2: connection.stop_id,
            x2: this.stops[connection.stop_id].x,
            y2: this.stops[connection.stop_id].y,
          });
        });
      })
    } catch (e) {
      console.log(e);
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
