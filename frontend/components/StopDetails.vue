<template>
  <div class="stop-details__wrapper">
    <div
      class="stop-details__close"
      @click="onHide"
    >
      ✕
    </div>

    <div
      v-for="departure in departures"
      :key="departure.id"
      class="departure--row"
    >
      <div class="departure--line">{{ departure.line }}</div>
      <div class="departure--direction">{{ departure.direction }}</div>
      <div class="departure--scheduled">{{ formatDate(departure.scheduled) }}</div>
      <div class="departure--delay">{{ getDelay(departure.scheduled, departure.real) }}</div>
    </div>
  </div>
</template>

<script>

  import moment from 'moment';

  export default {
    props: {
      departures: {
        type: Array,
        required: true
      },
      onHide: {
        type: Function,
        required: true
      }
    },
    methods: {
      formatDate(timestamp) {
        return moment(timestamp, 'X').format('HH:mm')
      },
      getDelay(scheduled, real) {
        return moment(real - scheduled, 'X').format('mm:ss')
      }
    }
  }
</script>
