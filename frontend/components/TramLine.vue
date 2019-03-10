<template>
  <g
    class="tram-line__wrapper"
  >
    <path
      :d="getLinePath()"
      :data-name="line"
      :stroke="getColorForLine()"
      class="tram-line"
      stroke-width="20"
      fill="transparent"
    />
  </g>
</template>

<script>
  import mapper from '~/utility/Mapper'

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
      },
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
          const sideAndOffset = mapper.getSideOfStop(previousStop, stop, this.line);

          switch (sideAndOffset.side) {
            case 1:
              coordinates.x += (sideAndOffset.offset - 1) * 25;
              break;
            case 2:
              coordinates.x += 100;
              coordinates.y += ((sideAndOffset.offset - 1) * 25);
              break;
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
