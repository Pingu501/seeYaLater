<template>
  <svg
    v-hammer:pinch="handlePinch"
    v-hammer:tap="handleMouseMove"
    ref="svgRef"
    :viewBox="viewBox"
    class="map"
    width="100%"
    @mousemove="handleMouseMove"
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
</template>

<script>
  import Stop from '~/components/Stop';
  import TramLine from '~/components/TramLine';

  import mapper from '~/utility/Mapper'

  export default {
    components: {Stop, TramLine},
    props: {
      lines: {
        required: true,
        type: Array
      },
      stops: {
        required: true,
        type: Array
      },
      minX: {
        required: true,
        type: Number
      },
      minY: {
        required: true,
        type: Number
      },

      maxX: {
        required: true,
        type: Number
      },

      maxY: {
        required: true,
        type: Number
      },
      updateInfoText: {
        required: true,
        type: Function
      }
    },
    computed: {
      viewBox() {
        return `${this.minX - 1000} ${this.minY - 1000} ${this.maxX + 1000} ${this.maxY + 1000}`
      }
    },
    methods: {
      getTramLineKey(line) {
        return `${line.line}-${line.direction}`;
      },
      handleMouseMove() {
        let text = '';
        const element = event.path[0];
        const tagName = element.tagName;

        switch (tagName) {
          case 'rect':
            const stop = mapper.getStop(element.id);

            if (stop) {
              text = 'Haltestelle: ' + stop.name;
            }
            break;
          case 'path':
            text = 'Linie: ' + element.getAttribute('data-name');
            break;
          default:
            text = '';
        }

        this.updateInfoText(text);
      },
      handlePinch(event) {
        this.$refs.svgRef.style.transform = `scale(${event.scale})`
      }
    }
  }
</script>
