<template>
  <div class="stop-details__wrapper">
    <div
      class="stop-details__close"
      @click="onHide"
    >
      X
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      onHide: {
        type: Function,
        required: true
      }
    }
  }
</script>
