<template>
  <div
    class="top-bar"
  >
    <div
      v-if="showLoadingSpinner"
      class="spinner"
    />

    <div
      v-if="infoText.type === 'stop'"
      class="top-bar--content"
      @click="handleClickStop"
    >
      Haltestelle: {{ stopName }}
      <u class="link-text">
        mehr
      </u>
    </div>

    <div
      v-if="infoText.type === 'text'"
    >
      {{ infoText.content }}
    </div>
  </div>
</template>

<script>
  import mapper from '~/utility/Mapper'

  export default {
    props: {
      infoText: {
        type: Object,
        required: true
      },
      showLoadingSpinner: {
        type: Boolean,
        required: true
      },
      onClickStop: {
        type: Function,
        required: true
      }
    },
    computed: {
      stopName() {
        return mapper.getStop(this.infoText.id).name;
      }
    },
    methods: {
      handleClickStop() {
        this.onClickStop(this.infoText.id)
      }
    }
  }
</script>
