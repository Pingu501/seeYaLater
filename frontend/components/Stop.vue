<template>
  <g
    class="stop__wrapper"
  >
    <rect
      :id="id"
      :x="x"
      :y="y"
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
      x: {
        required: true,
        type: Number
      },
      y: {
        required: true,
        type: Number
      }
    },
    computed: {
      width() {
        return 100
      },
      height() {
        return 100; // this.size * 30
      }
    }
  };
</script>
