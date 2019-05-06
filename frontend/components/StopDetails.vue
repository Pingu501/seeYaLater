<template>
  <div class="stop-details__wrapper">
    <div class="stop-details__header">
      <div
        :class="{'stop-details__header-item--active': tabIsActive('history')}"
        class="stop-details__header-item"
        @click="activateView('history')"
      >
        Aktuell
      </div>

      <div
        :class="{'stop-details__header-item--active': tabIsActive('stats')}"
        class="stop-details__header-item"
        @click="activateView('stats')"
      >
        Statistik
      </div>

      <div
        class="stop-details__header-item"
        @click="onHide"
      >
        Close ✕
      </div>
    </div>

    <div class="stop-details__table_wrapper">
      <DelayRow
        v-for="departure in departures"
        :key="departure.id"
        :line="departure.line"
        :direction="departure.direction"
        :scheduled="departure.scheduled"
        :real="departure.real"
      />
    </div>
  </div>
</template>

<script>
  import DelayRow from '~/components/DelayRow';

  export default {
    components: {DelayRow},
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
    data() {
      return {
        active: 'history'
      };
    },
    methods: {
      tabIsActive(name) {
        return this.active === name;
      },
      activateView(name) {
        this.active = name;
      }
    }
  }
</script>
