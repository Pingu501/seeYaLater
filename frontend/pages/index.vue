<template>
  <section
    class="container"
    @scroll="handleScroll"
  >
    <div class="rows">
      <TopBar
        :info-text="infoText"
        :on-click-stop="handleClickStop"
      />
      <Map
        :minX="minX"
        :minY="minY"
        :maxX="maxX"
        :maxY="maxY"
        :lines="lines"
        :stops="stops"
        :isCovered="showStopDetails"
        :updateInfoText="updateInfoText"
        :onClickStop="handleClickStop"
      />
      <StopDetails
        v-if="showStopDetails"
        :departures="departureData"
        :on-hide="handleHideStopDetails"
      />
    </div>
  </section>
</template>

<script>
  import Map from '~/components/Map';
  import StopDetails from '~/components/StopDetails';
  import TopBar from '~/components/TopBar';

  import mapper from '~/utility/Mapper'

  export default {
    components: {Map, TopBar, StopDetails},
    data() {
      return {
        stops: [],
        lines: [],
        departureData: [],
        infoText: {
          type: 'text',
          content: ''
        },
        minX: 0,
        minY: 0,
        maxX: 100,
        maxY: 100,

        showStopDetails: false
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

        this.minX = minX;
        this.minY = minY;

        this.maxX = maxX;
        this.maxY = maxY;

        const lineResponse = await this.$axios.get('stops-of-lines');
        this.lines = Object.values(lineResponse.data);

      } catch (e) {
        console.log(e);
      }
    },
    methods: {
      updateInfoText(infoText) {
        this.infoText = infoText;
      },
      handleScroll(event) {
        event.preventDefault();
        event.stopPropagation();
      },
      async handleClickStop(stopId) {
        try {
          const departureResponse = await this.$axios.get('departure', {params: {stop_id: stopId}});

          this.departureData = departureResponse.data;
          this.showStopDetails = true;
        } catch (e) {
          console.log(e);
        }
      },
      handleHideStopDetails() {
        this.showStopDetails = false;
      }
    }
  }
</script>
