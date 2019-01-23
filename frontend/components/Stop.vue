<template>
  <g
    class="stop"
    @mouseenter="toggleName"
    @mouseleave="toggleName"
  >
    <text
      :x="x_coordinate + 100"
      :y="y_coordinate + 60"
      :class="{'stop_text--hidden': !nameIsVisible}"
      class="stop__text"
    >
      {{ name }}
    </text>
    <rect
      :id="id"
      :x="x_coordinate"
      :y="y_coordinate"
      :width="width"
      :height="height"
      class="stop__rect"
    />
  </g>
</template>

<script>
export default {
  props: {
    id: {
      required: true,
      type: Number
    },
    name: {
      required: true,
      type: String
    },
    x_coordinate: {
      required: true,
      type: Number
    },
    y_coordinate: {
      required: true,
      type: Number
    },
    size: {
      required: true,
      type: Number
    }
  },
  data() {
    return {
      nameIsVisible: false
    }
  },
  computed: {
    width() {
      return 100
    },
    height() {
      return this.size * 30
    }
  },
  methods: {
    toggleName() {
      this.nameIsVisible = !this.nameIsVisible;
    }
  }
};
</script>
