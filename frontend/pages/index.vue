<template>
  <section class="container">
    <svg
      :viewBox="viewBox"
      height="100%"
      width="100%"
      class="map"
    >
      <g>
        <Stop
          v-for="stop in stops"
          :key="stop.id"
          :id="stop.id"
          :name="stop.name"
          :x_coordinate="stop.x"
          :y_coordinate="stop.y"
          :size="stop.size"
        />
      </g>
      <g>
        <Connection
          v-for="connection in connections"
          :key="getConnectionKey(connection)"
          :x1="connection.x1"
          :y1="connection.y1"
          :x2="connection.x2"
          :y2="connection.y2"
          :line="connection.line"
          :numberOfConnections="connection.numberOfConnections"
          :index="connection.index"

          :selected="selected"
          :onSelectLine="handleLineSelect"
        />
      </g>
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

        stop.connections.forEach((connection, i) => {
          this.connections.push({
            numberOfConnections: numberOfConnections,
            index: i,

            line: connection.line,
            x1: this.stops[stop.id].x,
            y1: this.stops[stop.id].y,

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
      return `${connection.x1}-${connection.y1}-${connection.x2}-${connection.y2}-${connection.line}-${connection.index}`;
    },
    handleLineSelect(line) {
      this.selected = (this.selected === line) ? null : line;
    }
  }
}
</script>
