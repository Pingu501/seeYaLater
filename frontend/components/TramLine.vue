<template>
  <g>
    <path
      :d="getLinePath()"
      :stroke="getColorForLine()"
      class="tram-line"
      stroke-width="20"
      fill="transparent"
    />
  </g>
</template>

<script>
  import mapper from '~/utility/Mapper'

  // get right side of the stop, 1 is up, 2 is right, 3 is down, 4 is left
  function getSideOfStop(previousStop, currentStop) {
    if (!previousStop) {
      return 2;
    }
    const dx = currentStop.x - previousStop.x;
    const dy = currentStop.y - previousStop.y;

    if (Math.abs(dx) > Math.abs(dy)) {
      return dx < 0 ? 2 : 4;
    } else {
      return dy < 0 ? 1 : 3;
    }
  }

  export default {
    props: {
      line: {
        required: true,
        type: String
      },
      direction: {
        required: true,
        type: String
      },
      stops: {
        required: true,
        type: Array
      }
    },
    methods: {
      getLinePath() {
        let path = '';

        // first move to start point
        const startPoint = mapper.getStop(this.stops[0]);
        path += `M ${startPoint.x} ${startPoint.y}`;

        let previousStop;
        this.stops.forEach(stopId => {
          const stop = mapper.getStop(stopId);
          let coordinates = {x: stop.x, y: stop.y};

          // offset to get the side
          const sideOfStop = getSideOfStop(previousStop, stop);
          const sideOffset = mapper.getOffsetForSide(stop.id, sideOfStop);
          switch (sideOfStop) {
            case 1:
              coordinates.x += (sideOffset - 1) * 20;
              break;
            case 2:
              coordinates.x += 100;
              coordinates.y += ((sideOffset - 1) * 20);
              break;
            case 3:
              coordinates.x += (sideOffset - 1) * 20;
              coordinates.y += 100;
              break;
            case 4:
              coordinates.y +=  ((sideOffset - 1) * 20);
          }

          path += ` L ${coordinates.x} ${coordinates.y}`;
          previousStop = stop;
        });

        return path;
      },
      getColorForLine() {
        return mapper.getColorForLine(this.line);
      }
    }
  }
</script>
