<template>
  <section class="container">
    <div class="rows">
      <TopBar
        :info-text="infoText"
      />
      <svg
        v-hammer:pinch="handlePinch"
        ref="svgRef"
        :viewBox="viewBox"
        class="map"
        width="100%"
        @mousemove="updateShowText"
      >
        <TramLine
          v-for="line in lines"
          :key="getTramLineKey(line)"
          :line="line.line"
          :direction="line.direction"
          :stops="line.stops"
        />
        <Stop
          v-for="stop in stops"
          :key="stop.id"
          :id="stop.id"
          :name="stop.name"
          :x="stop.x"
          :y="stop.y"
        />
      </svg>
    </div>
  </section>
</template>

<script>
  import TopBar from '~/components/TopBar';
  import Stop from '~/components/Stop';
  import TramLine from '~/components/TramLine';

  import mapper from '~/utility/Mapper'

  export default {
    components: {Stop, TramLine, TopBar},
    data() {
      return {
        stops: [],
        lines: [],
        selected: null,
        infoText: '',
        scale: 1,
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
      getTramLineKey(line) {
        return `${line.line}-${line.direction}`;
      },
      handleLineSelect(line) {
        this.selected = (this.selected === line) ? null : line;
      },
      updateShowText(event) {
        const element = event.path[0];
        const tagName = element.tagName;

        switch (tagName) {
          case 'rect':
            const stop = mapper.getStop(element.id);

            if (stop) {
              this.infoText = stop.name;
            }
            break;
          case 'path':
            this.infoText = 'Linie: ' + element.getAttribute('data-name');
            break;
          default:
            this.infoText = '';
        }
      },
      handlePinch(event) {
        this.$refs.svgRef.style.transform = `scale(${event.scale})`
      }
    }
  }
</script>
