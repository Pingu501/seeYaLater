<template>
  <section class="container">
    <div class="rows">
      <TopBar
        :info-text="infoText"
      />
      <Map
        :minX="minX"
        :minY="minY"
        :maxX="maxX"
        :maxY="maxY"
        :lines="lines"
        :stops="stops"
        :updateInfoText="updateInfoText"
      />
    </div>
  </section>
</template>

<script>
  import Map from '~/components/Map';
  import TopBar from '~/components/TopBar';

  import mapper from '~/utility/Mapper'

  export default {
    components: {Map, TopBar},
    data() {
      return {
        stops: [],
        lines: [],
        infoText: '',
        minX: 0,
        minY: 0,
        maxX: 100,
        maxY: 100
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

        this.stops = stopValues.map(stop => {
          const modifiedStop = {
            ...stop,
            x: stop.x - minX,
            y: ((stop.y - minY) - midY) * -1
          };

          mapper.addStop(modifiedStop);
          return modifiedStop;
        });

        this.maxX = maxX - minX;
        this.maxY = maxY - minY;

        const lineResponse = await this.$axios.get('stops-of-lines');
        this.lines = Object.values(lineResponse.data);

      } catch (e) {
        console.log(e);
      }
    },
    methods: {
      updateInfoText(infoText) {
        this.infoText = infoText;
      }
    }
  }
</script>
