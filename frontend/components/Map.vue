<template>
  <div
    v-hammer:pinch="handlePinch"
    :class="{ map__covered: isCovered }"
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
      <Elbe
        :minX="minX"
        :minY="minY"
        :maxY="maxY"
      />
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
        :onClickStop="onClickStop"
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
  import Elbe from '~/components/Elbe'
  import Stop from '~/components/Stop';
  import TramLine from '~/components/TramLine';

  export default {
    components: {Elbe, Stop, TramLine},
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
      isCovered: {
        required: true,
        type: Boolean
      },
      updateInfoText: {
        required: true,
        type: Function
      },
      onClickStop: {
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
        return `-1000 -1000 ${this.maxX - this.minX + 1000} ${this.maxY - this.minY + 1000}`
      }
    },
    methods: {
      getTramLineKey(line) {
        return `${line.line}-${line.direction}`;
      },
      activateLine(line, direction) {
        this.activeLine = this.getTramLineKey({line, direction});
      },
      handleMouseMove(event) {
        // drag map if mouse button is pressed
        if (event.buttons) {
          this.handleMove(event.x - this.mouseX, event.y - this.mouseY);

          this.mouseX = event.x;
          this.mouseY = event.y;
        }
      },
      handlePinch(event) {
        this.setScale(this.scale *= event.scale);
        this.updateMap();
      },
      upScale() {
        this.setScale(this.scale *= 1.5);
        this.updateMap()
      },
      downScale() {
        this.setScale(this.scale *= 0.75);
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
        event.preventDefault();
        event.stopPropagation();

        this.setScale(this.scale *= event.scale);

        this.handleMove(event.pageX - this.mouseX, event.pageY - this.mouseY);

        this.mouseX = event.pageX;
        this.mouseY = event.pageY;
      },
      handleMove(x, y) {
        this.x += x / this.scale;
        this.y += y / this.scale;
        this.updateMap();
      },
      setScale(scale) {
        if (scale > 10) {
          this.scale = 10;
        } else if (scale < 1) {
          this.scale = 1;
        } else {
          this.scale = scale;
        }
      },
      updateMap() {
        this.$refs.map.style.transform = `scale(${this.scale}) translate(${this.x}px, ${this.y}px)`;
      }
    }
  }
</script>
