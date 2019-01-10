<template>
  <circle
    :cx="y_coordinate"
    :cy="x_coordinate"
    r="30"
    fill="red"
  />
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
  }
};
</script>
