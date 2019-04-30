<template>
  <div
    class="map__wrapper"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @mousedown="handleMouseDown"
    @mousemove="handleMouseMove"
  >
    <svg
      ref="map"
      :viewBox="viewBox"
      class="map"
      width="100%"
    >
      <TramLine
        v-for="line in lines"
        :key="getTramLineKey(line)"
        :line="line.line"
        :direction="line.direction"
        :stops="line.stops"
        :activeLine="activeLine"
        :onChangeText="updateInfoText"
        :activateLine="activateLine"
      />
      <Stop
        v-for="stop in stops"
        :key="stop.id"
        :id="stop.id"
        :name="stop.name"
        :x="stop.x"
        :y="stop.y"
        :onChangeText="updateInfoText"
      />
    </svg>

    <div class="map--controls">
      <div
        class="button"
        @click="upScale"
      >
        +
      </div>

      <div
        class="button"
        @click="downScale"
      >
        -
      </div>
    </div>
  </div>
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
    data() {
      return {
        scale: 1,
        x: 0,
        y: 0,
        mouseX: 0,
        mouseY: 0,
        activeLine: ''
      };
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
      activateLine(line, direction) {
        console.log(line, direction, 'Stuff');
        this.activeLine = this.getTramLineKey({line, direction});
      },
      handleMouseMove(event) {
        if (event.buttons) {
          this.handleMove(event.x - this.mouseX, event.y - this.mouseY);

          this.mouseX = event.x;
          this.mouseY = event.y;
          return;
        }

        // TODO: not working in firefox!
        if (!event.path) {
          return;
        }

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
      upScale() {
        this.scale *= 1.5;
        this.updateMap()
      },
      downScale() {
        this.scale *= 0.75;
        this.updateMap()
      },
      handleMouseDown(event) {
        this.mouseX = event.x;
        this.mouseY = event.y;
      },
      handleTouchStart(event) {
        this.mouseX = event.pageX;
        this.mouseY = event.pageY;
      },
      handleTouchMove(event) {
        this.scale = event.scale;
        this.handleMove(event.pageX - this.mouseX, event.pageY - this.mouseY);

        this.mouseX = event.pageX;
        this.mouseY = event.pageY;
      },
      handleMove(x, y) {
        this.x += x / this.scale;
        this.y += y / this.scale;
        this.updateMap();
      },
      updateMap() {
        this.$refs.map.style.transform = `scale(${this.scale}) translate(${this.x}px, ${this.y}px)`;
      }
    }
  }
</script>
