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
        :x_coordinate="stop.x_coordinate"
        :y_coordinate="stop.y_coordinate"
      />
      <Connection
        v-for="connection in connections"
        :key="getConnectionKey(connection)"
        :stop1X="connection.stop1X"
        :stop1Y="connection.stop1Y"
        :stop2X="connection.stop2X"
        :stop2Y="connection.stop2Y"
        :line="connection.line"
        :direction="connection.direction"
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
      minX: 0,
      minY: 0,
      maxX: 100,
      maxY: 100
    }
  },
  computed: {
    viewBox() {
      return `${this.minX} ${this.minY} ${this.maxX} ${this.maxY}`
    }
  },
  async created() {
    try {
      // fetch stops
      const stopResponse = await this.$axios.get('stops');

      const x_coordinates = stopResponse.data.map(e => e.x_coordinate);
      const minX = Math.min(...x_coordinates);
      const maxX = Math.max(...x_coordinates);

      const y_coordinates = stopResponse.data.map(e => e.y_coordinate);
      const minY = Math.min(...y_coordinates);
      const maxY = Math.max(...y_coordinates);

      const midY = maxY - minY;

      stopResponse.data.forEach(e => {
        this.stops[e.id] = {
          ...e,
          x_coordinate: e.x_coordinate - minX,
          y_coordinate: ((e.y_coordinate - minY) - midY) * -1
        }
      });

      this.maxX = maxX - minX;
      this.maxY = (maxY - minY);
      
      // create connections
      const connectionResponse = await this.$axios.get('stops-of-lines');
      const connections = [];

      connectionResponse.data.forEach(line => {
        let previousStopId = null;
        line.stops.forEach(stopId => {
          if (!previousStopId) {
            previousStopId = stopId;
            return;
          }

          connections.push({
            stop1X: this.stops[previousStopId].x_coordinate,
            stop1Y: this.stops[previousStopId].y_coordinate,

            stop2X: this.stops[stopId].x_coordinate,
            stop2Y: this.stops[stopId].y_coordinate,
            line: line.line,
            direction: line.direction
          });
          previousStopId = stopId;
        });
      });

      this.connections = connections;

    } catch (e) {
      console.log(e);
    }
  },
  methods: {
    getConnectionKey(connection) {
      return `${connection.stop1X}-${connection.stop1Y}-${connection.stop2X}-${connection.stop2Y}-${connection.line}-${connection.direction}`;
    } 
  }
}
</script>
