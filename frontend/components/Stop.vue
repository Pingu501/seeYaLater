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
    <circle
      :cx="x_coordinate"
      :cy="y_coordinate"
      r="50"
      class="stop__point"
    />
  </g>
</template>

<script>
export default {
  props: {
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
    }
  },
  data() {
    return {
      nameIsVisible: false
    }
  },
  methods: {
    toggleName() {
      this.nameIsVisible = !this.nameIsVisible;
    }
  }
};
</script>
