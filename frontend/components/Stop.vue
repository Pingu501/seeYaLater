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
      @mouseover="handleHoverStop"
      @click="handleClickStop"
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
      },
      onClickStop: {
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
      handleHoverStop() {
        this.onChangeText({
          type: 'stop',
          id: this.id
        })
      },
      handleClickStop() {
        this.onClickStop(this.id)
      }
    }
  };
</script>
