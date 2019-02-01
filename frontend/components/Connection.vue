<template>
  <g>
    <text
      :x="x1"
      :y="y1"
      :class="{'connection__text--hidden': !lineIsVisible}"
      class="connection__text"
    >
      {{ line }}
    </text>
    <line
      :x1="x1Offset"
      :y1="y1Offset"
      :x2="x2Offset"
      :y2="y2Offset"
      :style="getColorForLine()"
      :class="{'connection--inactive': lineIsActive}"
      class="connection"
      @mouseenter="showLine()"
      @mouseleave="hideLine()"
      @click="selectLine()"
    />
  </g>
</template>

<script>
import colorMapper from './ColorMapper';
import connectionStopMapper from './ConnectionStopMapper.js';

export default {
  props: {
    stop1: {
      type: Number,
      required: true
    },
    x1: {
      type: Number,
      required: true
    },
    y1: {
      type: Number,
      required: true
    },
    stop2: {
      type: Number,
      required: true
    },
    x2: {
      type: Number,
      required: true
    },
    y2: {
      type: Number,
      required: true
    },
    line: {
      type: String,
      required: true
    },
    selected: {
      type: String,
      required: false,
      default: null
    },
    onSelectLine: {
      type: Function,
      required: true
    }
  },
  data() {
    return {
      stop1Index: connectionStopMapper.getLineIndexForStop(this.stop1, this.line),
      stop2Index: connectionStopMapper.getLineIndexForStop(this.stop2, this.line),
      dx: this.x1 - this.x2,
      dy: this.y1 - this.y2,
      lineIsVisible: false
    };
  },
  computed: {
    x1Offset() {
      return this.x1 + (this.dx > this.dy ? this.stop1Index * 40 : 0);
    },
    y1Offset() {
      return this.y1 + (this.dx > this.dy ? this.stop1Index * 40 : 0);
    },
    x2Offset() {
      return this.x2 + (this.dx > this.dy ? this.stop1Index * 40 : 0);
    },
    y2Offset() {
      return this.y2 + (this.dx > this.dy ? this.stop1Index * 40 : 0);
    },
    lineIsActive() {
      return this.selected !== null && this.selected !== this.line;
    }
  },
  methods: {
    showLine() {
      this.lineIsVisible = true;
    },
    hideLine() {
      this.lineIsVisible = false;
    },
    selectLine() {
      this.onSelectLine(this.line);
    },
    getColorForLine() {
      const color = colorMapper.getColorForLine(this.line);
      return `stroke:${color};stroke-width:50`;
    }
  }
};
</script>

