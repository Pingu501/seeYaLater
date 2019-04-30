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
      @mouseenter="handleMouseEnter"
      @click="handleMouseEnter"
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
      },
      name: {
        required: true,
        type: String
      },
      onChangeText: {
        required: true,
        type: Function
      }
    },
    computed: {
      width() {
        return 130
      },
      height() {
        return 130; // this.size * 30
      }
    },
    methods: {
      handleMouseEnter() {
        this.onChangeText(this.name)
      }
    }
  };
</script>
