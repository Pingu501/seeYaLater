<template>
  <div class="top-bar">
    {{ infoText }}
  </div>
</template>

<script>
  export default {
    props: {
      infoText: {
        type: String,
        required: false,
        default: ''
      }
    }
  }
</script>
