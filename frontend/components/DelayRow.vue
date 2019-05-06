<template>
  <div class="departure--row">
    <div class="departure--line">{{ line }}</div>
    <div class="departure--direction">{{ direction }}</div>
    <div class="departure--scheduled">{{ formatDate() }}</div>
    <div
      :class="getDelayColorClass()"
      class="departure--delay"
    >
      {{ formatDelay() }}
    </div>
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
      getDelaySeconds() {
        // TODO: .round(10, 'seconds')
        const real = moment(this.real, 'X');
        const scheduled = moment(this.scheduled, 'X');

        return real.diff(scheduled, 'seconds');
      },
      formatDelay() {
        const secondsDiff = this.getDelaySeconds();
        const minutes = Math.trunc(Math.abs(secondsDiff) / 60);
        const seconds = Math.abs(secondsDiff) % 60;

        return `${seconds < 0 ? '-' : ' '}${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
      },
      getDelayColorClass() {
        const delay = Math.abs(this.getDelaySeconds());

        switch (true) {
          case delay <= 120:
            return 'no-delay';
          case delay <= 300:
            return 'light-delay';
          default:
            return 'high-delay'
        }
      }
    }
  }
</script>
