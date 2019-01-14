<template>
  <g>
    <text
      :x="stop1X"
      :y="stop1Y"
      :class="{'stop_text--hidden': !lineIsVisible}"
      class="stop__text"
    >
      {{ line }} - {{ direction }}
    </text>
    <line
      :x1="stop1X"
      :y1="stop1Y"
      :x2="stop2X"
      :y2="stop2Y"
      :style="getColorForLine()"
      class="connection-line"
      @mouseenter="showLine()"
      @mouseleave="hideLine()"
    />
  </g>
</template>

<script>
import colorMapper from './ColorMapper';

export default {
  props: {
    stop1X: {
      type: Number,
      required: true
    },
    stop1Y: {
      type: Number,
      required: true
    },
    stop2X: {
      type: Number,
      required: true
    },
    stop2Y: {
      type: Number,
      required: true
    },
    line: {
      type: String,
      required: true
    },
    direction: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      lineIsVisible: false
    };
  },
  methods: {
    showLine() {
      this.lineIsVisible = true;
    },
    hideLine() {
      this.lineIsVisible = false;
    },
    getColorForLine() {
      const color = colorMapper.getColorForLine(this.line);
      return `stroke:${color};stroke-width:40`;
    }
  }
};
</script>

