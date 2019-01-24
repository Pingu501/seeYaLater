<template>
  <g>
    <text
      :x="x1"
      :y="y1"
      :class="{'stop_text--hidden': !lineIsVisible}"
      class="stop__text"
    >
      {{ line }}
    </text>
    <line
      :x1="x1"
      :y1="y1Offset"
      :x2="x2"
      :y2="y2"
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

export default {
  props: {
    x1: {
      type: Number,
      required: true
    },
    y1: {
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
    numberOfConnections: {
      type: Number,
      required: true
    },
    index: {
      type: Number,
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
      lineIsVisible: false
    };
  },
  computed: {
    y1Offset() {
      return this.y1 + (this.index * 40);
    },
    y2Offset() {
      return this.y2 + (this.index * 40);
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
      return `stroke:${color};stroke-width:70`;
    }
  }
};
</script>

