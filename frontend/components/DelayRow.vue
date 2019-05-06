<template>
  <div class="departure--row">
    <div class="departure--line">{{ line }}</div>
    <div class="departure--direction">{{ direction }}</div>
    <div class="departure--scheduled">{{ formatDate() }}</div>
    <div class="departure--delay">{{ getDelay() }}</div>
  </div>
</template>

<script>
  import moment from 'moment';

  export default {
    props: {
      line: {
        type: String,
        required: true
      },
      direction: {
        type: String,
        required: true
      },
      scheduled: {
        type: Number,
        required: true
      },
      real: {
        type: Number,
        required: true
      }
    },
    methods: {
      formatDate() {
        return moment(this.scheduled, 'X').format('HH:mm')
      },
      getDelay() {
        // TODO: .round(10, 'seconds')
        const real = moment(this.real, 'X');
        const scheduled = moment(this.scheduled, 'X');

        const secondsDiff = real.diff(scheduled, 'seconds');

        const minutes = Math.trunc(Math.abs(secondsDiff) / 60);
        const seconds = Math.abs(secondsDiff) % 60;

        return `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
      },
    }
  }
</script>
